import json


def getProductionByDemand(request, byPrice=False):
    # Information from request
    try:
        req = json.loads(request.data)
    except:
        return {
            "status": 'error',
            "message": 'Bad JSON payload'
        }
    try:
        load = float(req['load'])
    except KeyError:
        return {
            "status": 'error',
            "message": 'Missing load information'
        }
    except:
        return {
            "status": 'error',
            "message": 'bad data'
        }
    # Dictionary for prices/plant type and wind information -> May change depending on nature of plants
    fuels = {
        'gasfired': 'gas(euro/MWh)',
        'turbojet': 'kerosine(euro/MWh)',
        'windturbine': 'wind(%)'
    }

    # Initialize final plants configurations
    finalResult = []

    # 1 - Creating merit order (Criteria: cost/efficiency)
    list = []
    try:
        for plant in req['powerplants']:
            if plant['type'] != 'windturbine':
                # Cost per MWh
                plant['fuelCost'] = req["fuels"][fuels[plant['type']]] / plant['efficiency']
                # Emission allowances (increases)
                if plant['type'] == 'gasfired':
                    plant['fuelCost'] = plant['fuelCost'] + (req["fuels"]["co2(euro/ton)"] * 0.3)
                list.append(plant)
            else:
                # Windturbine plants go on top of the final plants configuration varible
                plant['fuelCost'] = 0
                plant['preal'] = plant['pmax'] * req['fuels']['wind(%)'] / 100
                finalResult.append(plant)
    except KeyError:
        return {
            "status": 'error',
            "message": 'Missing powerplants or fuels information'
        }
    except:
        return {
            "status": 'error',
            "message": 'bad data'
        }
    # Sort list to ger merit order
    sortedList = sorted(list, key=lambda x: x['fuelCost'])

    # 2 - Calculate charge for every plant
    breakpoint = False
    index = 0
    numWind = len(finalResult)
    load = load - sum([p['preal'] for p in finalResult])
    try:
        for i, plant in enumerate(sortedList):
            if load >= plant['pmax']:
                plant['preal'] = plant['pmax']
                load = load - plant['pmax']
                finalResult.append(plant)
            elif load > 0 and load < plant['pmin']: 
                plant['preal'] = 0.0
                finalResult.append(plant)
                if not breakpoint:
                    index = i + numWind
                    breakpoint = True
            elif load >= plant['pmin'] and load < plant['pmax']: 
                plant['preal'] = load
                load = 0
                finalResult.append(plant)
            else:
                plant['preal'] = 0.0
                finalResult.append(plant)
    except KeyError:
        return {
            "status": 'error',
            "message": 'Missing powerplants or fuels information'
        }
    except:
        return {
            "status": 'error',
            "message": 'bad data'
        }
    
    # 3 - If the enpoint was /productionplanprice
    if byPrice:
        if breakpoint: 
            if index + 1 == len(finalResult):
                finalResult[index]['preal'] = finalResult[index]['pmin']
            else:
                price1 = finalResult[index]['pmin'] * finalResult[index]['fuelCost']
                price2 = finalResult[index + 1]['preal'] * finalResult[index + 1]['fuelCost']
                if price1 < price2:
                    finalResult[index]['preal'] = finalResult[index]['pmin']
                    finalResult[index + 1]['preal'] = 0.0
    return [
        {
            "name": plant['name'],
            "p": round(plant['preal'], 1)
        }
    for plant in finalResult]

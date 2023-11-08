from flask import Flask, request, jsonify

from resources.algorithm import getProductionByDemand


app = Flask(__name__)


# Endpoint to meet the exact demand from available sources
@app.route('/productionplan', methods=['GET', 'POST'])
def productionPlan():
    return jsonify(getProductionByDemand(request))


# Enpoint to fulfill load based on cost (Will produce more than load if that configuration is cheaper)
@app.route('/productionplanprice', methods=['POST'])
def productionPlanPrice():
    return jsonify(getProductionByDemand(request, byPrice=True))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

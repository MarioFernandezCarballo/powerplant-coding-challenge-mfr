## Solution

The API has two endpoints.

/productionplan

Returns a response specifying for each powerplant how much power each powerplant should deliver, meeting the exact demand.

/productionplanprice

Returns a response specifying for each powerplant how much power each powerplant should deliver. It focuses on production costs and returns the less expensive configuration while fulfilling the energy demand (could be higer)

## Installation

Pull this repository

```bash
https://github.com/MarioFernandezCarballo/powerplant-coding-challenge-mfr.git
```

Navigate to the root directory

```bash
docker build -t powerplant-challenge .
```

then

```bash
docker run -it -p 8888:8888 -d powerplant-challenge
```

API is accessible from http://127.0.0.1:8888/productionplan
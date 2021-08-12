import json
import os
import requests

from flask import Flask, app
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask (__name__)

@app.route('/webhook',methods=["Post"])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = makeresponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeresponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")

    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+ city +'&appid=53c1f84150d78c282b57aae211c7691b')
    json_object = r.json()
    weather = json_object['list']
    for i in len(weather):
        if date in weather[i]['dt_txt']:
            condition=weather[i]['weather'][0]['description']




    speech = "The forecast for " + city + " on " + date + " is " + condition
    return {
        "speech" : speech,
        "displayText" : speech,
        "source": "dialogflow-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app on port %d" %port)
    app.run(debug=False, port=port, host='0.0.0.0')


    

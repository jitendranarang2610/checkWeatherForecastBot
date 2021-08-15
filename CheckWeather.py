import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    API_KEY = '53c1f84150d78c282b57aae211c7691b'  # initialize your key here
    city = request.args.get('q')  # city name passed as argument
    print("City value received is %d" %city)
    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    print("Url formed is %d" %url)
    response = requests.get(url).json()

    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'

    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        return f'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
    else:
        return f'Error getting temperature for {city.title()}'


@app.route('/')
def index():
    return '<h1>Welcome to weather app</h1>'


if __name__ == '__main__':
    print("Main method pre-entry")
    port = int(os.getenv('PORT',5000))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host='0.0.0.0')

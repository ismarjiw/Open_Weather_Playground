from flask import Flask, render_template, request, abort, Response, json
import urllib
import os

app = Flask(__name__)

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

@app.route('/')
def homepage():

    return render_template('request.html')
    
@app.route('/weather', methods=['GET'])
def get_weather():

    zipcode = request.args.get('zip')

    if not zipcode:
        abort(400, 'Missing argument zipcode')

    data = {}
    data['zip'] = request.args.get('zip')
    data['appid'] = OPEN_WEATHER_API_KEY
    data['units'] = 'imperial'

    url_values = urllib.parse.urlencode(data)
    url = 'http://api.openweathermap.org/data/2.5/weather'
    full_url = url + '?' + url_values
    data = urllib.request.urlopen(full_url)

    resp = Response(data)
    resp.status_code = 200

    return render_template('index.html', title='Weather Info', data = json.loads(data.read().decode('utf8')))

if __name__ == "__main__":  
    app.run(host="0.0.0.0", debug=True, threaded=True)
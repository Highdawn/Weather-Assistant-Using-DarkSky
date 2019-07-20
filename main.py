from darkSkyClient.DarkSkyClient import DarkSkyClient as DSC
import datetime 
import json
import os
import time

def check_rain(probability):
    if probability >= 10:
        return True # Going to Rain
    else:
        return False # Not Going to Rain

def check_temperature(temperature):
    if temperature >= 20:
        return True # Hot
    else:
        return False # Cold

def check_wind(wind):
    if wind >=10:
        return True # Windy
    else:
        return False # No Wind

def update_data(coordinates):
    DSClient = DSC()
    with open('darkSkyClient/data.json', 'w') as json_file:
        json.dump((DSClient.get_weather_date(coordinates)).json(), json_file)
    print("Data Updated")

def check_data(GPScoordinates):
    if os.path.isfile('darkSkyClient/data.json'):
        with open('darkSkyClient/data.json') as json_file:
            try:
                data = json.load(json_file)
                coordinates = str(data['latitude']) + ',' + str(data['longitude'])
                diference = int(time.time())-data['hourly']['data'][0]['time']
            except (ValueError, KeyError):
                print("ERROR: Couldn't read data.json file")
                update_data(GPScoordinates)
                return False
        if coordinates != GPScoordinates or diference >= 86400:
            update_data(GPScoordinates)
    else:
        update_data(GPScoordinates)
    return True


def check_weather(GPScoordinates):
    while not check_data(GPScoordinates):
        print("Checking data again")
    with open('darkSkyClient/data.json') as json_file:
        data = json.load(json_file)
        for p in data['hourly']['data']:
            temp = p['apparentTemperature']
            wind = p['windSpeed']
            rain = p['precipProbability']
            time = datetime.datetime.fromtimestamp(p['time']).strftime('%c')
            print(str(time) + " - ", end = '')
            
            # Check temperature and wind
            if check_temperature(temp) and not check_wind(wind):
                print ('Hot  (' + str(temp) + ') ' + ' | Wind (' + str(wind) + ')', end = '')
            else:
                print ('Cold (' + str(temp) + ')' + ' | Wind (' + str(wind) + ')', end = '')

            print(' | ', end = '')

            # Check rain
            if check_rain(rain):
                print ('Going to Rain (' + str(rain) + ')', end = '')
            else:
                print ('No Rain (' + str(rain) + ')')

print("Starting Script...")
GPScoordinates = input("Insert the coordinates of the location: ")
check_weather(GPScoordinates)
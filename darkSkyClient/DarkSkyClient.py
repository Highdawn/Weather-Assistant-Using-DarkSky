import json
import time
import os
import requests

class DarkSkyClient:
    key = None
            
    def __init__(self):
        if os.path.isfile('darkSkyClient/credentials.json'):
            with open('darkSkyClient/credentials.json') as json_file:
                data = json.load(json_file)
                self.key = data['client']['key']
        else:
            self.key = input("Insert the key for the DarkSky API: ")
            credentials ={"client":{"key":"" + str(self.key) +""}}
            with open('darkSkyClient/credentials.json', 'w') as json_file:
                json.dump(credentials, json_file)
            print("Key Updated")

    def change_key(self):
        status = None
        while status != 200:
            key = input("Insert the key for the DarkSky API: ")
            address = 'https://api.darksky.net/forecast/' + key + '/' + "37.234332,-115.806663"
            results = requests.get(address)
            status = results.status_code
            if status == 403:
                print("Key is Invalid")          
        credentials ={"client":{"key":"" + str(key) +""}}
        with open('darkSkyClient/credentials.json', 'w') as json_file:
            json.dump(credentials, json_file)
        self.key=key
        print("Key Updated")

    def change_coordinates(self):
        status = None
        while status != 200:
            coordinates = input("Insert the coordinates of the location: ")
            address = 'https://api.darksky.net/forecast/' + self.key + '/' + str(coordinates)
            results = requests.get(address)
            status = results.status_code
            if status == 400:
                print("The given location is invalid")  
        return coordinates
            
    def get_weather(self, coordinates):
        address = 'https://api.darksky.net/forecast/' + self.key + '/' + coordinates + '?units=ca&exclude=currently,flags,daily'
        results = requests.get(address)
        if results.status_code == 403:
            print("Key is Invalid")
            self.change_key()
            results = self.get_weather_date(coordinates)
        elif results.status_code == 400:
            print("The given location is invalid")
            coordinates = self.change_coordinates()
            results = self.get_weather(coordinates)
        return results

    def get_weather_date(self, coordinates):
        address = 'https://api.darksky.net/forecast/' + self.key + '/' + coordinates + ',' + str(int(time.time())) + '?units=ca&exclude=currently,flags,daily'
        results = requests.get(address)
        if results.status_code == 403:
            print("Key is Invalid")
            self.change_key()
            results = self.get_weather_date(coordinates)
        elif results.status_code == 400:
            print("The given location is invalid")
            coordinates = self.change_coordinates()
            results = self.get_weather_date(coordinates)
        return results

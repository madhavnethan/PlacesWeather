import csv
import requests
import logging
from datetime import datetime

from cs50 import get_string, get_int

#surpressing the debug statements inside the request library
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_places():
    with open('uszips.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        places = []
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                place = {'zip': row['zip'], 'lat': row['lat'], 'lng' : row['lng'], 'city': row['city'] ,'state': row['state_id'] , 'population': row['population']}
                places.append(place)
                
    return places


def search_by_zip(places, zipcode):
    #should return one dictionary.
    for place in places:
        if place['zip'] == zipcode:
            return place

def search_by_city(places, cityname, statecode):
    #should return a list of dictionaries.
    for place in places:
        if cityname.upper() == place['city'].upper():
            if statecode.upper() == place['state'].upper():
                return place

def display(place):
    if place is None:
            print("Couldn't find the place.")
    else:
        place_info = f"{place['city']} , {place['state']} , {place['zip']} , {place['lat']} , {place['lng']}"
        
        print("*" * len(place_info))
        print(place_info)
        print("*" * len(place_info))

def check_weather():
    place = search_by_cityZip()
    if place is not None:
        weather(place)     
    

def weather(place):
    lat = place['lat']
    lon = place['lng']
    units = "imperial"
    
    # Excluding the data that we don't use before calling API
    exculde_block = "minutely,hourly,alerts"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exculde_block}&appid=d6cc0aabe552423bf833fd23bf7f4f4e&units={units}"
    response = requests.get(url)
    
    
    # Get JSON string response
    weather_info = response.json()
    
    # Dictionary inside weather_info dictionary
    # Get the curent weather block
    cw = weather_info["current"]
    
    # Get the daily weather block
    daily = weather_info["daily"]
    
    # Print the current weather info  
    print("")
    print("Current Temp:\t",cw['temp'],"F")
    print("Feels Like:\t",cw['feels_like'],"F")
    print("Humidity:\t",cw['humidity'])
    print("Wind Speed:\t",cw['wind_speed'],"mph")
    print("Conditions:\t",cw['weather'][0]['description'])
    print("")
    
    # Print the daily forecast for the week
    print("Daily Forecast:")
    print("Day\t\tMin Temp\tMax Temp\tCondition\t\tWhat to have")
    print("------------------------------------------------------------------------------------")
    
    # Loop through daily dictionary
    for d in daily:
        
        # I used set so that there are no duplicate items
        items = set()
        
        # Converting unix time to readable format
        unix_ts = d['dt']
        print(datetime.utcfromtimestamp(unix_ts).strftime('%A, %d'),end='\t')
        print(d['temp']['min'],"F",end='\t\t')
        print(d['temp']['max'],"F",end='\t\t')
        condition = d['weather'][0]['description']
        
        # Rainy Day
        if "rain" in condition:
            items.add("jacket")
            items.add("umbrella")
        
        # Snow Day
        if "snow" in condition:
            items.add("boots")
            items.add("gloves")
        
        #Good temperature add a suitable clothes
        if d['temp']['max'] > 50:
            items.add("shorts")
            items.add("smile :)")
            # Looks like summer
            if d['temp']['max'] > 70:
                items.add("beach items")
         
        # Better alignment of last two columns   
        print ('{:<24}{:<24}'.format(condition,', '.join(items)))

        
        
def search_by_cityZip():
    userInput = get_string("Enter Zipcode or City name to search: ")
    if userInput.isnumeric():
        placeDict = search_by_zip(places, userInput)
        display(placeDict)
    else:
        stateCode = get_string("What state? ")
        placeDict = search_by_city(places, userInput, stateCode)
        display(placeDict)
    
    return placeDict
        
def listZipCodes():
    zipCounter = 0
    cityname = get_string("Enter City name to search: ")
    statecode = get_string("What state? ")
    for place in places:
        if cityname.upper() == place['city'].upper():
            if statecode.upper() == place['state'].upper():
                print(place['zip'])
                zipCounter += 1
    
    if zipCounter == 0:
        print("Couldn't find the place.")
    else:
        print(cityname + ", " + statecode + " has " + str(zipCounter) + " zipcodes.")

def showfunFacts():
    statecode = get_string("What state? ")
    minPop = 100000000000 # Setting a high value intially
    maxPop = 0
    minZip = "" # We also need to keep track of the Zipcode for the minimum and maximum values
    maxZip = ""
    found = False
    
    for place in places:
        if statecode.upper() == place['state'].upper():
            if place['population'] == "": # I found some empty population data in csv file
                continue
            else:
                found = True
            
            pop = int(place['population'])
        
            if minPop > pop:
                minPop = pop
                minZip = str(place['zip'])
                
            if maxPop < pop:
                maxPop = pop
                maxZip = str(place['zip'])
    
    if found:
        print("Min population: " + str(minPop) + " at Zipcode: " + minZip)
        print("Max population: " + str(maxPop) + " at Zipcode: " + maxZip)
    else:
        print("Couldn't find the state.")
    

def main():
    #this is your main program that interacts with the user.
    print("Welcome to Places.")

# getting the places list intially
places = get_places()

main()
while True:
    print("""
        
        
        
Menu
    1. Search by Zipcode or City Name
    2. List Zipcodes of a city
    3. Fun Facts about a State
    4. Check the weather
    5. Quit
    """)
    menuInput = get_string("> ")
    if menuInput == "1":
        search_by_cityZip()
    elif menuInput == "2":
        listZipCodes()
    elif menuInput == "3":
        showfunFacts()
    elif menuInput == "4":
        check_weather()
    elif menuInput == "5":
        break
        
        
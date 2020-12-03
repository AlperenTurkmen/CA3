# import libraries(datetime,time)
import time
from datetime import datetime
def weather_printer():
    import json
    with open('weathermapapi.json', 'r') as f:
	    weather = json.load(f)
    print('Description: ' + weather['weather'][0]['description'].capitalize() +
        '\nTemperature: ' + str(round(weather['main']['temp'] - 273)) +'°C' +
        '\nFeels like : ' + str(round(weather['main']['feels_like'] - 273)) +'°C' +
          '\nCity name  : ' + weather['name'])


def weather_api_caller():
    import requests
    import json
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "1645a2975bedad4d907a979d6339bb46"
    city_name = ""
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    # print response object
    response = requests.get(complete_url)
    with open('weathermapapi.json', 'w') as news_file:
        json.dump(response.json(), news_file)
    return response.json()

def weather_finished():
    weather_api_caller()
    weather_printer()

def news_printer():
    import json
    with open('temp.json', 'r') as f:
        news_dict = json.load(f)
        articles = news_dict["articles"]
        for article in articles:
            if '' in article['title'].lower(): #To enter the keyword
                print(article['title'])
                news_loud_reader(article['title'])
        return
def news_api_caller():
    import requests
    import json
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = "abba60cb95ca41ab96fc805234d90cf5"
    country = "tr" #To edit the country
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    # print response object
    response = requests.get(complete_url)
    with open('temp.json', 'w') as news_file:
        json.dump(response.json(), news_file)
    return response.json()
def news_loud_reader(article):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(article)
    engine.runAndWait()
def news_finished():
    news_api_caller()
    news_printer()

print("Hello, welcome to my alarming interface...")
print("It is based on 24 hours clock format...")

Name = input("Enter your name: ")

# printing the current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time is: ", current_time)

# Enter the time(Hours and minute)
Time=input("Enter the time (HH24:MM): ")

# starting the loop
while True:
    # Getting the standard time with the
    # help of datetime module
    Standard_time=datetime.now().strftime("%H:%M")
    # sleep the program for about 1 sec
    time.sleep(1)
    # if condition to check whether the input
    # time has matched or not
    if Time==Standard_time:
        news_finished()
        print("Thankyou For using the Interface")
        break


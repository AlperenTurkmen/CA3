'''This whole code is to display a web based covid-related briefing program.
It targets to help the user by giving them instant notifications about covid
(or else, the user can change the filters.). The user can also schedule an alarm to
remind how serious covid-19 is

Made by Alperen Türkmen'''
import datetime
import json
import logging
import requests
from uk_covid19 import Cov19API
from flask import Flask , render_template , request
import pyttsx3
logging.basicConfig(filename='covid.log',level=logging.DEBUG)
#To log activities and html return codes.
today = datetime.datetime.now()
app = Flask(__name__)
all_news_list = []
deleted_notification = []
announcement_list = []
deleted_announces = []
setted_alarms = []
with open('config.json', 'r') as f:
    conf_read = json.load(f)
logging.info('Program runned')
newsapikey = conf_read['newsapikey']
weatherapikey = conf_read['weatherapikey']
region = conf_read['region']
country = conf_read['country']
postal_abbreviation = conf_read['country postal abbreviation']
favicon = conf_read['favicon']
users_filter = conf_read['user\'s filter']
city = conf_read['city']

def covid_stats():
    '''Calls data from Public Health Service, uses the uk_covid19 module to do this.
    Makes a loud statement report right before finishing.'''
    area_filter = [
        'areaType=nation',
        'areaName=England'
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }
    api = Cov19API(filters=area_filter, structure=cases_and_deaths)
    data = api.get_json()
    date = data['data'][0]['date']
    location = region
    new_deaths = data['data'][0]["newDeathsByDeathDate"]
    new_cases = data['data'][0]["newCasesByPublishDate"]
    total_cases = data['data'][0]["cumCasesByPublishDate"]
    formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    formatted_date = datetime.datetime.strftime(formatted_date, "%-d %B %Y")
    text_to_read_covid = ('Covid news ' + str(location) +
        '. In ' + str(formatted_date) + ', ' + str(new_deaths) +
        ' has died of coronavirus; ' + str(new_cases) + ' people has been diagnosed by covid-19. ' +
        str(total_cases) + ' is the total case in ' + str(location) +'today.')
    announce(text_to_read_covid)

def news_printer():
    '''Reads the just-written json file and adds the news to the all_news_list
    which will be shown in the right-hand-side of the website.'''
    with open('temp.json', 'r') as converted:
        news_dict = json.load(converted)
        articles = news_dict["articles"]
        for article in articles:
            if users_filter in article['title'].lower(): #Filter is imported from the config file.
                if article not in all_news_list:
                    all_news_list.append(article)
        return all_news_list

def news_api_caller():
    '''Joins the entire url to achieve newsapi data, when making this,
     it needs information from the user by confing file.
     And finally writes them in a json file.'''
    date_of_today = datetime.datetime.now()
    date_of_today = date_of_today.strftime("%Y-%m-%d") #To get rid of hour and minute etc.
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = str(newsapikey) #This will be imported from the config file
    country_abb = str(postal_abbreviation) #To edit the country, from config file
    complete_url = base_url + "from=" + str(date_of_today) + \
                   "&country=" + country_abb + "&apiKey=" + api_key
    response = requests.get(complete_url)
    logging.info('News API called')
    with open('temp.json', 'w') as news_file:
        json.dump(response.json(), news_file)
    return response.json()

def all_in_one_news():
    '''Merged in sake of handsomeness...'''
    news_api_caller()
    news_printer()

def announce(announcement):
    '''This has been provided by Matt, it reads the announcements out loud, checks for errors.'''
    engine = pyttsx3.init()
    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop error')
    engine.say(announcement)
    engine.runAndWait() #I found out there is a bug in macintosh,
                        # I can not display multiple announces, it jumps to the last one.

def weather_printer():
    '''First reads the json, brings the arguments from there;
     calculates the centigrade degree of the temperatures, and reads out loud.'''
    with open('weathermapapi.json', 'r') as file:
        weather = json.load(file)
    weather_description = str(weather['weather'][0]['description'])
    weather_temperature = str(round(weather['main']['temp'] - 273))
    weather_feels_like = str(round(weather['main']['feels_like'] - 273))
    weather_city = str(city) #This will be imported from the config file
    weather_information = str('Description: ' + weather['weather'][0]['description'].capitalize() +
        '\nTemperature: ' + str(round(weather['main']['temp'] - 273)) +'°C' +
        '\nFeels like : ' + str(round(weather['main']['feels_like'] - 273)) +'°C' +
          '\nCity name  : ' + str(weather['name']))
    text_to_read = ('There is'+ weather_description + ' in ' + weather_city +' today. ' +
                    'People may feel like it is ' + weather_feels_like + ' degrees' +
                    ' but, our thermometers show:'+ weather_temperature +'degrees!')
    logging.info(weather_information)
    announce(text_to_read)

def weather_api_caller():
    '''Joins the entire url to bring API from, then writes them into a json file. '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = str(weatherapikey) #This will be imported from the config file
    city_name = city #This will be imported from the config file
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    logging.info('Weather API called')
    with open('weathermapapi.json', 'w') as news_file:
        json.dump(response.json(), news_file)
    return response.json()

def weather_finished():
    '''I merged them just to make it look more handsome.'''
    weather_api_caller()
    weather_printer()

def alarm_checker():
    '''Checkes the scheduled alarms if it is time or not,
     after that complies the user's requests
     (weather or news information) '''
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:00")

    # Enter the time(Hours and minute)
    setted_alarms.append(request.args.get('alarm'))
    for sample in announcement_list:
        if str(sample['content']) == str(current_time):
            covid_stats()
            if sample['news'] is not None:
                i = 0
                while i < 3:
                    announce(all_news_list[i]['title'])
                    i +=1
            if sample['weather'] is not None:
                weather_finished()
            announcement_list.remove(sample)
            logging.info('Alarm hour!')

@app.route("/index")
@app.route("/")
def index():
    '''This function schedules alarms, checks if there is a
     scheduled alarm upcoming, adds removes deleted alarms and notifications.
     And finally returns the html page to the user.'''
    logging.info('Page refreshed')
    all_in_one_news()
    alarm_checker()
    notification_id = request.args.get('notif')
    if notification_id is not None:
        deleted_notification.append(notification_id)
        for i in all_news_list:
            if i['title'] == notification_id:
                all_news_list.remove(i)
    announce_title = request.args.get('two')
    if announce_title is not None:
        announce_dict = {'content' : '' , 'date' : '' ,
                            'title' : '' , 'news' : '' , 'weather' : '' , 'alarm_item' : ''}
        alarm_time = str(request.args.get('alarm'))
        announce_dict['content'] = datetime.datetime.strptime(alarm_time, '%Y-%m-%dT%H:%M')
        announce_dict['title'] = request.args.get('two')
        announce_dict['news'] = request.args.get('news')
        announce_dict['weather'] = request.args.get('weather')
        announcement_list.append(announce_dict)
    alarm_item = request.args.get('alarm_item')
    if alarm_item is not None:
        deleted_announces.append(alarm_item)
        for i in announcement_list:
            if i['title'] == alarm_item:
                announcement_list.remove(i)

    return render_template('template.html' , alarms = announcement_list ,
                               notifications = all_news_list , image = favicon )
if __name__ == "__main__":
    app.run()

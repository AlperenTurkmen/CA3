from uk_covid19 import Cov19API
from flask import Flask , render_template , request
import datetime
import json
import requests
today = datetime.datetime.now()
app = Flask(__name__)
all_news_list = []
deleted_notification = []
announcement_list = []
deleted_announces = []
setted_alarms = []
with open('config.json', 'r') as f:
    conf_read = json.load(f)
newsapikey = conf_read['newsapikey']
weatherapikey = conf_read['weatherapikey']
region = conf_read['region']
country = conf_read['country']
postal_abbreviation = conf_read['country postal abbreviation']
favicon = conf_read['favicon']

def covid_stats():
    filter = [
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
    api = Cov19API(filters=filter, structure=cases_and_deaths)
    data = api.get_json()
    #print(data)
    date = data['data'][0]['date']
    location = data['data'][0]['areaName']
    new_deaths = data['data'][0]["newDeathsByDeathDate"]
    new_cases = data['data'][0]["newCasesByPublishDate"]
    total_cases = data['data'][0]["cumCasesByPublishDate"]
    formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    formatted_date = datetime.datetime.strftime(formatted_date, "%-d %B %Y")
    text_to_read_covid = ('Covid news. ' + ' In ' + str(formatted_date) + ', ' + str(new_deaths) +
        ' has died of coronavirus; ' + str(new_cases) + ' people has been diagnosed by covid-19. ' +
        str(total_cases) + ' is the total case in ' + str(location) +'today.')

    announce(formatted_date)
    announce(text_to_read_covid)

def news_printer():
    import json
    with open('temp.json', 'r') as f:
        news_dict = json.load(f)
        articles = news_dict["articles"]
        for article in articles:
            if 'covid' or 'corona' or 'virus'in article['title'].lower(): #To filter the news
                all_news_list.append(article)
                #print(article['title'])
                #announce(article['title'])      #article['title'])
        return all_news_list
def news_api_caller():
    import requests
    import json
    from datetime import date
    today = datetime.datetime.now()
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = str(newsapikey)
    country = str(postal_abbreviation) #To edit the country
    complete_url = base_url + "from=" + str(today) + "&country=" + country + "&apiKey=" + api_key
    print(complete_url)
    response = requests.get(complete_url)
    with open('temp.json', 'w') as news_file:
        json.dump(response.json(), news_file)
    return response.json()
def news_loud_reader(article):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(article)
    engine.runAndWait()
def all_in_one():
    news_api_caller()
    news_printer()
def weather_printer():
    import json
    with open('weathermapapi.json', 'r') as f:
	    weather = json.load(f)
    weather_description = str(weather['weather'][0]['description'])
    weather_temperature = str(round(weather['main']['temp'] - 273))
    weather_feels_like  =  str(round(weather['main']['feels_like'] - 273))
    weather_city        = str(weather['name'])
    weather_information = str('Description: ' + weather['weather'][0]['description'].capitalize() +
        '\nTemperature: ' + str(round(weather['main']['temp'] - 273)) +'°C' +
        '\nFeels like : ' + str(round(weather['main']['feels_like'] - 273)) +'°C' +
          '\nCity name  : ' + str(weather['name']))
    text_to_read = ('There is'+ weather_description + ' in ' + weather_city +' today. ' +
                    'People may feel like it is ' + weather_feels_like + ' degrees' + ' but, our thermometers show:'+ weather_temperature +'degrees!')
    announce(text_to_read)
def announce(announcement):
    import pyttsx3
    engine = pyttsx3.init()
    try:
        engine.endLoop()
    except:
        pass
        #logging.error('PyTTSx3 Endloop error')
    engine.say(announcement)
    engine.runAndWait()

def weather_api_caller():
    import requests
    import json
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = str(weatherapikey)
    city_name = "exeter"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    # print response object
    response = requests.get(complete_url)
    with open('weathermapapi.json', 'w') as news_file:
        json.dump(response.json(), news_file)
    return response.json()
def weather_finished():
    weather_api_caller()
    weather_printer()
def alarm_checker():
    # printing the current time
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:00")

    # Enter the time(Hours and minute)
    setted_alarms.append(request.args.get('alarm'))
    for sample in announcement_list:
        ''' print(sample)
        print(sample['content'])
        print(current_time)
        print(announcement_list)'''
        if str(sample['content']) != str(current_time):
            covid_stats()
            print('Alarm saati')
            #weather_finished()
            if sample['news'] is not None:
                print('Haberler başarılı')
                all_in_one()
            if sample['weather'] is not None:
                print('Hava durumu başarılı')
                weather_finished()
            announcement_list.remove(sample)

@app.route("/index")
@app.route("/")
def index():
    all_in_one()
    alarm_checker()
    notification_id = request.args.get('notif')
    if notification_id is not None:
        deleted_notification.append(notification_id)
        for i in all_news_list:
            if i['title'] == notification_id:
                all_news_list.remove(i)
    announce_title = request.args.get('two')
    if announce_title is not None:
        announce_dict = {'content' : '' , 'date' : '' , 'title' : '' , 'news' : '' , 'weather' : '' , 'alarm_item' : ''}
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
    print(set(setted_alarms))

    return render_template('template.html' , alarms = announcement_list , notifications = all_news_list , image = 'covidimage.png' )
if __name__ == "__main__":
    app.run()

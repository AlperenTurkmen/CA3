import json
conf = {
   "newsapikey" : "___",
     "areaType" : ["overview", "nation", "region"],
    "region" : "",
   "country": "england",
   "country postal abbreviation" : "gb",
    "city": "exeter",
   "weatherapikey" : "___",
   "favicon" : "covidimage.png",
    "user's filter" : "covid"
}
with open('config.json', 'w') as conf_file:
    json.dump(conf , conf_file)
with open('config.json', 'r') as f:
    conf_read = json.load(f)
    print(conf_read)
import json
conf = {
   "newsapikey" : "abba60cb95ca41ab96fc805234d90cf5",
   "region" : "london",
   "country": "england",
   "country postal abbreviation" : "gb",
   "weatherapikey" : "1645a2975bedad4d907a979d6339bb46",
   "favicon" : ["covidimage.png"]
}
with open('config.json', 'w') as conf_file:
    json.dump(conf , conf_file)
with open('config.json', 'r') as f:
    conf_read = json.load(f)
    print(conf_read)
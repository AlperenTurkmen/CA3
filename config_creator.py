import json
conf = {
   "newsapikey" : "66fad8b9efda4f9e9327bd9b7abd488c",
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
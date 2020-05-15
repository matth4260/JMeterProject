import sys, json, time, os

N = sys.argv[1]

with open("json/jobjmetermainsecours.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["metadata"]["name"] = "jobjmetermainsecours" + str(N)
data["spec"]["template"]["metadata"]["name"] = "jobjmetermainsecours" + str(N)
data["spec"]["template"]["spec"]["containers"][0]["name"] = "jobjmetermainsecours" + str(N)

with open("json/jobjmetermainsecours.json", "w") as jsonFile:
    json.dump(data, jsonFile)

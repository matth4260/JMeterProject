import os,json

nbSecoursPath = "/SharedVolume/"
nJob=0
for file in os.listdir(nbSecoursPath):
    if file.startswith("nbSecours"):
        nJob=file[9:]
print(nJob)

crashedInjectorsTXTPath = "/SharedVolume/"
if os.path.isfile(crashedInjectorsTXTPath + 'injectorToRelaunch.txt'):
    nbIP = 0
    with open(crashedInjectorsTXTPath + 'injectorToRelaunch.txt','r') as fin:
        listIP = fin.readlines()
        for ip in listIP:
            nbIP +=1
            



#Change injector job
with open("json/jobjmeterinj.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["spec"]["parallelism"] = nbIP
data["spec"]["completions"] = nbIP
data["metadata"]["name"] = "jobjmeterinj" + str(nJob)
data["spec"]["template"]["metadata"]["name"] = "jobjmeterinj" + str(nJob)
data["spec"]["template"]["spec"]["containers"][0]["name"] = "jobjmeterinj" + str(nJob)

with open("json/jobjmeterinj.json", "w") as jsonFile:
    json.dump(data, jsonFile)

#Change headless service
with open("json/injHeadlessService.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["metadata"]["labels"]["app"] = "jmeter-inj" + str(nJob)
data["metadata"]["name"]= "jmeter-inj" + str(nJob)
data["spec"]["selector"]["job-name"]= "jobjmeterinj" + str(nJob)

with open("json/injHeadlessService.json", "w") as jsonFile:
    json.dump(data, jsonFile)


#Change controler job
with open("json/jobjmetercont.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["metadata"]["name"] = "jobjmetercontsecours" + str(nJob)
data["spec"]["template"]["metadata"]["name"] = "jobjmetercontsecours" + str(nJob)
data["spec"]["template"]["spec"]["containers"][0]["name"] = "jobjmetercontsecours" + str(nJob)

with open("json/jobjmetercont.json", "w") as jsonFile:
    json.dump(data, jsonFile)
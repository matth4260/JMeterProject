import sys, json, time, os

N = int(os.environ['NINJECTOR'])
print("using " + str(N) + " injectors")

with open("json/jobjmeterinj.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["spec"]["parallelism"] = N
data["spec"]["completions"] = N

with open("json/jobjmeterinj.json", "w") as jsonFile:
    json.dump(data, jsonFile)

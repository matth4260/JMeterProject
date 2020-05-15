import sys, json, time
tab = json.load(sys.stdin)['items']

allSucceeded = True


for elem in tab:
	if str(elem['metadata']['name']).startswith("jobjmeterinj"):
		if elem['status']['phase'] != "Succeeded":
			allSucceeded = False
			break

if allSucceeded == True:
	print("True")
else:
	print("False")

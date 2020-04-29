import sys, json, time
tab = json.load(sys.stdin)['items']

allSucceeded = True


for elem in tab:
	if elem['status']['phase'] != "Succeeded":
		allSucceeded = False
		break

if allSucceeded == True:
	print("True")
else:
	print("False")

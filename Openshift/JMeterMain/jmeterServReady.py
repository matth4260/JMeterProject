import sys, json, time
tab = json.load(sys.stdin)['items']

ready = True

for elem in tab:
    if elem['status']['containerStatuses'][0]['ready'] == False:
    		ready = False
    		break

if ready == True:
    print("True")
else:
    print("False")

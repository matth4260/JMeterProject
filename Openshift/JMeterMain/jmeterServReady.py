import sys, json, time
tab = json.load(sys.stdin)['items']

ready = True

for elem in tab:

    if 'status' in elem.keys() and 'containerStatuses' in elem['status'].keys() and elem['status']['containerStatuses'][0]['ready'] == False:
    		ready = False
    		break

if ready == True:
    print("True")
else:
    print("False")

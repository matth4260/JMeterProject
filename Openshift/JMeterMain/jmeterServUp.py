import sys, json, time
tab = json.load(sys.stdin)['items']

ready = True

for elem in tab:
    
    if not('status' in elem.keys()) or  not('phase' in elem['status'].keys()) or  (elem['status']['phase'] != "Running"):
                ready = False
                break

if ready == True:
    print("True")
else:
    print("False")

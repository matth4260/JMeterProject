import sys, json, time, os.path

def manageFailedInjector(ip):
    crashedInjectorsTXTPath = "/SharedVolume/"

    if os.path.isfile(crashedInjectorsTXTPath + 'crashedInjectors.txt'):
        with open(crashedInjectorsTXTPath + 'crashedInjectors.txt', 'r') as fin:
            crashedInjectors = fin.readlines()
    else:
        crashedInjectors = []
    
    injectorAlreadyManaged = False

    for crashedInjectorIP in crashedInjectors:
        if (ip + '\n') == crashedInjectorIP:
            injectorAlreadyManaged = True
    
    if not(injectorAlreadyManaged):
        mode = 'w'
        if os.path.isfile(crashedInjectorsTXTPath + 'crashedInjectors.txt'):
            mode = 'a'
        with open(crashedInjectorsTXTPath + 'crashedInjectors.txt', mode) as fout:
            fout.write(ip + '\n')
            return True
    
    return False






tab = json.load(sys.stdin)['items']
crashedInjectors = []
nbOfCrashedInjectors = 0
for elem in tab:
    if 'status' in elem.keys() and 'phase' in elem['status'].keys() and elem['status']['phase'] == 'Failed' and str(elem['metadata']['name']).startswith("jobjmeterinj"):
    	if manageFailedInjector(elem['status']['podIP']):
		    crashedInjectors.insert(nbOfCrashedInjectors, elem['status']['podIP'])


for ip in crashedInjectors:
    injectorToRelaunchTXTPath = "/SharedVolume/"
    mode = 'w'
    if os.path.isfile(injectorToRelaunchTXTPath + "injectorToRelaunch.txt"):
        mode = 'a'
    with open(injectorToRelaunchTXTPath + "injectorToRelaunch.txt",mode) as fin:
        fin.write(ip + '\n')

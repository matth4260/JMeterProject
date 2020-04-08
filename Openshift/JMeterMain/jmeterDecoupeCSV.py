import sys
import os

def splitcsv(name, list_ip):
	print(name)


list_ip = sys.argv[1].split(';')
DIR = "csv/"

for file in os.listdir(DIR):
	if file.endswith(".csv"):
		file_name = os.path.join(DIR,file)
		splitcsv(file_name,list_ip)


if not os.path.exists('READY'): 
	file = open("./READY",'w')


import sys
import os

ip = sys.argv[1]
for file in os.listdir("/apache-jmeter-5.2.1/bin/"):
	if file.endswith(".csv"):
		new_name = file[:-(4+len(ip)+1)] + ".csv" #4 : .csv and 1 : -
		os.rename(file, new_name)

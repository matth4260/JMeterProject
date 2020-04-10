import sys
import os

def splitcsv(name, list_ip):

	file_path = '/SharedVolume/csv/'
	dest_path = '/SharedVolume/csvModif/'
	file_path = file_path + name + ".csv"

	try:
		csv_all_lines = open(file_path, 'r',encoding='utf-8').readlines()

		# extraction du header
		header = csv_all_lines[0]

		# supprimer le header
		csv_all_lines.pop(0)

		# Nombre de lignes
		row_count = len(csv_all_lines)

		nb_ip = len(list_ip)

		record_per_file = row_count // nb_ip

		for i in range(len(list_ip)):

			write_file = header
			for j in csv_all_lines[i*record_per_file:(i+1)*record_per_file]:
				write_file += j
			# creation du fichier
			open(dest_path + name+'-'+str(list_ip[i])+'.csv', 'w+',encoding='utf-8').writelines(write_file)
		return 0
	except:
		return 1

	

list_ip = sys.argv[1].split(',')
DIR = "/SharedVolume/csv/"
WORKING = "True"

#DIR = "csv/"

for file in os.listdir(DIR):
	if file.endswith(".csv"):
		file_name = file[0:-4]
		if splitcsv(file_name,list_ip) != 0:
			WORKING = "False"


if not os.path.exists('/SharedVolume/csvModif/READY'): 
	file = open("/SharedVolume/csvModif/READY",'w',encoding='utf-8')

print(WORKING)

import sys
import os

def splitcsv(name, list_ip):

	file_path = '/SharedVolume/csv/'
	dest_path = '/SharedVolume/csvModif/'
	file_path = file_path + name + ".csv"
	print("Filepath = " + file_path)
	csv_all_lines = open(file_path, 'r').readlines()

	# extraction du header
	header = csv_all_lines[0]

	# supprimer le header
	csv_all_lines.pop(0)

	# Nombre de lignes
	row_count = len(csv_all_lines)
	print("nombre de lignes : " + str(row_count))

	nb_ip = len(list_ip)
	print("Nombre d'ip : " + str(nb_ip))

	record_per_file = row_count // nb_ip
	print("nb de ligne par nouveau fichier : " + str(record_per_file))

	for i in range(len(list_ip)):

		write_file = header
		for j in csv_all_lines[i*record_per_file:(i+1)*record_per_file]:
			write_file += j
		# creation du fichier
		open(dest_path + name+'-'+str(list_ip[i])+'.csv', 'w+').writelines(write_file)
		print("J'écris dans " + name + "-" + str(list_ip[i]) + ".csv")
		print("J'ecris : " + write_file)


list_ip = sys.argv[1].split(';')
DIR = "/SharedVolume/csv/"
#DIR = "csv/"

for file in os.listdir(DIR):
	if file.endswith(".csv"):
		file_name = file[0:-4]
		splitcsv(file_name,list_ip)


if not os.path.exists('/SharedVolume/csvModif/READY'): 
	file = open("/SharedVolume/csvModif/READY",'w')

import sys
import os.path


#def decouperUnFichierCSV(name, list_ip)
name = 'user_creation_compte'
list_ip = ["192.0.0.1","192.0.0.2"]

file_path = 'csv/'
dest_path = 'csvModif/'
file_path = file_path + name +".csv"
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
        for j in csv_all_lines[i*record_per_file:(i+1)*record_per_file - 1]:	
                write_file += j
        # creation du fichier
        open(dest_path + name+'-'+str(list_ip[i])+'.csv', 'w+').writelines(write_file)
        print("J'écris dans " + name + "-" + str(list_ip[i]) + ".csv")
        print("J'ecris : " + write_file)

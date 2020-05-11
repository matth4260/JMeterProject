import sys
import os
import csv


def removeLinesInFile(csvName, csvPath,txtPath):
	usedLinesFileName = csvName + "UsedLines.txt"

	with open(txtPath + csvName + 'WithoutUsedLines.csv', 'w') as fout:
		writer = csv.writer(fout)

		usedLines = open(txtPath + usedLinesFileName, 'r',encoding='utf-8').readlines()
		print(usedLines[0])
		csvLines = open(csvPath + csvName + '.csv', 'r',encoding='utf-8').readlines()

		for csvLine in csvLines[1:]:
			if int(csvLine[0:csvLine.find(';')]) <= int(usedLines[0]):
				csvLines.pop(1)
			else:
				break

		
		open(txtPath + csvName + 'WithoutUsedLines.csv', 'w+',encoding='utf-8').writelines(csvLines)

	os.remove(csvPath + csvName + ".csv")
	os.remove(txtPath + usedLinesFileName)
	os.rename(txtPath + csvName + 'WithoutUsedLines.csv', csvPath + csvName + '.csv')



def mergeCSVFiles(csvName,csvToMergePath, csvPath):


	csvHeader = open(csvPath + csvName + ".csv", 'r',encoding='utf-8').readline()
	open(csvPath + csvName + "WithoutUsedLines.csv", 'w',encoding='utf-8').writelines(csvHeader)

	filesToMerge = False
	for file in os.listdir(csvToMergePath):
		if file.startswith(csvName):
			filesToMerge = True
			linesToAdd = open(csvToMergePath + file, 'r',encoding='utf-8').readlines()
			linesToAdd.pop(0) #removing header
			f = open(csvPath + csvName + "WithoutUsedLines.csv", 'a',encoding='utf-8')
			f.writelines(linesToAdd)
			if not(linesToAdd[-1].endswith('\n')):
				f.write('\n')
			os.remove(csvToMergePath + file)

	if filesToMerge:
		print("merge done")
		os.remove(csvPath + csvName + ".csv")
		os.rename(csvPath + csvName + "WithoutUsedLines.csv", csvPath + csvName + ".csv")
	else:
		print("no merge to do")
		os.remove(csvPath + csvName + "WithoutUsedLines.csv")


def mergeUsedLinesTxt(csvName, txtPath):
	print("For " + csvName)
	nbUsedLines = 0
	filesToMerge = False
	for file in os.listdir(txtPath):
		if file.startswith(csvName) and file.endswith("UsedLines.txt"):
			filesToMerge = True
			fileLinesUsed = open(txtPath + file, 'r',encoding='utf-8').readlines()
			print("we read in txt : " + fileLinesUsed[0])
			if int(fileLinesUsed[0]) > nbUsedLines:
				nbUsedLines=int(fileLinesUsed[0])
			os.remove(txtPath + file)
	print("Lines : " + str(nbUsedLines))
	if filesToMerge:
		open(txtPath + csvName + "UsedLines.txt",'w').writelines(str(nbUsedLines))
	return filesToMerge

def refreshUniqueID(csvPath,csvName):
	with open(csvPath + csvName + ".csv", "r", encoding='utf-8') as fin, open(csvPath + csvName + "RefreshedID.csv", "w",encoding='utf-8') as fout:
		reader = csv.reader(fin,delimiter=';')
		writer = csv.writer(fout,delimiter=';')
		i=0
		for row in reader:
			if i==0:
				writer.writerow(row)
			else:
				row[0] = str(i)
				writer.writerow(row)
			i+=1
	os.remove(csvPath + csvName + ".csv")
	os.rename(csvPath + csvName + "RefreshedID.csv", csvPath + csvName + ".csv")



	
	
	

                    
csvPath = "/SharedVolume/csv/"
csvModifPath = "/SharedVolume/csvModif/"

for file in os.listdir(csvModifPath):
	if file.endswith(".csv"):
		csvname = file[:-4]
		print("Merging TXT")
		if mergeUsedLinesTxt(csvname,csvModifPath):
			print("Removing Lines in file")
			removeLinesInFile(csvname,csvModifPath, csvModifPath)

for file in os.listdir(csvPath):
	if file.endswith(".csv"):
		csvname = file[:-4]
		print("merging csv files")
		mergeCSVFiles(csvname,csvModifPath,csvPath)
		print("refres unique ID")
		refreshUniqueID(csvPath,csvname)



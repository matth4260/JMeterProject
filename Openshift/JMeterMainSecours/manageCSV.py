import os,sys,csv


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


def changeCSV(previousIP,newIP):
	csvModifPath="/SharedVolume/csvModif/"
	csvPath="/SharedVolume/csv/"



	for file in os.listdir(csvPath):
		if file.endswith(".csv"):
			filename = file[:-4]
			if(mergeUsedLinesTxt(filename + "-" + previousIP,csvModifPath)):
				removeLinesInFile(filename + "-" + previousIP,csvModifPath,csvModifPath)
			os.rename(csvModifPath + filename + '-' + previousIP + '.csv',csvModifPath + filename + '-' + newIP + ".csv")

with open("/SharedVolume/injectorToRelaunch" + sys.argv[1] + ".txt",'r') as fin:
    listCrashedIPs = fin.readlines()
    listNewIPs = sys.argv[2].split(',')
    i = 0
    for crashedIP in listCrashedIPs:
        changeCSV(crashedIP[:-1],listNewIPs[i])
        i+=1



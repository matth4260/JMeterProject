import sys
import os
import csv


def removeLinesInFile(csvName, filesPath):
	usedLinesFileName = csvName + "UsedLines.txt"

	with open(filesPath + csvName + 'WithoutUsedLines.csv', 'w') as fout:
		writer = csv.writer(fout)

		usedLines = open(filesPath + usedLinesFileName, 'r',encoding='utf-8').readlines()
		print(usedLines[0])
		csvLines = open(filesPath + csvName + '.csv', 'r',encoding='utf-8').readlines()

		for csvLine in csvLines[1:]:
			if int(csvLine[0:csvLine.find(',')]) <= int(usedLines[0]):
				csvLines.pop(1)
			else:
				break

		
		open(filesPath + csvName + 'WithoutUsedLines.csv', 'w+',encoding='utf-8').writelines(csvLines)

	os.remove(filesPath + csvName + ".csv")
	os.remove(filesPath + usedLinesFileName)
	os.rename(filesPath + csvName + 'WithoutUsedLines.csv', filesPath + csvName + '.csv')



def mergeCSVFiles(csvName):

	csvPath = "/Users/leanovia/Downloads/csv/"
	csvToMergePath = "/Users/leanovia/Downloads/csvModif/"


	csvHeader = open(csvPath + csvName + ".csv", 'r',encoding='utf-8').readline()
	open(csvPath + csvName + "WithoutUsedLines.csv", 'w',encoding='utf-8').writelines(csvHeader)

	for file in os.listdir(csvToMergePath):
		print("watching " + file)
		if file.startswith(csvName):
			print("in if")
			linesToAdd = open(csvToMergePath + file, 'r',encoding='utf-8').readlines()
			linesToAdd.pop(0) #removing header
			open(csvPath + csvName + "WithoutUsedLines.csv", 'a',encoding='utf-8').writelines(linesToAdd)
			print(linesToAdd)


def mergeUsedLinesTxt(csvName):
	txtPath = "/Users/leanovia/Downloads/"

	nbUsedLines = 0
	for file in os.listdir(txtPath):
		if file.startswith(csvName) and file.endswith("UsedLines.txt"):
			fileLinesUsed = open(txtPath + file, 'r',encoding='utf-8').readlines()
			if int(fileLinesUsed[0]) > nbUsedLines:
				nbUsedLines=int(fileLinesUsed[0])
			os.remove(txtPath + file)
	
	open(txtPath + csvName + "UsedLines.txt",'w').writelines(str(nbUsedLines))
	
	
	

                    
DIR = "/Users/leanovia/Downloads/"

mergeUsedLinesTxt("customcsv")
removeLinesInFile("customcsv",DIR)



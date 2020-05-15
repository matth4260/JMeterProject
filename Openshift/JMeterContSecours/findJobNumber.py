import os

nbSecoursPath = "/SharedVolume/"
nJob=0
for file in os.listdir(nbSecoursPath):
    if file.startswith("nbSecours"):
        nJob=file[9:]

print(str(nJob))
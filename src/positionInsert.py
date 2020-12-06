import time
from src.lib.typeclass import FA, PA, PAA, PC
from src.position import insertpos
from os import listdir


start = time.time()
path = "data/position/"

files = listdir(path)
FAFiles = list(filter((lambda x: x.startswith("FA")), files))
PAFiles = list(filter((lambda x: x.startswith("PA")), files))
PAAFiles = list(filter((lambda x: x.startswith("PAA")), files))
PAFiles = [x for x in PAFiles if x not in PAAFiles]
PCFiles = list(filter((lambda x: x.startswith("PC")), files))

for file in FAFiles:
    insertpos(path+file, FA)

for file in PAFiles:
    insertpos(path+file, PA)

for file in PAAFiles:
    insertpos(path+file, PAA)

for file in PCFiles:
    insertpos(path+file, PC)


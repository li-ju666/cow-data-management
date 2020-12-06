from src.cowInfo import insertHealth, insertInfo
from os import listdir

path = "data/info/"

files = listdir(path)
KOFiles = list(filter((lambda x: x.startswith("KO")), files))
HealthFiles = list(filter((lambda x: x.startswith("Översikt")), files))

for file in KOFiles:
    insertInfo(path+file)

for file in HealthFiles:
    insertHealth(path+file)

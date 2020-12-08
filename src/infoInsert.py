from src.cowInfo import insertHealth, insertInfo, insertRef
from os import listdir

path = "data/info/"

files = listdir(path)
KOFiles = list(filter((lambda x: x.startswith("KO")), files))
KOFiles.sort()
HealthFiles = list(filter((lambda x: x.startswith("Översikt")), files))
HealthFiles.sort()
for file in KOFiles:
    #insertInfo(path+file)
    print(file)
    insertRef(path+file)
#
# for file in HealthFiles:
#     insertHealth(path+file)
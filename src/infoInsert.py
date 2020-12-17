from src.cowInfo import insertHealth, insertInfo, insertRef, insertMilk
from os import listdir

path = "data/info/"

files = listdir(path)

KOFiles = list(filter((lambda x: x.startswith("KO")), files))
KOFiles.sort()

HealthFiles = list(filter((lambda x: x.startswith("Översikt")), files))
HealthFiles.sort()

AvFiles = list(filter((lambda x: x.startswith("Avkastn")), files))
AvFiles.sort()

MilkFiles = list(filter((lambda x: x.startswith("Mjölkplats")), files))
MilkFiles.sort()


print(AvFiles)
print(MilkFiles)

# for i in range(len(AvFiles)):
#     insertMilk(path+AvFiles[i], path+MilkFiles[i])

# for file in KOFiles:
#     insertInfo(path+file)
#     print(file)
#     insertRef(path+file)
#
#
for file in HealthFiles:
    insertHealth(path+file)
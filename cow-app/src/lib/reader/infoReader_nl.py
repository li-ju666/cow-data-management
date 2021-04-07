import pandas as pd
import numpy as np
import math
from re import findall


# Reads non-empty rows of "Cow Data mmm - Vim.xlsx"
# Returns [[cow_id, ISO, tag_str, start_date, comment]]
def readCowData(filename):
    WS = pd.read_excel(filename)
    WS_np = np.array(WS)
    returnList = []

    for row in WS_np[0:]:
        # Skip row if blank or lack info
        if math.isnan(row[0]):
            continue
        if math.isnan(row[1]):
            continue

        cow_id = int(row[0])
        ISO = int(row[1])
        tag_str = row[2]
        start_date = row[3].strftime("%Y-%m-%d")
        comment = row[4]

        returnList.append([
            cow_id,
            ISO,
            tag_str,
            start_date,
            comment
        ])

    return returnList


# Adds filedate as the first entry and then all other entries
# Returns [[filedate, Cow_id, name, ISO, Celget, ..., LW]]
def readMilkData(filename):
    WS = pd.read_excel(filename)
    WS_np = np.array(WS)

    # fn = filename.split()

    returnList = []

    for row in WS_np[0:]:
        cow_id = row[0]
        name = row[1]
        Levnr = row[2][3] + row[2][4] + row[2][5] + row[2][6] + row[2][8] + row[2][9] + row[2][10] + row[2][11] + \
                row[2][13]
        kg_melk_dag = row[3]
        ISK = row[4]
        frac_v = row[5]
        eiw_frac_dag = row[6]
        lact_frac_dag = row[7]
        ur_dag = row[8]
        celget = row[9]
        klf_dat = row[10]
        lft_afk = row[11]
        MPR_lft = row[12]
        lactnr = row[13]
        lactatiedagen = row[14]
        kg_melk_tot_lact = row[15]
        kg_melk_tot_305 = row[16]
        vet_frac_lact = row[17]
        vet_frac_305 = row[18]
        eiwit_frac_lact = row[19]
        eiwit_frac_305 = row[20]
        kg_vet_lact = row[21]
        kg_vet_305 = row[22]
        kg_eiwit_lact = row[23]
        kg_eiwit_305 = row[24]
        LW = row[25]

        returnList.append([
            cow_id,
            name,
            Levnr,
            kg_melk_dag,
            ISK,
            frac_v,
            eiw_frac_dag,
            lact_frac_dag,
            ur_dag,
            celget,
            klf_dat,
            lft_afk,
            MPR_lft,
            lactnr,
            lactatiedagen,
            kg_melk_tot_lact,
            kg_melk_tot_305,
            vet_frac_lact,
            vet_frac_305,
            eiwit_frac_lact,
            eiwit_frac_305,
            kg_vet_lact,
            kg_vet_305,
            kg_eiwit_lact,
            kg_eiwit_305,
            LW
        ])
    return returnList
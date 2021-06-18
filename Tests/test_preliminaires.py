import sqlite3 as sql
import os
import pandas as pd

##Vérifions que les candidats dans les fichiers SCEI_XXX sont aussi dans tous les autres fichiers##

candidats_codes_SCEI = []
candidats_codes = []
direction = './../data'
non_SPE = []
SPE = []

for excel in os.listdir(direction):
    #1
    if excel.endswith("SCEI.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(1, len(a) - 1):
            if a.loc[i, "scei"] not in candidats_codes_SCEI:
                candidats_codes_SCEI.append(a.loc[i, "scei"])
    elif excel.endswith(".xlsx") and excel.startswith("ADMIS"):
        #Dans les excels Admis_XXX et Admissibles_XXX, le code est de la forme "Can _cod" 
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(len(a) - 1):
            code_etudiant = a.loc[i, 'Can _cod']
            if code_etudiant not in candidats_codes:
                candidats_codes.append(code_etudiant)
    elif excel.endswith(".xlsx") and excel.startswith("Inscript"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(1, len(a) - 2):
            if a.loc[i, " "] not in candidats_codes:
                candidats_codes.append(a.loc[i, " "])
    #2
    elif excel.startswith("ADMIS"):
        if excel.endswith("SPE.xlsx"):
            path = os.path.join(direction, excel)
            a = pd.read_excel(path, engine="openpyxl")
            for i in range(1, len(a) - 1):
                if a.loc[i, "Can _cod"] not in SPE:
                    SPE.append(a.loc[i, "Can _cod"])
        else:
            path = os.path.join(direction, excel)
            a = pd.read_excel(path, engine="openpyxl")
            for i in range(1, len(a) - 1):
                if a.loc[i, "Can _cod"] not in non_SPE:
                    non_SPE.append(a.loc[i, "Can _cod"])
        



#1 - Vérification que les candidats de SCEI sont bien dans les autres excels utilisés :
def test_candidats_SCEI_dans_autres_excels():
    for code in candidats_codes_SCEI:
        assert(code in candidats_codes)

#2 - Vérification que tous les candidats dans les SPE sont aussi dans les non SPE
def test_candidats_SPE():
    for code in SPE:
        assert (code in non_SPE)
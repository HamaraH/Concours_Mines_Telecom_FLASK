import sys
sys.path.append("..")
import main

def getClassementByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT  libelle, rang  FROM CLASSEMENT AS C, TYPE_ADMISSION AS TA WHERE C.can_cod = ? AND TA.id = C.type_rang ''', (code_candidat,))

    rows = result.fetchall()
    final_data = []

    for i in range(0, len(rows)):
        if rows[i][0] == "ADMISSIBLE":
            final_data.append(('ECRIT', rows[i][1]))
        if rows[i][0] == "ADMIS":
            final_data.append(('ECRIT + ORAL', rows[i][1]))

    return final_data


def getRangGeneralByEleve(code_candidat):


    db = main.get_db()
    result = db.execute(''' SELECT rang  FROM CLASSEMENT AS C, TYPE_ADMISSION AS TA WHERE C.can_cod = ? AND TA.libelle = "ADMIS" AND TA.id = C.type_rang ''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""

def getRangEcritByEleve(code_candidat):


    db = main.get_db()
    result = db.execute(''' SELECT rang  FROM CLASSEMENT AS C, TYPE_ADMISSION AS TA WHERE C.can_cod = ? AND TA.libelle = "ADMISSIBLE" AND TA.id = C.type_rang ''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""
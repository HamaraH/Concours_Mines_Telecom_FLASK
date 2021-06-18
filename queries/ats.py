import sys
sys.path.append("..")
import main


def getAllEleveATS():

    db = main.get_db()
    result = db.execute(''' SELECT  nom, prenom, can_cod FROM ATS ORDER BY (can_cod) ASC''')

    rows = result.fetchall()

    return rows

def getATSInfosByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT  nom, prenom, adresse, complement_adresse, cp, mail, num_fixe , num_portable FROM ATS WHERE ATS.can_cod = ?''', (code_candidat,))

    rows = result.fetchall()

    return rows

def isATS(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT  nom, prenom, adresse, complement_adresse, cp, mail, num_fixe , num_portable FROM ATS WHERE ATS.can_cod = ?''',(code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return True
    else:
        return False

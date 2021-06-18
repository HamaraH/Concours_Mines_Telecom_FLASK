import sys
sys.path.append("..")
import main


def getVoeuxByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT nom_ecole, ordre_voeux, reponse  FROM VOEUX AS V, ECOLE AS E  WHERE V.can_cod = ? AND V.code_ecole = E.code_ecole ORDER BY (ordre_voeux) ASC ''', (code_candidat,))

    rows = result.fetchall()

    return rows

def isDefined():

    db = main.get_db()
    result = db.execute(''' SELECT reponse FROM VOEUX''')

    rows = result.fetchall()

    if rows[0][0] == None:
        return False
    else:
        return True

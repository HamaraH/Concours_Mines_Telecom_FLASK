import sys
import main
sys.path.append("..")


def getAllEcoles():

    db = main.get_db()
    result = db.execute('''SELECT code_ecole,nom_ecole FROM ECOLE ORDER BY (nom_ecole) ASC ''')

    rows = result.fetchall()

    return rows

def getAllInfo(code_ecole):

    db = main.get_db()
    result = db.execute('''SELECT * FROM ECOLE WHERE code_ecole = ? ''',code_ecole)

    rows = result.fetchall()

    return rows

def getAllEcolesRne():

    db = main.get_db()
    result = db.execute('''SELECT code_ecole,nom_ecole FROM ECOLE ORDER BY (nom_ecole) ASC ''')

    rows = result.fetchall()

    final_data = []

    for i in range(0, len(rows)):
        final_data.append((rows[i][0], rows[i][1]))
    return final_data
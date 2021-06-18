import sys
import main
sys.path.append("..")

def getAllFilieres():

    db = main.get_db()
    result = db.execute(''' SELECT libelle_filiere FROM FILIERE''')

    rows = result.fetchall()
    result = []

    for i in range(0, len(rows)):
        if rows[i][0] != "ATS":
            result.append(rows[i][0])

    return result
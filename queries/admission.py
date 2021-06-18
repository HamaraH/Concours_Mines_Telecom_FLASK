import sys
sys.path.append("..")
import main


def getAdmissionByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT libelle FROM ADMISSION, TYPE_ADMISSION WHERE ADMISSION.can_cod = ? AND ADMISSION.id_type_admission = TYPE_ADMISSION.id''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return rows
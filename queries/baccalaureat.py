import sys
sys.path.append("..")
import main


def getBaccalaureatInfosByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT S.libelle, mention, departement, M.libelle, annee_obtention FROM BACCALAUREAT AS B, SERIE AS S, MOIS AS M
                            WHERE B.can_cod = ? AND B.code_serie=S.code_serie AND B.mois_obtention=M.id''', (code_candidat,))

    rows = result.fetchall()

    return rows

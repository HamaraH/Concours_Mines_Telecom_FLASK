import sys
sys.path.append("..")
import main

def getEpreuvesByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT DISTINCT libelle FROM TYPE_EPREUVE AS TE, RESULTAT AS R WHERE R.can_cod = ? AND R.type_epreuve = TE.id  ''', (code_candidat,))

    rows = result.fetchall()
    final_results = []

    for i in range(0, len(rows)):
        if rows[i][0] != "Harmonisation" and rows[i][0] != "Notes Ecrites" and rows[i][0] != "Notes orales Concours Mines-Télécom" and rows[i][0] != "Total" :
            final_results.append(rows[i])

    return final_results
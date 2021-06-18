import sys
import main
import queries.parcours_prepa
sys.path.append("..")

def getMatiereByFiliere(filiere):

    db = main.get_db()
    result = db.execute(''' SELECT DISTINCT libelle
                            FROM ELEVE AS E, RESULTAT AS R, MATIERE AS M, FILIERE AS F
                            WHERE E.id_filiere=F.code_concours
                            AND F.libelle_filiere= ?
                            AND E.can_cod = R.can_cod
                            AND R.id_matiere=M.id_matiere''', (filiere,))

    rows = result.fetchall()

    storage = []

    for i in range(0, len (rows)):
        if rows[i][0] != "total_ecrit" and rows[i][0] != "total_oral" and rows[i][0] != "total" and rows[i][0] != "total_avec_interclassement" and rows[i][0] != "Mathématiques (harmonisée)" and rows[i][0] != "Mathématiques (affichée)":
            storage.append(rows[i][0])

    return storage

def getMatiereByFiliereAndTypeEpreuve(filiere, type_epreuve):

    db = main.get_db()
    result = db.execute(''' SELECT DISTINCT M.libelle
                             FROM ELEVE AS E, RESULTAT AS R, MATIERE AS M, FILIERE AS F, TYPE_EPREUVE AS TE
                             WHERE E.id_filiere=F.code_concours
                             AND F.libelle_filiere= ?
                             AND E.can_cod = R.can_cod
                             AND R.id_matiere=M.id_matiere
                             AND TE.libelle = ?
                             AND TE.id = R.type_epreuve''', (filiere,type_epreuve))

    rows = result.fetchall()

    storage = []
    options = []

    for i in range(0, len(rows)):
        if rows[i][0] != "total_ecrit" and rows[i][0] != "total_oral" and rows[i][0] != "total" and rows[i][
            0] != "total_avec_interclassement" and rows[i][0] != "Mathématiques (harmonisée)" and rows[i][
            0] != "Mathématiques (affichée)" and rows[i][0] != "Langue" and rows[i][0] != "Informatique ou Sciences industrielles":
            storage.append(rows[i][0])



    if type_epreuve == "Notes Ecrites":

        langues = queries.parcours_prepa.getOptionsByFiliere(filiere)

        if filiere == "MP":

            options.append("Informatique")
            options.append("Sciences Industrielles")
            return storage, langues, options

        return storage, langues

    elif type_epreuve == "Notes orales Concours Mines-Télécom":

        return storage
import sys
sys.path.append("..")
import main

def getLangueLibelle(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT O.option FROM OPTION AS O, PARCOURS_PREPA AS P, ELEVE AS E WHERE E.can_cod = ? AND P.can_cod = E.can_cod AND P.option1=O.id_option ''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""

def getParcoursPrepaByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT ET.nom_etab, sujet_TIPE, puissance
                            FROM PARCOURS_PREPA AS P, ELEVE AS E
                            JOIN ETABLISSEMENT ET ON E.code_etablissement = ET.Rne
                            AND E.can_cod = ?
                            AND P.can_cod = E.can_cod
                            LIMIT (1)''', (code_candidat,))

    rows = result.fetchall()

    if rows == []:
        return ""
    else:
        rows = rows[0]
        final_result = []

        if rows[0] == None:
            final_result=("",rows[1], rows[2])
            return final_result
        else:
            return rows

def getOptionsByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT o1.option, o2.option, o3.option, o4.option
                            FROM PARCOURS_PREPA AS P
                            INNER JOIN OPTION o1 ON P.option1 = o1.id_option
                            INNER JOIN OPTION o2 ON P.option2 = o2.id_option
                            INNER JOIN OPTION o3 ON P.option3 = o3.id_option
                            INNER JOIN OPTION o4 ON P.option4 = o4.id_option
                            AND P.can_cod = ? ''', (code_candidat,))

    rows = result.fetchall()

    if rows == []:
        return ""
    else:
        rows = rows[0]  # Un candidat n'a qu'une ligne qui lui correspond, on la séléctionne directement
        final_result = []

        for i in range(len(rows)):  # Tous les candidats n'ont pas 4 options, on filtre si les valeurs sont vides
            if (rows[i] != None):
                final_result.append(rows[i])

    return final_result


def getOptionsByFiliere(filiere):

    db = main.get_db()
    result = db.execute('''SELECT DISTINCT(O.option) FROM ELEVE AS E, PARCOURS_PREPA AS P, FILIERE AS F, OPTION AS O
                           WHERE E.can_cod = P.can_cod
                           AND E.id_filiere = F.code_concours
                           AND F.libelle_filiere = ?
                           AND O.id_option = P.option1  ''', (filiere,))

    rows = result.fetchall()
    storage = []

    for i in range(0, len(rows)):
        storage.append(rows[i][0])

    return storage
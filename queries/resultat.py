import queries.classement
import queries.type_epreuve
import queries.admission
import queries.parcours_prepa
import sys
sys.path.append("..")
import main


def getNotesByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT libelle, note FROM RESULTAT AS R, MATIERE AS M WHERE R.can_cod = ? AND R.id_matiere = M.id_matiere ''', (code_candidat,))

    rows = result.fetchall()
    final_results = []

    for i in range(0, len(rows)):
        if rows[i][1] < 20:
            final_results.append(rows[i])

    return final_results

def getResultatEleveByTypeEpreuve(code_candidat, type_epreuve):

    db = main.get_db()
    result = db.execute(''' SELECT M.libelle, note FROM RESULTAT AS R,  MATIERE AS M, TYPE_EPREUVE AS TE WHERE R.can_cod = ? AND R.type_epreuve = TE.id AND TE.libelle = ? AND R.id_matiere = M.id_matiere''',
        (code_candidat, type_epreuve))

    rows = result.fetchall()

    return rows

def getTotalEcritByEleveAndTypeEpreuve(code_candidat, type_epreuve):

    db = main.get_db()
    result = db.execute(''' SELECT SUM(note) FROM RESULTAT AS R, TYPE_EPREUVE AS TE WHERE R.can_cod = ? AND R.type_epreuve = TE.id AND TE.libelle = ? ''',
    (code_candidat, type_epreuve))

    rows = result.fetchall()

    return rows

def getNotesEcritesByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT M.libelle, note FROM RESULTAT AS R, TYPE_EPREUVE AS TE, MATIERE AS M WHERE M.id_matiere = R.id_matiere AND R.can_cod = ? AND TE.id = R.type_epreuve AND TE.libelle = "Notes Ecrites" ''', (code_candidat,))

    rows = result.fetchall()

    storage = []

    for i in range(0, len(rows)):
        if rows[i][0] == "Langue":
            storage.append((queries.parcours_prepa.getLangueLibelle(code_candidat),rows[i][1]))
        else:
            storage.append(rows[i])

    return storage

def getNotesOralesByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT M.libelle, note FROM RESULTAT AS R, TYPE_EPREUVE AS TE, MATIERE AS M WHERE M.id_matiere = R.id_matiere AND R.can_cod = ? AND TE.id = R.type_epreuve AND TE.libelle = "Notes orales Concours Mines-Télécom" ''', (code_candidat,))

    rows = result.fetchall()

    return rows

def getTotalEcritByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT note FROM RESULTAT AS R, MATIERE AS M WHERE M.id_matiere = R.id_matiere AND R.can_cod = ? AND M.libelle = "total_ecrit" ''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""

def getMoyenneEcritByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT AVG(note) FROM RESULTAT AS R, MATIERE AS M, TYPE_EPREUVE AS TE WHERE TE.libelle = "Notes Ecrites" AND TE.id = R.type_epreuve AND M.id_matiere = R.id_matiere AND R.can_cod = ? ''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""

def getBarreEcrit(code_candidat):

    db = main.get_db()

    result = db.execute(''' SELECT MAX(rang) FROM ELEVE AS E,FILIERE AS F, TYPE_ADMISSION AS TA, CLASSEMENT AS C
    WHERE TA.libelle="ADMISSIBLE" AND TA.id = C.type_rang
    AND F.code_concours=E.id_filiere AND E.can_cod = ?''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""

def getTotalGeneralByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT note FROM RESULTAT AS R, MATIERE AS M WHERE M.id_matiere = R.id_matiere AND R.can_cod = ? AND M.libelle = "total" ''', (code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0][0]
    else:
        return ""

def computeNoteData(code_candidat):

    concours = queries.type_epreuve.getEpreuvesByEleve(code_candidat)
    if concours != []:
        storage = []
        for i in range(0, len(concours)):
            values = getResultatEleveByTypeEpreuve(code_candidat, concours[i][0])
            storage.append(values)

        statut = queries.admission.getAdmissionByEleve(code_candidat)
        total_ecrit = getTotalEcritByEleve(code_candidat)
        moyenne_ecrit = round(getMoyenneEcritByEleve(code_candidat), 2)
        rang_ecrit = queries.classement.getRangEcritByEleve(code_candidat)
        barre_ecrit = getBarreEcrit(code_candidat)
        total_general = getTotalGeneralByEleve(code_candidat)
        moyenne_generale = getMoyenneGeneraleByEleve(code_candidat)
        rang_general = queries.classement.getRangGeneralByEleve(code_candidat)

        data = (statut, total_ecrit, moyenne_ecrit, rang_ecrit, barre_ecrit, total_general, moyenne_generale, rang_general)

        return concours, storage, data
    else:
        return [], [], []

def getAvgByMatiere(matiere):

    db = main.get_db()
    result = db.execute(''' SELECT AVG(note) 
                            FROM RESULTAT AS R, MATIERE AS M, TYPE_EPREUVE AS TE
                            WHERE M.id_matiere = R.id_matiere AND M.libelle = ? AND TE.libelle = "Notes Ecrites" AND TE.id=R.type_epreuve''', (matiere,))

    rows = result.fetchall()

    return rows[0][0]

def computeGraphData(code_candidat):

    temp = queries.resultat.getResultatEleveByTypeEpreuve(code_candidat, "Notes Ecrites")

    subjects = []
    student_marks = []
    avg = []

    for i in range(0, len(temp)):
        subjects.append(temp[i][0])
        student_marks.append(temp[i][1])
        avg.append(round(getAvgByMatiere(temp[i][0]),2))

    return student_marks,avg,subjects

def getResultatByMatiereAndFiliere(matiere, filiere):

    db = main.get_db()
    result = db.execute(''' SELECT note
                            FROM RESULTAT AS R, MATIERE AS M, ELEVE AS E, FILIERE AS F
                            WHERE M.id_matiere=R.id_matiere
                            AND E.can_cod=R.can_cod
                            AND E.id_filiere=F.code_concours
                            AND F.libelle_filiere=?
                            AND M.libelle= ? ''',(filiere, matiere))

    rows = result.fetchall()
    storage = []

    for i in range(0, len(rows)):
        storage.append(rows[i][0])

    return storage

def getMoyenneGeneraleByEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT note 
                            FROM RESUlTAT, MATIERE
                            WHERE RESULTAT.can_cod = ?
                            AND RESULTAT.id_matiere = MATIERE.id_matiere
                            AND matiere.libelle = "Moyenne"''', (code_candidat,)) # on calcule l'average des notes obtenues pour les types épreuves Ecrites et Orales CMT, mais également Spécifiques CMT car ces dernières peuvent remplacer les notes orales CMT
    rows = result.fetchall()

    return rows[0][0]


def getNotesByLangueAndFiliere(langue, filiere):

    db = main.get_db()
    result = db.execute(''' SELECT R.note FROM ELEVE AS E, PARCOURS_PREPA AS P, OPTION AS O, RESULTAT AS R, TYPE_EPREUVE AS TE, MATIERE AS M, FILIERE AS F
                            WHERE E.can_cod = P.can_cod
                            AND P.option1 = O.id_option
                            AND O.option = ?
                            AND R.can_cod = E.can_cod
                            AND M.id_matiere = R.id_matiere
                            AND M.libelle = "Langue"
                            AND E.id_filiere = F.code_concours
                            AND F.libelle_filiere = ?''', (langue, filiere))

    rows = result.fetchall()

    storage = []

    for i in range(0, len(rows)):
        storage.append(rows[i][0])

    return storage

def getNotesByOptionMP(option):

    db = main.get_db()
    result = db.execute(''' SELECT note
                            FROM RESULTAT, MATIERE, PARCOURS_PREPA, OPTION
                            WHERE RESULTAT.can_cod = PARCOURS_PREPA.can_cod
                            AND RESULTAT.id_matiere = MATIERE.id_matiere
                            AND MATIERE.id_matiere = 599
                            AND OPTION.option = ?
                            AND OPTION.id_option = PARCOURS_PREPA.option2''', (option,))  # on calcule l'average des notes obtenues pour les types épreuves Ecrites et Orales CMT, mais également Spécifiques CMT car ces dernières peuvent remplacer les notes orales CMT
    rows = result.fetchall()

    storage = []

    for i in range(0, len(rows)):
        storage.append(rows[i][0])

    return storage

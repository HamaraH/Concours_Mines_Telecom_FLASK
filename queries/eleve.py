import sys
sys.path.append("..")
import main

def getAllEleve():

    db = main.get_db()
    result = db.execute(''' SELECT  nom, prenom, can_cod, INE FROM ELEVE ORDER BY (can_cod) ASC''')

    rows = result.fetchall()

    final_data = []

    for i in range(0, len(rows)):

        if rows[i][3] == None:
            final_data.append((rows[i][0], rows[i][1], rows[i][2],""))
        else:
            final_data.append((rows[i][0], rows[i][1], rows[i][2], rows[i][3]))

    return final_data

def getEleveInfos(code_candidat):

    db = main.get_db()
    result = db.execute('''SELECT   E.nom,
                                    E.prenom,
                                    E.autres_prenoms,
                                    E.date_naissance,
                                    E.adresse,
                                    E.complement_adresse,
                                    E.code_postal,
                                    E.numero_portable,
                                    E.numero_fixe,
                                    E.mail,
                                    E.can_cod,
                                    E.INE,
                                    ED.libelle,
                                    Q.libelle,
                                    F.libelle_filiere,
                                    t1.libelle,
                                    t2.libelle
                                    FROM ELEVE AS E, QUALITE AS Q, ETAT_DOSSIER AS ED, FILIERE AS F 
                                    INNER JOIN CSP t1 ON E.csp_pere = t1.id
                                    INNER JOIN CSP t2 ON E.csp_mere = t2.id
                                    WHERE can_cod = ? AND E.id_filiere = F.code_concours
                                    AND E.id_qualite = Q.id
                                    AND ED.code_etat = E.code_etat_dossier''', (code_candidat,))

    rows = result.fetchall()

    return rows

def updateInfos(nom, prenom, autres_prenoms, date_naissance, adresse, complement_adresse, code_postal, numero_portable, numero_fixe, mail, INE, code_candidat):

    db = main.get_db()
    db.execute(''' UPDATE ELEVE SET nom = ?,
                            prenom = ?,
                            autres_prenoms = ?,
                            date_naissance = ?,
                            adresse = ?,
                            complement_adresse = ?,
                            code_postal = ?,
                            numero_portable = ?,
                            numero_fixe = ?,
                            mail = ?,
                            INE = ? WHERE ELEVE.can_cod = ? ''', (nom, prenom, autres_prenoms, date_naissance, adresse, complement_adresse, code_postal, numero_portable, numero_fixe, mail, INE, code_candidat))

    db.commit()

def getElevesByFiliere(filiere):


    db = main.get_db()
    result = db.execute(''' SELECT nom, prenom, can_cod, INE FROM ELEVE AS E , FILIERE AS F  WHERE F.code_concours = E.id_filiere AND F.libelle_filiere = ? ''', (filiere,))

    rows = result.fetchall()

    final_data = []

    for i in range(0, len(rows)):

        if rows[i][3] == None:
            final_data.append((rows[i][0], rows[i][1], rows[i][2],""))
        else:
            final_data.append((rows[i][0], rows[i][1], rows[i][2], rows[i][3]))

    return final_data

def getDisplayInfosEleve(code_candidat):

    db = main.get_db()
    result = db.execute(''' SELECT nom, prenom, libelle_filiere FROM ELEVE AS E,FILIERE WHERE E.can_cod = ? AND FILIERE.code_concours = E.id_filiere ''',(code_candidat,))

    rows = result.fetchall()

    if rows != []:
        return rows[0]
    else:

        result = db.execute(''' SELECT nom, prenom FROM ATS AS A   WHERE A.can_cod = ? ''', (code_candidat,))
        rows = result.fetchall()

        if rows != []:
            storage = (rows[0][0], rows[0][1], "ATS")
            return storage
        else:
            return ""


def isEmpty():

    db = main.get_db()
    result = db.execute(''' SELECT COUNT (*) FROM ELEVE''')

    rows = result.fetchall()

    if rows[0][0] > 0:
        return False
    else:
        return True

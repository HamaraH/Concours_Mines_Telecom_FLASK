import sys
import main
import queries.resultat
sys.path.append("..")

D = {}
D["ATS"] = 5
D["MP"] = 161
D["PC"] = 169
D["PSI"] = 177
D["TSI"] = 833
D["PT"] = 834

def getAllEleveByFil(code_ecole,fil):

    db = main.get_db()
    result = db.execute('''SELECT V.can_cod, E.nom,E.prenom,V.rang_admission FROM voeux as V JOIN eleve as E ON E.can_cod=V.can_cod WHERE (V.code_ecole = ? AND reponse = " PROPOSITION" AND E.id_filiere = ?) ''',[code_ecole,D[fil]])

    rows = result.fetchall()

    final_data = []

    for i in range(0, len(rows)):
        final_data.append((rows[i][0], rows[i][1], rows[i][2], rows[i][3]))
    return final_data

def getNameEcole(code_ecole):

    db = main.get_db()
    result = db.execute('''SELECT nom_ecole FROM ecole WHERE code_ecole = ? ''',[code_ecole])

    rows = result.fetchall()

    return rows[0][0]

def checkEcole(code_ecole):

    db = main.get_db()
    result = db.execute('''SELECT * FROM ecole WHERE code_ecole = ? ''',[code_ecole])

    rows = result.fetchall()

    return rows

def countPlaceByFil(code_ecole,fil):
    db = main.get_db()
    result = db.execute('''SELECT nombre_place_'''+fil+''' FROM ecole WHERE code_ecole = ? ''',[code_ecole])
    rows = result.fetchall()
    return rows[0][0]

def countAllEleveByFil(code_ecole,fil):

    db = main.get_db()
    result = db.execute('''SELECT COUNT(V.can_cod) FROM voeux as V JOIN eleve as E ON E.can_cod=V.can_cod WHERE (V.code_ecole = ? AND reponse = " PROPOSITION" AND E.id_filiere = ?) ''',[code_ecole,D[fil]])

    rows = result.fetchall()

    return rows[0][0]

def countAllGirlByFil(code_ecole,fil):

    db = main.get_db()
    result = db.execute('''SELECT COUNT(V.can_cod) FROM voeux as V JOIN eleve as E ON E.can_cod=V.can_cod WHERE (V.code_ecole = ? AND reponse = " PROPOSITION" AND E.id_filiere = ? AND E.id_civilite = 2) ''',[code_ecole,D[fil]])

    rows = result.fetchall()

    return rows[0][0]

def countAllDemiByFil(code_ecole,fil):

    db = main.get_db()
    result = db.execute('''SELECT COUNT(V.can_cod)FROM voeux as V JOIN eleve as E ON E.can_cod=V.can_cod JOIN parcours_prepa as P ON V.can_cod = P.can_cod WHERE (V.code_ecole = ? AND reponse = " PROPOSITION" AND E.id_filiere = ? AND P.puissance = "3/2") ''',[code_ecole,D[fil]])

    rows = result.fetchall()

    return rows[0][0]

def countAllBoursierByFil(code_ecole,fil):

    db = main.get_db()
    result = db.execute('''SELECT COUNT(V.can_cod) FROM voeux as V JOIN eleve as E ON E.can_cod=V.can_cod WHERE (V.code_ecole = ? AND reponse = " PROPOSITION" AND E.id_filiere = ? AND E.id_qualite = 2) ''',[code_ecole,D[fil]])

    rows = result.fetchall()

    return rows[0][0]


def computeMoyenneData(code_ecole,fil):

    aux = getAllEleveByFil(code_ecole,fil)
    if aux != []:
        r_min = aux[0][3]
        moy_max = queries.resultat.getMoyenneGeneraleByEleve(aux[0][0])
        r_max = aux[-1][3]
        moy_min = queries.resultat.getMoyenneGeneraleByEleve(aux[-1][0])
        return [r_min,moy_max,r_max,moy_min]
    else:
        return ["","","",""]



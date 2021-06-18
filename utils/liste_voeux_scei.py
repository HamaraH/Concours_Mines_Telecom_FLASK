import os
import sqlite3 as sql
from copy import deepcopy
import pandas as pd

def dico_resultat_voeux():


    parent = os.path.dirname(os.path.dirname( __file__ ))
    direction = os.path.join (parent,'data')

    os.chdir(direction)
    path_name = []

    for dirpath, dirnames, filenames in os.walk(direction):
        for filename in filenames:
            path_name.append(filename)

    direction_data = '..'
    os.chdir(direction_data)
    con = sql.connect('MinesDB.db')
    D_eleve = {}
    filie = ['"MP"','"PSI"', '"PC"', '"PT"', '"TSI"', '"ATS"']
    for fil in filie:
        cur = con.cursor()
        if fil != '"ATS"':
            cur.execute('SELECT V.* FROM voeux AS V, eleve AS E, FILIERE AS F WHERE V.can_cod = E.can_cod AND E.id_filiere = F.code_concours AND F.libelle_filiere = ' + fil + ' ORDER BY rang_admission')
            voeux = cur.fetchall()
            cur.execute('SELECT can_cod FROM (SELECT V.* FROM voeux AS V, eleve AS E, FILIERE AS F WHERE V.can_cod = E.can_cod AND E.id_filiere = F.code_concours AND F.libelle_filiere = ' + fil + ' GROUP BY V.can_cod) ORDER BY rang_admission')
            candidat_fil = cur.fetchall() #liste des candidats ordonnée par leur rang d'admission
            cur.execute('SELECT * FROM ecole')
            ecole = cur.fetchall()
        else: #cas ATS
            cur.execute('SELECT V.* FROM voeux AS V, ats AS A WHERE V.can_cod = A.can_cod  ORDER BY rang_admission')
            voeux = cur.fetchall()
            cur.execute('SELECT can_cod FROM (SELECT V.* FROM voeux AS V, ats AS A WHERE V.can_cod = A.can_cod  GROUP BY V.can_cod) ORDER BY rang_admission')
            candidat_fil = cur.fetchall() #liste des candidats ordonnée par leur rang d'admission
            cur.execute('SELECT * FROM ecole')
            ecole = cur.fetchall()
        D_ecole = {}
        for i in ecole:
            cur.execute('SELECT nombre_place_'+fil[1:-1]+' FROM ecole WHERE code_ecole =' + str(i[0]))
            nombre_place = cur.fetchall()[0][0]
            cur.execute('SELECT nombre_place_attente FROM ecole WHERE code_ecole =' + str(i[0]))
            liste_attente = cur.fetchall()[0][0]
            D_ecole[i[0]] = [i[1],nombre_place,liste_attente]
        a = 0
        b = 0
        n = len(voeux)
        for i in candidat_fil:
            while (b < n) and (voeux[b][0] == i[0]):
                b += 1
            aux = voeux[a:b]
            a = b
            etat = 0
            L = []
            c = 1
            for j in aux:
                if etat == 1:
                    #L.append(str(j[3])+ " " + D_ecole[j[1]][0] + " DEMISSION CAUSE VOEUX " + str(c) + " proposé")
                    L.append(" Démission : voeux nº " + str(c) + " proposé")
                else:
                    if D_ecole[j[1]][1] > 0:
                        D_ecole[j[1]][1] -= 1
                        #L.append(str(j[3])+ " " + D_ecole[j[1]][0] + " PROPOSITION")
                        L.append(" PROPOSITION")
                        etat = 1
                    elif D_ecole[j[1]][1] > -1*D_ecole[j[1]][2]:
                        D_ecole[j[1]][1] -= 1
                        #L.append(str(j[3])+ " " + D_ecole[j[1]][0] + " LISTE D'ATTENTE RANG :  " +  str(abs(D_ecole[j[1]][1])))
                        L.append(" Liste d'attente rang :  " +  str(abs(D_ecole[j[1]][1])))
                        c+=1
                    else:
                        #L.append(str(j[3])+ " " + D_ecole[j[1]][0] + " HORS LISTE D'ATTENTE")
                        L.append(" Hors liste d'attente")
                        c+=1
            D_eleve[i[0]] = deepcopy(L)
            cur.close()

    print("Remplissage table : Voeux")

    for p in path_name[45:51]:  # la liste des _ATS / _MP
        path = os.path.join(direction, p)
        print("Enregistrement des données : " + p)
        x = pd.read_excel(path, engine='openpyxl')
        print("enregistrement terminé")
        for i in range(len(x)):
            con.execute(
                "INSERT OR REPLACE INTO voeux (can_cod, rang_admission, ordre_voeux, code_ecole, reponse) VALUES (?, ?, ?, ?, ?)",
                [int(x["Can _cod"][i]), int(x["Voe _ran"][i]), int(x["Voe _ord"][i]), int(x["Eco _cod"][i]),
                 D_eleve[int(x["Can _cod"][i])][int(x["Voe _ord"][i]) - 1]])

    print("Table remplie")

    con.commit()
    con.close()

    # Réponse dans D_eleve[code_candidat]


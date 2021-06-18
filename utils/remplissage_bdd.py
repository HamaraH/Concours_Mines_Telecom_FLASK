import os
import pandas as pd
import sqlite3 as sql
from random import randint
from utils import functions

## Zone fonctions utilent au programme

## Début remplissage

def fill_DB():

    parent = os.path.dirname(os.path.dirname( __file__ ))
    direction = os.path.join (parent,'data')

    os.chdir(direction)
    path_name = []

    for dirpath, dirnames, filenames in os.walk(direction):
      for filename in filenames:
        path_name.append(filename)

    print(path_name[56])

    direction_data = '..'
    os.chdir(direction_data)
    con = sql.connect('MinesDB.db') # nous sommes désormais connecté à la bdd

    path = os.path.join(direction, "Inscription.xlsx")
    print("Enregistrement des données : Inscription.xlsx")
    inscription = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")

    ### TABLE PAYS

    print("Remplissage table : Pays")

    D_path_inscription = {} #dico pour se retrouver dans le nom des colonnes
    for colonne in inscription:
        D_path_inscription[inscription[colonne][0]] = colonne

    con.execute("INSERT OR IGNORE INTO pays (code_pays, nom) VALUES (?, ?)", [inscription[D_path_inscription["FRANCAIS"]][1],"France"]) #On rajoute "à la main" la France

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO pays (code_pays, nom) VALUES (?, ?)", [inscription[D_path_inscription["CODE_PAYS"]][i],inscription[D_path_inscription["LIBELLE_PAYS"]][i]])
            con.execute("INSERT OR IGNORE INTO pays (code_pays, nom) VALUES (?, ?)", [inscription[D_path_inscription["CODE_PAYS_NAISSANCE"]][i],inscription[D_path_inscription["PAYS_NAISSANCE"]][i]])

    print("Table remplie")

    ### TABLE VILLE

    print("Remplissage table : Ville")

    for i in range(1,len(inscription)): #Pour chaque ligne on vérifié que le code postal n'est pas présent dans la table ville
        con.execute("INSERT OR IGNORE INTO ville (code_postal, nom_ville, pays_ville) VALUES (?, ?, ?)", [int(inscription[D_path_inscription["CP"]][i]),inscription[D_path_inscription["VILLE"]][i],inscription[D_path_inscription["CODE_PAYS"]][i]])

    print("Table remplie")

    ### TABLE ETABLISSEMENT + complete ville

    print("Remplissage table : Etablissement")

    D_pays_id = {} # Si on doit ajouter des villes, on doit reconnaitre le pays
    cur = con.cursor()
    cur.execute('SELECT code_pays,nom FROM pays')
    aux = cur.fetchall() #rows contient les rne déja existants dans la BDD
    cur.close()
    for i in aux:
        D_pays_id[i[1]] = i[0]
    del aux


    path = os.path.join(direction, "listeEtablissements.xlsx")
    print("Enregistrement des données : listeEtablissements.xlsx")
    etablissement = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")

    for i in range(len(etablissement)):
            con.execute("INSERT OR IGNORE INTO ville (code_postal, nom_ville, pays_ville) VALUES (?, ?, ?)", [int(etablissement["Code _postal _etab"][i]),etablissement["Ville _etab"][i],D_pays_id[etablissement["Pays _atab"][i]]])
            con.execute("INSERT OR IGNORE INTO etablissement (rne, type_etab, nom_etab, code_postal) VALUES (?, ?, ?, ?)", [etablissement["Rne"][i],etablissement["Type _etab"][i],etablissement["Etab"][i],int(etablissement["Code _postal _etab"][i])])


    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO etablissement (rne, type_etab, nom_etab, code_postal) VALUES (?, ?, ?, ?)", [inscription[D_path_inscription["CODE_ETABLISSEMENT"]][i],functions.select_type_etab(inscription[D_path_inscription["ETABLISSEMENT"]][i]),inscription[D_path_inscription["ETABLISSEMENT"]][i],None])


    print("Table remplie")

    ### TABLE BAC

    print("Remplissage table : BAC")

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO baccalaureat (can_cod, annee_obtention, mois_obtention, code_serie, departement, mention) VALUES (?, ?, ?, ?, ?, ?)",[inscription[D_path_inscription["CODE_CANDIDAT"]][i],inscription[D_path_inscription["ANNEE_BAC"]][i], inscription[D_path_inscription["MOIS_BAC"]][i], inscription[D_path_inscription["CODE_SERIE"]][i], inscription[D_path_inscription["CAN_DEP_BAC"]][i], inscription[D_path_inscription["MENTION"]][i]])

    print("Table remplie")

    ### TABLE SERIE

    print("Remplissage table : Serie")

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO serie (code_serie, libelle) VALUES (?, ?)",[int(inscription[D_path_inscription["CODE_SERIE"]][i]), inscription[D_path_inscription["SERIE"]][i]])

    print("Table remplie")

    ### TABLE NATIONALITE

    print("Remplissage table : Nationalite")

    for i in range(1,len(inscription)):
        con.execute("INSERT OR IGNORE INTO nationalite (id, libelle) VALUES (?, ?)",[inscription[D_path_inscription["CODE_PAYS_NATIONALITE"]][i],inscription[D_path_inscription["AUTRE_NATIONALITE"]][i]])

    D_nationalite_id = {}
    cur = con.cursor()
    cur.execute('SELECT id,libelle FROM nationalite')
    aux = cur.fetchall()
    cur.close()
    for i in aux:
        D_nationalite_id[i[1]] = i[0]
    del aux

    print("Table remplie")

    ### TABLE OPTION

    print("Remplissage table : Option")

    new = []
    cur = con.cursor()
    cur.execute('SELECT option FROM option')
    rows_option = cur.fetchall() #rows contient les codes postal déja existants dans la BDD
    for i in range(len(rows_option)):
        rows_option[i] = rows_option[i][0]
    cur.close()

    for i in range(1,len(inscription)):
        if not(functions.appartient(rows_option,functions.add(inscription[D_path_inscription["OPTION1"]][i]))):
            rows_option.append(functions.add(inscription[D_path_inscription["OPTION1"]][i]))
            new.append([functions.add(inscription[D_path_inscription["OPTION1"]][i]),functions.add(inscription[D_path_inscription["EPREUVE1"]][i])])
        if not(functions.appartient(rows_option,functions.add(inscription[D_path_inscription["OPTION2"]][i]))):
            rows_option.append(functions.add(inscription[D_path_inscription["OPTION2"]][i]))
            new.append([functions.add(inscription[D_path_inscription["OPTION2"]][i]),functions.add(inscription[D_path_inscription["EPREUVE2"]][i])])
        if not(functions.appartient(rows_option,functions.add(inscription[D_path_inscription["OPTION3"]][i]))):
            rows_option.append(functions.add(inscription[D_path_inscription["OPTION3"]][i]))
            new.append([functions.add(inscription[D_path_inscription["OPTION3"]][i]),functions.add(inscription[D_path_inscription["EPREUVE3"]][i])])
        if not(functions.appartient(rows_option,functions.add(inscription[D_path_inscription["OPTION4"]][i]))):
            rows_option.append(functions.add(inscription[D_path_inscription["OPTION4"]][i]))
            new.append([functions.add(inscription[D_path_inscription["OPTION4"]][i]),functions.add(inscription[D_path_inscription["EPREUVE4"]][i])])

    con.executemany("INSERT INTO option (option, epreuve) VALUES (?, ?)", new)

    D_option_id = {} # Si on doit ajouter des options, on doit reconnaitre l'identifiant
    cur = con.cursor()
    cur.execute('SELECT id_option,option FROM option')
    aux = cur.fetchall() #rows contient les rne déja existants dans la BDD
    cur.close()
    for i in aux:
        D_option_id[i[1]] = i[0]
    del aux

    print("Table remplie")
    del new
    del rows_option


    ### TABLE PARCOURS_PREPA

    print("Remplissage table : Parcours_prepa")

    for i in range(1,len(inscription)):
        con.execute("INSERT OR IGNORE INTO parcours_prepa (can_cod, sujet_TIPE, puissance, option1, option2, option3, option4) VALUES (?, ?, ?, ?, ?, ?, ?)",[inscription[D_path_inscription["CODE_CANDIDAT"]][i],functions.retire_saut_de_ligne(inscription[D_path_inscription["SUJET_TIPE"]][i]), inscription[D_path_inscription["PUISSANCE"]][i], D_option_id[functions.add(inscription[D_path_inscription["OPTION1"]][i])], D_option_id[functions.add(inscription[D_path_inscription["OPTION2"]][i])], D_option_id[functions.add(inscription[D_path_inscription["OPTION3"]][i])], D_option_id[functions.add(inscription[D_path_inscription["OPTION4"]][i])]])

    print("Table remplie")

    ### TABLE QUALITE

    print("Remplissage table : Qualite")

    new = []
    cur = con.cursor()
    cur.execute('SELECT libelle FROM qualite')
    rows_qualite = cur.fetchall() #rows contient les codes postal déja existants dans la BDD
    for i in range(len(rows_qualite)):
        rows_qualite[i] = rows_qualite[i][0]
    cur.close()

    for i in range(1,len(inscription)):
        if not(functions.appartient(rows_qualite,inscription[D_path_inscription["QUALITE"]][i])):
            rows_qualite.append(inscription[D_path_inscription["QUALITE"]][i])
            new.append([inscription[D_path_inscription["QUALITE"]][i]])

    con.executemany("INSERT INTO qualite (libelle) VALUES (?)", new)

    D_qualite_id = {}
    cur = con.cursor()
    cur.execute('SELECT id,libelle FROM qualite')
    aux = cur.fetchall() #rows contient les rne déja existants dans la BDD
    cur.close()
    for i in aux:
        D_qualite_id[i[1]] = i[0]
    del aux
    del new
    del rows_qualite

    con.execute("UPDATE qualite SET libelle = 'Non boursier' WHERE libelle = ' '")
    print("Table remplie")

    ### TABLE CSP

    print("Remplissage table : CSP")

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO csp (id, libelle) VALUES (?, ?)",[int(inscription[D_path_inscription["COD_CSP_PERE"]][i]), inscription[D_path_inscription["LIB_CSP_PERE"]][i],])
            con.execute("INSERT OR IGNORE INTO csp (id, libelle) VALUES (?, ?)",[int(inscription[D_path_inscription["COD_CSP_MERE"]][i]), inscription[D_path_inscription["LIB_CSP_MERE"]][i]])

    print("Table remplie")

    ### TABLE civilite

    print("Remplissage table : Civilite")

    new = [[1,"Mr"],[2,"Mme"]] #On suppose qu'il n'y a que des hommes et des femmes mais on se laisse la possibiliter d'ajouter d'autres choses parceque 2021...

    cur = con.cursor()
    cur.execute('SELECT id_civilite FROM civilite')
    rows_civilite = cur.fetchall() #rows contient les codes postal déja existants dans la BDD
    for i in range(len(rows_civilite)):
        rows_civilite[i] = rows_civilite[i][0]
    cur.close()

    if rows_civilite != [1,2]:
        con.executemany("INSERT INTO civilite (id_civilite, libelle) VALUES (?, ?)", new)

    del new
    del rows_civilite
    print("Table remplie")

    ### TABLE etat_dossier

    print("Remplissage table : Etat_dossier")

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO etat_dossier (code_etat, libelle) VALUES (?, ?)",[int(inscription[D_path_inscription["CODE_ETAT_DOSSIER"]][i]), inscription[D_path_inscription["LIBELLE_ETAT_DOSSIER"]][i]])

    print("Table remplie")


    ### TABLE etat_reponse

    print("Remplissage table : Etat_reponse")

    path = os.path.join(direction, "listeEtatsReponsesAppel.xlsx")
    print("Enregistrement des données : listeEtatsReponsesAppel.xlsx")
    etat_reponse = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")

    for i in range(len(etat_reponse)):
            con.execute("INSERT OR IGNORE INTO etat_reponse (id, libelle) VALUES (?, ?)",[int(etat_reponse["Ata _cod"][i]), etat_reponse["Ata _lib"][i]])

    print("Table remplie")

    ### TABLE ECOLE

    print("Remplissage table : Ecole")

    path = os.path.join(direction, "listeEcoles.xlsx")
    print("Enregistrement des données : listeEcoles.xlsx")
    liste_ecole = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")

    for i in range(len(liste_ecole)):
            con.execute("INSERT OR IGNORE INTO ecole (code_ecole, nom_ecole, nombre_place_MP, nombre_place_PSI, nombre_place_PC, nombre_place_PT, nombre_place_TSI, nombre_place_ATS, nombre_place_attente) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",[int(liste_ecole["Ecole"][i]), liste_ecole["Nom _ecole"][i], randint(5,12), randint(5,9), randint(5,7), randint(4,5), randint(2,3), randint(1,3), randint(2,6)]) #on suppose qu'une ecole admet un nombre eleve d'une fillière donnée et en place entre 2 et 10 en liste d'attente

    print("Table remplie")


    ### TABLE FILLIERE

    print("Remplissage table : Filiere")

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO filiere (code_concours, libelle_filiere) VALUES (?, ?)",[int(inscription[D_path_inscription["CODE_CONCOURS"]][i]), inscription[D_path_inscription["VOIE"]][i]])

    con.execute("INSERT OR IGNORE INTO filiere (code_concours, libelle_filiere) VALUES (?, ?)",[5,'ATS']) #arbitraire

    print("Table remplie")

    D_filiere_id = {}
    cur = con.cursor()
    cur.execute('SELECT code_concours,libelle_filiere FROM filiere')
    aux = cur.fetchall() #
    cur.close()
    for i in aux:
        D_filiere_id[i[1]] = i[0]
    del aux

    ### TABLE VOEUX

    print("Remplissage table : Voeux")

    for p in path_name[45:51]: #la liste des _ATS / _MP
        path = os.path.join(direction, p)
        print("Enregistrement des données : "+p)
        x = pd.read_excel(path,engine='openpyxl')
        print("enregistrement terminé")
        for i in range(len(x)):
            con.execute("INSERT OR IGNORE INTO voeux (can_cod, rang_admission, ordre_voeux, code_ecole) VALUES (?, ?, ?, ?)",[int(x["Can _cod"][i]), int(x["Voe _ran"][i]), int(x["Voe _ord"][i]), int(x["Eco _cod"][i])])

    print("Table remplie")
    ### TABLE TYPE_ADMISSION

    print("Remplissage table : Type_admission")
    new = []
    aux = ["ADMIS","ADMISSIBLE","REFUSE"]

    for i in range(len(aux)):
            new.append([i,aux[i]])
    del aux

    con.executemany("INSERT OR IGNORE INTO type_admission (id, libelle) VALUES (?, ?)", new)

    print("Table remplie")

    ### TABLE TYPE_EPREUVE

    print("Remplissage table : Epreuve")
    new = []
    aux = ["Notes Ecrites","Notes épreuves spécifiques Concours Mines-Télécom","Notes orales Concours Mines-Télécom", "Notes orales Concours Commun Mines-Ponts", "Notes orales Concours Centrale Supelec", "Notes orales ATS", "Harmonisation", "Total"]

    for i in range(len(aux)):
            new.append([i,aux[i]])
    del aux

    con.executemany("INSERT OR IGNORE INTO type_epreuve (id, libelle) VALUES (?, ?)", new)

    print("Table remplie")

    ### TABLE ADMISSION

    print("Remplissage table : Admission")

    for i in range(22,32,2):
        path = os.path.join(direction, path_name[i])
        print("Enregistrement des données : " +path_name[i])
        x = pd.read_excel(path,engine='openpyxl')
        print("enregistrement terminé")
        D_path_x = {}
        for colonne in x:
            D_path_x[x[colonne][0]] = colonne
        for i in range(1,len(x)):
            con.execute("INSERT OR IGNORE INTO admission (can_cod, id_type_admission) VALUES (?, ?)",[int(x[D_path_x["login"]][i]), 0]) #classé = admis

    for i in range(11,22):
        path = os.path.join(direction, path_name[i])
        print("Enregistrement des données : " +path_name[i])
        x = pd.read_excel(path,engine='openpyxl')
        print("enregistrement terminé")
        for i in range(1,len(x)):
            con.execute("INSERT OR IGNORE INTO admission (can_cod, id_type_admission) VALUES (?, ?)",[int(x["Can _cod"][i]), 0]) #admis, de fait on rajoute les ATS

    for i in range(11):
        path = os.path.join(direction, path_name[i])
        print("Enregistrement des données : " +path_name[i])
        x = pd.read_excel(path,engine='openpyxl')
        print("enregistrement terminé")
        for i in range(1,len(x)):
            con.execute("INSERT OR IGNORE INTO admission (can_cod, id_type_admission) VALUES (?, ?)",[int(x["Can _cod"][i]), 1]) #admissible

    for i in range(1,len(inscription)):
        con.execute("INSERT OR IGNORE INTO admission (can_cod, id_type_admission) VALUES (?, ?)",[int(inscription[D_path_inscription["CODE_CANDIDAT"]][i]), 2])

    path = os.path.join(direction, path_name[56]) # ecrit_ATS
    print("Enregistrement des données : " +path_name[56])
    x = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")

    for i in range(1,len(x)):
        con.execute("INSERT OR IGNORE INTO admission (can_cod, id_type_admission) VALUES (?, ?)",[int(x["Numéro d'inscription"][i]), 2])

    print("Table remplie")


    ### TABLE CLASSEMENT

    print("Remplissage table : Classement")

    for i in range(22,32,2):
        path = os.path.join(direction, path_name[i])
        print("Enregistrement des données : " +path_name[i])
        x = pd.read_excel(path,engine='openpyxl')
        print("enregistrement terminé")
        D_path_x = {}
        for colonne in x:
            D_path_x[x[colonne][0]] = colonne
        for i in range(1,len(x)):
            con.execute("INSERT OR IGNORE INTO classement (can_cod, type_rang, rang) VALUES (?, ?, ?)",[int(x[D_path_x["login"]][i]), 1, int(x[D_path_x["rang_admissible"]][i])])
            con.execute("INSERT OR IGNORE INTO classement (can_cod, type_rang, rang) VALUES (?, ?, ?)",[int(x[D_path_x["login"]][i]), 0, int(x[D_path_x["rang_classe"]][i])])
    """ Chelou, pas de rang
    for i in range(11):
        path = os.path.join(direction, path_name[i])
        x = pd.read_excel(path,engine='openpyxl')
        for i in range(1,len(x)):
                #con.execute("INSERT OR IGNORE INTO classement (can_cod, type_rang, rang) VALUES (?, ?, ?)",[int(x["Can _cod"][i]), 1, int(x["rang"][i])]) #admissible
                #print(int(x["Can _cod"][i]))
                print(x["rang"][i])
    """
    path = os.path.join(direction, path_name[11]) # ADMIS ATS
    print("Enregistrement des données : " +path_name[11])
    x = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")
    for i in range(len(x)):
        con.execute("INSERT OR IGNORE INTO classement (can_cod, type_rang, rang) VALUES (?, ?, ?)",[int(x["Can _cod"][i]), 0, int(x["rang"][i])]) #ADMIS

    path = os.path.join(direction, path_name[0]) # ADMISSIBLE ATS
    print("Enregistrement des données : " +path_name[0])
    x = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")
    for i in range(len(x)):
        con.execute("INSERT OR IGNORE INTO classement (can_cod, type_rang, rang) VALUES (?, ?, ?)",[int(x["Can _cod"][i]), 1, int(x["rang"][i])]) #ADMISSIBLE

    print("Table remplie")

    ### TABLE ATS

    print("Remplissage table : ATS")
    print("Enregistrement des données : " +path_name[0])
    path = os.path.join(direction, path_name[0]) # ADMISSIBLE ATS
    x = pd.read_excel(path,engine='openpyxl')
    print("enregistrement terminé")

    D = {}
    D["M."] = 1
    D["Mme"] = 2

    for i in range(len(x)):
            con.execute("INSERT OR IGNORE INTO ats (can_cod, id_civilite, nom, prenom, adresse, complement_adresse, cp, mail, num_fixe, num_portable, id_filiere) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",[int(x["Can _cod"][i]),D[x["Civ _lib"][i]],x["Nom"][i],x["Prenom"][i],x["Can _ad 1"][i],functions.add(x["Can _ad 2"][i]),int(x["Can _cod _pos"][i]),x["Can _mel"][i],functions.bien_numerote(functions.add(x["Can _tel"][i])),functions.bien_numerote(functions.add(x["Can _por"][i])),5])

    for i in range(len(x)):
            con.execute("INSERT OR IGNORE INTO ville (code_postal, nom_ville, pays_ville) VALUES (?, ?, ?)",[int(x["Can _cod _pos"][i]),x["Can _com"][i],D_pays_id[x["Can _pay _adr"][i]]])

    print("Table remplie")

    ### TABLE ELEVE

    print("Remplissage table : Eleve")

    for i in range(1,len(inscription)):
            con.execute("INSERT OR IGNORE INTO eleve (can_cod,INE,nom,prenom,autres_prenoms,date_naissance,ville_naissance,francais,id_autre_nationalite,adresse,complement_adresse,code_postal,numero_portable,numero_fixe,mail,code_etablissement,csp_pere,csp_mere,code_etat_dossier,arrondissement_naissance,handicap,id_qualite,ville_ecrit,id_civilite,id_filiere) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?)",[int(inscription[D_path_inscription["CODE_CANDIDAT"]][i]), functions.add(inscription[D_path_inscription["NUMERO_INE"]][i]),inscription[D_path_inscription["NOM"]][i],inscription[D_path_inscription["PRENOM"]][i],functions.add(inscription[D_path_inscription["AUTRES_PRENOMS"]][i]),inscription[D_path_inscription["DATE_NAISSANCE"]][i],inscription[D_path_inscription["VILLE_NAISSANCE"]][i],int(inscription[D_path_inscription["FRANCAIS"]][i]),D_nationalite_id[inscription[D_path_inscription["AUTRE_NATIONALITE"]][i]],inscription[D_path_inscription["ADRESSE1"]][i],functions.add(inscription[D_path_inscription["ADRESSE2"]][i]),int(inscription[D_path_inscription["CP"]][i]),functions.bien_numerote(functions.add(inscription[D_path_inscription["TEL_PORTABLE"]][i])),functions.bien_numerote(functions.add(inscription[D_path_inscription["TELEPHONE"]][i])),inscription[D_path_inscription["EMAIL"]][i], inscription[D_path_inscription["CODE_ETABLISSEMENT"]][i], int(inscription[D_path_inscription["COD_CSP_PERE"]][i]),int(inscription[D_path_inscription["COD_CSP_MERE"]][i]),inscription[D_path_inscription["CODE_ETAT_DOSSIER"]][i], int(inscription[D_path_inscription["ARRONDISSEMENT_NAISSANCE"]][i]),inscription[D_path_inscription["DECLARATION_HANDICAP"]][i],D_qualite_id[inscription[D_path_inscription["QUALITE"]][i]],inscription[D_path_inscription["LIBELLE_VILLE_ECRIT"]][i],inscription[D_path_inscription["CIVILITE"]][i],inscription[D_path_inscription["CODE_CONCOURS"]][i]])

    print("Table remplie")

    ### TABLE RESULTAT + MATIERE

    print("Remplissage table : Résultat et Matière ")

    con.execute("INSERT OR IGNORE INTO matiere (id_matiere, libelle) VALUES (?, ?)",[0,"Moyenne"])

    def select_filiere(st): #selectionne la filiere dans le nom d'un fichier classe_fil_
        c = 0
        for i in st:
            if i == "_":
                break
            c+=1
        j = c+1
        for i in st[c+1:]:
            if i == "_":
                break
            j+=1
        return st[c+1:j]

    def born_stop(L):
        aux = []
        R = []
        for i in L:
            if i == "STOP":
                R.append(aux)
                aux = []
                continue
            aux.append(i)
        return(R)

    R = []
    for z in range(22,32,2):
        print("Enregistrement des données : " +path_name[z])
        aux = []
        path = os.path.join(direction, path_name[z])
        x = pd.read_excel(path,engine='openpyxl')
        print("enregistrement terminé")
        D_path_x = {}
        aux = []
        functions.add = 0
        L = []
        for colonne in x:
            D_path_x[x[colonne][0]] = colonne
            if str(x[colonne][0]) == 'nan':
                continue
            elif x[colonne][0] == "bonification_ecrit":
                L.append("STOP")
            elif x[colonne][0] == "bonification_oral":
                L.append("STOP")
            elif x[colonne][0][:5] == "total":
                aux.append([1000+functions.add,x[colonne][0]])
                functions.add+=1
            else:
                c = 0
                for u in x[colonne][0]:
                    if u == " ":
                        L.append([x[colonne][0][:c],x[colonne][0][c+2:-1],x[colonne][0]])
                        break
                    c+=1
        fil = select_filiere(path_name[z])
        R = born_stop(L)
        R = [R[0],R[1][:-2],R[1][-2:],aux]
        for j in R:
            for i in j:
                con.execute("INSERT OR IGNORE INTO matiere (id_matiere, libelle) VALUES (?, ?)",[int(i[0]),i[1]])
        if fil == "TSI":
            for i in range(1,len(x)):
                for j in R[0]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),0,x[D_path_x[j[-1]]][i]])#partie ecrie (0)
                for j in R[1][:4]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),1,x[D_path_x[j[-1]]][i]])#partie CMT spécifique (1)
                for j in R[1][4:]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),4,x[D_path_x[j[-1]]][i]])#partie CSS (4)
                for j in R[2]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),6,x[D_path_x[j[-1]]][i]])#partie Harmonisation (6)
                for j in R[3]:
                    con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),6,x[D_path_x[j[-1]]][i]])#partie totale (7)
        elif fil == "PT":
            for i in range(1,len(x)):
                for j in R[0]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),0,x[D_path_x[j[-1]]][i]])#partie ecrie (0)
                for j in R[1][:4]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),1,x[D_path_x[j[-1]]][i]])#partie CMT spécifique (1)
                for j in R[1][4:]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),2,x[D_path_x[j[-1]]][i]])#partie CMT (2)
                for j in R[2]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),6,x[D_path_x[j[-1]]][i]])#partie Harmonisation (6)
                for j in R[3]:
                    con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),6,x[D_path_x[j[-1]]][i]])#partie totale (7)
        else:
            for i in range(1,len(x)):
                for j in R[0]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),0,x[D_path_x[j[-1]]][i]])#partie ecrie (0)
                for j in R[1][:4]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),1,x[D_path_x[j[-1]]][i]])#partie CMT spécifique (1)
                for j in R[1][4:8]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),2,x[D_path_x[j[-1]]][i]])#partie CMT (2)
                for j in R[1][8:]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),3,x[D_path_x[j[-1]]][i]])#partie CCMP (3)
                for j in R[2]:
                    if str(x[D_path_x[j[-1]]][i]) != 'nan':
                        con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),6,x[D_path_x[j[-1]]][i]])#partie Harmonisation (6)
                for j in R[3]:
                    con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[int(x[D_path_x["login"]][i]),int(j[0]),6,x[D_path_x[j[-1]]][i]])#partie totale (7)

    print("Tables remplies")

    ### TABLE MOIS

    print("Remplissage table : Mois")
    new = []
    aux = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    for i in range(1,len(aux)+1):
            new.append([i,aux[i-1]])
    del aux

    con.executemany("INSERT OR IGNORE INTO mois (id, libelle) VALUES (?, ?)", new)

    print("Table remplie")


    for z in range(23,33,2):
        print("Enregistrement des données : " +path_name[z])
        aux = []
        path = os.path.join(direction, path_name[z])
        df = pd.read_csv(path, sep = '\t')
        print("enregistrement terminé")
        for i in range(len(df)):
            if df["scei;nom;etat;total_oral;total_points;moyenne_generale;rang_classe"][i][-1] != ";":
                con.execute("INSERT OR IGNORE INTO resultat (can_cod, id_matiere, type_epreuve, note) VALUES (?, ?, ?, ?)",[functions.select_id_csv(df["scei;nom;etat;total_oral;total_points;moyenne_generale;rang_classe"][i],0),0,7,functions.select_id_csv(df["scei;nom;etat;total_oral;total_points;moyenne_generale;rang_classe"][i],5)]) # bidouillage pour selectionner les meilleurs infos


    print("It's over Anakin. I have the high ground")

    con.commit()
    con.close()
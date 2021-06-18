import sqlite3
import sys
import os

direction_data = './'
os.chdir(direction_data)

def openDB():

    connexion = sqlite3.connect('MinesDB.db')

    if connexion == None:
        print("Error : the database can't be opened")
        sys.exit()

    else:

        connexion.execute('''CREATE TABLE IF NOT EXISTS ELEVE
                   ([can_cod] INTEGER PRIMARY KEY NOT NULL,
                    [INE] text,
                    [nom] text NOT NULL,
                    [prenom] text NOT NULL,
                    [autres_prenoms] text,
                    [date_naissance] date NOT NULL,
                    [ville_naissance] text NOT NULL,
                    [francais] integer NOT NULL,
                    [id_autre_nationalite] integer,
                    [adresse] text NOT NULL,
                    [complement_adresse] text,
                    [code_postal] integer NOT NULL,
                    [numero_portable] text NOT NULL,
                    [numero_fixe] text,
                    [mail] text NOT NULL,
                    [code_etablissement] text NOT NULL,
                    [csp_pere] integer NOT NULL,
                    [csp_mere] integer NOT NULL,
                    [code_etat_dossier] integer NOT NULL,
                    [arrondissement_naissance] integer,
                    [handicap] text NOT NULL,
                    [id_qualite] integer NOT NULL,
                    [ville_ecrit] text NOT NULL,
                    [id_civilite] integer NOT NULL,
                    [id_filiere] int NOT NULL,
                    FOREIGN KEY (code_postal)
                    REFERENCES VILLE (code_postal)
                    FOREIGN KEY (csp_mere)
                    REFERENCES CSP (id)
                    FOREIGN KEY (csp_pere)
                    REFERENCES CSP (id)
                    FOREIGN KEY (code_etat_dossier)
                    REFERENCES ETAT_DOSSIER (code_etat)
                    FOREIGN KEY (id_civilite)
                    REFERENCES CIVILITE (id)
                    FOREIGN KEY (id_qualite)
                    REFERENCES QUALITE (id)
                    FOREIGN KEY (code_etablissement)
                    REFERENCES ETABLISSEMENT (rne)
                    FOREIGN KEY (id_autre_nationalite)
                    REFERENCES NATIONALITE (id)
                    FOREIGN KEY (id_filiere)
                    REFERENCES FILIERE (code_concours)
                    )''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS NATIONALITE
                    ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                     [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS QUALITE
            ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
             [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS PAYS
            ([code_pays] INTEGER PRIMARY KEY NOT NULL,
             [nom] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS ETABLISSEMENT
            ([rne] TEXT PRIMARY KEY NOT NULL,
             [nom_etab] text NOT NULL,
             [type_etab] text NOT NULL,
             [code_postal] integer,
             FOREIGN KEY (code_postal)
             REFERENCES VILLE (code_postal))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS VILLE
                ([code_postal] INTEGER PRIMARY KEY NOT NULL,
                 [nom_ville] text NOT NULL,
                 [pays_ville] integer NOT NULL,
                 FOREIGN KEY (pays_ville)
                 REFERENCES PAYS (code_pays))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS BACCALAUREAT
                ([can_cod] INTEGER PRIMARY KEY,
                 [annee_obtention] integer NOT NULL,
                 [mois_obtention] integer NOT NULL,
                 [code_serie] integer NOT NULL,
                 [mention] text,
                 [departement] integer,
                 FOREIGN KEY (can_cod)
                 REFERENCES ELEVE (can_cod)
                 FOREIGN KEY (code_serie)
                 REFERENCES SERIE (code_serie))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS OPTION
                ([id_option] INTEGER PRIMARY KEY AUTOINCREMENT,
                 [option] text,
                 [epreuve] text)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS SERIE
                ([code_serie] integer PRIMARY KEY NOT NULL,
                 [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS CSP
                ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                 [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS ETAT_DOSSIER
                ([code_etat] INTEGER PRIMARY KEY NOT NULL,
                 [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS FILIERE
                ( [code_concours] INTEGER PRIMARY KEY NOT NULL,
                  [libelle_filiere] TEXT NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS CLASSEMENT
                ([can_cod] INTEGER NOT NULL,
                 [type_rang] integer NOT NULL,
                 [rang] integer NOT NULL,
                 PRIMARY KEY (can_cod, type_rang)
                 FOREIGN KEY (can_cod)
                 REFERENCES ELEVE (can_cod)
                 FOREIGN KEY (type_rang)
                 REFERENCES TYPE_ADMISSION (id))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS VOEUX
                    ([can_cod] INTEGER NOT NULL,
                     [code_ecole] INTEGER NOT NULL,
                     [rang_admission] integer NOT NULL,
                     [ordre_voeux] integer NOT NULL,
                     [reponse] text,
                     PRIMARY KEY (can_cod, code_ecole)
                     FOREIGN KEY (can_cod)
                     REFERENCES ELEVE (can_cod)
                     FOREIGN KEY (code_ecole)
                     REFERENCES ECOLE (code_ecole))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS ECOLE
                    ([code_ecole] INTEGER PRIMARY KEY NOT NULL,
                     [nom_ecole] text,
                     [nombre_place_MP] INTEGER NOT NULL,
                     [nombre_place_PSI] INTEGER NOT NULL,
                     [nombre_place_PC] INTEGER NOT NULL,
                     [nombre_place_PT] INTEGER NOT NULL,
                     [nombre_place_TSI] INTEGER NOT NULL,
                     [nombre_place_ATS] INTEGER NOT NULL,
                     [nombre_place_attente] INTEGER NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS TYPE_ADMISSION
                           ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                            [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS ADMISSION
                    ([can_cod] INTEGER PRIMARY KEY NOT NULL,
                     [id_type_admission] int NOT NULL,
                     FOREIGN KEY (id_type_admission)
                     REFERENCES type_admission (id))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS PARCOURS_PREPA
                    ([can_cod] INTEGER PRIMARY KEY,
                     [sujet_TIPE] text NOT NULL,
                     [puissance] text,
                     [option1] integer,
                     [option2] integer,
                     [option3] integer,
                     [option4] integer,
                     FOREIGN KEY (option1)
                     REFERENCES OPTION (id_option)
                     FOREIGN KEY (can_cod)
                     REFERENCES ELEVE (can_cod)
                     FOREIGN KEY (option2)
                     REFERENCES OPTION (id_option)
                     FOREIGN KEY (option3)
                     REFERENCES OPTION (id_option)
                     FOREIGN KEY (option4)
                     REFERENCES OPTION (id_option))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS CIVILITE
                    ([id_civilite] INTEGER PRIMARY KEY AUTOINCREMENT,
                     [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS MATIERE
                    ([id_matiere] INTEGER PRIMARY KEY NOT NULL,
                     [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS RESULTAT
                    ([can_cod] INTEGER NOT NULL,
                     [id_matiere] integer NOT NULL,
                     [type_epreuve] integer NOT NULL,
                     [note] real NOT NULL,
                     PRIMARY KEY (can_cod, id_matiere, type_epreuve)
                     FOREIGN KEY (can_cod)
                     REFERENCES ELEVE (can_cod)
                     FOREIGN KEY (id_matiere)
                     REFERENCES MATIERE (id_matiere)
                     FOREIGN KEY (type_epreuve)
                     REFERENCES TYPE_EPREUVE (id))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS ORAUX
                    ([can_cod] INTEGER PRIMARY KEY NOT NULL,
                     [centre] text,
                     [jury] text,
                     FOREIGN KEY (can_cod)
                     REFERENCES ELEVE (can_cod))''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS ETAT_REPONSE
                    ([id] INTEGER PRIMARY KEY NOT NULL,
                     [libelle] text NOT NULL)''')

        connexion.execute(''' CREATE TABLE IF NOT EXISTS COMPTE
                    ([login] text PRIMARY KEY NOT NULL,
                    [password] text NOT NULL)''')

        connexion.execute(''' CREATE TABLE IF NOT EXISTS ATS
                            ([can_cod] int PRIMARY KEY NOT NULL,
                            [id_civilite] int NOT NULL,
                            [nom] text NOT NULL,
                            [prenom] text NOT NULL,
                            [adresse] text NOT NULL,
                            [complement_adresse] text,
                            [cp] int NOT NULL,
                            [mail] text NOT NULL,
                            [num_fixe] text,
                            [num_portable] text NOT NULL,
                            [id_filiere] int NOT NULL,
                            FOREIGN KEY  (id_civilite)
                            REFERENCES  CIVILITE (id)
                            FOREIGN KEY (cp)
                            REFERENCES VILLE (code_postal)
                            FOREIGN KEY (id_filiere)
                            REFERENCES FILIERE (code_concours) )''')

        connexion.execute(''' CREATE TABLE IF NOT EXISTS TYPE_EPREUVE
                          ([id] int PRIMARY KEY,
                          [libelle] text NOT NULL)''')

        connexion.execute('''CREATE TABLE IF NOT EXISTS MOIS
                    ([id] INTEGER PRIMARY KEY AUTOINCREMENT,
                     [libelle] text NOT NULL)''')

    return connexion

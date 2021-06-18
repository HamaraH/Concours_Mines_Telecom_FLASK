import sqlite3 as sql
import os
from typing import Counter
import pandas as pd

#####Création des différents listes de données à partir des excels#####

candidats_codes = []
admis = []
admissibles = []
refuses = []


direction = './../data'

for excel in  os.listdir(direction):
    #on parcourt tous les excels à la recherche de ceux qui contiennent des codes de candidats
    #Dans les excels Admis_XXX et Admissibles_XXX, le code est de la forme "Can _cod"
    if excel.startswith("ADMIS_") and not excel.endswith("ATS.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(len(a) - 1):
            code_etudiant = a.loc[i, 'Can _cod']
            if code_etudiant not in candidats_codes:
                candidats_codes.append(code_etudiant)
            if code_etudiant not in admis:
                admis.append(code_etudiant)
    elif excel.startswith("ADMISSIBLE_") and not excel.endswith("ATS.xlsx"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(len(a) - 1):
            print(i, admissibles, excel, "\n")
            code_etudiant = a.loc[i, 'Can _cod']
            if code_etudiant not in candidats_codes:
                candidats_codes.append(code_etudiant)
            # if code_etudiant not in admissibles:
            #     admissibles.append(code_etudiant)
    #les candidats qui ne sont que dans les tables résultats n'ont que des résultats : on a décidé de pas en tenir compte (juste pour les stats)
    elif excel.endswith(".xlsx") and excel.startswith("Inscript"):
        path = os.path.join(direction, excel)
        a = pd.read_excel(path, engine="openpyxl")
        for i in range(1, len(a) - 2):
            if a.loc[i, " "] not in candidats_codes:
                candidats_codes.append(a.loc[i, " "])


#affinage de la liste des admissibles : on retire ceux qui sont admis des admissibles
for code in admis:
    if code in admissibles:
        admissibles.remove(code)
for code in candidats_codes:
    #création de la liste des refuses
    if (code not in admis) and (code not in admissibles):
        refuses.append(code)


#######TESTS########


DATABASE = './MinesDB copy.db'

con = sql.connect(DATABASE)
cur = con.cursor()


#print(cur.execute('SELECT * FROM ORAUX').fetchall())



##Contraintes de domaine##

def test_contrainte_domaine_ADMISSION():
    #Types d'admissions
    for id in cur.execute('SELECT id_type_admission FROM ADMISSION').fetchall():
        assert(id[0] == 0 or id[0] == 1 or id[0] == 2)

def test_contrainte_domaine_ATS():
    #Civilité
    for id in cur.execute('SELECT id_civilite FROM ATS').fetchall():
        assert(id[0] == 1 or id[0] == 2)
    #adresse email
    for mail in cur.execute('SELECT mail FROM ATS').fetchall():
        assert("@" in mail[0] and "." in mail[0])               ##Paufiner - regex ?
    #Numéros de téléphone
    #fixe
    for tel in cur.execute('SELECT num_fixe FROM ATS').fetchall():
        if tel[0] != None:
            assert(tel[0].startswith("+33 (0)") and len(tel[0]) == 20)
    #portable
    for tel in cur.execute('SELECT num_portable FROM ATS').fetchall():
        assert(tel[0].startswith("+33 (0)") and len(tel[0]) == 20)
    #filière
    for id in cur.execute('SELECT id_filiere FROM ATS').fetchall():
        assert(id[0] == 5)
    
def test_contrainte_domaine_BACCALAUREAT():
    #année d'obtention
    for annee in cur.execute('SELECT annee_obtention FROM BACCALAUREAT').fetchall():
        assert(0 <= annee[0] <= 2020)
    #mention
    for mention in cur.execute('SELECT mention FROM BACCALAUREAT').fetchall():
        assert(mention[0] == "AB" or mention[0] == "B" or mention[0] == "TB" or mention[0] == "S")

def test_contrainte_domaine_CLASSEMENT():
    #type_rang
    for type in cur.execute('SELECT type_rang FROM CLASSEMENT').fetchall():
        assert(type[0] == 0 or type[0] == 1)
    #rang
    for rang in cur.execute('SELECT rang FROM CLASSEMENT').fetchall():
        assert(rang[0] >= 1)

def test_contrainte_domaine_ECOLE():
    #on vérifie que le nombre de place est toujours supérieur ou égal à 0
    for nbre_place in cur.execute('SELECT DISTINCT nombre_place_MP FROM ECOLE').fetchall():
        assert nbre_place[0] >= 0
    for nbre_place in cur.execute('SELECT DISTINCT nombre_place_PSI FROM ECOLE').fetchall():
        assert nbre_place[0] >= 0
    for nbre_place in cur.execute('SELECT DISTINCT nombre_place_PC FROM ECOLE').fetchall():
        assert nbre_place[0] >= 0
    for nbre_place in cur.execute('SELECT DISTINCT nombre_place_PT FROM ECOLE').fetchall():
        assert nbre_place[0] >= 0
    for nbre_place in cur.execute('SELECT DISTINCT nombre_place_TSI FROM ECOLE').fetchall():
        assert nbre_place[0] >= 0
    for nbre_place in cur.execute('SELECT DISTINCT nombre_place_ATS FROM ECOLE').fetchall():
        assert nbre_place[0] >= 0

def test_contrainte_domaine_ELEVE():
    #INE
    for ine in cur.execute('SELECT INE FROM ELEVE').fetchall():
        if ine[0] != None:
            assert len(ine[0]) == 11
    #Date de naissance
    for date in cur.execute('SELECT date_naissance FROM ELEVE').fetchall():
        assert date[0][2] == date[0][5] == "/"
        assert len(date[0]) == 10
    #Les nationalités sont dans la bdd
    nationalites = cur.execute('SELECT id FROM NATIONALITE').fetchall()
    for id_nat in cur.execute('SELECT id_autre_nationalite FROM ELEVE').fetchall():
        assert id_nat in nationalites
    #Villes (codes postaux)
    for code in cur.execute('SELECT code_postal FROM ELEVE').fetchall():
        assert(0 <= code[0] <= 99999)
    #codes postaux sont bien dans la bdd
    codes_postaux = cur.execute('SELECT code_postal FROM VILLE').fetchall()
    for code in cur.execute('SELECT code_postal FROM ELEVE').fetchall():
        assert code in codes_postaux
    #Numéros de téléphone
    for tel in cur.execute('SELECT numero_portable FROM ELEVE').fetchall():
        assert(tel[0].startswith("+33 (0)") and len(tel[0]) == 20)
    #Les codes établissement sont dans la bdd
    codes = cur.execute('SELECT rne FROM ETABLISSEMENT').fetchall()
    for code in cur.execute('SELECT code_etablissement FROM ELEVE').fetchall():
        assert code in codes
    #Les CSP mère et père sont dans la bdd
    CSP = cur.execute('SELECT id FROM CSP').fetchall()
    for csp in cur.execute('SELECT csp_mere FROM ELEVE').fetchall():
        assert csp in CSP
    for csp in cur.execute('SELECT csp_pere FROM ELEVE').fetchall():
        assert csp in CSP
    #handicap
    for handicap in cur.execute('SELECT handicap FROM ELEVE').fetchall():
        assert handicap[0] == "oui" or handicap[0] == "non"
    #qualité
    for qualite in cur.execute('SELECT id_qualite FROM ELEVE').fetchall():
        assert qualite[0] == 1 or qualite[0] == 2 or qualite[0] == 3
    #Civilité
    for id in cur.execute('SELECT id_civilite FROM ELEVE').fetchall():
        assert(id[0] == 1 or id[0] == 2)
    #filière
    id_filieres = cur.execute('SELECT code_concours FROM FILIERE').fetchall()
    for id in cur.execute('SELECT id_filiere FROM ELEVE'):
        assert id in id_filieres

def test_contrainte_domaine_ETABLISSEMENT():
    #type etablissement
    for type in cur.execute('SELECT type_etab FROM ETABLISSEMENT').fetchall():
        assert(type[0] == "Lycée" or type[0] == "Université" or type[0] == "IUT" or type[0] == "Ecole" or type[0] == "Institut")
    #tous les codes postaux des établissements sont dans la bdd
    # codes_postaux = cur.execute('SELECT code_postal FROM VILLE').fetchall()
    # for code in cur.execute('SELECT code_postal FROM ETABLISSEMENT').fetchall():
    #     assert code in codes_postaux
   

# def test_contrainte_domaine_ORAUX():
#     assert True

def test_contrainte_domaine_PARCOURS_PREPA():
    #puissance
    for puissance in cur.execute('SELECT puissance FROM PARCOURS_PREPA').fetchall():
        assert(puissance[0] == "5/2" or puissance[0] == "3/2" or puissance[0] == "7/2")
    #les options sont dans OPTION de la bdd
    options = cur.execute('SELECT id_option FROM OPTION').fetchall()
    for option in cur.execute('SELECT option1 FROM PARCOURS_PREPA').fetchall():
        assert option in options
    for option in cur.execute('SELECT option2 FROM PARCOURS_PREPA').fetchall():
        assert option in options
    for option in cur.execute('SELECT option3 FROM PARCOURS_PREPA').fetchall():
        assert option in options
    for option in cur.execute('SELECT option4 FROM PARCOURS_PREPA').fetchall():
        assert option in options

def test_contrainte_domaine_RESULTAT():
    #Notes
    for note in cur.execute('SELECT note FROM RESULTAT').fetchall():
        if type(note[0]) == float:
            assert((float(0) <= note[0] <= float(20)) or (float(100) <= note[0]))
        if type(note[0]) == str:
            if len(note[0]) == 4:
                if len(note[0][0]) <= 1:
                    assert(note[0][1] <= "9")
                else:
                    assert(note[0][1] == "0")
            else:
                assert True
    #les matières sont bien celles de la bdd
    ids_matieres = cur.execute('SELECT id_matiere FROM MATIERE').fetchall()
    for id_matiere in cur.execute('SELECT id_matiere FROM RESULTAT').fetchall():
        assert id_matiere in ids_matieres
    #les épreuves sont bien celles de la bdd
    types_epreuves = cur.execute('SELECT id FROM TYPE_EPREUVE').fetchall()
    for type_epreuve in cur.execute('SELECT type_epreuve FROM RESULTAT').fetchall():
        assert type_epreuve in types_epreuves



def test_contrainte_domaine_VILLE():
    #pays de la ville
    ids_pays = cur.execute('SELECT code_pays FROM PAYS').fetchall()
    for id_pays in cur.execute('SELECT pays_ville FROM VILLE').fetchall():
        assert(id_pays in ids_pays)
    #code postal
    for code in cur.execute('SELECT code_postal FROM VILLE').fetchall():
        assert(0 <= code[0] <= 99999)

def test_contrainte_domaine_VOEUX():
    #ecole du voeux
    ids_ecoles = cur.execute('SELECT code_ecole FROM ECOLE').fetchall()
    for id_ecole in cur.execute('SELECT code_ecole FROM ECOLE').fetchall():
        assert(id_ecole in ids_ecoles)




##Bon import des données, cohérence##

#Vérification que tous les candidats des excels sont dans la BDD :
def test_grosse_boucle_de_lenfer():
    for code in candidats_codes:
        a = cur.execute('SELECT can_cod FROM ELEVE WHERE can_cod = (?)', (float(code),)).fetchone()
        if a is None:
            a = cur.execute('SELECT can_cod FROM ATS WHERE can_cod = (?)', (float(code),)).fetchone()
        if a is None:
            a = cur.execute('SELECT can_cod FROM RESULTAT WHERE can_cod = (?)', (float(code),)).fetchone()
        assert a == (float(code),)

#Vérification que tous les admissibles (admis / refuses) sont bien admissibles dans la BDD (admis / refuses)
def test_admis_admissibles():
    for code in admis:
        a = cur.execute('SELECT can_cod FROM Admission WHERE can_cod = (?) AND id_type_admission = 0', (float(code),)).fetchone()
        assert a == (float(code),)
    # for code in admissibles:
    #     a = cur.execute('SELECT can_cod FROM Admission WHERE can_cod = (?) AND id_type_admission = 1', (float(code),)).fetchone()
    #     assert a == (float(code),)
    # for code in refuses:
    #     a = cur.execute('SELECT can_cod FROM Admission WHERE can_cod = (?) AND id_type_admission = 2', (float(code),)).fetchone()
    #     assert a == (float(code),)


def test_coherence_VOEUX():
    candidats = cur.execute('SELECT DISTINCT can_cod FROM VOEUX').fetchall()
    for code in candidats:
        #on vérifie que l'ordre des voeux est unique (pas deux éléments en troisième position) (cohérence)
        rangs_voeux = cur.execute('SELECT ordre_voeux FROM VOEUX WHERE can_cod = (?)', (float(code[0]),)).fetchall()
        for i in rangs_voeux:
            assert (rangs_voeux.count(i) == 1)
        #on vérifie que le rang d'admission pour 1 candidat est bien toujours le même (cohérence)
        rang_admission = cur.execute('SELECT rang_admission FROM VOEUX WHERE can_cod = (?)', (float(code[0]),)).fetchall()
        assert(rang_admission.count(rang_admission[0]) == len(rang_admission))

def test_coherence_RESULTAT():
    candidats = cur.execute('SELECT DISTINCT can_cod FROM RESULTAT').fetchall()
    for code in candidats:
        #un candidat a 1 note par matière
        matieres = cur.execute('SELECT id_matiere FROM RESULTAT WHERE can_cod = (?)', (float(code[0]),)).fetchall()
        for i in matieres:
            assert(matieres.count(i) == 1)

# def test_coherence_ELEVE():
#     #les INE sont tous différents
#     INE = cur.execute('SELECT INE FROM ELEVE').fetchall()
#     for ine in INE:
#         if ine != None:
#             assert (INE.count(ine) == 1)
#     assert True

# con.close()

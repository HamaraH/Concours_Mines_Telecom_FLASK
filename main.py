from flask import Flask, render_template, request, g, session, redirect
import pdfkit  # package permettant la création de pdf dynamiquement
import queries.eleve, queries.matiere, queries.compte, queries.baccalaureat, queries.ecole, queries.voeux, queries.classement, queries.filiere, queries.resultat, queries.ats, queries.parcours_prepa,queries.type_epreuve, queries.admission, queries.integration
from utils import graph_note_eleve, graph_note_stats, DBCreation, remplissage_bdd, liste_voeux_scei # scripts permettant de créer des graphiques de statistiques sur les notes des élèves + de créer la bdd

app = Flask(__name__)
app.secret_key = "super secret key"  # clé secrète permettant de chiffrer la session
DATABASE = './MinesDB.db'  # chemin vers la BDD

#path_wkhtmltopdf = r'H:\\Programmes_info\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'  # chemin d'accès à l'utilitaire PDF
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)  # configuration du chemin d'accès

@app.after_request  # permet d'afficher dynamiquement les graph de notes du candidat (par défaut, ils ne sont pas refresh dynamiquement)
def add_header(response):
    response.cache_control.max_age = 0 # durée de vie des images dans le cache
    return response

# permet de charger la bdd au premier lancement de l'application
@app.before_first_request
def activate_bd():
    get_db()
    if queries.eleve.isEmpty():
        remplissage_bdd.fill_DB()
    if queries.compte.isEmpty():
        queries.compte.createStudentsAccounts()   # fonction qui permet d'assigner un compte à chaque candidat pour se connecter sur la plateforme
    if not queries.voeux.isDefined():
        liste_voeux_scei.dico_resultat_voeux()
# getInstance pour n'avoir qu'une seule connexion à la DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DBCreation.openDB()   # si la BDD n'existe pas, appel au script de création
    return db

# en cas de fermeture brutale du site
@app.teardown_appcontext
def close_connexion(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()  # fermeture de la BDD

# page d'accueil
@app.route("/", methods=['GET', 'POST'])
def home():

    if request.method == 'POST':  # cas où un utilisateur effectue une demande de connection

        if queries.compte.accountExists(request.form['username'], request.form['password']):  # si le compte existe

            session['username'] = request.form['username']  # création de la variable de session
            if '@' in request.form['username']:   # si c'est un email, ce n'est pas un candidat
                session['typeCompte'] = "teacher"
            else:
                session['typeCompte'] = "student" # sinon c'est un candidat
                data = queries.eleve.getDisplayInfosEleve(session['username'])  # on récupère le nom et prénom du candidat
                session['nom'] = data[0]  # création des variables de session permettant l'affichage des informations dans le header
                session['prenom'] = data[1]
                session['filiere'] = data[2]

            return render_template("base.html", connected = True)   # le booleen permet de désactiver l'affichage de la notice sur le site
        else:
            return render_template("login.html") # si le compte n'existe pas, l'utilisateur est renvoyé sur la page de login
    else:
        return render_template("base.html")  # cas où on arrive simplement sur l'accueil du site !

# page d'inscription au site
@app.route("/register", methods=['GET', 'POST'])
def register():

    return render_template("register.html")

# page de connexion
@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':  # cas où un utilisateur vient d'effectuer une création de compte, son compte est créé et il est directement invité à se connecter
        if not queries.compte.accountExists(request.form['mail'], request.form['password']):
            queries.compte.createAccount(request.form['mail'], request.form['password'])
        else:
            return render_template("erreur.html",display_title = "Ce compte existe déjà! ")

    return render_template("login.html")

# consultation de tous les élèves inscrits au concours
@app.route("/listeEleve", methods=['GET', 'POST'])
def showAllEleves():

    buttons = queries.filiere.getAllFilieres()
    buttons.append('ATS')

    if request.method == "POST":  # cas où l'enseignant a effectué une recherche par filiere

        if request.form['filiere'] == "ATS":   # si la recherche concerne les ATS (table à part), on récupère les données correspondantes
            return render_template("listeEleve.html", data=queries.ats.getAllEleveATS(), headers=["Nom", "Prénom", "Numéro de candidat"], display_title="Liste des élèves de la filière " + request.form['filiere'] + " au concours Mines-Télécom", buttons= buttons, ATS = True)
        else:  # sinon, on utilise la méthode getElevesByFiliere "classique"

            return render_template("listeEleve.html", data = queries.eleve.getElevesByFiliere(request.form["filiere"]), headers = ["Nom", "Prénom", "Numéro de candidat", "INE"], display_title = "Liste des élèves de la filière " + request.form['filiere'] +" au concours Mines-Télécom", buttons = buttons)

    else:
        # cas de base où l'on souhaite accèder à la page simplement
        return render_template("listeEleve.html", data = queries.eleve.getAllEleve(), headers = ["Nom", "Prénom", "Numéro de candidat", "INE"], display_title = "Liste des élèves inscrits au concours Mines-Télécom", buttons = buttons)

# déconnexion du site (fermeture de la session)
@app.route("/deconnexion", methods=['GET', 'POST'])
def disconnect():

    session.clear()  # permet de détruire les variables de session
    return redirect("/") # redirige sur la page d'accueil une fois déconnecté

# affiche toutes les écoles accessibles par le concours MT
@app.route("/ecoles", methods=['GET', 'POST'])
def displayAllEcoles():

    return render_template("display.html", data=queries.ecole.getAllEcoles(), display_title= "Liste des écoles accessibles via le concours Mines-Télécom", headers = ["Nom de l'école"])

# permet à un candidat de consulter / modifier les informations de son dossier
@app.route("/dossier", methods=['GET', 'POST'])
def displayDossier():

    # Si on est en POST, cela signifie que l'élève a souhaité modifier des informations de son dossier
    if request.method == "POST":
        queries.eleve.updateInfos(request.form['nom'], request.form['prenom'], request.form['autres_prenoms'], request.form['date_naissance'], request.form['adresse'], request.form['complement_adresse'], request.form['code_postal'], request.form['numero_portable'], request.form['numero_fixe'], request.form['mail'], request.form['INE'], session['username'])

        return render_template("dossier.html",
                               data=queries.eleve.getEleveInfos(session['username']),
                               baccalaureat=queries.baccalaureat.getBaccalaureatInfosByEleve(session['username']),
                               CPGE=queries.parcours_prepa.getParcoursPrepaByEleve(session['username']),
                               options=queries.parcours_prepa.getOptionsByEleve(session['username']),
                               headersBAC=["Série", "Mention", "Département", "Mois d'obtention", "Année d'obtention"],
                               headersCPGE=["Etablissement", "Sujet TIPE", "Puissance"])

    # Si on est en GET, cela signifie qu'un personnel administratif souhaite consulter le dossier du candidat
    elif request.method == "GET":

        if 'can_cod' in request.args:

            if 'ATS' in request.args:
                return render_template("dossierATS.html", data=queries.ats.getATSInfosByEleve(request.args['can_cod']), teacherView=True)

            if queries.eleve.getEleveInfos(request.args['can_cod']) == []:  # si le numéro de candidat n'est pas dans la BDD

                return render_template("erreur.html", display_title="Mauvais numéro de candidat")

            else:
                # si le can_cod est dans la BDD, on récupère les données correspondantes
                student_marks, avg, subjects = queries.resultat.computeGraphData(request.args['can_cod'])  # méthode permettant de récupèrer les données nécessaires au graph

                if student_marks != []:
                    graph_note_eleve.computeGraph(student_marks, avg, subjects)  # appel au script qui permet de créer le graph des notes
                # les différents concours de passe le candidat (ex: Mines Pont) + les données correspondantes
                concours, concours_data, data2 = queries.resultat.computeNoteData(request.args['can_cod'])

                return render_template("dossierTeacherView.html",
                                       data=queries.eleve.getEleveInfos(request.args['can_cod']),
                                       baccalaureat=queries.baccalaureat.getBaccalaureatInfosByEleve(request.args['can_cod']),
                                       CPGE=queries.parcours_prepa.getParcoursPrepaByEleve(request.args['can_cod']),
                                       options=queries.parcours_prepa.getOptionsByEleve(request.args['can_cod']),
                                       headersBAC=["Série", "Mention", "Département", "Mois d'obtention", "Année d'obtention"],
                                       headersCPGE=["Etablissement", "Sujet TIPE", "Puissance"],
                                       concours=concours,
                                       ecrit = queries.resultat.getNotesEcritesByEleve(request.args['can_cod']),
                                       oral = queries.resultat.getNotesOralesByEleve(request.args['can_cod']),
                                       liste_concours = concours,
                                       concours_data = concours_data,
                                       data2 = data2,
                                       teacherView = True)

        else:

            if queries.ats.isATS(session['username']):
                return render_template("dossierATS.html", data=queries.ats.getATSInfosByEleve(session['username']))

            else:
                # Sinon, nous sommes juste dans le cas où un candidat souhaite consulter son dossier (aucune requête à passer car le can_cod est stocké dans la session)
                return render_template("dossier.html",
                                       data=queries.eleve.getEleveInfos(session['username']),
                                       baccalaureat=queries.baccalaureat.getBaccalaureatInfosByEleve(session['username']),
                                       CPGE=queries.parcours_prepa.getParcoursPrepaByEleve(session['username']),
                                       options=queries.parcours_prepa.getOptionsByEleve(session['username']),
                                       headersBAC=["Série", "Mention", "Département", "Mois d'obtention","Année d'obtention"],
                                       headersCPGE=["Etablissement", "Sujet TIPE", "Puissance"])


# permet à un candidat d'obtenir toutes ses notes
@app.route("/notes", methods=['GET', 'POST'])
def displayNotes():

    student_marks,avg,subjects = queries.resultat.computeGraphData(session['username'])  # méthode permettant de récupèrer les données nécessaires au graph
    if student_marks != []:
        graph_note_eleve.computeGraph(student_marks,avg,subjects) # appel au script qui permet de créer le graph des notes
    # les différents concours de passe le candidat (ex: Mines Pont) + les données correspondantes
    concours, concours_data, data = queries.resultat.computeNoteData(session['username'])
    # on reconstruit une liste propre des données des concours supplémentaires
    concours_storage = []

    for i in range(0, len(concours)):
        concours_storage.append([concours[i][0], concours_data[i]])

    return render_template("notes.html", data = data, ecrit = queries.resultat.getNotesEcritesByEleve(session['username']), oral = queries.resultat.getNotesOralesByEleve(session['username']), concours_data = concours_storage)

# permet à un candidat de consulter sa liste de voeux
@app.route("/voeux", methods=['GET', 'POST'])
def displayVoeux():

    return render_template("voeux.html", display_title = "Liste des voeux" ,  data=queries.voeux.getVoeuxByEleve(session['username']), rang=queries.classement.getRangGeneralByEleve(session['username']), headers = ["Nom de l'école", "Ordre de voeux", "Réponse obtenue"])

@app.route("/stats", methods=['GET', 'POST'])
def displayStats():

    if request.method == "POST":  # POST = on a cliqué sur un bouton
        options = []
        # on récupère les matières passées par les candidats de la filière en question
        if request.form['filiere'] == "MP":
            liste_matiere_ecrites, langues, options = queries.matiere.getMatiereByFiliereAndTypeEpreuve(request.form['filiere'], "Notes Ecrites")
        else:
            liste_matiere_ecrites, langues = queries.matiere.getMatiereByFiliereAndTypeEpreuve(request.form['filiere'], "Notes Ecrites")

        liste_matiere_orales = queries.matiere.getMatiereByFiliereAndTypeEpreuve(request.form['filiere'], "Notes orales Concours Mines-Télécom")
        liste_label_img_orales = []
        liste_label_img_ecrites = [] # listes permettant de contenir les chemins vers les images qui vont être crées
        table_data_ecrite = []
        table_data_orale = []

        #if request.form['filiere'] == "MP":  # différenciation info / SI

        for i in range(0, len(liste_matiere_ecrites)): # pour chaque matière écrite, on récupère les données correspondantes, on crée le graph et on stocke son chemin
            notes=queries.resultat.getResultatByMatiereAndFiliere(liste_matiere_ecrites[i], request.form['filiere'])
            if(notes != []):
                liste_label_img_ecrites.append("static/graphs/graphm_" + liste_matiere_ecrites[i].strip().replace("/", " ").replace(" ", "_") + ".png")
                graph_data = graph_note_stats.computeGraph(notes, (liste_matiere_ecrites[i].strip().replace("/", " ").replace(" ", "_")))
                table_data_ecrite.append((liste_matiere_ecrites[i],round(graph_data[0],2), round(graph_data[1],2), round(graph_data[2],2), round(graph_data[3],2), round(graph_data[4],2)))

        for i in range(0, len(liste_matiere_orales)):  # pareil pour chaque matiere orale
            notes = queries.resultat.getResultatByMatiereAndFiliere(liste_matiere_orales[i], request.form['filiere'])
            if (notes != []):
                liste_label_img_orales.append("static/graphs/graphm_" + liste_matiere_orales[i].strip().replace("/", " ").replace(" ", "_") + ".png")
                graph_data = graph_note_stats.computeGraph(notes, (liste_matiere_orales[i].strip().replace("/", " ").replace(" ", "_")))
                table_data_orale.append((liste_matiere_ecrites[i], round(graph_data[0], 2), round(graph_data[1], 2), round(graph_data[2], 2), round(graph_data[3], 2), round(graph_data[4], 2)))

        for i in range(0, len(langues)):
            notes = queries.resultat.getNotesByLangueAndFiliere(langues[i], request.form['filiere'])
            if (notes != []):
                liste_label_img_ecrites.append("static/graphs/graphm_" + langues[i].strip().replace("/", " ").replace(" ", "_") + ".png")
                graph_data = graph_note_stats.computeGraph(notes, (langues[i].strip().replace("/", " ").replace(" ", "_")))
                table_data_ecrite.append((langues[i], round(graph_data[0], 2), round(graph_data[1], 2), round(graph_data[2], 2), round(graph_data[3], 2), round(graph_data[4], 2)))

        if options != []:
            for i in range(0, len(options)):
                notes = queries.resultat.getNotesByOptionMP(options[i])
                if (notes != []):
                    liste_label_img_ecrites.append(
                        "static/graphs/graphm_" + options[i].strip().replace("/", " ").replace(" ", "_") + ".png")
                    graph_data = graph_note_stats.computeGraph(notes,
                                                               (options[i].strip().replace("/", " ").replace(" ", "_")))
                    table_data_ecrite.append((options[i], round(graph_data[0], 2), round(graph_data[1], 2),
                                              round(graph_data[2], 2), round(graph_data[3], 2),
                                              round(graph_data[4], 2)))

        return render_template("stats.html",  table_data_orale = table_data_orale, table_data_ecrite = table_data_ecrite, headers=["Epreuve","Q1", "Q2", "Q3", "Moyenne", "Ecart_type"], liste_label_img_ecrites = liste_label_img_ecrites, liste_label_img_orales = liste_label_img_orales, buttons = queries.filiere.getAllFilieres())

    else: # cas de base: on arrive sur la page sans avoir choisi une filiere

        return render_template("stats.html", buttons = queries.filiere.getAllFilieres())

@app.route("/toPDF", methods=['POST'])
def pageToPDF():

    options = {
        "enable-local-file-access": None,
        'page-size': 'A2',
        'dpi': 400,
        '--disable-smart-shrinking': ''
        # option permettant d'accéder à des images stockées localement
    }

    if 'notes' in request.form:  # si on clique sur le bouton PDF de la page notes
        red = "notes"
        concours, concours_data, data = queries.resultat.computeNoteData(session['username']) # on effectue le même cheminement que pour afficher la page note

        rendered = render_template("notes.html", data=data,
                               ecrit=queries.resultat.getNotesEcritesByEleve(session['username']),
                               oral=queries.resultat.getNotesOralesByEleve(session['username']),
                               liste_concours=concours, concours_data=concours_data)

    elif 'voeux' in request.form:  # si on clique sur le bouton PDF de la page voeux

        red = "voeux"
        rendered = render_template("display.html", display_title = "Liste des voeux" ,  data=queries.voeux.getVoeuxByEleve(session['username']), rang=queries.classement.getRangGeneralByEleve(session['username']), headers = ["Nom de l'école", "Ordre de voeux"])

    # création du pdf et stockage vers le chemin spécifié

    pdfkit.from_string(rendered, 'rapports/' + red +'.pdf', configuration=config, options=options, css="static\styles\main.css")

    return redirect(red)


@app.route("/listeIntegration", methods=['GET', 'POST'])
def showAllIntegration():

    return render_template("listeIntegration.html", data=queries.ecole.getAllEcolesRne(), headers = ["Code Ecole","Nom de l'école"], display_title = "Liste des écoles accessibles via le concours Mines-Télécom")



@app.route("/integration", methods=['GET', 'POST'])
def displayIntegration():
    buttons = queries.filiere.getAllFilieres()
    buttons.append('ATS')

    # Si on est en GET, cela signifie qu'un personnel administratif souhaite consulter les résultats d'intégration de l'école
    if request.method == "GET":

        if 'code_ecole' in request.args:

            if queries.integration.checkEcole(request.args['code_ecole']) == []:  # si l'école n'est pas dans la BDD

                return render_template("erreur.html", display_title="Mauvais numéro d'école")

    if request.method == "POST":  # cas où l'enseignant a effectué une recherche par filiere
        acc = []

        if request.form['filiere'] == "ATS":   # si la recherche concerne les ATS (table à part), on récupère les données correspondantes
            #return render_template("listeEleve.html", data=queries.ats.getAllEleveATS(), headers=["Nom", "Prénom", "Numéro de candidat"], display_title="Liste des élèves de la filière " + request.form['filiere'] + " au concours Mines-Télécom", buttons= buttons, ATS = True)
            return render_template("erreur.html", display_title="Problème ATS")
        else:
            acc = [request.form["filiere"]]
            acc.append(queries.integration.countPlaceByFil(request.args['code_ecole'],request.form["filiere"]))
            acc.append(queries.integration.countAllEleveByFil(request.args['code_ecole'],request.form["filiere"]))
            if acc[2] != 0:
                aux = str((queries.integration.countAllGirlByFil(request.args['code_ecole'],request.form["filiere"])/acc[2])*100)
                if len(aux) >= 5:
                    aux = aux[:5]
                acc.append(aux+"%")
                aux = str((queries.integration.countAllDemiByFil(request.args['code_ecole'],request.form["filiere"])/acc[2])*100)
                if len(aux) >= 5:
                    aux = aux[:5]
                acc.append(aux+"%")
                aux = str((queries.integration.countAllBoursierByFil(request.args['code_ecole'],request.form["filiere"])/acc[2])*100)
                if len(aux) >= 5:
                    aux = aux[:5]
                acc.append(aux+"%")
            else:
                acc = acc + ["","",""]
            acc += queries.integration.computeMoyenneData(request.args['code_ecole'],request.form["filiere"])
            return render_template("integration.html",acc = acc, data = queries.integration.getAllEleveByFil(request.args['code_ecole'],request.form["filiere"]), headers = ["Code Candidat", "Nom", "Prénom", "Rang d'admission"], code = request.args['code_ecole'], display_title = "Liste des admis à " + queries.integration.getNameEcole(request.args['code_ecole']), buttons = buttons)

    else: # cas de base où l'on souhaite accèder à la page simplement
        acc = ["MP"]
        acc.append(queries.integration.countPlaceByFil(request.args['code_ecole'],"MP"))
        acc.append(queries.integration.countAllEleveByFil(request.args['code_ecole'],"MP"))
        if acc[2] != 0:
            aux = str((queries.integration.countAllGirlByFil(request.args['code_ecole'],"MP")/acc[2])*100)
            if len(aux) >= 5:
                aux = aux[:5]
            acc.append(aux+"%")
            aux = str((queries.integration.countAllDemiByFil(request.args['code_ecole'],"MP")/acc[2])*100)
            if len(aux) >= 5:
                aux = aux[:5]
            acc.append(aux+"%")
            aux = str((queries.integration.countAllBoursierByFil(request.args['code_ecole'],"MP")/acc[2])*100)
            if len(aux) >= 5:
                aux = aux[:5]
            acc.append(aux+"%")
        else:
            acc = acc + ["","",""]
        acc += queries.integration.computeMoyenneData(request.args['code_ecole'],"MP")
        return render_template("integration.html",acc = acc, data = queries.integration.getAllEleveByFil(request.args['code_ecole'],"MP"), headers = ["Code Candidat", "Nom", "Prénom", "Rang d'admission"], code = request.args['code_ecole'], display_title = "Liste des admis à " + queries.integration.getNameEcole(request.args['code_ecole']), buttons = buttons)

# main: lancement de l'application web
if __name__ == "__main__":
    app.run()

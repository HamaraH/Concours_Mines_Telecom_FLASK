Afin de fonctionner, le projet nécessite l'installation préalable des libraires suivantes via le gestionnaire de package pip:
- pdfkit
- Flask (évidemment !)
- matplotlib
- numpy
- sqlite3
- pandas
- pytest
- openpyxl


Il est également nécessaire, si l'on souhaite pouvoir exporter les pages du site au format PDF, d'installer la librairie "wkhtmltopdf" disponible à l'adresse :  
https://wkhtmltopdf.org/downloads.html
Et d'insérer le chemin vers cette librairie une fois installée dans la ligne 10 du fichier main.py

Architecture du projet : 

- Répertoire "queries" : contient l'ensemble des requêtes utiles au site
- Répertoire "rapport" : contient les rapports générés en PDF via le site
- Répertoire "static" : contient l'ensemble des images utiles au site, des graphiques de notes générés par le script (ne pas toucher à ce répertoire !)
- Répertoire "Templates" : contient l'ensemble des templates du site
- Répertoire "Tests" : contient les tests unitaires effectués sur la cohérence de la BDD
- Répertoire "utils" : contient des scripts permettant notamment la création, le remplissage de la BDD (ne pas toucher à ce répertoire !)   





  
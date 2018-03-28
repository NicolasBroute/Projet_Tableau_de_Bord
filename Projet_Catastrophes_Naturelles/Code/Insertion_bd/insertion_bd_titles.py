import pyodbc
import csv

# Connexion à la base de données sur SQL Server
host = "DESKTOP-QEBO46O\SQLSERV"
db = "master"
user = ""
pwd = ""

conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=" + host +
                      ";DATABASE=" + db + ";UID=" + user + ";PWD=" + pwd)

# Création du curseur
cursor = conn.cursor()

# Ouverture et lecture du fichier csv contenant les mots clés
# des titres des articles
f = open('Fichier_csv_insertion/titres.csv', 'r', encoding="utf8")
file_titles = csv.reader(f, delimiter=',', quotechar='"')

# Pour chaque mot clé du titre on insère les informations
# dans la  base de données
for title in file_titles:
    cursor.execute("exec dbo.INSERTION_TITRE @pid_titre = " + title[0] +
                   ", @pposition_mot = " + title[1] + ", @pscore_tf_idf = " +
                   title[2] + ", @pid_article = " + title[3] +
                   ", @pid_mot = " + title[4] + ", @pid_nombre = " + title[5])

    # On enregistre l'ajout de la ligne qu'on vient de faire
    cursor.commit()

# Fermeture du fichier csv
f.close()

# Fermeture de la connexion à la base de données
conn.close()

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

# Ouverture et lecture du fichier csv contenant tous les différents mots présents dans les articles
# (mots qui ont un tf*idf supérieur à un certain score)
f = open('Fichier_csv_insertion/mots.csv', 'r', encoding="utf8")
fichier_mots = csv.reader(f, delimiter=',', quotechar='"')

# Pour chaque mot on insère les informations dans la  base de données
for mot in fichier_mots:
    m = "'" + mot[1] + "'"
    entite = "'" + mot[2] + "'"
    type_mot = "'" + mot[3] + "'"
    cursor.execute("exec dbo.INSERTION_MOTS @pid_mot = " + mot[0] +
                   ", @pmot = " + m + ", @ptype_mot = " + type_mot +
                   ", @pentite = " + entite)

    # On enregistre l'ajout de la ligne qu'on vient de faire
    cursor.commit()

# Fermeture du fichier csv
f.close()

# Fermeture de la connexion à la base de données
conn.close()

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

# Ouverture et lecture du fichier csv contenant tous les différents nombres présents dans les articles
f = open('Fichier_csv_insertion/nombres.csv', 'r', encoding="utf8")
fichier_nombres = csv.reader(f, delimiter=',', quotechar='"')

# Pour chaque nombre on insère les informations dans la  base de données
for nb in fichier_nombres:
    if nb[2] == 'km2':
        nb[2] = 'NULL'
    if nb[2] == 'Richter':
        nb[2] = 4774
    cursor.execute("exec dbo.INSERTION_NOMBRES @pid_nombre = " + nb[0] +
                   ", @pnombre = " + nb[1] + ", @pid_mot = " + nb[2])

    # On enregistre l'ajout de la ligne qu'on vient de faire
    cursor.commit()

# Fermeture du fichier csv
f.close()

# Fermeture de la connexion à la base de données
conn.close()

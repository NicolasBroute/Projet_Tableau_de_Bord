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

# Ouverture et lecture du fichier csv contenant les mots clés des contenus
f = open('Fichier_csv_insertion/contenu_mots_cles.csv', 'r', encoding="utf8")
file_content = csv.reader(f, delimiter=',', quotechar='"')

# Pour chaque mot clé du contenu on insère les informations dans la  base de données
for content in file_content:
    cursor.execute("exec dbo.INSERTION_CONTENU_MOTS_CLES @pid_contenu = " +
                   content[0] + ", @pposition_mot = " + content[1] +
                   ", @pscore_tf_idf = " + content[2] + ", @pid_article = " +
                   contenu[3] + ", @pid_mot = " + content[4] +
                   ", @pid_nombre = " + content[5])

    # On enregistre l'ajout de la ligne qu'on vient de faire
    cursor.commit()

# Fermeture du fichier csv
f.close()

# Fermeture de la connexion à la base de données
conn.close()

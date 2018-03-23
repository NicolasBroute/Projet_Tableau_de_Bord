import pyodbc
import csv
import re

# Connexion à la base de données sur SQL Server
host = "DESKTOP-QEBO46O\SQLSERV"
db = "master"
user = ""
pwd = ""

conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=" + host +
                      ";DATABASE=" + db + ";UID=" + user + ";PWD=" + pwd)

# Création du curseur
cursor = conn.cursor()

# Ouverture et lecture du fichier csv contenant les articles
f = open('Fichier_csv_insertion/articles.csv', 'r', encoding="utf8")
file_articles = csv.reader(f, delimiter=',', quotechar='"')

# Pour chaque article on insère les informations dans la  base de données
for article in file_articles:
    if re.search("\'", article[2]):
        author = article[2]
        author = author.replace("'", " ")
        author = "'" + author + "'"
    else:
        author = "'" + article[2] + "'"

    if re.search("\'", article[4]):
        theme = article[4]
        theme = theme.replace("'", " ")
        theme = "'" + theme + "'"
    elif re.search("\,", article[4]):
        theme = article[4]
        theme = theme.replace(",", " ")
        theme = "'" + theme + "'"
    else:
        theme = "'" + article[4] + "'"
    
    journal = "'" + article[1] + "'"
    
    if article[3] == '':
        article[3] = 'NULL'

    cursor.execute("exec dbo.INSERTION_ARTICLE @pid_article = " + article[0] +
                   ", @pjournal = " + journal + ", @pauteur = " +
                   author + ", @pdate_article = " + article[3] +
                   ", @ptheme = " + theme)
    # On enregistre l'ajout de la ligne qu'on vient de faire
    cursor.commit()

# Fermeture du fichier csv
f.close()

# Fermeture de la connexion à la base de données
conn.close()

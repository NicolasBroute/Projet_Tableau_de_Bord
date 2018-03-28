import csv
import pyodbc
import unidecode
from collections import defaultdict

# Connexion à la base de données sur SQL Server
host = "DESKTOP-QEBO46O\SQLSERV"
db = "master"
user = ""
pwd = ""

conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=" + host +
                      ";DATABASE=" + db + ";UID=" + user + ";PWD=" + pwd)

# Création du curseur
cursor = conn.cursor()

f = open('sql-pays.csv', 'r', encoding="utf8")
file = csv.reader(f, delimiter=',', quotechar='"')
list_country = []
for line in file:
    country = line[4]
    country = country.lower()
    country = unidecode.unidecode(country)
    list_country.append(country)

cursor.execute("SELECT score_tf_idf, mot FROM contenus_mots_cles c, mots m " +
               "WHERE entite ='PAYS' and c.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")
result = []
row = cursor.fetchone()

while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

country_presents = []
result_country = []
for resu in result:
    if resu[1] in list_country:
        if resu not in result_country:
            result_country.append(resu)
            country_presents.append(resu[1])

dictionnary = defaultdict(int)
for resu in result_country:
    dictionnary[resu[1]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])


link = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Semestre 2/" + \
    "Projet_tableau_de_bord/"
name = "requete_pays_plus_touches.csv"


def export_csv(link, name, file):
    with open(link + name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)


export_csv(link, name, table)

f.close()


conn.close()

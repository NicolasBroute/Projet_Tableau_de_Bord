import csv
import pyodbc
import unidecode

# Connexion à la base de données sur SQL Server
host = "DESKTOP-QEBO46O\SQLSERV"
db = "master"
user = ""
pwd = ""

conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=" + host +
                      ";DATABASE=" + db + ";UID=" + user + ";PWD=" + pwd)

# Création du curseur
cursor = conn.cursor()

# Ouverture et lecture du fichier contenant une liste des pays
f = open('sql-pays.csv', 'r', encoding="utf8")
file = csv.reader(f, delimiter=',', quotechar='"')
list_country_coord = []
list_country = []
for line in file:
    c = []
    country = line[4]
    country = country.lower()
    country = unidecode.unidecode(country)
    c.append(line[2])
    c.append(country)
    list_country_coord.append(c)
    list_country.append(country)

# Ouverture et lecture du fichier contenant les coordonnées des pays
coord = open('coord_ville.csv', 'r', encoding="utf8")
file_coord = csv.reader(coord, delimiter=',', quotechar='"')
list_coord = []
for line in file_coord:
    coordinates = []
    coordinates.append(line[0])
    coordinates.append(line[1])
    coordinates.append(line[2])
    list_coord.append(coordinates)

# Requete pour obtenir les mots
cursor.execute("SELECT score_tf_idf, mot FROM contenus_mots_cles c, mots m " +
               "WHERE c.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")
result = []
row = cursor.fetchone()

while row:
    line_result = []
    line_result.append(row[0])
    if row[1] == 'hongkong':
        line_result.append('hong-kong')
    elif row[1] == 'paysbas':
        line_result.append('pays-bas')
    elif row[1] == 'nouvellezelande':
        line_result.append('nouvelle-zelande')
    elif row[1] == 'nouvellecaledonie':
        line_result.append('nouvelle-caledonie')
    elif row[1] == 'royaumeuni':
        line_result.append('royaume-uni')
    elif row[1] == 'etatsunis':
        line_result.append('etats-unis')
    else:
        line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

# On récupère la liste des pays présents dans notre BD
list_c = []
country_presents = []
for resu in result:
    if resu[1] in list_country:
        if resu[1] not in list_c:
            line = []
            valeur_index = list_country.index(resu[1])
            line.append(list_country_coord[valeur_index][0])
            line.append(resu[1])
            country_presents.append(line)
            list_c.append(resu[1])

# On asoocie à chaque pays sa lattitude et sa longitude
country_lati_longi = []
for i in range(0, len(country_presents)):
    for j in range(0, len(list_coord)):
        if list_coord[j][0] == country_presents[i][0]:
            ligne = []
            ligne.append(country_presents[i][1])
            ligne.append(list_coord[j][1])
            ligne.append(list_coord[j][2])
            country_lati_longi.append(ligne)

# On modifie entite pour savoir quels mots sont les pays
for country in list_c:
    country = "'" + country + "'"
    cursor.execute("UPDATE mots SET entite = 'PAYS' WHERE mot = " + country)
    cursor.commit()

# Requete nb articles par pays par theme
cursor.execute("SELECT mot as Pays, theme, count(a.id_article) as " +
               "Nombre_articles FROM Articles a, Contenus_mots_cles c, " +
               "Mots m WHERE a.id_article = c.id_article and c.id_mot " +
               "= m.id_mot and entite = 'PAYS' and (theme = 'seisme' or " +
               "theme = 'ouragan' or theme = 'inondation' or theme = " +
               "'tremblement de terre' or theme = " +
               "'cyclone' or theme = 'typhon') GROUP BY theme, mot")
result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

link = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Semestre 2/" + \
    "Projet_tableau_de_bord/"
name = "requete_pays_theme_nb_articles.csv"


def export_csv(link, name, file):
    with open(link + name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)


export_csv(link, name, result)


# Requete nb articles et nb_morts par pays par theme
cursor.execute("SELECT T1.mot, T2.theme, AVG(T2.Nombre_morts), " +
               "count(T1.id_article) FROM (select id_article, mot from " +
               "Contenus_mots_cles c2, Mots m2 where c2.id_mot = m2.id_mot " +
               "and entite = 'PAYS') T1, (SELECT a.theme, AVG(n.nombre) as " +
               "Nombre_morts, a.id_article FROM Nombres n, " +
               "Contenus_mots_cles c, Articles a WHERE  n.id_nombre = " +
               "c.id_nombre and a.id_article = c.id_article and (n.id_mot " +
               "= 139 or n.id_mot = 3431 or n.id_mot = 3991) and (theme = " +
               "'seisme' or theme = 'ouragan' or theme = 'inondation' or " +
               "theme = 'tremblement de terre' or " +
               "theme = 'cyclone' or theme = 'typhon') and nombre < 50000 " +
               "and (nombre NOT BETWEEN 1950 and 2050) and a.id_article in " +
               "(select id_article from Contenus_mots_cles c2, Mots m2 " +
               "where c2.id_mot = m2.id_mot and entite = 'PAYS') GROUP BY " +
               "a.theme, a.id_article) T2 WHERE T1.id_article = " +
               "T2.id_article GROUP BY T2.theme, T1.mot")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    line_result.append(row[3])
    result.append(line_result)
    row = cursor.fetchone()

country_ok = []
for country in country_lati_longi:
    line = []
    c = country[0]
    c = c.replace("-", "")
    line.append(c)
    line.append(country[1])
    line.append(country[2])
    country_ok.append(line)

result_lati_longi = []
for i in range(0, len(result)):
    for j in range(0, len(country_ok)):
        if result[i][0] == country_ok[j][0]:
            line = []
            line.append(result[i][0])
            line.append(country_ok[j][1])
            line.append(country_ok[j][2])
            line.append(result[i][1])
            line.append(result[i][2])
            line.append(result[i][3])
            result_lati_longi.append(ligne)

name = "requete_pays_lati_longi_theme_nb_articles_nb_morts.csv"

export_csv(link, name, result_lati_longi)

# Requete nb morts et nb articles par pays
cursor.execute("SELECT T1.mot, AVG(T2.Nombre_morts), count(T1.id_article) " +
               "FROM (select id_article, mot from Contenus_mots_cles c2, " +
               "Mots m2 where c2.id_mot = m2.id_mot and entite = 'PAYS') " +
               "T1, (SELECT AVG(n.nombre) as Nombre_morts, a.id_article " +
               "FROM Nombres n, Contenus_mots_cles c, Articles a WHERE " +
               "n.id_nombre = c.id_nombre and a.id_article = c.id_article " +
               "and (n.id_mot = 139 or n.id_mot = 3431 or n.id_mot = 3991) " +
               "and nombre < 50000 and (nombre NOT BETWEEN 1950 and 2050) " +
               "and a.id_article in (select id_article from " +
               "Contenus_mots_cles c2, Mots m2 where c2.id_mot = " +
               "m2.id_mot and entite = 'PAYS') GROUP BY a.id_article) T2 " +
               "WHERE T1.id_article = T2.id_article GROUP BY T1.mot")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

country_ok = []
for country in country_lati_longi:
    line = []
    c = country[0]
    c = c.replace("-", "")
    line.append(c)
    line.append(country[1])
    line.append(country[2])
    country_ok.append(line)


result_lati_longi = []
for i in range(0, len(result)):
    for j in range(0, len(country_ok)):
        if result[i][0] == country_ok[j][0]:
            line = []
            line.append(result[i][0])
            line.append(country_ok[j][1])
            line.append(country_ok[j][2])
            line.append(result[i][1])
            line.append(result[i][2])
            result_lati_longi.append(line)

name = "requete_pays_nb_morts_nb_article.csv"

export_csv(link, name, result_lati_longi)

conn.close()

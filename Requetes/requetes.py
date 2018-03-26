import csv
import pyodbc
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

link = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Semestre 2/" + \
    "Projet_tableau_de_bord/"


def export_csv(link, name, file):
    with open(link + name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)


# Requete 1 : nombre d'articles par journal
cursor.execute("SELECT journal, count(id_article) as Nombre_articles " +
               "FROM Articles GROUP BY journal")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_articles_journal.csv"
export_csv(link, name, result)

# Requete 2 : nombre d'articles par theme
cursor.execute("SELECT theme, count(id_article) as Nombre_articles " +
               "FROM Articles WHERE theme = 'seisme' or theme = 'ouragan' " +
               "or theme = 'inondation' or " +
               "theme = 'tremblement de terre' or theme = 'cyclone' " +
               "or theme = 'typhon' GROUP BY theme;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_articles_theme.csv"
export_csv(link, name, result)

# Requete 3 : nombre d'articles par année
cursor.execute("SELECT year(date_article) as Annee, count(id_article)" +
               "as Nombre_articles FROM Articles GROUP BY year(date_article)" +
               "ORDER BY year(date_article)")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_articles_annee.csv"
export_csv(link, name, result)

# Requete 4 : effectif des mots représentant les nombres
cursor.execute("SELECT mot, COUNT(mot) FROM Nombres n, Mots m " +
               "WHERE n.id_mot = m.id_mot GROUP BY mot")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_mot_rpz_nombre.csv"
export_csv(link, name, result)

# Requete 5 : nombre d'articles par theme et par année
cursor.execute("SELECT theme, year(date_article) as Annee, " +
               "count(id_article) as Nombre_article FROM Articles " +
               "WHERE theme = 'seisme' or theme = 'ouragan' or " +
               "theme = 'inondation' or " +
               "theme = 'tremblement de terre' or theme = 'cyclone' " +
               "or theme = 'typhon' GROUP BY theme, year(date_article) " +
               "ORDER BY year(date_article);")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_evolution_nb_art.csv"
export_csv(link, name, result)

# Requete 6 : nombre de morts par theme
cursor.execute("SELECT a.theme, AVG(n.nombre) as Nombre_morts " +
               "FROM Nombres n, Contenus_mots_cles c, Articles a " +
               "WHERE n.id_nombre = c.id_nombre and a.id_article = " +
               "c.id_article and (n.id_mot = 139 or n.id_mot = 3431 or " +
               "n.id_mot = 3991) and (theme = 'seisme' or theme = 'ouragan' " +
               "or theme = 'inondation' or theme = " +
               "'tremblement de terre' or theme = 'cyclone' or theme = " +
               "'typhon') and nombre < 50000 and (nombre NOT BETWEEN 1950 " +
               "and 2050) GROUP BY a.theme")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_mort_theme.csv"
export_csv(link, name, result)

# Requete 7 : nombre de mort par theme et par année
cursor.execute("SELECT a.theme, year(a.date_article), AVG(n.nombre) AS " +
               "Nombre_morts FROM Nombres n, Contenus_mots_cles c, " +
               "Articles a WHERE  n.id_nombre = c.id_nombre and " +
               "a.id_article = c.id_article and (n.id_mot = 139 or " +
               "n.id_mot = 3431 or n.id_mot = 3991) and (theme = " +
               "'seisme' or theme = 'ouragan' or theme = 'inondation' " +
               "or theme = 'tremblement de terre' " +
               "or theme = 'cyclone' or theme = 'typhon') and nombre < " +
               "50000 and (nombre NOT BETWEEN 1950 and 2050) GROUP BY " +
               "a.theme, year(a.date_article) ORDER BY year(date_article)")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_mort_theme_annee.csv"
export_csv(link, name, result)

# Requete 8 : côut par theme
cursor.execute("SELECT a.theme, AVG(n.nombre) AS Cout FROM Nombres n, " +
               "Contenus_mots_cles c, Articles a WHERE  n.id_nombre = " +
               "c.id_nombre and a.id_article = c.id_article and " +
               "(n.id_mot = 4859 or n.id_mot = 2341)and (theme = 'seisme' " +
               "or theme = 'ouragan' or theme = 'inondation' or theme = " +
               "'tremblement de terre' or theme = " +
               "'cyclone' or theme = 'typhon') and nombre < 100000000000 " +
               "and (nombre NOT BETWEEN 1950 AND 2050) GROUP BY a.theme;")
result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_cout_theme.csv"
export_csv(link, name, result)

# Requete 9 : côut total par année
cursor.execute("SELECT year(a.date_article), AVG(n.nombre) AS Cout FROM " +
               "Nombres n, Contenus_mots_cles c, Articles a WHERE " +
               "n.id_nombre = c.id_nombre and a.id_article = c.id_article " +
               "and (n.id_mot = 4859 or n.id_mot = 2341) and (theme = " +
               "'seisme' or theme = 'ouragan' or theme = 'inondation' " +
               "or theme = 'tremblement de terre' " +
               "or theme = 'cyclone' or theme = 'typhon') and nombre < " +
               "100000000000and (nombre NOT BETWEEN 1950 AND 2050) GROUP " +
               "BY year(date_article) ORDER BY year(date_article);")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_cout_annee.csv"
export_csv(link, name, result)

# Requete 9-bis : côut total par theme et par année
cursor.execute("SELECT a.theme, year(a.date_article), AVG(n.nombre) AS Cout " +
               "FROM Nombres n, Contenus_mots_cles c, Articles a WHERE " +
               "n.id_nombre = c.id_nombre and a.id_article = c.id_article " +
               "and (n.id_mot = 4859 or n.id_mot = 2341) and (theme = " +
               "'seisme' or theme = 'ouragan' or theme = 'inondation' " +
               "or theme = 'tremblement de terre' " +
               "or theme = 'cyclone' or theme = 'typhon') and nombre < " +
               "100000000000 and (nombre NOT BETWEEN 1950 AND 2050) GROUP " +
               "BY a.theme, year(date_article) ORDER BY year(date_article);")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_cout_theme_annee.csv"
export_csv(link, name, result)


# Requete 10 : nombre de morts par année
cursor.execute("SELECT year(date_article), AVG(n.nombre) AS Nombre_morts " +
               "FROM Nombres n, Contenus_mots_cles c, Articles a WHERE " +
               "n.id_nombre = c.id_nombre and a.id_article = c.id_article " +
               "and (n.id_mot = 139 or n.id_mot = 3431 or n.id_mot = 3991) " +
               "and nombre < 50000 and (nombre NOT BETWEEN 1950 and 2050) " +
               "GROUP BY year(date_article) ORDER BY year(date_article);")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_mort_annee.csv"
export_csv(link, name, result)

# Requete 11 : verbes les plus fréquents dans les contenus
cursor.execute("SELECT mot , score_tf_idf " +
               "FROM Contenus_mots_cles c, mots m " +
               "WHERE m.type_mot = 'VERB' and c.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

dictionnary = defaultdict(int)
for resu in result:
    dictionnary[resu[0]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])

name = "requete_frequence_verbe_contenu.csv"
export_csv(link, name, table)

# Requete 12 : adjectifs les plus fréquents dans les contenus
cursor.execute("SELECT mot , score_tf_idf " +
               "FROM Contenus_mots_cles c, mots m " +
               "WHERE m.type_mot = 'ADJ' and c.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

dictionnary = defaultdict(int)
for resu in result:
    dictionnary[resu[0]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])

name = "requete_frequence_adjectif_contenu.csv"
export_csv(link, name, table)

# Requete 13 : noms les plus fréquents dans les contenus
cursor.execute("SELECT mot , score_tf_idf " +
               "FROM Contenus_mots_cles c, mots m " +
               "WHERE m.type_mot = 'NOUN' and c.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

dictionnary = defaultdict(int)
for resu in result:
    dictionnary[resu[0]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])

name = "requete_frequence_nom_contenu.csv"
export_csv(link, name, table)

# Requete 14 : verbes les plus fréquents dans les titres
cursor.execute("SELECT score_tf_idf, mot FROM Titres t, mots m " +
               "WHERE m.type_mot = 'VERB' and t.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

dictionnary = defaultdict(int)
for resu in result:
    dictionnary[resu[1]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])

name = "requete_frequence_verbe_titre.csv"
export_csv(link, name, table)

# Requete 15 : adjectifs les plus fréquents dans les titres
cursor.execute("SELECT score_tf_idf, mot FROM Titres t, mots m " +
               "WHERE m.type_mot = 'ADJ' and t.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

dictionnary = defaultdict(int)
for resu in result:
    dictionnary[resu[1]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])

name = "requete_frequence_adjectif_titre.csv"
export_csv(link, name, table)

# Requete 16 : noms les plus fréquents dans les titres
cursor.execute("SELECT score_tf_idf, mot FROM Titres t, mots m " +
               "WHERE m.type_mot = 'NOUN' and t.id_mot = m.id_mot " +
               "ORDER BY score_tf_idf DESC;")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    result.append(line_result)
    row = cursor.fetchone()

dictionnary = defaultdict(int)
for resu in result:
    dictionnary[resu[1]] += 1

table = []
for key in sorted(dictionnary, key=dictionnary.get, reverse=True):
    table.append([key, dictionnary[key]])

name = "requete_frequence_nom_titre.csv"
export_csv(link, name, table)

# Requete 17 : requêtes corrélation
cursor.execute("SELECT year(date_article), count(a.id_article), " +
               "AVG(n.nombre) AS Nombre_morts FROM Nombres n, " +
               "Contenus_mots_cles c, Articles a WHERE  n.id_nombre " +
               "= c.id_nombre and a.id_article = c.id_article and " +
               "(n.id_mot = 139 or n.id_mot = 3431 or n.id_mot = 3991) " +
               "and nombre < 50000 and (nombre NOT BETWEEN 1950 and 2050) " +
               "and theme = 'cyclone' GROUP BY year(date_article) ORDER BY " +
               "year(date_article);")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_correlation_cyclone.csv"
export_csv(link, name, result)

# Requete 17 : nombre articles par thème et par mois
cursor.execute("SELECT theme, month(date_article) as Mois, " +
               "count(id_article) as Nombre_article FROM Articles " +
               "WHERE theme = 'seisme' or theme = 'ouragan' or theme " +
               "= 'inondation' or theme = 'tremblement de terre' or " +
               "theme = 'cyclone' or theme = 'typhon' GROUP BY theme, " +
               "month(date_article) ORDER BY month(date_article);")

result = []
row = cursor.fetchone()
while row:
    line_result = []
    line_result.append(row[0])
    line_result.append(row[1])
    line_result.append(row[2])
    result.append(line_result)
    row = cursor.fetchone()

name = "requete_nb_articles_theme_mois.csv"
export_csv(link, name, result)


conn.close()

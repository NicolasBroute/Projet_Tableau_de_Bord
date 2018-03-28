###############################################################################
#                               description
###############################################################################
# Ce code à pour but de nettoyer les articles que les crawlers ont récupérés
# sur internet. Il doit pouvoir reduire au maximum le nombre distinct de mots
# grace à la librairie spacy et ainsi améliorer les résultats de l'étude.
# On y extrait les TF-IDF (calcul utile pour le text mining)
# En sortie de ce code se trouve 5 fichiers csv representant chacun une table
# dans notre base de données.

###############################################################################
#                               librairies
###############################################################################
# lire fichier json du crolleur
import json
# lire fichier stopword.p
import pickle
# nettoie fichier stopword
import unidecode
# exporter données propres sur ordinateur window
import csv
# librarie de nettoyage de texte
import spacy
# recherche pattern de mots dans texte
import re
# visualisation temps de traitement du programme
import datetime
# librarie mathematique pour les tableaux
import numpy as np
# creer tableau tfidf
from sklearn.feature_extraction.text import TfidfVectorizer
# import librairie des mots français  de spacy
nlp = spacy.load('fr_core_news_sm')


###############################################################################
#                                   fonctions
###############################################################################
def clean(contenu):
    # DESCRIPTION:
    # Fonction permettant de nettoyer partiellement le texte en enlevant tout
    # les caracteres spéciaux (, ; . ? : /)
    # ENTREE: contenu (string) // soit le titre, soit le contenus d'un article
    # SORTIE: contenu (string)
    contenu = "".join(
            [x if x.isalpha() or x.isnumeric() else " " for x in contenu])
    contenu = " ".join(contenu.split())
    return contenu


def KeepNumber(type_file, text, ID_numbers, ID_articles, export_numbers):
    # DESCRIPTION:
    # Fonction permettant de ressortir les chiffres importants pour notre étude
    #  et d'avoir ,pour chaque chiffre, le mot associé à ce dernier. Il
    # modifie les textes pour éviter des erreurs liées aux nombres.
    # ENTREE: type_ (string) //'title' ou 'content'
    #        text (string) // titre ou du contenu de l'article
    #        ID_numbers (int) //identifiant utilisé pour l'export des données
    #        ID_articles (int) //identifiant utilisé pour l'export des données
    #        export_numbers (array) //enregistre les infos pour chaque chiffre
    # SORTIE: text (string)
    #        ID_numbers (int)

    # liste de mots prédéfinis.
    # On ne gardera que les chiffres qui ont ces mots après eux
    liste_mot_associe = ["mort", "mourir", "deceder", "euro", "dollar",
                         "victime", "deces", "km", "km2", "km3", "metre",
                         "metres", "Richter"]
    liste = []
    # Trouver les heures
    for val in re.finditer('[0-9]{2}H[0-9]{2}', text):
        liste.append(val.group(0))
        text = text.replace(val.group(0), "")
    # Trouver les dates
    for val in re.finditer('[0-9]{2} [0-9]{2} [0-9]{4}', text):
        date = val.group(0)
        date = date.split(" ")
        date = date[0]+"-"+date[1]+"-"+date[2]
        liste.append(date)
        text = text.replace(val.group(0), "")
    # Trouver tous les autres nombres
    liste_bis = []
    for val in re.finditer('[0-9]+( [0-9]+)*( mille| million| milliard)?',
                           text):
        liste_bis.append(val.group(0))

    liste_propre = []
    for i in range(0, len(liste_bis)):
        nombre = liste_bis[i]
        if re.search("[0-9]+( [0-9]+)* [0-9]+", nombre) or re.search("[0-9]*",
                                                                     nombre):
            nombre = nombre.replace(" ", "")
        else:
            nombre = nombre.replace(" ", ".")

        if re.search("mille", nombre):
            if re.search("\.", nombre):
                nombre = nombre.replace("mille", "1000")
                sep = nombre.split(".")
                premier_nombre = sep[0] + "." + sep[1]
                deuxieme_nombre = sep[2]
                nombre = str(float(premier_nombre)*float(deuxieme_nombre))
                nombre = nombre[:-2]
            else:
                nombre = nombre.replace("mille", ".1000")
                sep = nombre.split(".")
                nombre = str(int(sep[0])*int(sep[1]))

        if re.search("million", nombre):
            if re.search("\.", nombre):
                nombre = nombre.replace("million", "1000000")
                sep = nombre.split(".")
                premier_nombre = sep[0] + "." + sep[1]
                deuxieme_nombre = sep[2]
                nombre = str(float(premier_nombre)*float(deuxieme_nombre))
                nombre = nombre[:-2]
            else:
                nombre = nombre.replace("million", ".1000000")
                sep = nombre.split(".")
                nombre = str(int(sep[0])*int(sep[1]))

        if re.search("milliard", nombre):
            if re.search("\.", nombre):
                nombre = nombre.replace("milliard", "1000000000")
                sep = nombre.split(".")
                premier_nombre = sep[0] + "." + sep[1]
                deuxieme_nombre = sep[2]
                nombre = str(float(premier_nombre)*float(deuxieme_nombre))
                nombre = nombre[:-2]
            else:
                nombre = nombre.replace("milliard", ".1000000000")
                sep = nombre.split(".")
                nombre = str(int(sep[0])*int(sep[1]))

        liste_propre.append(nombre)

    for i in range(0, len(liste_propre)):
        text = text.replace(liste_bis[i], liste_propre[i])
    liste_propre.extend(liste)
    liste_nb_mot_associe = []
    for nb in liste_propre:
        ligne_liste = []
        ligne_liste.append(nb)
        for mot in liste_mot_associe:
            if re.search(nb + "( [a-z]*){0,4}" + ' ' + mot + ' ', text):
                export_numbers.append([type_file, ID_articles,
                                       int(text.split().index(mot))+1,
                                       ID_numbers, nb, mot])
                ID_numbers += 1
                ligne_liste.append(mot)
        if ligne_liste not in liste_nb_mot_associe:
            liste_nb_mot_associe.append(ligne_liste)
    return text, ID_numbers


def timer(text):
    # DESCRIPTION:
    # Fonction permettant d'afficher l'heure et connaitre l'avancement du
    # programme
    # ENTREE: text (string) //text pour savoir l'etape du programme executée
    # SORTIE: x
    print('\n-------'+str(datetime.datetime.now().hour) + ':' +
          str(datetime.datetime.now().minute) + '-------')
    print(text)


def format_date(file):
    # DESCRIPTION:
    # les dates peuvent etre de type différents, vides ou dans le mauvais
    # format
    # le code suivant homogénise toutes le dates
    # ENTREE: file (string) //dqte de chaque articles
    # SORTIE: x
    date = file
    if date != '':
        if daily_name[j] == 'LeMonde':
            y = date[6:10]
            m = date[3:5]
            d = date[0:2]
        else:
            y = date[0:4]
            m = date[5:7]
            d = date[8:10]
        date = "'" + y + '-' + d + '-' + m + "'"
    return date


def Extract(type_file, file, all_, list_word, details_word,
            ID_numbers, ID_articles, export_numbers):
    # DESCRIPTION:
    # Fonction permettant de
    #         1) nettoyer texte
    #         2) recuperer tout les mots distincts et d'avoir les infos sur eux
    #         3) sauvegarder tout les textes propres dans des tableaux
    # ENTREE: type_file (string) //'title' ou 'content'
    #        file (string) // titre ou contenu de l'article
    #        all_ (list) // liste sauvegardant tout les texte nettoyés
    #        list_word (list) //liste de tout les mots distincts gardés
    #        details_word (array) // tableau avec le mots lemmatisé, son type
    #                                et son entité nommées
    #        ID_numbers (int) //identifiant utilisé pour l'export des données
    #        ID_articles (int) //identifiant utilisé pour l'export des données
    #        export_numbers (array) //enregistre les infos pour chaque chiffre
    # SORTIE: ID_numbers(int)

    text = " ".join(file)

    text = text.replace('Hong Kong', 'HongKong')
    text = text.replace('Pays Bas', 'PaysBas')
    text = text.replace('Nouvelle Zelande', 'NouvelleZelande')
    text = text.replace('Nouvelle Caledonie', 'NouvelleCaledonie')
    text = text.replace('Royaume Unis', 'RoyaumeUnis')
    text = text.replace('Etats Unis', 'EtatsUnis')

    # prend en compte les majucule le 1er mot de la phrase
    for i in text.split():
        if i[0].isupper():
            if str(i.lower()) != str(([token.lemma_ for token
                                      in nlp(i.lower())])[0]) \
                    and str(([token.ent_type_ for token in nlp(i)])[0]) == '':
                text = text.replace(i, str(([token.lemma_ for token in
                                             nlp(i.lower())])[0]), 1)
    text = nlp(text)
    text_str = str(text)
    for token in text:
        if str(token).isalpha():
            if token.lemma_ not in list_word:
                if token.lemma_.lower() not in list(((" ".join(list_word)).
                                                    lower()).split()):
                    list_word.append(token.lemma_)
                    type_ = token.ent_type_
                    if type_ == '' or type_ == 'MISC':
                        type_ = 'NULL'
                    details_word.append([token.lemma_.lower(), type_,
                                         token.tag_])
                else:
                    type_ = token.ent_type_
                    type_previous = list(np.array(details_word)[:, 0]). \
                        index(token.lemma_.lower())
                    if ((type_ != '' or type_ != 'MISC') and
                        (type_previous == '' or type_previous == 'MISC' or
                         type_previous == 'NULL')):
                        details_word[list(np.array(details_word)[:, 0])
                                     .index((token.lemma_.lower()))] = \
                                    ([token.lemma_.lower(), token.ent_type_,
                                      token.tag_])
            text_str = text_str.replace(token.text, token.lemma_)
            text_str = text_str.replace('rr', 'r')
            text_str = text_str.replace('  ', ' ')
    text_str, ID_numbers = KeepNumber(type_file, text_str, ID_numbers,
                                      ID_articles, export_numbers)
    all_.append(text_str.lower())
    return ID_numbers


def table_title_content(type_, all_, export, vec, tfidf, ID):
    # DESCRIPTION:
    # Fonction permettant de mettre en forme les données relatives aux tables
    # "contenus_mots_cles" et "titres"
    # ENTREE: type_ (string) //'title' ou 'content'
    #        all_ list) // liste sauvegardant tout les texte nettoyés
    #        export (array) //tableau contenant les infos relatives aux tables
    #                           "contenus_mots_cles" et "titres"
    #        vec (TfidfVectorizer) //fonction tfidf paramètrée
    #        tfidf (array) //tableau des tfidf titre et contenu differents
    #        ID (int) //Identifiant pour la table titres et contenus_mot_cles
    # SORTIE: x

    timer('Traitement des '+str(type_)+' en cours...')
    debut2 = datetime.datetime.now()

    for i in all_:
        if all_.index(i) == 1000:
            print('il reste approximativement ' +
                  str(((datetime.datetime.now() - debut2).seconds/60) *
                      len(all_)/1000) + ' min')
        if all_.index(i) % 100 == 0 and all_.index(i) != 0:
            print(str(all_.index(i)) + ' / ' + str(len(all_)))
        for word in list(vec.vocabulary_.keys()):
            if word in i.split() and word.isalpha() and word in \
                    [export_words[x][1] for x in range(0, len(export_words))]:
                pos_ = (i.split()).index(word) + 1
                a1 = all_.index(i)
                a2 = list(vec.vocabulary_.values())
                a3 = list(vec.vocabulary_.keys()).index(word.lower())
                tfidf_ = tfidf[a1][a2[a3]]
                id_word = [export_words[x][1] for x in
                           range(0, len(export_words))].index(word) + 1
                export.append([ID, pos_, tfidf_, all_.index(i) + 1,
                               id_word, 'NULL'])
        duplicate_ = []
        for number in [export_numbers[x] for x in
                       range(0, len(export_numbers))]:
            if number[4] in i.split() and number[0] == type_ and \
                    ((i.split()).index(number[4])+1) not in duplicate_:
                export.append([ID, (i.split()).index(number[4]) + 1, 'NULL',
                               all_.index(i) + 1, 'NULL',
                               (list(np.array(export_numbers)[:, 4]).index(
                                       number[4]))+1])
                duplicate_.append((i.split()).index(number[4])+1)
        ID += 1


def export_number():
    # DESCRIPTION:
    # Fonction permettant d'attribuer les clés étrangères des mots aux nombres
    # ENTREE: x
    # SORTIE: x
    timer('Traitement clés etrangères nombre en cours...')
    for i in np.array(export_words)[:, 1]:
        for j in np.array(export_numbers)[:, 5]:
            if i.lower() == j.lower():
                export_numbers[list(np.array(export_numbers)[:, 5]).
                               index(j)][5] = list(np.array(export_words)
                                                   [:, 1]).index(i) + 1


def export_csv(link, nom, file):
    # DESCRIPTION:
    # Fonction permettant d'exporter les tableaux relatifs aux tables en csv
    # ENTREE: link (string) //lien pour enregistrer les fichiers
    #        nom (string) //nom des différents fichiers
    #        file (array) //tableau à exporter
    # SORTIE: x
    with open(link + nom, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file)

###############################################################################
#                             initialisation
###############################################################################


stop_words = pickle.load(open('/home/formationsid/Bureau/Catastrophes_' +
                              'Naturelles/stopwords.p', 'rb'))
for i in range(0, len(stop_words)):
    stop_words[i] = unidecode.unidecode(clean(stop_words[i]))


link = '/home/formationsid/Bureau/Catastrophes_Naturelles/data/'
daily_name = ['LePoint', 'NouvelObs', 'Liberation', 'LeMonde', 'Figaro']
daily_number = [3969, 1741, 362, 2245, 3218]
# total=11535
before_nb = ['art_lpt_', 'art_noob_', 'art_lb_', 'art_lm_', 'art_lf_']
after_nb = ['_2018-03-05_robot.json', '_2018-01-31_robot.json',
            '_2018-03-07_robot.json', '_2018-03-07_robot.json',
            '_2018-03-07_robot.json']

all_doc = []
all_title = []
list_word = []
details_word = []

export_articles = []
export_contents = []
export_titles = []
export_numbers = []
export_words = []

ID_numbers = 1
ID_articles = 1
ID_contents = 1
ID_titles = 1
ID_words = 1

###############################################################################
#                              Nettoyage
###############################################################################

print('-------' + str(datetime.datetime.now().hour) + ':' +
      str(datetime.datetime.now().minute) + '-------')
debut = datetime.datetime.now()
for j in range(0, len(daily_name)):
    print('-------  ' + str(j) + '  -------')
    for i in range(1, daily_number[j] + 1):
        if i % 100 == 0:
            print(str(i) + ' / ' + str(daily_number[j]))

        # ouvre fichier json contenant les informations d'un article
        file = open(link + daily_name[j] + '/' + before_nb[j] + str(i) +
                    after_nb[j])
        file = json.load(file)
        if file["content"] != '' and file["title"] != '':
            date = format_date(file["date_publi"])
            export_articles.append([ID_articles, str(file["newspaper"]),
                                    str(" ".join(file["author"])), str(date),
                                    str(file["theme"])])
            ID_articles += 1

            file["content"] = clean(file["content"])
            file["content"] = file["content"].split()
            file["title"] = clean(file["title"])
            file["title"] = file["title"].split()

            # enleve les stopwords
            for k in range(0, len(stop_words)):
                while stop_words[k] in file["content"]:
                    file["content"].remove(stop_words[k])
                while stop_words[k] in file["title"]:
                    file["title"].remove(stop_words[k])

            ID_numbers = Extract('title', file["title"], all_title, list_word,
                                 details_word, ID_numbers, i, export_numbers)
            ID_numbers = Extract('content', file["content"], all_doc,
                                 list_word,
                                 details_word, ID_numbers, i, export_numbers)

###############################################################################
#                              Calcul
###############################################################################

print('\nrecuperer tout les documents et mots à duré ' +
      str((datetime.datetime.now() - debut).seconds / 60) + ' min')
print('il y a ' + str(len(list_word)) + ' mots \n\n')
timer('tf_idf en cours...')

# parametrage TF_IDF pour les contenus
vec_content = TfidfVectorizer(max_df=1.0, min_df=30, max_features=10000)
tfidf_content = vec_content.fit_transform(all_doc)
tfidf_content = tfidf_content.toarray()

# parametrage TF_IDF pour les titres
vec_title = TfidfVectorizer(max_df=1.0, min_df=5, max_features=1000)
tfidf_title = vec_title.fit_transform(all_title)
tfidf_title = tfidf_title.toarray()

# Récupérer TOUT les mots distincts (contenus et titres confondu)
a = list(vec_content.vocabulary_.keys())
b = list(vec_title.vocabulary_.keys())
a.extend(b)
word = list(set(a))

timer('Export word en cours...')

# créer tableau représentant la table mots
for i in range(0, len(word)):
    for j in range(0, len(details_word)):
        if word[i].lower() == details_word[j][0].lower() and word[i].isalpha():
            export_words.append([ID_words, str(details_word[j][0]),
                                details_word[j][1], details_word[j][2]])
            ID_words += 1

table_title_content('title', all_title, export_titles, vec_title,
                    tfidf_title, ID_titles)
table_title_content('content', all_doc, export_contents, vec_content,
                    tfidf_content, ID_contents)
export_number()

###############################################################################
#                                Export
###############################################################################
link = '/home/formationsid/Bureau/Catastrophes_Naturelles/BD/'

export_csv(link, 'articles.csv', export_articles)
export_csv(link, 'mots.csv', export_words)
export_csv(link, 'nombres.csv', np.array(export_numbers)[:, 3:6])
export_csv(link, 'titres.csv', export_titles)
export_csv(link, 'contenu_mots_cles.csv', export_contents)


print('\n\ntemps d execution: ' + str(round((datetime.datetime.now() - debut).
                                            seconds / 60, 2)) + ' min')
print('temps d execution: ' + str(round((datetime.datetime.now() - debut).
                                        seconds / 3600, 2)) + ' heures')

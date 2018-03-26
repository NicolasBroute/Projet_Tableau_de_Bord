###############################################################################
#                               description
###############################################################################
# Ce code à pour but de générer des cartes pour représenter les pays qui sont
# les plus cités dans les journaux de notre corpus et voir ceux qui sont les
# plus meurtriers. Nous avons 6 catastrophe naturelles différentes, ainsi, ce
# code génère 7 cartes, en prenant en compte la cartes toutes catastrophe
# confondues


###############################################################################
#                               librairies
###############################################################################
# permet de sauvegarder la carte en html
import os
# permet de générer et manipuler la carte
import folium
# permet de lire les fichiers csv
import csv


###############################################################################
#                                   fonctions
###############################################################################
def circle(color, pos, radius, text, weight):
    # DESCRIPTION:
    # Fonction permettant de créer des cercles sur la carte
    # ENTREE: color (string) // couleur du cercle
    #         pos (array) // coordonnées géographique d'un pays
    #         radius (int) // circonférence cercle
    #         text (string) // texte qui apparaitra dans l'infobulle
    #         weight (int) //epaisseur des trais
    # SORTIE: x
    folium.CircleMarker(
        color=color,
        location=pos,
        radius=radius,
        fill=True,
        popup=text,
        weight=weight,
    ).add_to(maps)


def color(victime):
    # DESCRIPTION:
    # Fonction permettant d'associer une couleur à un pays en fonction des
    # victimes
    # ENTREE: victime (int) // nombre de victimes moyenne par catastrophe
    # SORTIE: couleur (string) //couelur du cercle
    if victime < 500:
        couleur = '#00CC66'
    elif victime < 1000:
        couleur = '#00CC00'
    elif victime < 1500:
        couleur = '#CCCC00'
    elif victime < 2000:
        couleur = '#CC6600'
    else:
        couleur = '#CC0000'
    return couleur


def infobulles(pays, morts, articles, theme):
    # DESCRIPTION:
    # Fonction permettant de générer le texte de l'infobulle d'un pays
    # ENTREE: pays (string)
    #         morts (float)
    #         articles (float) // nombre d'articles citant ce pays
    #         theme // nom d'une catastrophe particuliere ou bien en général
    # SORTIE: txte de l'infobulle
    return(str('------------------------------' + pays +
               '-----------------------------' +
               ' -------------- '+'moyenne de morts par ' + theme + ' : ' +
               str(round(float(morts))) +
               ' -------------- nombre d article paru : ' +
               str(round(float(articles)))))


###############################################################################
#                             initialisation
###############################################################################
#/!\ toujours garder le format 'carte_xxxxxx'
list_name = ['carte_mondial',
             'carte_tremblement de terre',
             'carte_typhon',
             'carte_seisme',
             'carte_ouragan',
             'carte_inondation',
             'carte_cyclone']

# la liste suivante permet de grossir les cercles de la carte si les données
# associées de ces derniers ne sont pas assez fortes. Il est préférable de
# faire cela pour ne pas avoir une carte avec uniquement des petits points
# et non des cercles.
list_multiplier = [0.1,
                   15,
                   0.3,
                   1,
                   0.3,
                   0.6,
                   0.3]

link = '/home/formationsid/Bureau/Catastrophes_Naturelles/' +\
       'Projet_Tableau_de_Bord/Requetes/'


###############################################################################
#                              Maps
###############################################################################
for i in range(0, len(list_name)):
    # génère une carte centrée en coordonnée [18, 0] avec un zoom de 3
    maps = folium.Map(location=[18, 0], zoom_start=3, tiles='Stamen Toner')
    # cas général
    if list_name[i] == 'carte_mondial':
        file = open(link + 'requete_pays_nb_morts_nb_article.csv', 'r')
        data = csv.reader(file, delimiter=',', quotechar='"')
        theme = 'catastrophe'
        for row in data:
            col = str(color(float(row[3])))
            text = infobulles(row[0], row[3], row[4], str(theme))
            circle(col,
                   [float(row[1]), float(row[2])],
                   float(row[4])*list_multiplier[i],
                   text,
                   5)
    # cas spécifiques
    else:
        file = open(link +
                    'requete_pays_lati_longi_theme_nb_articles_nb_morts.csv',
                    'r')
        data = csv.reader(file, delimiter=',', quotechar='"')
        theme = (list_name[i])[6:]
        for row in data:
            if row[3] == theme:
                col = str(color(float(row[4])))
                text = infobulles(row[0], row[4], row[5], str(theme))

                circle(col,
                       [float(row[1]), float(row[2])],
                       float(row[5])*list_multiplier[i],
                       text,
                       5)

    # légende pour les tailles de cercles
    circle('#FFFFFF', [-45.2, -98], 5,
           str(round(5/list_multiplier[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-44.4, -111], 10,
           str(round(10/list_multiplier[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-43.6, -124], 15,
           str(round(10/list_multiplier[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-42.8, -137], 20,
           str(round(15/list_multiplier[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-42, -150], 25,
           str(round(20/list_multiplier[i])) +
           ' articles "' + theme + '"', 5)

    # légendes pour les couleurs de cercles
    circle('#00CC66', [-51, -150], 25, 'Inférieur à 500 morts par ' +
           theme + ' en moyenne', 5)
    circle('#00CC00', [-51, -137], 25, 'Entre 500 et 1000 morts par ' +
           theme + ' en moyenne', 5)
    circle('#CCCC00', [-51, -124], 25, 'Entre 1000 et 1500 morts par ' +
           theme + ' en moyenne', 5)
    circle('#CC6600', [-51, -111], 25, 'Entre 1500 et 2000 morts par ' +
           theme + ' en moyenne', 5)
    circle('#CC0000', [-51, -98], 25, 'Supérieur à 2000 morts par ' +
           theme + ' en moyenne', 5)

    # enregistrement de la carte
    maps.save(os.path.join('results', '/home/formationsid/Bureau/' +
                           'Catastrophes_Naturelles/carte/' + theme + '.html'))

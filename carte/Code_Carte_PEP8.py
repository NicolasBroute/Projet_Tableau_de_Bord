import os
import folium
import csv


def circle(color, pos, radius, text, weight):
    folium.CircleMarker(
        # couleur
        color=color,
        # geolocalisation
        location=pos,
        # circonference
        radius=radius,
        fill=True,
        # texte du pop up
        popup=text,
        # epaisseur
        weight=weight,
    ).add_to(m)


liste_nom = ['carte_mondial',
             'carte_tremblement de terre',
             'carte_typhon',
             'carte_seisme',
             'carte_ouragan',
             'carte_inondation',
             'carte_cyclone']

liste_multiplicateur = [0.1,
                        15,
                        0.3,
                        1,
                        0.3,
                        0.6,
                        0.3]

link = '/home/formationsid/Bureau/Catastrophes_Naturelles/' + \
       'Projet_Tableau_de_Bord/Requetes/'

for i in range(0, len(liste_nom)):
    m = folium.Map(location=[18, 0], zoom_start=3, tiles='Stamen Toner')
    if liste_nom[i] == 'carte_mondial':
        x = open(link + 'requete_pays_nb_morts_nb_article.csv', 'r')
        data = csv.reader(x, delimiter=',', quotechar='"')
        theme = 'mondial'
        for row in data:
            victime = float(row[3])
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

            text = str('------------------------------' + row[0] +
                       '-----------------------------' +
                       ' -------------- moyenne de morts par catastrophe : ' +
                       str(round(float(row[3]))) + '\ \ \ '
                       ' -------------- nombre d article paru : ' +
                       str(round(float(row[4]))))

            circle(couleur,
                   [float(row[1]), float(row[2])],
                   float(row[4])*liste_multiplicateur[i],
                   text,
                   5)
    else:
        x = open(link +
                 'requete_pays_lati_longi_theme_nb_articles_nb_morts.csv', 'r')
        data = csv.reader(x, delimiter=',', quotechar='"')
        theme = (liste_nom[i])[6:]
        for row in data:
            if row[3] == theme:
                victime = float(row[4])
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

                text = str('------------------------------' + row[0] +
                           '-----------------------------' +
                           ' -------------- moyenne de morts par ' +
                           str(theme) +
                           ': ' + str(round(float(row[4]))) + '\ \ \ ' +
                           ' -------------- nombre d article paru : ' +
                           str(round(float(row[5]))))

                circle(couleur,
                       [float(row[1]), float(row[2])],
                       float(row[5])*liste_multiplicateur[i],
                       text,
                       5)

    circle('#FFFFFF', [-45.2, -98], 5,
           str(round(5/liste_multiplicateur[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-44.4, -111], 10,
           str(round(10/liste_multiplicateur[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-43.6, -124], 15,
           str(round(10/liste_multiplicateur[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-42.8, -137], 20,
           str(round(15/liste_multiplicateur[i])) +
           ' articles "' + theme + '"', 5)
    circle('#FFFFFF', [-42, -150], 25,
           str(round(20/liste_multiplicateur[i])) +
           ' articles "' + theme + '"', 5)

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

    m.save(os.path.join('results', '/home/formationsid/Bureau/' +
                        'Catastrophes_Naturelles/carte/' + theme + '.html'))

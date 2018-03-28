# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:24:41 2018

@author: Nicolas
"""

import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def Cloud(link):
    '''
    Objectif de la fonction est de réaliser un nuage de mot selon la requête
    fournie
    ENTRE : un fichier requête qui contient dans la première colonne les noms
            et dans la deuxième colonne leurs poids associés
    SORTIE : la fonction affiche un top 10 des mots les plus importants
            illustré par nuage de mot
    '''
    file = open(link, "r")
    file = csv.reader(file)
    dict_values = {}
    for row in file:
        dict_values[row[0]] = int(row[1])

    dict_sort = sorted(dict_values.items(), reverse=True, key=lambda t: t[1])
    dict_back = {}
    for k, v in dict_sort:
        dict_back[k] = v
        if len(dict_back) == 10:
            break

    wordcloud = WordCloud(background_color='white', mode='RGB',
                          prefer_horizontal=1)
    wordcloud.generate_from_frequencies(frequencies=dict_back)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

link = "requete_frequence_adjectif_contenu.csv"
Cloud(link)

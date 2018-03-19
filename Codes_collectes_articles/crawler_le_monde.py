# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 10:37:23 2018

@author: Nicolas
"""

import os
import datetime as date
from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode
import g4_utils_v40 as utils
import time


def recup_articles():
    """ Objectif de la fonction est de récupérer la liste url des arcticles
    selon le mot clé recherché.
    Retourne : list_url_articles : liste des url (chaine de caractère)
    """
    list_url_articles = []
    list_page = []
    for i in range(0, 230, 10):
        list_page.append(i)
    for i in range(1, 230):
        if i in list_page:
            time.sleep(15)
            urli = ['http://www.lemonde.fr/recherche/?keywords=cyclones+' +
                    'cyclone&page_num=' + str(i) + '&operator=or&exclude_' +
                    'keywords=&qt=recherche_texte_titre&author=&period=' +
                    'custom_date&start_day=01&start_month=01&start_year=' +
                    '2000&end_day=22&end_month=02&end_year=2018&sort=asc']
            soup = utils.recovery_flux_url_rss(urli)

            for h3 in soup.find_all('div', attrs={'class': 'grid_11 conteneu' +
                                                  'r_fleuve alpha omega'}):
                for a in h3.find_all('a'):
                    if 'http://' in a.get('href'):
                        list_url_articles.append(a.get('href'))
                    else:
                        list_url_articles.append('http://www.lemonde.fr' +
                                                 a.get('href'))
        else:
            urli = 'http://www.lemonde.fr/recherche/?keywords=ouragan&page' +\
                '_num=' + str(i) + '&operator=and&exclude_keywords=&qt=' +\
                'recherche_texte_titre&author=&period=custom_date&start_day' +\
                '=01&start_month=01&start_year=2000&end_day=22&end_month=' +\
                '02&end_year=2018&sort=asc'
            soup = utils.recovery_flux_url_rss(urli)

            for h3 in soup.find_all('div', attrs={'class': 'grid_11 conten' +
                                                  'eur_fleuve alpha omega'}):
                for a in h3.find_all('a'):
                    if 'http://' in a.get('href'):
                        list_url_articles.append(a.get('href'))
                    else:
                        list_url_articles.append('http://www.lemonde.fr' +
                                                 a.get('href'))
    return (list_url_articles)


def info_articles(article_link):
    """ Objectif est de récupérer les différents élèments contenu dans les
    artciles : titre , date, auteur et contenu
    Arguments : liste d'articles
    Retourne : un article avec les différents élèments
    """

    soup = utils.recovery_flux_url_rss(article_link)
    title = soup.title.string

    newspaper = "Le Monde"

    # Article theme
    if(soup.find("li", class_="ariane z2")):
        theme = soup.find("li", class_="ariane z2").find("a").get_text()
    else:
        theme = 'Forum'

    # Author of the article
    if(soup.find("span", class_="auteur")):
        if(soup.find("span", class_="auteur").a):
            author = soup.find("span", class_="auteur").find("a").get_text()
        else:
            author = soup.find("span", class_="auteur").get_text()
        author = re.sub(r"\s\s+", " ", author)
        author = re.sub(r"^ ", "", author)
    else:
        author = ""

    # publication date
    date_p = ""
    da = re.search(r"\d{4}-\d{2}\-\d{2}", soup.find("time").get("datetime"))[0]
    if(da):
        date_p = date.datetime.strptime(da, "%Y-%m-%d").strftime("%d/%m/%Y")
    else:
        date_p = str(date.datetime.now().strftime("%d/%m/%Y"))

    # Article content
    content = ""
    for div in soup.find_all('div', attrs={'class': 'contenu_article js_' +
                                           'article_body'}):
        for p in div.find_all('p'):
            content += p.get_text() + " "
    # content = unidecode.unidecode(re.sub(r"\s\s+", " ", content))

    new_article = utils.recovery_article(
        title, newspaper, [author], date_p, content, theme)

    return new_article


def recuperation_info_lmde():
    """ Procedure qui appelle toutes les autres fonctions dans l'ordre
    pour collecter les articles depuis un journal contenu dans un ficher
    """

    links = list(set(recup_articles()))
    file_target = "data/clean/robot/" + str(date.datetime.now().date()) + "/"
    os.makedirs(file_target, exist_ok=True)
    source = "l/"
    file_target_source = file_target + source
    os.makedirs(file_target_source, exist_ok=True)
    abbreviation = "lmde"
    page = 0
    i = 0
    list_articles = []
    list_page = []
    for i in range(0, 2200, 10):
        list_page.append(i)

    for article_link in links:
        if "/article/" in article_link:
            i += 1
            page += 1

            if page in list_page:
                time.sleep(30)
                list_articles.append(info_articles(article_link))

                if i == 20:
                    utils.create_json(
                        file_target, list_articles, source, abbreviation)
                    i = 0
                    list_articles = []
            else:
                list_articles.append(info_articles(article_link))

                if i == 20:
                    utils.create_json(
                        file_target, list_articles, source, abbreviation)
                    i = 0
                    list_articles = []

    utils.create_json(file_target, list_articles, file_target_source,
                      abbreviation)


if __name__ == '__main__':
    recuperation_info_lmde()

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:39:16 2018

@author: Nicolas
"""

import time
import utils_v40 as utils
import datetime as date
from bs4 import BeautifulSoup
import re
import unidecode
import requests


def collect_url_articles():
    """ Objectif de la fonction est de récupérer la liste url des arcticles
    selon le mot clé recherché mais le contenu n'est pas dans cette page
    HTML il faudra appelé une autre fonction
    Retourne : list_url_articles : liste des url (chaine de caractère)
    """
    liste_url = ['http://www.liberation.fr/recherche/?sort=-publication_date' +
                 '_time&q=cyclone&period=custom&period_start_day=1&period_' +
                 'start_month=1&period_start_year=2000&period_end_day=29&' +
                 'period_end_month=1&period_end_year=2018&editorial_source' +
                 '=&paper_channel=460&page=']
    list_url_articles = []
    for url in liste_url:
        for i in range(1, 18):
            time.sleep(15)
            urli = url + str(i)
            soup = utils.recovery_flux_url_rss(urli)
            for h3 in soup.find_all('h3', attrs={'class': 'live-title'}):
                for a in h3.find_all('a'):
                    if 'http://' in a.get('href'):
                        list_url_articles.append(a.get('href'))
                    else:
                        list_url_articles.append('http://www.liberation.fr' +
                                                 a.get('href'))
    return (list_url_articles)


def collect_url_bis(list_url_articles):
    """ Objectif de la fonction est de récupérer la liste url des arcticles
    selon le mot clé recherché.
    Retourne : list_url_articles : liste des url (chaine de caractère)
    """
    url_final = []
    for url in list_url_articles:
        soup = utils.recovery_flux_url_rss(url)
        for link in soup.find_all('link'):
            if (url[25:] and "amphtml") in link.get('href'):
                url_final.append(link.get('href'))
    return (url_final)


def collect_article(article_link):
    """ Objectif est de récupérer les différents élèments contenu dans les
    artciles : titre , date, auteur et contenu
    Arguments : liste d'articles
    Retourne : un article avec les différents élèments
    """
    if "video" in article_link or "/apps/" in article_link \
        or "checknews" in article_link or not re.search(r"\d\d\d\d/\d\d/\d\d",
                                                        article_link):
        return None

    else:
        req = requests.get(article_link)
        data = req.text
        soup = BeautifulSoup(data, "lxml")
        try:
            theme = re.search("http://www.liberation.fr/(.*)", article_link)[1]
            theme = theme.split('/')[0]
        except:
            theme = ''

        if soup.find("div", class_="direct-headband") \
                or article_link != req.url:
            return None
        else:
            balise_title = soup.find("h1")
            balise_title = balise_title.get_text()
            balise_title = re.sub(r"\s\s+", "", balise_title)

            newspaper = "Liberation"
            title = unidecode.unidecode(balise_title)

            date_p = ""
            authors = []
            for span in soup.find_all('span'):
                if span.get("class") == ['author']:
                    if(span.a):
                        author = span.a.string
                        if author:
                            authors.append(author)
                if span.get("class") == ['date']:
                    if(span.time):
                        date_p = date.datetime.strptime(span.time.get
                                                        ("datetime"), "%Y-%m" +
                                                        "-%dT%H:%M:%S").date()
                        date_p = date_p.strftime("%d/%m/%Y")
            date_p = str(date.datetime.strptime(date_p,
                                                "%d/%m/%Y").date())
            if not authors:
                authors = ["liberation"]

            content = ""

            for h3 in soup.find_all('div', attrs={'class': 'article-body'}):
                for p in h3.find_all('p'):
                    content += p.get_text()
            content = re.sub("<>", "", content)
            content = unidecode.unidecode(content)

            new_article = utils.recovery_article(title, newspaper, authors,
                                                 date_p, content, theme)

            return new_article


def recovery_new_articles_libe(file_target="data/clean/robot/" +
                               str(date.datetime.now().date()) + "/"):
    """ Procedure qui appelle toutes les autres fonctions dans l'ordre
    pour collecter les articles depuis un journal contenu dans un ficher
    Arguments:
        file_target {string} -- chemin où les articles seront enregistrés
    """
    list_dictionaries = []

    list_url = collect_url_articles()
    list_url_articles = collect_url_bis(list_url)
    for url_article in list_url_articles:
        article = collect_article(url_article)
        list_dictionaries.append(article)
    utils.create_json(file_target, list_dictionaries, 'Liberation/', 'libe')


if __name__ == '__main__':
    recovery_new_articles_libe()

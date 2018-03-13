# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 10:43:21 2018

@author: Nicolas
"""

from bs4 import BeautifulSoup
import requests
import re
import g4_utils_v40 as utils
import datetime as date
import time


def collect_url_themes():
    """Create a list containing the URL or the differents themes
    Arguments:
        url_figaro {string} -- url of the newspaper Le Figaro.fr
    Returns:
        list_url_themes {list} -- list of URL (string)
    """
    list_url_articles = []
    liste_url = ['http://recherche.lefigaro.fr/recherche/cyclone/?datemin=01-01-2008&datemax=02-02-2018&page=']
    for url in liste_url:
        for i in range (1,5):
            urli=url + str(i)
            soup = utils.recovery_flux_url_rss(urli)
            
            #recuperer liste article recherche

            for h3 in soup.find_all('h2', attrs={'class': 'fig-profil-headline'}):
                for a in h3.find_all('a'):
                    if 'http://' in a.get('href'):
                        list_url_articles.append(a.get('href'))
                    else:
                        list_url_articles.append('http://www.lefigaro.fr' + a.get('href'))

    return list_url_articles


def collect_url_sub_themes(url_theme):
    """Create a list containing the URL or the differents sub-themes
    Arguments:
        url_theme {string} -- URL of a theme
    Returns:
        list_url_sub_themes {list} -- list of URL (string)
    """
    req = requests.get(url_theme)
    data = req.text
    soup = BeautifulSoup(data, "lxml")

    list_url_sub_themes = []
    for a in soup.find_all("a"):
        if (a.get("class") == ['figh-keyword__link']
                and "http://www.lefigaro.fr/" in a.get('href')):
            list_url_sub_themes.append(a.get('href'))
            
    return list_url_sub_themes



def collect_articles(list_dictionaries, list_url_articles, theme):
    """Add the articles (dictionaries) from a list of URL in a list of
    dictionaries
    Arguments:
        list_dictionaries {list} -- list of dictionaries
        list_url_articles {list} -- list of URL
        theme {string} -- theme related to the list of dictionaries
    """
    #list_url_articles=['http://www.lefigaro.fr/flash-actu/2018/01/15/97001-20180115FILWWW00238-pre-alerte-cyclonique-a-la-reunion.php']
    
    for url_article in list_url_articles:
        req = requests.get(url_article)
        data = req.text
        soup = BeautifulSoup(data, "lxml")

        title = soup.title.string

        list_authors = []
        for a in soup.find_all('a'):
            if a.get("class") == ['fig-content-metas__author']:
                name = re.sub("\s\s+", "", a.get_text())
                name = re.sub("\n", "", name)
                list_authors.append(name)
        if len(list_authors) == 0:
            for span in soup.find_all('span'):
                if span.get("class") == ['fig-content-metas__author']:
                    name = re.sub("\s\s+", "", span.get_text())
                    name = re.sub("\n", "", name)
                    list_authors.append(name)

        date_publication = ''
        for marker_time in soup.find_all('time'):
            for valeur in re.finditer('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
                                      str(marker_time)):
                date_publication = valeur.group(0)
        date_publication = str(date.datetime.strptime(date_publication,
                                                      "%d/%m/%Y").date())

        content = ''
        for p in soup.find_all('p'):
            if p.get("class") == ['fig-content__chapo']:
                content = p.get_text() + " "

        for h3 in soup.find_all('div', attrs={'class': 'fig-content__body'}):
            for p in h3.find_all('p'):
                content += p.get_text()
        
        
        for div in soup.find_all('div'):
            if div.get("class") == ['fig-content__body']:
                for p in div.find_all('p'):
                    content += p.get_text() + " "

        new_article = utils.recovery_article(title, 'LeFigaro',
                                             list_authors,
                                             date_publication, content,
                                             theme)
        if not utils.is_empty(new_article):
            list_dictionaries.append(new_article)
        
        return(new_article)

def recovery_new_articles_lfi(file_target="data/clean/robot/" +
                              str(date.datetime.now().date()) + "/"):
    """Procedure that calls all the others functions and procedures in order to
    collect articles from a newspaper in a file
    Arguments:
        file_target {string} -- path where the articles will be recorded
    """
    list_url_themes = collect_url_themes() #collecter url articlES

    for url_theme in list_url_themes:

        list_dictionaries = []

        #theme = re.search("http://www.lefigaro.fr/(.*)", url_theme)[1]
        #theme = re.sub("/", "", theme)


        #list_url_sub_themes = collect_url_sub_themes(url_theme)

        list_url_articles = []

        article=collect_articles(list_dictionaries, list_url_articles, "test")
        print(article)

        if article != None:
            list_dictionaries.append(article)
                    # Buffer
            number_articles += 1
            if number_articles % 50 == 0:
                utils.create_json(file_target, list_dictionaries, 'leFigaro/',
                  'lfi')
                list_dictionaries.clear()
        #time.sleep(3)

        utils.create_json(file_target, list_dictionaries, 'leFigaro/',
                          'lfi')


if __name__ == '__main__':
    recovery_new_articles_lfi()
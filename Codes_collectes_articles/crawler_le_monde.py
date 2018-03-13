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

#cyclones 2021 elements 229 pages
#http://www.lemonde.fr/recherche/?keywords=cyclones+cyclone&page_num=1&operator=or&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=22&end_month=02&end_year=2018&sort=asc


#seisme 591 pages 5097 elements
#http://www.lemonde.fr/recherche/?keywords=s%C3%A9isme&page_num=1&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=22&end_month=02&end_year=2018&sort=asc

#inondations 465 pages 4644 elements
#http://www.lemonde.fr/recherche/?keywords=inondations&page_num=1&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=22&end_month=02&end_year=2018&sort=asc




#recuperer articles recherches

def recup_articles():
    
    list_url_articles = []
    #url = ['http://www.lemonde.fr/recherche/?keywords=typhon&page_num=1&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=20&end_month=02&end_year=2018&sort=desc']        
    liste_page=[]
    for i in range(0,230,10):
        liste_page.append(i)
    
    
    for i in range(1,230):
        if i in liste_page:
            time.sleep(15)
            print(i)
            urli = 'http://www.lemonde.fr/recherche/?keywords=cyclones+cyclone&page_num=' +str(i) +'&operator=or&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=22&end_month=02&end_year=2018&sort=asc'
            soup = utils.recovery_flux_url_rss(urli)
        
            for h3 in soup.find_all('div', attrs={'class': 'grid_11 conteneur_fleuve alpha omega'}):
                for a in h3.find_all('a'):
                    if 'http://' in a.get('href'):
                        list_url_articles.append(a.get('href'))
                    else:
                        list_url_articles.append('http://www.lemonde.fr' + a.get('href'))
        else :
            print(i)
            urli = 'http://www.lemonde.fr/recherche/?keywords=ouragan&page_num=' +str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=22&end_month=02&end_year=2018&sort=asc'
            soup = utils.recovery_flux_url_rss(urli)
        
            for h3 in soup.find_all('div', attrs={'class': 'grid_11 conteneur_fleuve alpha omega'}):
                for a in h3.find_all('a'):
                    if 'http://' in a.get('href'):
                        list_url_articles.append(a.get('href'))
                    else:
                        list_url_articles.append('http://www.lemonde.fr' + a.get('href'))
                    
             
    return (list_url_articles)

'''
#recherche du contenu

url=['http://www.lemonde.fr/planete/article/2018/01/15/des-milliers-de-philippins-evacues-par-crainte-du-reveil-d-un-volcan_5241666_3244.html?xtmc=typhon&xtcr=1']
for u in url:
    soup = utils.recovery_flux_url_rss(u)
    
    for h2 in soup.find_all('div',attrs={'class': 'contenu_article js_article_body'}):
        print(h2.get_text())
'''    
      

def info_articles(article_link):

    soup = utils.recovery_flux_url_rss(article_link)
    title=soup.title.string

    #title = unidecode.unidecode(soup.find('title').string)

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
    date_p =""
    da = re.search(r"\d{4}-\d{2}\-\d{2}", soup.find("time").get("datetime"))[0]
    if(da):
        date_p = date.datetime.strptime(da, "%Y-%m-%d").strftime("%d/%m/%Y")
    else:
        date_p = str(date.datetime.now().strftime("%d/%m/%Y"))

    # Article content
    content = ""
    for div in soup.find_all('div',attrs={'class': 'contenu_article js_article_body'}):
        for p in div.find_all('p'):
            content += p.get_text() + " "
    #content = unidecode.unidecode(re.sub(r"\s\s+", " ", content))

    new_article = utils.recovery_article(
        title, newspaper, [author], date_p, content, theme)

    return new_article


#def recuperation_info_lmde():
    # Directory path

#links = recent(url)
links = recup_articles()
links=list(set(links))
'''
suppr='http://www.lemonde.fr/climat/article/2017/09/08/irma-a-saint-martin-et-saint-barthelemy-le-difficile-acheminement-des-secours_5182721_1652612.html?xtmc=ouragan&xtcr=1818'
if suppr in links:
    print("oui")
    links.remove(suppr)
suppr1='http://www.lemonde.fr/archives/article/2003/12/17/le-che-et-le-photographe_346302_1819218.html?xtmc=ouragan&xtcr=266'
if suppr1 in links:
    print("oui")
    links.remove(suppr1)
''' 
links1 =links[pos+1:] 
pos= links1.index('http://www.lemonde.fr/archives/article/2003/12/17/le-che-et-le-photographe_346302_1819218.html?xtmc=ouragan&xtcr=266')    

links2= links[pos+1:]

file_target = "data/clean/robot/" + str(date.datetime.now().date()) + "/"
os.makedirs(file_target, exist_ok=True)
source = "l/"
file_target_source = file_target + source
os.makedirs(file_target_source, exist_ok=True)
abbreviation = "lmde"
url = "http://www.lemonde.fr"
page = 0
i = 0
list_articles = []


liste_page=[]
for i in range(0,2200,10):
    liste_page.append(i)

for article_link in links2:
    if "/article/" in article_link:
        i += 1
        page += 1
        print("page :",page)
        print(article_link)
        
        if page in liste_page:
            time.sleep(30)
            list_articles.append(info_articles(article_link))

            if i == 20:
                utils.create_json(
                    file_target, list_articles, source, abbreviation)
                i = 0
                list_articles = []
        else :
            list_articles.append(info_articles(article_link))

            if i == 20:
                utils.create_json(
                    file_target, list_articles, source, abbreviation)
                i = 0
                list_articles = []

utils.create_json(file_target, list_articles, file_target_source, abbreviation)

# http://www.lemonde.fr/international/article/2008/05/21/_1047683_3210.html?xtmc=typhon&xtcr=492

if __name__ == '__main__':
    recuperation_info_lmde()
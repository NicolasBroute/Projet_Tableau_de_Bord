import utils_v40 as utils
import re
from datetime import datetime
import datetime as date


def recovery_information_noob(url_article):
    """
        Arguments:
            - url de l'article dont on va récupérer les informations utiles
        Retour:
            - informations de l'article en format json
    """
    soup_article = utils.recovery_flux_url_rss(url_article)

    title = soup_article.title.get_text()

    # Récupération de la date de publication de l'article
    find_date = soup_article.find('time', attrs={"class": "date"})
    for a in find_date.find_all('a'):
        find_valeur = re.compile('[0-9]{4}\/[0-9]{2}\/[0-9]{2}')
        for valeur in find_valeur.finditer(str(a.get("href"))):
            date_p = valeur.group(0)
            date_p = datetime.strptime(date_p, "%Y/%m/%d")\
                .strftime("%Y-%m-%d")

    # Récupération de l'auteur de l'article
    author = []
    for div in soup_article.find_all('div'):
        if re.search('author', str(div.get("class"))):
            author.append(div.p.span.get_text())

    # Récupération du thème de l'article
    theme = ""
    for nav in soup_article.find_all('nav'):
        if nav.get("class") == ['breadcrumb']:
            for ol in nav.find_all('ol'):
                for a in ol.find_all('a'):
                    theme = a.get_text()

    # Récupération du contenu de l'article
    content = ""
    for div in soup_article.find_all('div'):
        if re.search('body', str(div.get("id"))):
            for aside in div.find_all('aside'):
                for p in aside.find_all('p'):
                    p.string = ""
            for p in div.find_all('p'):
                for a in p.find_all('a'):
                    if a.get("class") == ['lire']:
                        a.string = ""
                for img in p.find_all('img'):
                    p.string = ""
                content += p.get_text() + " "

    article = utils.recovery_article(title, 'NouvelObservateur',
                                     author, date_p, content, theme)
    return(article)


def recovery_link_new_articles_noob_crawler():
    """
        Retour :
            - liste des url de tous les articles de toutes les catégories
    """
    list_category = ["inondation", "inondations", "typhon", "typhons",
                     "ouragan", "ouragans", "cyclone", "cyclones", "seisme",
                     "seismes", "tremblement+de+terre",
                     "tremblements+de+terre"]

    article_noob = []
    for cat in list_category:
        url = "https://recherche.nouvelobs.com/?referer=nouvelobs&q=" + cat
        soup = utils.recovery_flux_url_rss(url)
        for h2 in soup.find_all('h2'):
            if h2.get("class") == ['title']:
                for a in h2.find_all('a'):
                    if not re.search("\/galeries\-photos\/",
                                     str(a.get("href"))) and not re.search(
                                        "\/cinema\/", str(a.get("href")))\
                                     and not re.search("\/video\/", str(
                                             a.get("href"))) and not re.search(
                                     "\/magazine\/", str(a.get("href")))\
                                     and not re.search("\/qui\-a\-dit\/",
                                                       str(a.get("href"))):
                        if re.search('www', str(a.get("href"))):
                            article_noob.append(a.get("href"))
        for i in range(2, 21):
            url_noob = "http://recherche.nouvelobs.com/?p=" +\
                str(i) + "&q=" + cat
            soup_url = utils.recovery_flux_url_rss(url_noob)
            for h2 in soup_url.find_all('h2'):
                if h2.get("class") == ['title']:
                    for a in h2.find_all('a'):
                        if not re.search("\/galeries\-photos\/", str(a.get(
                                "href"))) and not re.search(
                                "\/cinema\/", str(a.get("href")))\
                                and not re.search("\/video\/", str(
                                        a.get("href"))) and not re.search(
                                         "\/magazine\/", str(a.get("href")))\
                                and not re.search("\/qui\-a\-dit\/",
                                                  str(a.get("href"))):
                            if re.search('www', str(a.get("href"))):
                                article_noob.append(a.get("href"))

    return(article_noob)


def recovery_new_articles_noob_crawler(file_target="data/clean/robot/" +
                                       str(date.datetime.now().date()) + "/"):
    """
            La fonction créée dans un fichier NouvelObs tous les fichiers json.
            Un fichier json contient les informations pour un article.
    """

    file_json = []
    article_noob = recovery_link_new_articles_noob_crawler()

    for article in article_noob:
        new_article = recovery_information_noob(article)
        if new_article["content"] != "":
            file_json.append(new_article)

    utils.create_json(file_target, file_json, "NouvelObs/", "noob")


if __name__ == '__main__':
    file_target = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Semestre 2/" +\
        "Projet_tableau_de_bord/data/clean/robot/" +\
        str(date.datetime.now().date()) + "/"
    recovery_new_articles_noob_crawler(file_target)

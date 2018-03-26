import time
import datetime as date
import re
import utils_v40 as utils


def collect_url_articles():
    """
        Retour :
            - liste d'url des articles en fonction de la categorie choisie
        list_category = ["inondation", "typhon", "ouragan", "cyclone",
                         "seisme", "tremblement+de+terre"]
    """
    list_url_articles = []

    cat = "seisme"
    url = "http://www.lepoint.fr/recherche/index.php?query=" + cat +\
        "&date_from=01%2F01%2F2000&date_to=31%2F01%2F2018&type=ARTICLE"
    soup_url = utils.recovery_flux_url_rss(url)
    for ol in soup_url.find_all('ol'):
        if ol.get("class") == ['pagination', 'bottom']:
            for li in ol.find_all('li'):
                for a in li.find_all('a'):
                    if not a.get("class"):
                        derniere_page = int(li.get_text())
    for article in soup_url.find_all('article'):
            for div in article.find_all('div'):
                if div.get("class") == ['col', 'pls']:
                    for a in div.find_all('a'):
                        debut_url = "http://www.lepoint.fr"
                        if re.search('journalistes',
                                     str(a.get("href"))) is False:
                            list_url_articles.append(debut_url + a.get("href"))

    print(len(list_url_articles))
    for i in range(2, derniere_page):
        time.sleep(61)
        url = "http://www.lepoint.fr/recherche/index.php?query=" + cat +\
            "&date_from=01%2F01%2F2000&date_to=06%2F02%2F2018&type=" +\
            "ARTICLE&page=" + str(i)
        soup_url = utils.recovery_flux_url_rss(url)
        for article in soup_url.find_all('article'):
            for div in article.find_all('div'):
                if div.get("class") == ['col', 'pls']:
                    for a in div.find_all('a'):
                        debut_url = "http://www.lepoint.fr"
                        new_url = debut_url + a.get("href")
                        list_url_articles.append(new_url)
                        if re.search("journalistes", str(a.get("href"))):
                            list_url_articles.remove(new_url)
                        if re.search("frhttp", str(a.get("href"))):
                            list_url_articles.remove(new_url)

    return list_url_articles


def collect_articles():
    """
        Retour :
            - Liste contenant les informations de tous les articles récupérés
    """

    list_url_articles = collect_url_articles()

    list_new_articles = []

    i = 0
    for url_article in list_url_articles:
        i += 1
        if i % 10 == 0:
            time.sleep(61)
        soup = utils.recovery_flux_url_rss(url_article)

        # Récupération du titre de l'article
        for div in soup.find_all('div'):
            if div.get("class") == ["page-title"]:
                title = div.get_text()

        # Récupération de l'auteur de l'article
        list_authors = []
        for span in soup.find_all('span'):
            if span.get("rel") == ["author"]:
                list_authors.append(span.get_text())

        # Récupération de la date de publication de l'article
        date_publi = ""
        for div in soup.find_all('div'):
            if div.get("class") == ['reset-text', 'art-date-infos', 'mts', 'list-view']:
                for balise_time in div.find_all('time'):
                    date = balise_time.get("datetime")
                    date_publi = date[0:10]

        # Récupération du contenu de l'article
        content = ""
        for h2 in soup.find_all('h2'):
            if h2.get('class') == ['art-chapeau']:
                content += h2.get_text()+" "
        for div in soup.find_all('div'):
            if div.get('class') == ['art-text']:
                for p in div.find_all('p'):
                    content += p.get_text()+" "

        new_article = utils.recovery_article(title, 'LePoint',
                                             list_authors,
                                             date_publi, content,
                                             'seisme')
        if not utils.is_empty(new_article):
            list_new_articles.append(new_article)

        return list_new_articles


def recovery_new_articles_lpt(file_target="data/clean/robot/" +
                              str(date.datetime.now().date()) + "/"):
    """
            La fonction créée dans un fichier LePoint tous les fichiers json.
            Un fichier json contient les informations pour un article.
    """

    list_new_articles = collect_articles()

    file_target = "C:/Users/deloe/Desktop/Travail_ecole/M1_SID/Semestre 2/" +\
        "Projet_tableau_de_bord/data/clean/robot/" +\
        str(date.datetime.now().date()) + "/"

    utils.create_json(file_target, list_new_articles, "LePoint/", "lpt")


if __name__ == '__main__':
    file_target = "/data/clean/robot/" + str(date.datetime.now().date()) + "/"
    recovery_new_articles_lpt(file_target)

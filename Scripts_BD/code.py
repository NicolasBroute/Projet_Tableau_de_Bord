###############################################################################
#                               librairies
###############################################################################
import json
import pickle
import unidecode
import csv
import spacy
import re
import datetime
import numpy as np
nlp = spacy.load('fr_core_news_sm')
from sklearn.feature_extraction.text import TfidfVectorizer
###############################################################################
#                                   fonctions
###############################################################################
def clean(contenu):
    contenu = "".join(
            [x if x.isalpha() or x.isnumeric() else " " for x in contenu]) 
    contenu = " ".join(contenu.split())
    return contenu






def KeepNumber(text, ID_numbers, ID_articles, export_numbers):
#    print('------')
#    print(ID_numbers)
#    print(ID_articles)
#    print(export_numbers)
    liste_mot_associe=["mort", "mourir", "deceder", "euro", "dollar",
                       "victime", "deces", "km", "km2" , "km3", "metre", "metres", "Richter"]
    liste = []
    #Trouver les heures
    for val in re.finditer('[0-9]{2}H[0-9]{2}', text):
        liste.append(val.group(0))
        text = text.replace(val.group(0),"")
    #Trouver les dates
    for val in re.finditer('[0-9]{2} [0-9]{2} [0-9]{4}', text):
        date = val.group(0)
        date = date.split(" ")
        date = date[0]+"-"+date[1]+"-"+date[2]
        liste.append(date)
        text = text.replace(val.group(0),"")    
    #Trouver tous les autres nombres
    liste_bis = []
    for val in re.finditer('[0-9]+( [0-9]+)*( mille| million| milliard)?', text):
        liste_bis.append(val.group(0))
 
    liste_propre = []           
    for i in range(0, len(liste_bis)):
        nombre = liste_bis[i]
        #print('\n'+str(nombre))
        if re.search("[0-9]+( [0-9]+)* [0-9]+", nombre) or re.search("[0-9]*", nombre):
            nombre = nombre.replace(" ", "")
        else:
            nombre = nombre.replace(" ", ".")

        if re.search("mille", nombre):
            if re.search("\.",nombre):
                nombre = nombre.replace("mille", "1000")
                sep = nombre.split(".")
                premier_nombre = sep[0] +"."+ sep[1]
                deuxieme_nombre = sep[2]
                nombre = str(float(premier_nombre)*float(deuxieme_nombre))
                nombre = nombre[:-2]
            else:
                nombre = nombre.replace("mille", ".1000")
                sep = nombre.split(".")
                nombre = str(int(sep[0])*int(sep[1]))

        if re.search("million", nombre):
            #print('-------million')
            #print(nombre)
            if re.search("\.",nombre):
                #print('a')
                nombre = nombre.replace("million", "1000000")
                sep = nombre.split(".")
                #print(sep)
                premier_nombre = sep[0] +"."+ sep[1]
                deuxieme_nombre = sep[2]
                nombre = str(float(premier_nombre)*float(deuxieme_nombre))
                nombre = nombre[:-2]
            else:
                #print('b')
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
            if re.search(nb + "( [a-z]*){0,4}"+' ' + mot+ ' ' , text):
                export_numbers.append([ID_articles,int(text.split().index(mot))+1,ID_numbers,nb,mot])
                ID_numbers+=1
                ligne_liste.append(mot)
        if ligne_liste not in liste_nb_mot_associe:
            liste_nb_mot_associe.append(ligne_liste)
#    if len(liste_propre) != 0:
    return ID_numbers
#    
    
    


def Extract_alpha(type_file,file,all_,list_word,details_word,ID_numbers,ID_articles,export_numbers):
    
    text = " ".join(file)

    for i in text.split(): #prend en compte les majucule pour le premier mot de la phrase
        if i[0].isupper():
            if str(i.lower())!=str(([token.lemma_ for token in nlp(i.lower())])[0]) and str(([token.ent_type_ for token in nlp(i)])[0])=='':
                text=text.replace(i,str(([token.lemma_ for token in nlp(i.lower())])[0]),1)
    text = nlp(text)
    text_str=str(text)

    for token in text:
        if str(token).isalpha(): # and token.ent_type_!='MISC':
            if token.lemma_ not in list_word:
                if token.lemma_.lower() not in (" ".join(list_word)).lower():
                    list_word.append(token.lemma_)
                    type_=token.ent_type_
                    if type_=='' or type_=='MISC':
                        type_='NULL'
                        
                    details_word.append([token.lemma_,type_,token.dep_])
                    
                if token.lemma_.lower() in ((" ".join(list_word)).lower()).split() and token.lemma_[0].upper()==token.lemma_[0] :
#                    print(token.lemma_)
#                    print(token.lemma_.lower())
#                    print(list_word)
                    if token.lemma_ in list_word:
                        list_word[list_word.index(token.lemma_)]=token.lemma_                 
                        details_word[list(np.array(details_word)[:,0]).index((token.lemma_))]=([token.lemma_,token.ent_type_,token.dep_])

            text_str=text_str.replace(token.text, token.lemma_)
            text_str=text_str.replace('rr','r')
            text_str=text_str.replace('  ',' ')
    ID_numbers=KeepNumber(text_str,ID_numbers,ID_articles,export_numbers)
    all_.append(text_str)
    return ID_numbers




#details_word=[['Essone', 'LOC', 'nsubj']]
#list(np.array(details_word)[:,0]).index(('Essone'))

#text='Inondations alpha inondation Noémie Ber'
#text_lower='inondations alpha inondation Noémie Ber'
#text_nlp=nlp(text)
#text_lower_nlp=nlp(text_lower)
#
#for i in text.split():
#    if i[0].isupper():
#        if str(i.lower())!=str(([token.lemma_ for token in nlp(i.lower())])[0]):
#            print(i)
#            print(str(([token.lemma_ for token in nlp(i.lower())])[0]))
#            text=text.replace(i,str(([token.lemma_ for token in nlp(i.lower())])[0]),1)

################################################################################
###########################   initialisation   #################################
################################################################################
stop_words = pickle.load(open('/home/formationsid/Bureau/Catastrophes_Naturelles/stopwords.p', 'rb'))
for i in range(0, len(stop_words)):
    stop_words[i] = unidecode.unidecode(clean(stop_words[i]))


link='/home/formationsid/Bureau/Catastrophes_Naturelles/data/'
daily_name=['LePoint','NouvelObs','Liberation','LeMonde','Figaro']
daily_number=[3969,1741,362,2245,3218] #total=11535
before_nb=['art_lpt_','art_noob_','art_lb_','art_lm_','art_lf_']
after_nb=['_2018-03-05_robot.json','_2018-01-31_robot.json','_2018-03-07_robot.json','_2018-03-07_robot.json','_2018-03-07_robot.json']

all_doc=[]
all_title=[]
list_word=[]
details_word=[]

export_articles=[]
export_contents=[]
export_titles=[]
export_numbers=[]
export_words=[]

ID_numbers=1
ID_articles=1
ID_contents=1
ID_titles=1
ID_words=1



################################################################################
############################   Nettoyage     ###################################
################################################################################
debut=datetime.datetime.now()
for j in range(0,1):#len(daily_name)):
    for i in range(1,daily_number[j]+1): 
        if i % 100 ==0:
            print(i)

        file=open(link+daily_name[j]+'/'+before_nb[j]+str(i)+after_nb[j])
        file = json.load(file)
        
        #BD - Articles
        date=file["date_publi"]
        y=date[0:4]
        m=date[5:7]
        d=date[8:10]
        date="'"+y+'-'+d+'-'+m+"'"
        export_articles.append([ID_articles,str(file["newspaper"]),str(" ".join(file["author"])),str(date),str(file["theme"])])
        ID_articles+=1
        
        file["content"] = clean(file["content"])
        file["content"] = file["content"].split()
        file["title"] = clean(file["title"])
        file["title"] = file["title"].split()
        for k in range(0, len(stop_words)):
            while stop_words[k] in file["content"]:
                file["content"].remove(stop_words[k])
            while stop_words[k] in file["title"]:
                file["title"].remove(stop_words[k])
        #print(file["title"])
        ID_numbers=Extract_alpha('content',file["content"],all_doc,list_word,details_word,ID_numbers,i,export_numbers)
        ID_numbers=Extract_alpha('title',file["title"],all_title,list_word,details_word,ID_numbers,i,export_numbers)
        #print('-----' +str(ID_numbers))







print('tf_idf en cours...')
vec_content=TfidfVectorizer()#max_df=1, min_df=1,max_features=None)
tfidf_content = vec_content.fit_transform(all_doc)
tfidf_content = tfidf_content.toarray()
vec_title=TfidfVectorizer()#(max_df=1, min_df=1,max_features=100)
tfidf_title = vec_title.fit_transform(all_title)
tfidf_title=tfidf_title.toarray()

#(vec_title.fit_transform(['aa bb ','aa'])).toarray()
#(vec_title.fit_transform(['facturer precise inondation', 'inondation difficile retour normal'])).toarray()


#np.shape(tfidf_title)
a=list(vec_content.vocabulary_.keys())
b=list(vec_title.vocabulary_.keys())
a.extend(b)

vec_title.vocabulary_.values()
word = list(set(a))
print('Export word en cours...')
for i in range(0,len(word)):
    for j in range(0,len(details_word)):
        if word[i].lower()==details_word[j][0].lower() and word[i].isalpha():
           export_words.append([ID_words,str(details_word[j][0]),details_word[j][1],details_word[j][2]])#bug car maj => voir "ministre"
           ID_words+=1
              

print('Export title en cours...')
for i in all_title:
    for word in [export_words[x][1] for x in range(0,len(export_words))]:
        if word in i.split():
            pos_=(i.split()).index(word)+1
            tfidf_=tfidf_title[all_title.index(i)][list(vec_title.vocabulary_.values())[list(vec_title.vocabulary_.keys()).index(word.lower())]]
            id_word=[export_words[x][1] for x in range(0,len(export_words))].index(word)+1
            export_titles.append([ID_titles,pos_,tfidf_,all_title.index(i)+1,id_word,'NULL'])
            #print([ID_titles,pos_,tfidf_,all_title.index(i)+1,id_word,'NULL'])

    for number in [export_numbers[x][3] for x in range(0,len(export_numbers))]:
        if number in i.split():  
            export_titles.append([ID_titles,(i.split()).index(number)+1,'Null',all_title.index(i)+1,'NULL',(list(np.array(export_numbers)[:,3]).index(number))+1])
            #print([ID_titles,(i.split()).index(number)+1,'Null',all_title.index(i)+1,'NULL',(list(np.array(export_numbers)[:,3]).index(number))+1])

    ID_titles+=1

#tfidf_title[0][list(vec_title.vocabulary_.keys()).index('precise')]
print('Export content en cours...')
for i in all_doc:
    for word in [export_words[x][1] for x in range(0,len(export_words))]:
        if word in i.split():
            pos_=(i.split()).index(word)+1
            tfidf_=tfidf_content[all_doc.index(i)][list(vec_content.vocabulary_.values())[list(vec_content.vocabulary_.keys()).index(word.lower())]]
            id_word=[export_words[x][1] for x in range(0,len(export_words))].index(word)+1                #################################
            export_contents.append([ID_contents,pos_,tfidf_,all_doc.index(i)+1,id_word,'NULL'])
            #print([ID_contents,pos_,tfidf_,all_doc.index(i)+1,id_word,'NULL'])

    for number in [export_numbers[x][3] for x in range(0,len(export_numbers))]:
        if number in i.split():  
            export_contents.append([ID_contents,(i.split()).index(number)+1,'Null',all_doc.index(i)+1,'NULL',(list(np.array(export_numbers)[:,3]).index(number))+1])
            #print([ID_contents,(i.split()).index(number)+1,'Null',all_doc.index(i)+1,'NULL',(list(np.array(export_numbers)[:,3]).index(number))+1])

    ID_titles+=1                  
print('Export number en cours...')
for i in np.array(export_words)[:,1]:
    for j in np.array(export_numbers)[:,4]:
        if i==j:
            export_numbers[list(np.array(export_numbers)[:,4]).index(j)][4]=list(np.array(export_words)[:,1]).index(i)+1
        

################################################################################
############################     Export      ###################################
################################################################################


with open('/home/formationsid/Bureau/Catastrophes_Naturelles/BD/LP_articles.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(["Id_Article","journal","auteur","date_article","theme"])
    writer.writerows(export_articles)

with open('/home/formationsid/Bureau/Catastrophes_Naturelles/BD/LP_mots.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(["Id_mot","mot","type_mot","entite"])
    writer.writerows(export_words)

with open('/home/formationsid/Bureau/Catastrophes_Naturelles/BD/LP_nombres.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(["Id_nombre","nombre","id_mot"])
    writer.writerows(np.array(export_numbers)[:,2:5])

with open('/home/formationsid/Bureau/Catastrophes_Naturelles/BD/LP_titres.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(["Id_titre","position_mot","score_tf_idf","id_article","id_mot","id_number"])
    writer.writerows(export_titles)

with open('/home/formationsid/Bureau/Catastrophes_Naturelles/BD/LP_contenu_mots_cles.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    #writer.writerow(["id_contenu","position_mot","score_tf_idf","id_article","id_mot","id_number"])
    writer.writerows(export_contents)

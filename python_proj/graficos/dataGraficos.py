import sqlite_db.bdsql as bd
import pesquisa_whoosh.pesquisa_whoosh as pq
import html_parser.bsoup as bsoup
import pesquisa_whoosh.findPers as findEntities
import sentiment.sentiment as sentilex
import graficos.saveLoadEstado as saveLoad
import feedparser
from collections import namedtuple

import os
import os.path

#//Funcao faz print dos politicos e a sua positividade no dia (numero de notcias positivas em que e referenciado) || Este print e feito apenas uma vez por dia 

def savePosPolitico(positividade, data):
    fname ='PositividadePoliticos' + '__' + data + '.txt'
    
    #if os.path.isfile(fname):
        #print "O ficheiro ja existe"
    #else:
    f = open(fname, 'w+')
   
    for key in positividade:
        f.write("%s:%s\n" % (key, positividade[key]))
    
#savePosPolitico()    

#//Esta funcao faz print de um ficheiro com o numero de referencias de cada politico || Este print e feito uma vez por dia 

def politicosMaisFalados (nRefPoliticos, data):
    fname = 'PoliticosMaisFalados' + '__' + data + '.txt'
      
    
    #fname = 'PoliticosMaisFalados.txt'
    #if os.path.isfile(fname):
        #print "O ficheiro ja existe"
    #else:
    f = open(fname, 'w+')
        
    for key in nRefPoliticos:
        f.write("%s:%d\n" % (key, nRefPoliticos[key]))
            

def saveDataGraficos(noticiasAnalisar ,data, queryCurs):
    fname1 = 'PoliticosMaisFaladosDia' + '__' + data + '.txt'
    fname2 = 'PositividadePoliticosDia' + '__' + data + '.txt'
    
    positividade = dict()
    
    personalidadesRank1, personalidadesRank2 = findEntities.initPers()
        
    entitiesInNoticia = findEntities.findPersInNot(queryCurs, personalidadesRank1, noticiasAnalisar)
    
    sentimentNoticias = sentilex.NoticiasSentiment(noticiasAnalisar)
    
    nRefpoliticos = findEntities.numeroReferenciasPolitico(entitiesInNoticia)
    
    
    for key in entitiesInNoticia:
        for politico in entitiesInNoticia[key]:
            if politico in positividade:
                positividade[politico] = positividade[politico] + sentimentNoticias[key]
            else:
                positividade[politico] =  sentimentNoticias[key]
                
                
    f = open(fname2, 'w+')
   
    for key in positividade:
        f.write("%s:%s\n" % (key, positividade[key]))
        
        
    f = open(fname1, 'w+')
        
    for key in nRefPoliticos:
        f.write("%s:%d\n" % (key, nRefPoliticos[key]))
                
    
                
    
    
    
 #// Guarda a positividade das noticias| numero de noticias positivas, neutras e negativas || este print e feito uma vez por dia 
 
def positividadeDoDia(sentimentNoticias, data):
    positivas = 0
    neutras = 0
    negativas = 0  
    
    fname = 'PosividadeDoDia' + '__' + data + '.txt'
    #fname = 'PosividadeDoDia.txt'
    if os.path.isfile(fname):
        print "O ficheiro ja existe"
    else:
        f = open(fname, 'a+')
        for id in sentimentNoticias:
            if sentimentNoticias[id] > 0:
                positivas +=1
            elif sentimentNoticias[id] < 0:
                negativas +=1
            else: 
                neutras +=1
                

        f.write("%s:%d\n%s:%d\n%s:%d\n" % ('positivas', positivas,'neutras', neutras, 'negativas', negativas))
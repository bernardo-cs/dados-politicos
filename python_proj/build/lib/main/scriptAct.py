import sqlite_db.bdsql as bd
import pesquisa_whoosh.pesquisa_whoosh as pq
import html_parser.bsoup as bsoup
import pesquisa_whoosh.findPers as findEntities
import sentiment.sentiment as sentilex
import graficos.dataGraficos as saveData
import graficos.saveLoadEstado as saveLoad
import feedparser
from collections import namedtuple
import sys
import os

print 'Iniciei'
urlsFeeds = ['http://feeds.dn.pt/DN-Politica','http://feeds.jn.pt/JN-Politica']
#Fazer os loads

print 'inicia load'
#entitiesInNoticia =  saveLoad.loadPoliticosInNoticias()
#sentimentNoticias = saveLoad.loadSentimentNoticias()
#positividade = saveLoad.loadPositividadePolitico()
print 'fim load'
entitiesInNoticia =  dict()
sentimentNoticias = dict()
positividade = dict()

#Adicionar ultimas noticias dos feeds

print 'inicia put bd'
for url in urlsFeeds:

    feed = feedparser.parse(url)
        
    #print(feed[ "channel" ][ "link" ])
    #print(feed[ "channel" ][ "title" ])
    data = (feed[ "channel" ][ "date" ])
    
    createDb, queryCurs = bd.criaDb()
        
    bd.createTable(queryCurs)
    
    for entrie in feed.entries:
        summary, noticia = bsoup.getNoticia(entrie.link)
        bd.addNoticia(entrie.title, entrie.description, entrie.link, summary, noticia, queryCurs)
            
    bd.commitDb(createDb)

print 'fim putbd'


#get id ultima noticia analisada
ultimaNoticia = saveLoad.getIdUltimaNoticia(sentimentNoticias)

#noticias = bd.getUltimasNoticias(queryCurs, 1)
#print 'noticias'
#print noticias
print 'ultima noticia'
print ultimaNoticia

#vai buscar todas as noticias ainda nao analisadas
noticiasAnalisar = bd.getUltimasNoticias(queryCurs, ultimaNoticia)
print noticiasAnalisar

noticiasAnalisar = bd.getUltimasNoticias(queryCurs, 0) # teste

if noticiasAnalisar:
    
    
    
    #Faz load do ficheiro com as personalidades
    personalidadesRank1, personalidadesRank2 = findEntities.initPers()
        
    entitiesInNoticia = findEntities.findPersInNot(queryCurs, personalidadesRank1, noticiasAnalisar)
    print entitiesInNoticia
    
    
    sentimentNoticias = sentilex.NoticiasSentiment(noticiasAnalisar)
    print '---------sentimentNoticias---------'
    print sentimentNoticias
    
    
    #Positividade
    
        
    for key in entitiesInNoticia:
        for politico in entitiesInNoticia[key]:
            if politico in positividade:
                positividade[politico] = positividade[politico] + sentimentNoticias[key]
            else:
                positividade[politico] =  sentimentNoticias[key]
    
    print '---positividade---'            
    print positividade


    #Falta save data
    
    splitdata = list()
    data = data.encode('utf-8')
    splitdata = data.split()
    realData = splitdata[1] + splitdata[2] + splitdata[3]
    
    #POSITIVIDADE POLITICOS
    print 'iniciar save data'
    saveData.savePosPolitico(positividade, realData)
    
    
    #-----------guarda dados politico mais falado----
        
    nRefpolitico = findEntities.numeroReferenciasPolitico(entitiesInNoticia)
    saveData.politicosMaisFalados(nRefpolitico, realData)
    
    #------- guarda posivitividade das noticias
    saveData.positividadeDoDia(sentimentNoticias ,realData)
    
    
    
    saveLoad.savePoliticosInNoticias(entitiesInNoticia)
    saveLoad.saveSentimentNoticias(sentimentNoticias)
    saveLoad.savePositividadePolitico(positividade)
    
bd.closeDb(queryCurs)
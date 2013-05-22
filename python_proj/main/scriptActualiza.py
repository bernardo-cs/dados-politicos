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


urlsFeeds = ['http://feeds.dn.pt/DN-Politica','http://feeds.jn.pt/JN-Politica']
#Fazer os loads

print 'Inicia load dict'
entitiesInNoticia =  saveLoad.loadPoliticosInNoticias()
sentimentNoticias = saveLoad.loadSentimentNoticias()
positividade = saveLoad.loadPositividadePolitico()

print 'entidades em noticias'
print entitiesInNoticia
print 'sentimentos em noticias'
print sentimentNoticias
print 'positividade'
print positividade

#entitiesInNoticia = dict()
#sentimentNoticias = dict()
#positividade = dict()

#Adicionar ultimas noticias dos feeds

print 'Verifica se ha novas noticias e coloca na db'
for url in urlsFeeds:

    feed = feedparser.parse(url)
        
    #print(feed[ "channel" ][ "link" ])
    #print(feed[ "channel" ][ "title" ])
    data = (feed[ "channel" ][ "date" ])
    
    
    splitdata = list()
    data = data.encode('utf-8')
    splitdata = data.split()
    realData = splitdata[1] + splitdata[2] + splitdata[3]
    
    createDb, queryCurs = bd.criaDb()
        
    bd.createTable(queryCurs)
    
    for entrie in feed.entries:
        summary, noticia = bsoup.getNoticia(entrie.link)
        bd.addNoticia(entrie.title, entrie.description, entrie.link, summary, noticia, realData, queryCurs)
            
    bd.commitDb(createDb)



#get id ultima noticia analisada
ultimaNoticia = saveLoad.getIdUltimaNoticia(sentimentNoticias)



#vai buscar todas as noticias ainda nao analisadas
noticiasAnalisar = bd.getUltimasNoticias(queryCurs, ultimaNoticia)


if noticiasAnalisar:
    print 'a novas noticias, comeca a analise'
    
    
    #Faz load do ficheiro com as personalidades
    personalidadesRank1, personalidadesRank2 = findEntities.initPers()
        
    entitiesInNoticia_aux = findEntities.findPersInNot(queryCurs, personalidadesRank1, noticiasAnalisar)
    
    for key in entitiesInNoticia_aux:
        entitiesInNoticia[key] = entitiesInNoticia_aux[key]
            
    
    sentimentNoticias_aux = sentilex.NoticiasSentiment(noticiasAnalisar)
    
    for key in sentimentNoticias_aux:
        sentimentNoticias[key] = sentimentNoticias_aux[key]

    
    
    #Positividade
    
        
    for key in entitiesInNoticia:
        for politico in entitiesInNoticia[key]:
            if politico in positividade:
                positividade[politico] = positividade[politico] + sentimentNoticias[key]
            else:
                positividade[politico] =  sentimentNoticias[key]
    



    #Falta save data
    
   
    
    print 'Actualiza ficheiros para graficos'
    #POSITIVIDADE POLITICOS
    saveData.savePosPolitico(positividade, realData)
    
    
    #-----------guarda dados politico mais falado----
        
    nRefpolitico = findEntities.numeroReferenciasPolitico(entitiesInNoticia)
    print 'politicos mais falados'
    print nRefpolitico
    saveData.politicosMaisFalados(nRefpolitico, realData)
    
    #------- guarda posivitividade das noticias
    saveData.positividadeDoDia(sentimentNoticias ,realData)
    

    
    
    print 'salva o estado'
    saveLoad.savePoliticosInNoticias(entitiesInNoticia)
    saveLoad.saveSentimentNoticias(sentimentNoticias)
    saveLoad.savePositividadePolitico(positividade)
    
else:
    print 'nao ha noticias novas'
    #bd.closeDb(queryCurs)
    
#------------------
    
fname1 = 'PoliticosMaisFaladosDia' + '__' + realData + '.txt'
    
fname2 = 'PositividadePoliticosDia' + '__' + realData + '.txt'
    
if os.path.isfile(fname1) and os.path.isfile(fname2):
    print "O ficheiro ja existe"
else:
    noticiasDia = bd.getNoticiasDoDias(queryCurs, realData)
    saveData.saveDataGraficos(noticiasDia ,realData, queryCurs)
    
bd.closeDb(queryCurs)
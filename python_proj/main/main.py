import sqlite_db.bdsql as bd
import pesquisa_whoosh.pesquisa_whoosh as pq
import html_parser.bsoup as bsoup
import pesquisa_whoosh.findPers as findEntities
import sentiment.sentiment as sentilex
import graficos.dataGraficos as saveData
import graficos.saveLoadEstado as saveLoad
#import xml_parser as feedp
import feedparser
from collections import namedtuple
import sys
import os




#x = raw_input('What is your name? /n mariaasdasda')

print "BEM VINDO"
print "Escolha uma opcao"
print "1 - Dados das noticias "
print "2 - Positividade de dois politicos"
print "3 - Pesquisa"
x = raw_input()
print "loading BD"
db_filename = 'exemplo.db'
db_is_new = not os.path.exists(db_filename)

print 'EXISTE DB?'
print db_is_new

if db_is_new:
    print 'Need to create schema'
    #createDb, queryCurs = bd.criaDb()
else:
    print 'Database exists, assume schema does, too.'

urlsFeeds = ['http://feeds.dn.pt/DN-Politica','http://feeds.jn.pt/JN-Politica']
#Insere os varios feeds na BD
for url in urlsFeeds:
    
    #feedp.feedBd(url)
    
    feed = feedparser.parse(url)
        
    print(feed[ "channel" ][ "link" ])
    print(feed[ "channel" ][ "title" ])
    data = (feed[ "channel" ][ "date" ])
    
    createDb, queryCurs = bd.criaDb()
        
    bd.createTable(queryCurs)
    
    for entrie in feed.entries:
        summary, noticia = bsoup.getNoticia(entrie.link)
        bd.addNoticia(entrie.title, entrie.description, entrie.link, summary, noticia, queryCurs)
            
    bd.commitDb(createDb)

#Verifica o input do utilizador
if x == '3':
    
    #Indexacao do Whoosh
    pq.indexer(queryCurs)
    
    
    #------------PROCURA COM WHOOSH-----------
    input = raw_input("Introduza a pesquisa: ")
    
    print pq.procura(input)
    
elif x == '2' or x == '1':
    
    print "PASSEI AQUI"
    #------------------- PROCURA POLITICOS EM NOTICIAS ---------------- 
    descricaoAll = bd.getDescricao(queryCurs)
    
    #print descricaoAll 
    
    personalidadesRank1, personalidadesRank2 = findEntities.initPers()
    
    entitiesInNoticia = findEntities.findPersInNot(queryCurs, personalidadesRank1, descricaoAll)
    
    
    print entitiesInNoticia
    #-------------teste save enteties------------
    print 'antes de iniciar save estado'
    saveLoad.savePoliticosInNoticias(entitiesInNoticia)
    #print 'load args'
    #entitiesInNoticia =  saveLoad.loadPoliticosInNoticias()
    
   
    #---------------------SENTIMENTOS NOTICIA------------------------  

    

    sentimentNoticias = sentilex.NoticiasSentiment(descricaoAll)
    
    print "-------------Sentimentos em noticia------------"
    print sentimentNoticias
    
    #----------------------------------------------- TESTE LOAD SAVE SENTIMENT
    print 'Salva estado dos sentimentos'
    saveLoad.saveSentimentNoticias(sentimentNoticias)
    #print 'load estado dos sentimentos'
    #sentimentNoticias = saveLoad.loadSentimentNoticias()
    #print sentimentNoticias
    
    #teste get id ultima noticia
    ultimaNoticia = saveLoad.getIdUltimaNoticia(sentimentNoticias)
    print 'ultima noticia'
    print ultimaNoticia
    print 'fim ultima noticia'
    
    
    #-------------Politicos amigos----
    
    if x == '2':
        print "PASSEI AQUI !!!!!!!!!!!!!!!!"
        pol1 = raw_input("Introduza o nome do primeiro politico:")
        pol2 = raw_input("Introduza o nome do segundo politico:")
        
               
        
        print findEntities.PosiXPoliticos (sentimentNoticias, entitiesInNoticia, pol1, pol2)
    
    #if x == 1: 
        
            
        
        
    #print entrie.description
    
    #createDb, queryCurs = bd.criaDb()
    
    #bd.createTable(queryCurs)
    
    #for entrie in feed.entries:
        #bd.addNoticia(entrie.title, entrie.description, entrie.link, queryCurs)
        
        
    #bd.commitDb(createDb)
    
    
    
    
    
    
    
    #----Positividade politicos----------
    
    
    #POSITIVIDADE
    
    positividade = dict()
    
    for key in entitiesInNoticia:
        for politico in entitiesInNoticia[key]:
            if politico in positividade:
                positividade[politico] = positividade[politico] + sentimentNoticias[key]
            else:
                positividade[politico] =  sentimentNoticias[key]
                
    #Procura positividade dois politicos ----politicos amigos
    #PosiXPoliticos (sentimentNoticias, entitiesInNoticia, pol1 pol2)
    
    
    print "---------POSITIVIDADE---------------"
    print positividade
            
    #----- TESTE GUARDA ESTADO POSITIVIDADE-------
    print 'Guarda estado positividade'
    saveLoad.savePositividadePolitico(positividade)
    print 'Load estado positividade'
    
    posi = saveLoad.loadPositividadePolitico()
    print posi
    

    
    #------------------------GUARDAR DADOS ---------------------
    
    
    #Limpa data
    splitdata = list()
    data = data.encode('utf-8')
    splitdata = data.split()
    realData = splitdata[1] + splitdata[2] + splitdata[3]
    print "real data"
    print realData
    #POSITIVIDADE POLITICOS
    saveData.savePosPolitico(positividade, realData)
    
    
    #-----------guarda dados politico mais falado----
    
    nRefpolitico = findEntities.numeroReferenciasPolitico(entitiesInNoticia)
    saveData.politicosMaisFalados(nRefpolitico, realData)

    ##------- guarda posivitividade das noticias
    #saveData.positividadeDoDia(sentimentNoticias ,realData)
    
    #--------------TESTE GET NOTICIAS----------------
    #print bd.getAllNoticia(queryCurs)
    
    #----------Teste get ultimas noticias
    #ultimoId = 47
    #print 'ultimas noticias'
    #print bd.getUltimasNoticias(queryCurs, ultimoId)
    
    
#close Db

bd.closeDb(queryCurs)
    
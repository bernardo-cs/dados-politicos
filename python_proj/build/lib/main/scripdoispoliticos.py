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



pol1 = sys.argv[1]
pol2 = sys.argv[2]



politicoaux1 = pol1.split('_')
politicoaux2 = pol2.split('_')


politico1 = ''
for k, nome in enumerate(politicoaux1):
     if k == 0:
          politico1 = nome
     else:
          politico1 =  politico1 +' '+ nome

          
politico2 = ''
for k, nome in enumerate(politicoaux2):
     if k == 0:
          politico2 = nome
     else:
          politico2 =  politico2 +' '+ nome          
    
    
entitiesInNoticia =  saveLoad.loadPoliticosInNoticias()
sentimentNoticias = saveLoad.loadSentimentNoticias()

print politico1
print politico2
print findEntities.PosiXPoliticos (sentimentNoticias, entitiesInNoticia, politico1, politico2)
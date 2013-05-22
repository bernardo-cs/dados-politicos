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


pol = str(sys.argv[1]) #+ ' ' +'Portas'
nomespolitico = pol.split('_')


politico = ''
for k, nome in enumerate(nomespolitico):
     if k == 0:
          politico = nome
     else:
          politico =  politico +' '+ nome

entitiesInNoticia =  saveLoad.loadPoliticosInNoticias()

nRefpolitico = findEntities.numeroReferenciasPolitico(entitiesInNoticia)

#print nRefpolitico
try:
     print nRefpolitico[politico]
except:
     print 'Este politico nao e referenciado em noticias'
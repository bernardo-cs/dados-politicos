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


pesquisaaux = str(sys.argv[1])
pesquisasplit = pesquisaaux.split('_')

input = ''
for k, palavra in enumerate(pesquisasplit):
     if k == 0:
          input = palavra
     else:
          input =  input +' '+ palavra
          
print input
          
createDb, queryCurs = bd.criaDb()

pq.indexer(queryCurs)

listid = pq.procura(input)

for id in listid:
     for link in bd.getLink(queryCurs, int(id)):
          print link[0].encode('utf-8')
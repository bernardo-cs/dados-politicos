import feedparser
import sqlite_db.bdsql as bd

#d = feedparser.parse('http://feedparser.org/docs/examples/atom10.xml')
#d['feed']['title']

python_wiki_rss_url = 'http://feeds.dn.pt/DN-Politica'

#f = open('noticias','w')

feed = feedparser.parse(python_wiki_rss_url)

print(feed[ "channel" ][ "link" ])
print(feed[ "channel" ][ "title" ] )
#print(feed.entries[0].title)
#print(feed.entries[0].link)
#print(feed.entries[0].description)

#f.write(title.encode('utf-8')) --------------- 
#f.write(feed.entries[0].title)
#f.write(feed.entries[0].link)
#f.write(feed.entries[0].description)

#f.close()

createDb, queryCurs = bd.criaDb()

bd.createTable(queryCurs)

for entrie in feed.entries:
    bd.addNoticia(entrie.title, entrie.description, entrie.link, queryCurs)
    
bd.commitDb(createDb)
print('------------Print DB----------')
bd.printDb(queryCurs)
    


    

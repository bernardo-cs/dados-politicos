import sqlite3

def criaDb():
    createDb = sqlite3.connect('exemplo.db') #Passar para estatica
    queryCurs = createDb.cursor()
    
    return createDb, queryCurs

#def connectDb():
    #queryCurs = sqlite3.connect(db_filename)
    #return createDb, queryCurs

def createTable(queryCurs):
    queryCurs.execute('''CREATE TABLE IF NOT EXISTS noticias
    (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT UNIQUE, descricao TEXT UNIQUE, link TEXT UNIQUE, summary TEXT UNIQUE, noticia TEXT UNIQUE, data TEXT)''')
    
def addNoticia(titulo, descricao, link, summary, noticia, data, queryCurs): #INSERT OR IGNORE
    queryCurs.execute('''INSERT OR IGNORE INTO noticias(titulo, descricao, link, summary, noticia, data)
    VALUES (?,?,?,?,?,?)''', (titulo, descricao, link, summary, noticia, data))

def commitDb(createDb):
    createDb.commit()

def printDb(queryCurs):
    
    queryCurs.execute('SELECT * FROM noticias')
    for i in queryCurs:
        print "\n"
        for j in i:
            print j
    queryCurs.close()
    
    
def getDescricao(queryCurs):
    queryCurs.execute('SELECT * FROM noticias')
    return queryCurs.fetchall()

def getUltimasNoticias(queryCurs, ultimoId):
    teste = (ultimoId,)
    
    queryCurs.execute('SELECT id, summary ,noticia FROM noticias WHERE id > ? ', teste)
    return queryCurs.fetchall()
    
def getLink(queryCurs, id):
    teste = (id,)
    
    queryCurs.execute('SELECT link FROM noticias WHERE id = ? ', teste)
    return queryCurs.fetchall()

def getNoticiasDoDias(queryCurs, realdata):
    teste = (realdata,)
    
    queryCurs.execute('SELECT id, summary, noticia FROM noticias WHERE data = ? ', teste)
    return queryCurs.fetchall()

def getAllNoticia(queryCurs):
    queryCurs.execute('SELECT noticia FROM noticias')
    return queryCurs.fetchall()

def closeDb (queryCurs):
    queryCurs.close()
    
    
   
    
#def main():
    #createTable()
    
    #addNoticia()
    
    #createDb.commit()
    
    #queryCurs.execute('SELECT * FROM noticias')
    #for i in queryCurs:
        #print "\n"
        #for j in i:
            #print j 

    
    
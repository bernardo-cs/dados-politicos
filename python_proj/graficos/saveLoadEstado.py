import os
import os.path

def savePoliticosInNoticias(entitiesInNoticia):
    fname ='estadoPolitcosInNoticias.txt'
    print 'a iniciar save estado' 
    #if os.path.isfile(fname):
        #print "O ficheiro ja existe"
    #else:
    f = open(fname, 'w+')
       
    for id in entitiesInNoticia:
        f.write("%s:" % (id))
        for politico in entitiesInNoticia[id]:
            if politico == entitiesInNoticia[id][-1]:
                #print 'remove n'
                #print type(politico)
                #print 'antes de remove'
                #politico = politico.replace('\n', '')
                #print politico
                #print 'antes 2 remove'
                #politico = politico.rstrip('\n')
                #print politico
                #print 'antes 3 remove'
                #politico = politico.strip()
                #print politico
                f.write("%s" % (politico))
            else:
                f.write("%s," % (politico))
            
        f.write("\n")
        
        
def loadPoliticosInNoticias():
    fname ='estadoPolitcosInNoticias.txt'
    entitiesInNoticia = dict()    
    
    f = open(fname, 'r+')
    
    for line in f:
        linha = line.split(':')
        politicos = linha[1].split(',')
        politicos[-1] = politicos[-1].strip()
        entitiesInNoticia[linha[0]] = politicos
    #print 'Teste Load'
    
    return entitiesInNoticia
        

def saveSentimentNoticias(sentimentNoticias):
    fname ='estadoSentimentNoticias.txt'
    f = open(fname, 'w+')
       
    for id in sentimentNoticias:
        f.write("%d:" % (id))
        f.write("%d\n" % (sentimentNoticias[id]))
        
        
        
def loadSentimentNoticias():
    fname ='estadoSentimentNoticias.txt'
    
    sentimentNoticias = dict()
    
    f = open(fname, 'r+')
    
    for line in f:
        linha = line.split(':')
        sentimentNoticias[int(linha[0])] = int(linha[1].strip())
        
    return sentimentNoticias


def savePositividadePolitico(positividade):
    fname ='estadoPositividadePoliticos.txt'
    f = open(fname, 'w+')
       
    for id in positividade:
        f.write("%s:" % (id))
        f.write("%d\n" % (positividade[id]))
      
        
        
def loadPositividadePolitico():
    fname ='estadoPositividadePoliticos.txt'
    
    positividade = dict()
    
    f = open(fname, 'r+')
    
    for line in f:
        linha = line.split(':')
        positividade[linha[0]] = int(linha[1].strip())
        
    return positividade


def getIdUltimaNoticia(sentimentNoticias):
    
    id_aux = 0
    for id in sentimentNoticias:
        if id > id_aux:
            id_aux = id
        else:
            continue
        
    return id_aux
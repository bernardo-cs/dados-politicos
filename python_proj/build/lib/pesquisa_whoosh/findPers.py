import re
from sets import Set
import sqlite_db.bdsql as bd


def isodd(num):
    return num & 1 and True or False


def initPers():
    f = open('personalities.txt', 'r')
    
    personalidadesRank1 = list()
    personalidadesRank2 = list()
    
    for line in f:
        for k ,name in enumerate(line.split('"')):
                if k > 2 and isodd(k):
                    personalidadesRank1.append(name)
                    for n in name.split():
                        personalidadesRank2.append(n)
                        
                        
    return personalidadesRank1, personalidadesRank2




def findPersInNot(queryCurs, personalidadesRank1, descricaoAll):
    
    politicos_in =  dict()
    politicos_in_noticia_rank1 = list()
    

    for line in descricaoAll:
        #Se quiser ID line[0]
        key = line[0]
        print key
        print "-------------------DIVIDE-------------"
        noticia = line[2].encode('utf-8')
        #print noticia
        for politico in personalidadesRank1:
            aux = list()
            politicoRepetido = False
            ola = [politico.decode('utf-8')]
            aux = re.findall(r'\b(%s)\b' % '|'.join(ola), noticia)
            if not aux:
                continue
            else:
                if key in politicos_in:
                    for pol in politicos_in[key]:
                        if pol == aux[0]:
                            print 'break'
                            print 'politico repetido'
                            politicoRepetido = True
                    if politicoRepetido == True:
                        continue
                    else:
                        politicos_in[line[0]].append(aux[0])
                else:
                    politicos_in[line[0]] = [aux[0]]
                #aux.append(line[0])
                #print 'ENCONTREI'
                #politicos_in_noticia_rank1.append(aux)
    
   
    
    #return politicos_in_noticia_rank1            
    return politicos_in


#---------------------Procura positividade dois politicos 
def PosiXPoliticos (sentimentNoticias, entitiesInNoticia, pol1, pol2):

    encontraPol1 = False
    encontraPol2 = False
    positividade = 0
    
    for key in entitiesInNoticia:
        encontraPol1 = False
        encontraPol2 = False
        for politico in entitiesInNoticia[key]:
            if pol1 == politico:
                encontraPol1 = True
            if pol2 == politico:
                encontraPol2 = True
                
        if encontraPol1 and encontraPol2:
            positividade = positividade + sentimentNoticias[int(key)]
            
    
    return positividade

#def fastFind 
def numeroReferenciasPolitico(entitiesInNoticia):
    
    nRefPoliticos = dict()
    
    for key in entitiesInNoticia:
        for politico in entitiesInNoticia[key]:
            if politico in nRefPoliticos:
                nRefPoliticos[politico] = nRefPoliticos[politico] + 1
            else:
                nRefPoliticos[politico] = 1
                
    return nRefPoliticos

        
import re

def initSentiment():
    f = open('SentiLex-lem-PT02.txt', 'r')

    sentimentos =  dict()
    var = False # Variavel para verificar se a palavra do dicionario e do tipo HUM
    
    for line in f:
        #print re.split('. | ;', line)
        palavra = line.split('.')
        #print palavra[0]
        for k ,name in enumerate(line.split(';')):
            #print name
            n = re.search('(?<=N0=)\w+', name)
            m = re.search('(?<=TG=)HUM', name)
            #print name
            #if m:
                ##print n.group(0)
                #var = True
            var = True #Comentar para meter o hum a funcionar
            if n and var:
                #print n.group(0)
                sentimentos[palavra[0]] = int(n.group(0))
                
    return sentimentos


def NoticiasSentiment(descricaoAll):
    sentimentos = initSentiment()

    sentimentos_noticias =  dict()
    
    
    for line in descricaoAll:
        #Se quiser ID da noticia line[0]
        noticia = line[2].encode('utf-8')
        #print noticia
        #print line[0]
        setNoticia = set(noticia.split())
        #print type(setNoticia)
        keys = setNoticia.intersection(sentimentos)
        NewDic = {k: sentimentos[k] for k in keys}
        #print NewDic
        sentimentos_noticias [line[0]]= sum(NewDic.values())
    
    return sentimentos_noticias



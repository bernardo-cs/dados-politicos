from bs4 import BeautifulSoup
from urllib import urlopen

#url = 'http://rss.feedsportal.com/c/32443/f/622337/s/2c110120/l/0L0Sjn0Bpt0CPaginaInicial0CPolitica0CInterior0Baspx0Dcontent0Iid0F3225921/story01.htm'

def cleanHtml(i):
    
    i = str(i)    
    bs = BeautifulSoup(i)
    i = bs.getText()
    
    return i


def getNoticia(url):
    
    webpage = urlopen(url)
    soup = BeautifulSoup(webpage)

    summary = soup.findAll(id='NewsSummary')

    nCompleta = soup.findAll(id='Article')

    #for i in nCompleta:
    summary = cleanHtml(summary)
    nCompleta = cleanHtml(nCompleta) # para imprimir sem str descomentar o for 


    #print(nCompleta)
    #print(summary)
    return summary, nCompleta
    
#getNoticia(url)
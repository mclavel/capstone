import urllib.request
from bs4 import BeautifulSoup
import unidecode
import os
__author__ = 'cilopez'



def reader(url):
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(webpage, "html.parser")
        fecha = soup.find('h2',
                                attrs={'class': 'tit-modulo'})
        final_score = soup.find_all('div',
                                attrs = {'class': 'cont-resultado finalizado'})
        local_team = soup.find_all('div',
                             attrs={'class': 'equipo-local'})
        vis_team = soup.find_all('div',
                               attrs={'class': 'equipo-visitante'})
        fecha = fecha.text.strip()
        i = 0
        for elems in final_score:
            result = elems.text.strip().split('-')
            data = ([unidecode.unidecode(local_team[i].text.strip()).replace("'"," "), result[0], result[1]
                        , unidecode.unidecode(vis_team[i].text.strip()).replace("'"," ")])
            with open("campeonato.csv", "a") as db:
                db.write('{},{},{},{},{}\n'.format(fecha,
                                                       *data))
            i += 1

if __name__ == '__main__':
    b_path = os.getcwd()
    path = os.path.join(b_path,'campeonato.csv')
    with open(path,"w") as db:
                db.write("FECHA,LOCAL,GOLESLOCAL,GOLESVIS,VISITA\n")
    fase = ['clausura','apertura']
    years = ['2017','2015_2016','2014_2015']
    y = 2018
    for i in range(1, 31):
                reader('https://chile.as.com/resultados/futbol/chile/'
                   '{}/jornada/regular_a_{}/'.format(y, i))


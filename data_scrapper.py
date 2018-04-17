import urllib.request
from bs4 import BeautifulSoup
import os
__author__ = 'cilopez'


def reader(url, year, fase):
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
            data = ([local_team[i].text.strip(), result[0], result[1]
                        , vis_team[i].text.strip()])
            with open("chilean_db.csv", "a") as db:
                db.write('{},{},{},{},{},{},{}\n'.format(year, fase, fecha,
                                                       *data))
            i += 1

if __name__ == '__main__':
    b_path = os.getcwd()
    path = os.path.join(b_path,'data','chilean_db.csv')
    with open(path,"w") as db :
                db.write("AÑO,FASE,FECHA,,LOCAL,GOLESLOCAL,GOLESVIS,VISITA\n")
    fase = ['clausura','apertura']
    years = ['2017','2015_2016','2014_2015']
    for y in years:
        for x in fase:
            for i in range(1, 16):
                reader('https://chile.as.com/resultados/futbol/chile_{}/'
                   '{}/jornada/regular_a_{}/'.format(x, y, i), y, x)


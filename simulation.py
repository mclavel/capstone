from gurobipy import *
from equipos import equipos_santiago
from equipos import EQUIPOS
from equipos import nombres as equipos
from prob import ODDS
from schedueling import CALENDARIO
import random
from numpy.random import choice


class Simulacion:
    def __init__(self, calendario,odds,equipos):
        self.calendario = calendario
        self.tabla = []
        self.equipos = equipos
        self.fecha = 0
        self._results = {}
        self.odds = odds
        self._pdraw = 0.26 #Dato historico de empates
        self._localwin = 0.4396 #Probabilidad de que un equipo local gane
        self.epsilon = 1 #Factor que le da mas chances de ganar a A

    def add_victoria(self,a,b):
        a.victorias.append(b)
        b.derrotas.append(a)

    def p_empate(self):
        if self.fecha == 0:
            return self._pdraw
        n_empates_actuales = sum([len(x.empates) for x in self.equipos])/2
        n_partidos = len([keys for keys in self._results])*8
        return max(self._pdraw - 0.05 , min(self._pdraw + 0.05, 
            n_empates_actuales / n_partidos  ))

    def p_alpha (self,A):
        if self.fecha == 0:
            return 0.5
        n_partidos = len([keys for keys in self._results])
        #Tengo que arreglar aca ya que es el numero de partidos ganados como local
        #Esto se debe arreglar
        print(len(A.victorias)/n_partidos)
        return max(0.5, len(A.victorias)/n_partidos)

    def p_betha (self,A,B):
        if self.fecha == 0:
            return 0.5
        return (A.rendimiento /(A.rendimiento + B.rendimiento))

    def p_gamma (self,A,B):
        return (A.ranking/(A.ranking + B.ranking))

    def p_local(self,A,B):
        factor = (2 * self.p_alpha(A) * self.p_betha(A,B)) + self.p_gamma(A,B)
        return (1-self.p_empate())* factor * self.epsilon


    def match_ending(self, victory, draw):
        x = random.uniform(0,1)
        if x <= victory:
            return "LW"
        elif x > victory and x < (draw + victory):
            return "D"
        else:
            return "AW" 

    def evento(self,local,visita):
        empate = self.p_empate()
        victoria_local = self.p_local(local,visita)
        r = self.match_ending(victoria_local,empate)
        if r == "LW":
            self.add_victoria(local,visita)
            return "LW"
        elif r == "AW":
            self.add_victoria(visita,local)
            return "AW"
        else:
            local.empates.append(visita)
            visita.empates.append(local)
            return "D"
           
           
    def results(self,match):
        local, away = match.split(",")
        eqlocal = [x for x in self.equipos if x.nombre == local.strip()]
        eqvis = [x for x in self.equipos if x.nombre == away.strip()]
        resultado = self.evento(*eqlocal,*eqvis)
        return resultado
    
    def run(self):
        for fechas in self.calendario:
            self.fecha += 1
            self._results[fechas.numero]= []
            for x in fechas.partidos:
                self._results[fechas.numero].append(self.results(x))
        self.equipos.sort(key=lambda x: x.puntaje, reverse = True)
        for x in self.equipos:
            print(x)


if __name__ == "__main__":
	print("Empieza la simulación")
	s = Simulacion(CALENDARIO,ODDS,EQUIPOS)
	s.run()
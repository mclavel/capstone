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
        self._results = {}
        self.odds = odds

    def victoria(self,a,b):
        a.victorias.append(b)
        b.derrotas.append(a)

    def match_ending(self):
        x = random.uniform(0,1)
        y = random.uniform(0, 1-x)
        final = choice(["LW", "D", "AW"], 1, p=[x,y,1-x-y])
        return final

    def evento(self,local,visita):
        r = self.match_ending()
        if r == "LW":
            self.victoria(local,visita)
        elif r == "AW":
            self.victoria(visita,local)
        else:
            local.empates.append(visita)
            visita.empates.append(local)
           
           
    def results(self,match):
        local, away = match.split(",")
        eqlocal = [x for x in self.equipos if x.nombre == local.strip()]
        eqvis = [x for x in self.equipos if x.nombre == away.strip()]
        resultado = self.evento(*eqlocal,*eqvis)
    
    def run(self):
        for fechas in self.calendario:
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
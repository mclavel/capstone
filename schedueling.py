from gurobipy import *
from equipos import equipos_santiago
from equipos import EQUIPOS
from equipos import nombres as equipos
from prob import ODDS
import random
from numpy.random import choice

class Fecha:
    def __init__(self, num, partidos):
        self.numero = num
        self.partidos = partidos
        self.resultados = None

    def __repr__(self):
        return str(self.numero)

class Simulacion:
    def __init__(self, calendario,odds,equipos):
        self.calendario = calendario
        self.tabla = []
        self.equipos = equipos
        self._results = {}
        self.odds = odds

    def evento(self,local,visita):
        x = random.uniform(0,1)
        y = random.uniform(0, 1-x)
        r = choice(["LW", "D", "AW"], 1, p=[x,y,1-x-y])
        if r == "LW":
            local.puntaje += 3
            local.victorias.append(visita)
            visita.derrotas.append(local)
        elif r == "AW":
            visita.puntaje +=3
            visita.victorias.append(local)
            local.derrotas.append(local)
        else:
            local.empates.append(visita)
            visita.empates.append(local)
            local.puntaje += 1
            visita.puntaje += 1
        
        
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


fechas = [i for i in range(1, 16)]
U = [0, 1, 2]

m = Model("Tournament")

#1 si juega el equipo i de local contra j en la fecha k
match = m.addVars(equipos, equipos, fechas, vtype=GRB.BINARY, name="match")

#Todos jueguen con todos y solo una vez en cada fecha
m.addConstrs((quicksum(match[i, j, k] + match[j, i, k] for j in equipos) == 1 for i in equipos for k in fechas))

#No jueguen contra si mismos
m.addConstrs(match[i, i, k] == 0 for k in fechas for i in equipos)

#No mas de 2 partidos consecutivos de local o visita
m.addConstrs((quicksum(match[i, j, k + l] for j in equipos for l in U) <= 2 for i in equipos for k in fechas[:13]))

#No mas de 3 en Santiago, ya que no es posible tope en otra ciudad
m.addConstrs((quicksum(match[i, j, k] for i in equipos_santiago) <= 3 for j in equipos for k in fechas))

#La funcion objetivo no es de importancia pero cuenta que esten todas las fechas
m.setObjective(quicksum(match[i, j, k] for i in equipos for j in equipos for k in fechas), GRB.MINIMIZE)

m.optimize()

CALENDARIO = []
# Print solution
if m.status == GRB.Status.OPTIMAL:
    solution = m.getAttr('x', match)
    for k in fechas:
        f = []
        for i in equipos:
            for j in equipos:
                if solution[i, j, k] > 0:
                    f.append("{}, {}".format(i,j))
        fecha = Fecha(k,f)
        CALENDARIO.append(fecha)

print("Empieza la simulación")
s = Simulacion(CALENDARIO,ODDS,EQUIPOS)
s.run()


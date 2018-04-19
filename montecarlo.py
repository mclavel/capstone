from equipos import EQUIPOS
import simulation
from schedueling import CALENDARIO

class Montecarlo:
    def __init__(self):
        self.simulaciones = []
        self.tabla = [x for x in EQUIPOS]

    def agregar_simulacion(self, simulacion):
        self.simulaciones.append(simulacion)

    def tabla_esperada(self):
        for x in self.simulaciones:
            for w in x.equipos:
                for y in self.tabla:
                    if w.nombre == y.nombre:
                        y._fake += w.puntaje
        for teams in self.tabla:
            y = teams._fake / (len(self.simulaciones)**2)
            teams._fake = y
        return self.tabla

	
if __name__ == "__main__":
    m = Montecarlo()
    for x in range(1000):
        s = None
        s = simulation.Simulacion(CALENDARIO,None,EQUIPOS)
        s.run()
        m.agregar_simulacion(s)
    final = (m.tabla_esperada())
    final.sort(key=lambda x: x.puntaje, reverse = True)
    for teams in final:
        print(teams.fake_show())
from equipos import EQUIPOS
import simulation
from schedueling import CALENDARIO
import copy

class Montecarlo:
    def __init__(self):
        self.simulaciones = []
        self.tabla = [x for x in EQUIPOS]

    def agregar_simulacion(self, simulacion):
        self.simulaciones.append(simulacion)

    def tabla_esperada(self):
        #Esto funciona pero esta mal 
        for x in self.simulaciones:
            for w in x.equipos:
                for y in self.tabla:
                    if w.nombre == y.nombre:
                        y._fake += w.puntaje
                        [y._fake_victorias.append(x) for x in w.victorias[:]]
                        [y._fake_empates.append(x) for x in w.empates[:]]
                        [y._fake_derrotas.append(x) for x in w.derrotas[:]]
        for teams in self.tabla:
            #Nose porque al poner el len al cuadrado funciona
            y = round(teams._fake / (len(self.simulaciones)))
            teams._fake = y
        return self.tabla

	
if __name__ == "__main__":
    m = Montecarlo()
    for x in range(2000):
        s = None
        s = simulation.Simulacion(CALENDARIO,None,EQUIPOS)
        s.run()
        m.agregar_simulacion(s)
    final = (m.tabla_esperada())
    final.sort(key=lambda x: x._fake, reverse = True)
    for teams in final:
        print(teams.fake_show())
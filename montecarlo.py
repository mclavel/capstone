from equipos import EQUIPOS
import simulation
import time


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
            y = round(teams._fake / (len(self.simulaciones)))
            teams._fake = y
        return self.tabla

def simulacion_montecarlo(calendario, puntajes=False):
    m = Montecarlo()
    start_time = time.time()
    n = 1000
    for x in range(n):
        s = None
        s = simulation.Simulacion(calendario,EQUIPOS)
        s.run()
        m.agregar_simulacion(s)
    final = (m.tabla_esperada())
    tabla = []
    final.sort(key=lambda x: x._fake, reverse=True)
    print("\n {} seconds to {} simulations".format
          (round(time.time() - start_time, 2), n))
    if puntajes:
        tabla = dict()
        for teams in final:
            tabla[teams.nombre] = teams._fake
            print(teams.fake_show(n))

    else:
        for teams in final:
            tabla.append(teams.nombre)
            print(teams.fake_show(n))
    return tabla
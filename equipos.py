import random

class Equipo:
    def __init__(self, nombre, localia, ranking, presupuesto , puntaje=0):
        self.nombre = nombre
        self.goles = 0
        self.presupuesto =  presupuesto
        self.localia = localia
        self._fake= 0
        self.partidos_local = []
        self.partidos_visita = []
        self.derrotas = []
        self.victorias = []
        self.empates = []
        self.ranking = ranking

    @property
    def puntaje (self):
      return len(self.empates) + 3 * len(self.victorias)
  
    @property
    def rendimiento(self):
      if len(self.partidos_local) == 0 and len(self.partidos_visita) == 0:
          return 1
      return self.puntaje/ len(self.partidos_local)+len(self.partidos_visita)
    
    def fake_show(self):
        return self.nombre +": {}".format(self._fake)
    
    def __repr__(self):
        return self.nombre + ": {} |W{} |D{} |L{} ".format(str(self.puntaje),len(self.victorias),len(self.empates),len(self.derrotas))


nombre_ciudad = [("U. de Chile", "Santiago", 50,500), ("Colo Colo", "Santiago", 137,500),
           ("CD San Luis", "Quillota", 50,87), ("O Higgins", "Rancagua", 165,82),
           ("Huachipato", "Talcahuano", 50,85), ("Palestino", "Santiago", 50,87),
           ("A. Italiano", "Santiago", 50,95), ("Everton Vina", "Vina del Mar", 219,125),
           ("U. Espanola", "Santiago", 447,125), ("U. de Conce", "Concepcion", 50,95),
           ("D. Iquique", "Iquique", 1010,80), ("U. Catolica", "Santiago", 928,350),
           ("Antofagasta", "Antofagasta", 50,100), ("U. La Calera", "La Calera", 50,70),
           ("Curico Unido", "Curico", 50,70), ("Deportes Temuco", "Temuco", 50,80)]

equipos_santiago = ["U. de Chile", "Colo Colo", "Palestino", "U. Espanola",
                    "U. Catolica", "A. Italiano"]
equipos_valparaiso = ["Everton Vina", "CD San Luis", "U. La Calera"]
equipos_biobio = ["Huachipato", "U. de Conce"]
equipos_grandes = ["U. de Chile", "Colo Colo", "U. Catolica"]



nombres = [equipo[0] for equipo in nombre_ciudad]
EQUIPOS = []
clubes = []

for equipo in nombre_ciudad:
    clubes.append(equipo[0])
    e = Equipo(*equipo)
    EQUIPOS.append(e)

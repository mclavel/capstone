import random

class Equipo:
    def __init__(self, nombre, localia, ranking, puntaje=0):
        self.nombre = nombre
        self.goles = 0
        self.localia = localia
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

      
    def __repr__(self):
        return self.nombre + ": {} |W{} |D{} |L{} ".format(str(self.puntaje),len(self.victorias),len(self.empates),len(self.derrotas))


nombre_ciudad = [("U. de Chile", "Santiago", 50), ("Colo Colo", "Santiago", 137),
           ("CD San Luis", "Quillota", 50), ("O Higgins", "Rancagua", 165),
           ("Huachipato", "Talcahuano", 50), ("Palestino", "Santiago", 50),
           ("A. Italiano", "Santiago", 50), ("Everton Vina", "Vina del Mar", 219),
           ("U. Espanola", "Santiago", 447), ("U. de Conce", "Concepcion", 50),
           ("D. Iquique", "Iquique", 1010), ("U. Catolica", "Santiago", 928),
           ("Antofagasta", "Antofagasta", 50), ("U. La Calera", "La Calera", 50),
           ("Curico Unido", "Curico", 50), ("Deportes Temuco", "Temuco", 50)]

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

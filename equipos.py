import random

class Equipo:
    def __init__(self, nombre, localia, puntaje=0):
        self.nombre = nombre
        self.goles = 0
        self.localia = localia
        self.partidos_local = []
        self.partidos_visita = []
        self.derrotas = []
        self.victorias = []
        self.empates = []
        self.ranking = 50

    @property
    def puntaje (self):
      return len(self.empates) + 3* len(self.victorias)
  
    @property
    def rendimiento(self):
      if len(self.partidos_local) == 0 and len(self.partidos_visita) == 0:
          return 1
      return self.puntaje/ len(self.partidos_local)+len(self.partidos_visita)

      
    def __repr__(self):
        return self.nombre + ": {} |W{} |D{} |L{} ".format(str(self.puntaje),len(self.victorias),len(self.empates),len(self.derrotas))


nombre_ciudad = [("U. de Chile", "Santiago"), ("Colo Colo", "Santiago"),
           ("CD San Luis", "Quillota"), ("O Higgins", "Rancagua"),
           ("Huachipato", "Talcahuano"), ("Palestino", "Santiago"),
           ("A. Italiano", "Santiago"), ("Everton Vina", "Vina del Mar"),
           ("U. Espanola", "Santiago"), ("U. de Conce", "Concepcion"),
           ("D. Iquique", "Iquique"), ("U. Catolica", "Santiago"),
           ("Antofagasta", "Antofagasta"), ("U. La Calera", "La Calera"),
           ("Curico Unido", "Curico"), ("Deportes Temuco", "Temuco")]

equipos_santiago = ["U. de Chile", "Colo Colo", "Palestino", "U. Espanola",
                    "U. Catolica", "A. Italiano"]
nombres = [equipo[0] for equipo in nombre_ciudad]

EQUIPOS = []
clubes = []

for equipo in nombre_ciudad:
    clubes.append(equipo[0])
    e = Equipo(*equipo)
    EQUIPOS.append(e)

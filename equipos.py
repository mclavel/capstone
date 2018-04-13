import random

class Equipo:
    def __init__(self, nombre, localia, puntaje=0):
        self.nombre = nombre
        self.puntaje = random.randint(0, 20) if puntaje == 0 else puntaje
        self.goles = 0
        self.localia = localia
        self.partidos_local = []
        self.partidos_visita = []

    def __repr__(self):
        return self.nombre + ": {}".format(str(self.puntaje))


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

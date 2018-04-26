import random
import csv
import os



class Equipo:
    def __init__(self, nombre, localia, presupuesto, ranking, capacidad,
                 espectadores):
        self.nombre = nombre
        self.goles = 0
        self.presupuesto =  presupuesto
        self.localia = localia
        self.capacidad = capacidad
        self.espectadores = espectadores
        self._fake= 0
        self._fake_victorias = []
        self._fake_derrotas = []
        self._fake_empates= []
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
    
    def fake_show(self,n_simulation):
        return self.nombre +": {} |W:{}|D:{}|L:{}".format(self._fake,
                               (len(self._fake_victorias)/n_simulation)
                               ,(len(self._fake_empates)/n_simulation),
                               (len(self._fake_derrotas)/n_simulation))
    
    def __repr__(self):
        return self.nombre + ": {} |W{} |D{} |L{} ".format(str(self.puntaje),len(self.victorias),len(self.empates),len(self.derrotas))


nombre_ciudad = [("U. de Chile", "Santiago",500), ("Colo Colo", "Santiago",500),
           ("CD San Luis", "Quillota",87), ("O Higgins", "Rancagua",82),
           ("Huachipato", "Talcahuano",85), ("Palestino", "Santiago",87),
           ("A. Italiano", "Santiago",95), ("Everton Vina", "Vina del Mar",125),
           ("U. Espanola", "Santiago",125), ("U. de Conce", "Concepcion",95),
           ("D. Iquique", "Iquique",80), ("U. Catolica", "Santiago",350),
           ("Antofagasta", "Antofagasta",100), ("U. La Calera", "La Calera",70),
           ("Curico Unido", "Curico",70), ("Deportes Temuco", "Temuco",80)]

equipos_santiago = ["U. de Chile", "Colo Colo", "Palestino", "U. Espanola",
                    "U. Catolica", "A. Italiano"]
equipos_valparaiso = ["Everton Vina", "CD San Luis", "U. La Calera"]
equipos_biobio = ["Huachipato", "U. de Conce"]
equipos_grandes = ["U. de Chile", "Colo Colo", "U. Catolica"]


def reader(file,row1,column1):
    data = {}   
    path = os.path.join(os.getcwd(),"data",file)
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data[row[row1]]= row[column1]
    return data

ranking = reader("puntajes.csv",'Equipo','Puntaje total')
espectators = reader("espectadores.csv","Equipo","Espectadores")
capacity = reader("capacidad.csv","Equipo","Capacidad")



nombres = [equipo[0] for equipo in nombre_ciudad]
EQUIPOS = []
clubes = []

for equipo in nombre_ciudad:
    clubes.append(equipo[0])
    e = Equipo(ranking=float(ranking[equipo[0]]),
    espectadores=float(espectators[equipo[0]]),
    capacidad=float(capacity[equipo[0]]), *equipo)
    #print(e.__dict__)
    EQUIPOS.append(e)

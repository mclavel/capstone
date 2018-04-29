from gurobipy import *
from equipos import equipos_santiago, equipos_biobio, equipos_valparaiso, \
    equipos_grandes
from equipos import nombres as equipos


class Fecha:
    def __init__(self, num, partidos):
        self.numero = num
        self.partidos = partidos
        self.resultados = None

    def __repr__(self):
        return str(self.numero)

def aux(jugados): #funcion sin importancia
    p_jugados = []
    for fecha in jugados:
        for partido in fecha.partidos:
            p_jugados.append([partido.split(",")[0], partido.split(",")[1][1:]])
    return p_jugados

def calendarizacion(n_fechas, jugados=None, tabla=None):
    fechas = [i for i in range(1, n_fechas + 1)]

    m = Model("Tournament")

    #1 si juega el equipo i de local contra j en la fecha k
    match = m.addVars(equipos, equipos, fechas, vtype=GRB.BINARY, name="match")

    #Todos jueguen con todos y solo una vez en cada fecha
    m.addConstrs((quicksum(match[i, j, k] + match[j, i, k] for j in equipos) ==
                  1 for i in equipos for k in fechas))

    #No jueguen contra si mismos
    m.addConstrs(match[i, i, k] == 0 for k in fechas for i in equipos)

    #No mas de 2 partidos consecutivos de local o visita
    m.addConstrs((quicksum(match[i, j, k + l] for j in equipos for l in [0, 1,
                 2]) <= 2 for i in equipos for k in fechas[:n_fechas - 2]))

    #No mas de 3 en Santiago
    m.addConstrs((quicksum(match[i, j, k] for i in equipos_santiago) <= 3 for j
                  in equipos for k in fechas))

    # No mas de 1 en Valparaiso
    m.addConstrs(
        (quicksum(match[i, j, k] for i in equipos_valparaiso) <= 1 for j in
         equipos for k in fechas))

    # No mas de 1 en BioBio
    m.addConstrs(
        (quicksum(match[i, j, k] for i in equipos_biobio) <= 1 for j in equipos for
         k in fechas))

    if jugados is not None:
        m.addConstrs((quicksum(match[i, j, k] for i, j in aux(jugados)) == 0 for k in fechas))

    if tabla is not None:
        # No pueden jugarse los clasicos
        m.addConstrs((quicksum(match[i, j, k] for i in equipos_grandes for j in
                      equipos_grandes) == 0 for k in fechas))


        # No jueguen contra equipos del mismo cluster
        m.addConstrs(match[i, j, k] == 0 for k in fechas for
                     i in tabla[0:8] for j in tabla[0:8])

        m.addConstrs(match[i, j, k] == 0 for k in fechas for
                     i in tabla[8:] for j in tabla[8:])


    m.setObjective(quicksum(match[i, j, k] for i in equipos for j in equipos for
                   k in fechas), GRB.MINIMIZE)

    m.optimize()

    CALENDARIO = [] #Calendario inicial factible
    # Print solution
    if m.status == GRB.Status.OPTIMAL:
        solution = m.getAttr('x', match)
        for k in fechas:
            print "Fecha", k
            f = []
            for i in equipos:
                for j in equipos:
                    if solution[i, j, k] > 0:
                        f.append("{}, {}".format(i, j))
                        print i, "-", j
            fecha = Fecha(k,f)
            CALENDARIO.append(fecha)
    return CALENDARIO




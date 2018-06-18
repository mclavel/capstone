from gurobipy import *
from equipos import nombres as equipos, equipos_valparaiso, equipos_biobio, equipos_santiago
from schedueling import Fecha, aux
from schedueling import local_solo_ult, local_ult_2, visita_solo_ult, visita_ult_2

def min_var(rho, n_fechas, u2_partidos, jugados, puntaje_inicial, matriz_p, fecha,
            clusters=False, gap=None):
    print "jugados", jugados, len(jugados)
    p0 = puntaje_inicial
    if fecha == 20: #calendarizar 8 fechas (23, 24, 25 | 26, 27, 28, 29, 30)
        fechas = [i for i in range(1, 9)]
    elif fecha == 24: #calendarizar 5 fechas (26, 27, 28 | 29, 30)
        fechas = [i for i in range(1, 6)]
    elif fecha == 27: #calendarizar 2 fechas (29, 30)
        fechas = [i for i in range(1, 3)]
    m = Model("Tournament")
    m.setParam('OutputFlag', 0)

    match = m.addVars(equipos, equipos, fechas, vtype=GRB.BINARY, name="match") # 1 si el partido se juega (es factible)
    x = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="x") # 1 si el equipo i gana
    p_x = m.addVars(fechas, name="px")
    y = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="y") # 1 si el equipo j gana
    p = m.addVars(equipos, name="p") #puntos equipo i

    if clusters:
        a1 = m.addVar(name="a1")  # mayor puntaje 1er cluster
        b1 = m.addVar(name="b1")  # menor puntaje 1er cluster
        a2 = m.addVar(name="a2")  # mayor puntaje 2do cluster
        b2 = m.addVar(name="b2")  # menor puntaje 2do cluster
        m.setObjective(
            (a1 - b1) + (a2 - b2) - rho * quicksum(p_x[k] for k in fechas[:n_fechas]),
            GRB.MINIMIZE)  # FO

    else:
        a = m.addVar(name="a")  # mayor puntaje
        b = m.addVar(name="b")  # menor puntaje
        m.setObjective((a - b) - rho * quicksum(p_x[k] for k in fechas[:n_fechas]),
                       GRB.MINIMIZE)  # FO

        m.addConstrs(p[i] <= a for i in equipos)

        m.addConstrs(p[i] >= b for i in equipos)


    #RESTRICCIONES
    print len(aux(jugados))
    for i in aux(jugados):
        print i

    m.addConstrs((quicksum(match[i, j, k + l] for j in equipos for l in [0, 1, 2]) <= 2 for i in equipos for k in fechas[:len(fechas) - 2]))

    m.addConstrs((quicksum(match[j, i, k + l] for j in equipos for l in [0, 1, 2]) <= 2 for i in equipos for k in fechas[:len(fechas) - 2]))

    m.addConstrs((quicksum(match[i, j, k] + match[j, i, k] for j in equipos) == 1 for i in equipos for k in fechas))

    m.addConstrs(quicksum(match[i, j, k] + match[j, i, k] for k in fechas) <= 1 for i in equipos for j in equipos if i != j)

    m.addConstrs(match[i, i, k] == 0 for k in fechas for i in equipos)

    m.addConstrs(match[i, j, k] == 0 for i, j in aux(jugados) for k in fechas)

    m.addConstrs(p[i] == p0[i] + quicksum(3 * x[i, k] + y[i, k] for k in fechas[:n_fechas]) for i in equipos)

    m.addConstrs(match[i, j, k] <= (x[i, k] + y[i, k] + x[j, k] + y[j, k]) for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(x[i, k] + y[i, k] <= 1 for i in equipos for k in fechas)

    m.addConstrs(y[i, k] - y[j, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(y[j, k] - y[i, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(p_x[k] == quicksum(matriz_p[i][j] * x[i, k] for i in equipos for j in matriz_p[i]) for k in fechas[:n_fechas])

    m.addConstr(quicksum(y[i, k] for i in equipos for k in fechas) / 2 <= n_fechas * 8 * 0.25)

    m.addConstr(quicksum(y[i, k] for i in equipos for k in fechas) / 2 >= n_fechas * 8 * 0.15)

    m.addConstrs((quicksum(match[i, j, k] for i in equipos_santiago) <= 3 for j in equipos for k in fechas))

    m.addConstrs((quicksum(match[i, j, k] for i in equipos_valparaiso) <= 1 for j in equipos for k in fechas))

    m.addConstrs((quicksum(match[i, j, k] for i in equipos_biobio) <= 1 for j in equipos for k in fechas))

    if len(local_ult_2(u2_partidos)) != 0:
        m.addConstrs(quicksum(match[i, j, 1] for j in equipos) == 0
                     for i in local_ult_2(u2_partidos))

    if len(visita_ult_2(u2_partidos)) != 0:
        m.addConstrs(quicksum(match[i, j, 1] for i in equipos) == 0
                     for j in visita_ult_2(u2_partidos))

    if len(local_solo_ult(u2_partidos)) != 0:
        m.addConstrs(quicksum(match[i, j, 1] + match[i, j, 2] for j in
                              equipos) <= 1 for i in local_solo_ult(u2_partidos))

    if len(visita_solo_ult(u2_partidos)) != 0:
        m.addConstrs(quicksum(match[i, j, 1] + match[i, j, 2] for i in
                              equipos) <= 1 for j in visita_solo_ult(u2_partidos))
    if clusters:
        equipos_a = sorted(p0.items(), key=lambda x: x[1], reverse=True)
        equipos_ordenados = [x[0] for x in equipos_a]
        equipos_ordenados = equipos

        m.addConstrs(p[i] <= a1 for i in equipos_ordenados[:8])
        m.addConstrs(p[i] <= a2 for i in equipos_ordenados[8:])

        m.addConstrs(p[i] >= b1 for i in equipos_ordenados[:8])
        m.addConstrs(p[i] >= b2 for i in equipos_ordenados[8:])

    if gap is not None:
        m.params.MIPGap = gap
    m.optimize()

    CALENDARIO = []
    # Print solution
    if m.status in (GRB.Status.INF_OR_UNBD, GRB.Status.INFEASIBLE):
        return None
    if m.status == GRB.Status.OPTIMAL:
        solution = m.getAttr('x', match)
        if clusters:
            print ("Amplitud:", a1.X - b1.X, a2.X - b2.X)
        else:
            print ("Amplitud:", a.X - b.X)
        print ("Prob:", sum(list(p_x[k].X for k in fechas)))
        for l, k in enumerate(fechas):
            f = []
            if l < n_fechas:
                print ("\n")
                print ("Fecha", k)
            for i in equipos:
                for j in equipos:
                    if solution[i, j, k] > 0:
                        if l < n_fechas:
                            print (i ,"-", j, " -> ", "LW" if x[i, k].X == 1 else "D" if y[i, k].X == 1 else "AW") #matriz_p[i][j], matriz_p[j][i]
                        f.append("{}, {}".format(j, i))
            if fecha == 24:  # calendarizar 5 fechas (26, 27, 28 | 29, 30)
                fe = Fecha(k + 25, f)
            elif fecha == 27:  # calendarizar 2 fechas (29, 30)
                fe = Fecha(k + 28, f)
            else:
                fe = Fecha(k + 22, f)
            CALENDARIO.append(fe)
        print ("\n")
        if n_fechas == 3:
            return CALENDARIO[:n_fechas], CALENDARIO[n_fechas:]
        else:
            return CALENDARIO


from gurobipy import *
from equipos import nombres as equipos, equipos_valparaiso, equipos_biobio, equipos_santiago
from schedueling import Fecha, aux
from schedueling import local_solo_ult, local_ult_2, visita_solo_ult, visita_ult_2
p = 10

def min_var(n_fechas, jugados, puntaje_inicial,matriz_p, clusters=False, gap=None):
    p0 = puntaje_inicial
    fechas = [i for i in range(1, n_fechas + 1)]
    m = Model("Tournament")

    match = m.addVars(equipos, equipos, fechas, vtype=GRB.BINARY, name="match") # 1 si el partido se juega (es factible)
    x = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="x") # 1 si el equipo i gana
    p_x = m.addVars(fechas, name="px")
    y = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="y") # 1 si el equipo j gana
    p = m.addVars(equipos, name="p") #puntos equipo i

    if clusters:
        print "cluster 1"
        a1 = m.addVar(name="a1")  # mayor puntaje 1er cluster
        b1 = m.addVar(name="b1")  # menor puntaje 1er cluster
        a2 = m.addVar(name="a2")  # mayor puntaje 2do cluster
        b2 = m.addVar(name="b2")  # menor puntaje 2do cluster
        m.setObjective(
            (a1 - b1) + (a2 - b2) - 100 * quicksum(p_x[k] for k in fechas),
            GRB.MINIMIZE)  # FO

    else:
        print "cluster 2"
        a = m.addVar(name="a")  # mayor puntaje
        b = m.addVar(name="b")  # menor puntaje
        m.setObjective((a - b) - 100 * quicksum(p_x[k] for k in fechas),
                       GRB.MINIMIZE)  # FO

        m.addConstrs(p[i] <= a for i in equipos)

        m.addConstrs(p[i] >= b for i in equipos)



    #RESTRICCIONES

    m.addConstrs((quicksum(match[i, j, k + l] for j in equipos for l in [0, 1, 2]) <= 2 for i in equipos for k in fechas[n_fechas - 3:n_fechas - 2]))

    m.addConstrs((quicksum(match[i, j, k] + match[j, i, k] for j in equipos) == 1 for i in equipos for k in fechas))

    m.addConstrs(quicksum(match[i, j, k] + match[j, i, k] for k in fechas) <= 1 for i in equipos for j in equipos if i != j)

    m.addConstrs(match[i, i, k] == 0 for k in fechas for i in equipos)

    m.addConstrs((quicksum(match[i, j, k] for i, j in aux(jugados)) == 0 for k in fechas))

    m.addConstrs(p[i] == p0[i] + quicksum(3 * x[i, k] + y[i, k] for k in fechas) for i in equipos)

    m.addConstrs(match[i, j, k] <= (x[i, k] + y[i, k] + x[j, k] + y[j, k])  for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(x[i, k] + y[i, k] <= 1 for i in equipos for k in fechas)

    m.addConstrs(y[i, k] - y[j, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(y[j, k] - y[i, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(p_x[k] == quicksum(matriz_p[i][j] * x[i, k] for i in equipos for j in matriz_p[i]) for k in fechas)

    m.addConstr(quicksum(y[i, k] for i in equipos for k in fechas) / 2 <= n_fechas * 8 * 0.25)

    m.addConstr(quicksum(y[i, k] for i in equipos for k in fechas) / 2 >= n_fechas * 8 * 0.15)

    # No mas de 3 en Santiago
    m.addConstrs((quicksum(match[i, j, k] for i in equipos_santiago) <= 3 for j
                  in equipos for k in fechas))

    # No mas de 1 en Valparaiso
    m.addConstrs(
        (quicksum(match[i, j, k] for i in equipos_valparaiso) <= 1 for j in
         equipos for k in fechas))

    # No mas de 1 en BioBio
    m.addConstrs(
        (quicksum(match[i, j, k] for i in equipos_biobio) <= 1 for j in equipos
         for k in fechas))

    if len(local_ult_2(jugados)) != 0:
        print "local_ult_2: ", local_ult_2(jugados)
        m.addConstrs(quicksum(match[i, j, 1] for j in equipos) == 0
                     for i in local_ult_2(jugados))

    if len(visita_ult_2(jugados)) != 0:
        print "visita_ult_2: ", visita_ult_2(jugados)
        m.addConstrs(quicksum(match[i, j, 1] for i in equipos) == 0
                     for j in visita_ult_2(jugados))

    if len(local_solo_ult(jugados)) != 0:
        print "local_solo_ult: ", local_solo_ult(jugados)
        m.addConstrs(quicksum(match[i, j, 1] + match[i, j, 2] for j in
                              equipos) <= 1 for i in local_solo_ult(jugados))

    if len(visita_solo_ult(jugados)) != 0:
        print "visita_solo_ult: ", visita_solo_ult(jugados)
        m.addConstrs(quicksum(match[i, j, 1] + match[i, j, 2] for i in
                              equipos) <= 1 for j in visita_solo_ult(jugados))
    if clusters:
        equipos_a = sorted(p0.items(), key=lambda x: x[1], reverse=True)
        equipos_ordenados = [x[0] for x in equipos_a]
        print type(equipos_ordenados[0]) == type(equipos[0])
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
    if m.status == GRB.Status.OPTIMAL:
        solution = m.getAttr('x', match)
        if clusters:
            print ("Amplitud:", a1.X - b1.X, a2.X - b2.X)
        else:
            print ("Amplitud:", a.X - b.X)
        print ("Prob:", sum(list(p_x[k].X for k in fechas)))
        print equipos
        print fechas
        for k in fechas:
            f = []
            print ("\n", "Fecha", k)
            #print "\n Fecha", k
            for i in equipos:
                for j in equipos:
                    print i, j, k
                    if solution[i, j, k] > 0:
                        print (i,"-", j, " -> ", "LW" if x[i, k].X == 1 else "D" if y[i, k].X == 1 else "AW", matriz_p[i][j], matriz_p[j][i])
                        #print i, j
                        f.append("{}, {}".format(j, i))
                        #print "LW:", x[i, k].X, " D:", y[i, k].X
            fecha = Fecha(k + 22, f)
            CALENDARIO.append(fecha)
        print ("\n PUNTAJES teoricos")
        #print "\n PUNTAJES"
        dic = {}
        for i in equipos:
            dic[i] = int(p[i].X)
        dic_sorted = sorted(dic.items(), key=operator.itemgetter(1),
                              reverse=True)
        for i in dic_sorted:
            print (i)
        return CALENDARIO




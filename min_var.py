from gurobipy import *
from equipos import nombres as equipos
from schedueling import Fecha, aux
p = 10

def min_var(n_fechas, jugados, puntaje_inicial,matriz_p):
    print matriz_p
    #print "\n Minimizando la varianza a lo loco"
    #Varguitas la mama
    p0 = puntaje_inicial
    #print p0
    fechas = [i for i in range(1, n_fechas + 1)]
    m = Model("Tournament")

    match = m.addVars(equipos, equipos, fechas, vtype=GRB.BINARY, name="match") #1 si el partido se juega (es factible)
    x = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="x") #1 si el equipo i gana
    p_x = m.addVars(fechas, name="px")
    y = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="y") #1 si el equipo j gana
    p = m.addVars(equipos, name="p") #puntos equipo i
    a = m.addVar(name="a") #mayor puntaje
    b = m.addVar(name="b") #menor puntaje
    m.setObjective((a - b) - 100 * quicksum(p_x[k] for k in fechas), GRB.MINIMIZE) #FO


    #RESTRICCIONES

    m.addConstrs((quicksum(match[i, j, k + l] for j in equipos for l in [0, 1, 2]) <= 2 for i in equipos for k in fechas[n_fechas - 3:n_fechas - 2]))

    m.addConstrs((quicksum(match[i, j, k] + match[j, i, k] for j in equipos) == 1 for i in equipos for k in fechas))

    m.addConstrs(quicksum(match[i, j, k] + match[j, i, k] for k in fechas) <= 1 for i in equipos for j in equipos if i != j)

    m.addConstrs(match[i, i, k] == 0 for k in fechas for i in equipos)

    m.addConstrs((quicksum(match[i, j, k] for i, j in aux(jugados)) == 0 for k in fechas))

    m.addConstrs(p[i] <= a for i in equipos)

    m.addConstrs(p[i] >= b for i in equipos)

    m.addConstrs(p[i] == p0[i] + quicksum(3 * x[i, k] + y[i, k] for k in fechas) for i in equipos)

    m.addConstrs(match[i, j, k] <= (x[i, k] + y[i, k] + x[j, k] + y[j, k])  for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(x[i, k] + y[i, k] <= 1 for i in equipos for k in fechas)

    m.addConstrs(y[i, k] - y[j, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(y[j, k] - y[i, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(p_x[k] == quicksum(matriz_p[i][j] * x[i, k] for i in equipos for j in matriz_p[i]) for k in fechas)

    m.addConstr(quicksum(y[i, k] for i in equipos for k in fechas) / 2 <= n_fechas * 8 * 0.25)

    m.addConstr(quicksum(y[i, k] for i in equipos for k in fechas) / 2 >= n_fechas * 8 * 0.15)

    
    #m.params.MIPGap = 0.3 #Aceptamos una solucion con gap de 0.3
    m.optimize()

    CALENDARIO = []
    # Print solution
    if m.status == GRB.Status.OPTIMAL:
        solution = m.getAttr('x', match)
        print "Amplitud:", a.X - b.X
        print "Prob:", sum(list(p_x[k].X for k in fechas))
        for k in fechas:
            f = []
            for i in equipos:
                for j in equipos:
                    if solution[i, j, k] > 0:
                        f.append("{}, {}".format(i,j))
            fecha = Fecha(k,f)
            CALENDARIO.append(fecha)
        for k in fechas:
            f = []
            print "\n", "Fecha", k
            #print "\n Fecha", k
            for i in equipos:
                for j in equipos:
                    if solution[i, j, k] > 0:
                        print i,"-", j, " -> ", "LW" if x[i, k].X == 1 else "D" if y[i, k].X == 1 else "AW", matriz_p[i][j], matriz_p[j][i]
                        #print i, j
                        f.append("{}, {}".format(j, i))
                        #print "LW:", x[i, k].X, " D:", y[i, k].X
            fecha = Fecha(k + 15, f)
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




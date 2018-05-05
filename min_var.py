from gurobipy import *
from equipos import nombres as equipos
from schedueling import Fecha, aux

f = {
  ('U. de Chile', 'Colo Colo'): 0.4,
  ('CD San Luis', 'O Higgins'): 0.3,
  ('Colo Colo', 'O Higgins'): 0.4,
  ('O Higgins', 'Colo Colo'): 0.3,
  ('O Higgins', 'U. de Chile'): 0.25,
  ('O Higgins', 'CD San Luis'): 0.4,
  ('Colo Colo', 'CD San Luis'):  0.4,
  ('Colo Colo',  'U. de Chile'): 0.7,
  ('CD San Luis', 'U. de Chile'): 0.3,
  ('CD San Luis', 'Colo Colo'): 0.1,
  ('U. de Chile', 'CD San Luis'): 0.4,
  ('U. de Chile',  'O Higgins'): 0.3,
  ('O Higgins', 'O Higgins'): 0,
  ('CD San Luis', 'CD San Luis'): 0,
  ('Colo Colo', 'Colo Colo'): 0,
  ('U. de Chile', 'U. de Chile'): 0}
e = {
  ('U. de Chile', 'Colo Colo'): 0,
  ('CD San Luis', 'O Higgins'):   0,
  ('Colo Colo', 'O Higgins'):  0,
  ('O Higgins', 'Colo Colo'): 0,
  ('O Higgins', 'U. de Chile'): 0,
  ('O Higgins', 'CD San Luis'): 0,
  ('Colo Colo', 'CD San Luis'):  0,
  ('Colo Colo',  'U. de Chile'): 0,
  ('CD San Luis', 'U. de Chile'): 0,
  ('CD San Luis', 'Colo Colo'): 0,
  ('U. de Chile', 'CD San Luis'): 0,
  ('U. de Chile',  'O Higgins'): 0,
  ('O Higgins', 'O Higgins'): 0,
  ('CD San Luis', 'CD San Luis'): 0,
  ('Colo Colo', 'Colo Colo'): 0,
  ('U. de Chile', 'U. de Chile'): 0}


def min_var(n_fechas, jugados, puntaje_inicial):
    #print "\n Minimizando la varianza a lo loco"
    p0 = puntaje_inicial
    #print p0
    fechas = [i for i in range(1, n_fechas + 1)]
    m = Model("Tournament")

    match = m.addVars(equipos, equipos, fechas, vtype=GRB.BINARY, name="match") #1 si el partido se juega (es factible)
    x = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="x") #1 si el equipo i gana
    y = m.addVars(equipos, fechas, vtype=GRB.BINARY, name="y") #1 si el equipo j gana
    p = m.addVars(equipos, name="p") #puntos equipo i
    a = m.addVar(name="a") #mayor puntaje
    b = m.addVar(name="b") #menor puntaje
    m.setObjective(a - b, GRB.MINIMIZE) #FO


    #RESTRICCIONES

    # No mas de 2 partidos consecutivos de local o visita
    m.addConstrs((quicksum(match[i, j, k + l] for j in equipos for l in [0, 1, 2]) <= 2
                  for i in equipos for k in fechas[:n_fechas - 2]))

    m.addConstrs((quicksum(match[i, j, k] + match[j, i, k] for j in equipos) == 1
                  for i in equipos for k in fechas)) #Todos y solo una vez en cada fecha

    m.addConstrs(match[i, i, k] == 0 for k in fechas for i in equipos) #No jueguen contra si mismos

    m.addConstrs((quicksum(match[i, j, k] for i, j in aux(jugados)) == 0 for k in fechas))

    m.addConstrs(p[i] <= a for i in equipos)

    m.addConstrs(p[i] >= b for i in equipos)

    m.addConstrs(p[i] == p0[i] + quicksum(3 * x[i, k] + y[i, k] for k in fechas) for i in equipos)

    m.addConstrs(match[i, j, k] <= x[i, k] + y[i, k] + x[j, k] + y[j, k] for i in equipos for j in equipos if i != j for k in fechas)

    m.addConstrs(x[i, k] + y[i, k] <= 1 for i in equipos for k in fechas)

    m.addConstrs(y[i, k] - y[j, k] <= 1 - match[i, j, k] for i in equipos for j in equipos if i != j for k in fechas)

    #m.addConstrs(f[i, j] >= 0.2 * x[i, k] for i in equipos for j in equipos for k in fechas)
    #m.addConstrs(e[i, j] >= 0.2 * y[i, k] for i in equipos for j in equipos for k in fechas)

    m.optimize()

    CALENDARIO = []
    # Print solution
    if m.status == GRB.Status.OPTIMAL:
        solution = m.getAttr('x', match)
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
            print ("\n Fecha", k)
            #print "\n Fecha", k
            for i in equipos:
                for j in equipos:
                    if solution[i, j, k] > 0:
                        print (i, j)
                        #print i, j
                        f.append("{}, {}".format(j, i))
                        print ("LW:", x[i, k].X, " D:", y[i, k].X)
                        #print "LW:", x[i, k].X, " D:", y[i, k].X
            fecha = Fecha(k + 15, f)
            CALENDARIO.append(fecha)
        print ("\n PUNTAJES")
        #print "\n PUNTAJES"
        for i in equipos:
            print (i, "{}".format(p[i].X))
        print (a.X, b.X)
        #print a.X, b.X
        for i in equipos:
            for k in fechas:
                if x[i, k].X == 1:
                    print ("W", i, k)
                    #print "W", i, k
                if y[i, k].X == 1:
                    print ("D", i, k)
                    #print "D", i, k
        return CALENDARIO




from schedueling import *
from montecarlo import simulacion_montecarlo
from min_var import min_var
from simulation import simulacion_unica
from equipos import EQUIPOS, nombres


def match_probs(s,team):
    probs ={}
    e1, e2 = s.no_jugados(team)
    for x in e1:
        probs[x.nombre] = s.p_local(team,x)
    for y in e2:
        probs[y.nombre] = 1-s.p_local(y,team)-s.p_empate()
    return probs

def prob_matrix(simulation):
    prob_matrix = {}
    for team in simulation.equipos:
        prob_matrix[team.nombre] = match_probs(simulation,team)
    return prob_matrix
        

def modelo():
    primeras_15_fechas = calendarizacion(15)
    #sim_m = simulacion_montecarlo(primeras_15_fechas, True)
    sim2, s = simulacion_unica(primeras_15_fechas,None,EQUIPOS,None)
    segundas_7_fechas = calendarizacion(7, primeras_15_fechas, sim2)
    s.agregar_fechas(segundas_7_fechas)
    sim2, s = simulacion_unica(primeras_15_fechas,None,EQUIPOS,s)
    #print(s.p_local(s.buscar_equipo('U. La Calera'),s.buscar_equipo('Colo Colo')))
    #print(s.p_local(s.buscar_equipo('Colo Colo'),s.buscar_equipo('U. La Calera')))
    #print(s.buscar_equipo('Colo Colo').jugados)
    #print(s.buscar_equipo('Colo Colo').partidos_visita)
    #print(s.buscar_equipo('Colo Colo').partidos_local)
 

    #problems here Houston
    terceras_5_fechas = min_var(3, s.calendario, sim2, prob_matrix(s))
    s.agregar_fechas(terceras_5_fechas)
    sim2, s = simulacion_unica(primeras_15_fechas,None,EQUIPOS,s)


if __name__ == "__main__" :
    modelo()



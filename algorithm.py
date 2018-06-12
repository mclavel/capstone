from schedueling import *
from montecarlo import simulacion_montecarlo
from min_var import min_var
from simulation import simulacion_unica,crear_simulacion
from equipos import EQUIPOS, nombres
import copy


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
    primeras_15_fechas,calendario_16_30 = calendarizacion(15,invertir=True)
    #sim_m = simulacion_montecarlo(primeras_15_fechas, True)
    resultados, instancia_inicial = crear_simulacion(primeras_15_fechas,EQUIPOS)
    instancia = copy.deepcopy(instancia_inicial)
    calendario_factible = calendarizacion(7, primeras_15_fechas, resultados)
    fechas_15_22 = calendario_factible[:8]
    instancia.agregar_fechas(fechas_15_22[:5])
    fechas_21_22 = fechas_15_22[5:]
    resultados, instancia = simulacion_unica(instancia)
    fechas_23_25 = min_var(3, instancia.calendario, resultados, prob_matrix(instancia))
    fechas_23_24 = fechas_23_25[:2]
    instancia.agregar_fechas(fechas_21_22+fechas_23_24)
    resultados, instancia = simulacion_unica(instancia)
    fechas_26_28 = min_var(3, instancia.calendario, resultados, prob_matrix(instancia))
    fechas_25_27 = fechas_23_25[2:] + fechas_26_28[:2]
    instancia.agregar_fechas(fechas_25_27)
    resultados, instancia = simulacion_unica(instancia)
    fechas_29_30 = min_var(2, instancia.calendario, resultados, prob_matrix(instancia), 0.03)
    fechas_28_30 = fechas_26_28[2:] + fechas_29_30 
    instancia.agregar_fechas(fechas_28_30)
    resultados, instancia = simulacion_unica(instancia)
    #Comparo
    instancia_inicial.agregar_fechas(calendario_16_30)
    resultadosG, instanciaG = simulacion_unica(instancia_inicial)
    
    
    
    """
    fechas_15_22 = calendarizacion(7, primeras_15_fechas, resultados)
    instancia.agregar_fechas(fechas_15_22)
    
    fechas_22_25 = min_var(3, instancia2.calendario, resultados,
                           prob_matrix(instancia2))
    instancia2.agregar_fechas(fechas_22_25)
    resultados, instancia3 = simulacion_unica(instancia2)
    fechas_25_28 = min_var(3, instancia3.calendario, resultados, prob_matrix(instancia3))
    instancia3.agregar_fechas(fechas_25_28)
    print(instancia3.no_jugados(instancia3.buscar_equipo('Colo Colo')))
    fdfdf
    #Chequear por que uso [2:]
    resultados, instancia4 = simulacion_unica(instancia3)
    fechas_28_30 = min_var(2, instancia.calendario, resultados, prob_matrix(instancia4))
    instancia.agregar_fechas(fechas_28_30[3:])
    resultados, instancia = simulacion_unica(instancia)"""
  
    
    #tercerae_3_fechas = min_var(3, s.calendario, sim2, prob_matrix(s))
    #s.agregar_fechas(terceras_5_fechas)
    #sim2, s = simulacion_unica(primeras_15_fechas,None,EQUIPOS,s)


if __name__ == "__main__" :
    modelo()



from schedueling import *
from montecarlo import simulacion_montecarlo
from min_var import min_var
from simulation import simulacion_unica,crear_simulacion
from equipos import EQUIPOS, nombres
import copy


def match_probs(s,team):
    """Dada una simulacion s, calcula para un equipo las probabilidades
    de ganar frente a los equipos que le resta por jugar"""
    probs ={}
    e1, e2 = s.no_jugados(team)
    for x in e1:
        probs[x.nombre] = s.p_local(team,x)
    for y in e2:
        probs[y.nombre] = 1-s.p_local(y,team)-s.p_empate()
    return probs

def prob_matrix(simulation):
    """Calcula todas la probabilidades de los equipos del torneo y
    entrega un diccionario con aquellos datos."""
    prob_matrix = {}
    for team in simulation.equipos:
        prob_matrix[team.nombre] = match_probs(simulation,team)
    return prob_matrix
        

def modelo():
    """Modelo del Capstone: 
        Primero se calendarizan 15 fechas que sean únicamente fatcibles"""
    primeras_15_fechas,calendario_16_30 = calendarizacion(15,invertir=True)
    #Creamos nuestra simulacion
    resultados, instancia_inicial = crear_simulacion(primeras_15_fechas,EQUIPOS)
    #Copiamos la primera parte de la simulación para poder comparar metricas
    instancia = copy.deepcopy(instancia_inicial)
    #Buscamos una calendarizacion factible y que cumpla con el criterio
    #De hacer jugar dos cluster de equipos
    fechas_15_22 = calendarizacion(7, primeras_15_fechas, resultados)
    #Agregamos las fechas a la instancia de simulacion, entregamos
    #Solo entregamos las 5 ya que luego se calenzariza unicamente con 
    #la informacion hasta la fecha 20
    instancia.agregar_fechas(fechas_15_22[:5])
    #Guardamos las otras fechas
    fechas_21_22 = fechas_15_22[5:]
    #Simulamos
    resultados, instancia = simulacion_unica(instancia)
    #Buscamos las proximas 3 fechas segun el modelo de minvar
    fechas_23_25 = min_var(3, instancia.calendario, resultados,
                           prob_matrix(instancia))
    #Nuevamente, solo podemos tomar 2 fechas 1 la guardamos
    fechas_23_24 = fechas_23_25[:2]
    #Agregamos las fechas
    instancia.agregar_fechas(fechas_21_22+fechas_23_24)
    #Simulamos
    resultados, instancia = simulacion_unica(instancia)
    #idem
    fechas_26_28 = min_var(3, instancia.calendario, resultados,
                           prob_matrix(instancia))
    fechas_25_27 = fechas_23_25[2:] + fechas_26_28[:2]
    instancia.agregar_fechas(fechas_25_27)
    resultados, instancia = simulacion_unica(instancia)
    #Buscamos las ultimas fechas a agregar
    fechas_29_30 = min_var(2, instancia.calendario, resultados,
                           prob_matrix(instancia),0.03)
    fechas_28_30 = fechas_26_28[2:] + fechas_29_30 
    instancia.agregar_fechas(fechas_28_30)
    resultados, instancia = simulacion_unica(instancia)

    #Comparo con otra simulacion que es identica hasta la fecha 15 pero
    #luego toma otro tipo de calendarizacion: espejo, repeticion,etc.
    instancia_inicial.agregar_fechas(calendario_16_30)
    resultadosG, instanciaG = simulacion_unica(instancia_inicial,color="red")
    


if __name__ == "__main__" :
    modelo()



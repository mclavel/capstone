from schedueling import *
from montecarlo import simulacion_montecarlo
from min_var import min_var
from simulation import simulacion_unica,crear_simulacion
from equipos import EQUIPOS, nombres
import time
import copy
import os, sys

class HiddenPrints:
    #Clase para ocultar prints
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout


def match_probs(s,team):
    #Calcula en una instancia s las probabilidades de ganar de un equipo(team)
    #Frente a los que les resta por jugar
    probs ={}
    e1, e2 = s.no_jugados(team)
    for x in e1:
        probs[x.nombre] = s.p_local(team,x)
    for y in e2:
        probs[y.nombre] = 1-s.p_local(y,team)-s.p_empate()
    return probs

def prob_matrix(simulation):
    #Obtiene las probabilidades para todos los equipos y entrega un diccionario
    prob_matrix = {}
    for team in simulation.equipos:
        prob_matrix[team.nombre] = match_probs(simulation,team)
    return prob_matrix

def simular_campeonato_actual(cantidad_s = 5000):
    #Se realiza una simulacion de montecarlo con el calendario actual
    #que tiene la ANFP para poder comparar
    anfp_30_fechas = cargar_calendario(archivo_csv='campeonato.csv')
    #resultados, instancia_inicial = crear_simulacion(anfp_30_fechas,EQUIPOS)
    sim_m,a = simulacion_montecarlo(anfp_30_fechas,True,cantidad=cantidad_s)
    print(a)

def imprimir(fecha):
    print ("Tabla de posiciones fecha {}".format(str(fecha)))
    print ("\n")
    
def comparacion_rho(n_iteraciones = 100, rango_rho = 2, rho_inicial =100, rho_final = 101):
    #Se compara rho, el parametro utilizado en el modelo de opt: MIN_VAR
    start_time = time.time()
    comparacion_rho ={}
    for x in range(rango_rho):
        a = 0
        print("{}% done".format(round((x/rango_rho),2)*100))
        for n in range(n_iteraciones):
            try:
                with HiddenPrints():
                    a += modelo(rho_inicial+((rho_final-rho_inicial)/(rango_rho-1) * x))
            except Exception as err:
                print(err)
            comparacion_rho[str(rho_inicial+((rho_final-rho_inicial)/(rango_rho-1) * x))] = a/n_iteraciones
        print(a/n_iteraciones)
        print("\n {} seconds to 1 iteration".format
                  (round(time.time() - start_time, 2)))
    print(comparacion_rho)
    print("\n {} seconds to {} simulations".format
          (round(time.time() - start_time, 2), n_iteraciones * rango_rho))     
        

def modelo(rho=100):
    #Se Crea el modelo
    #FECHA 0: Obtenemos 15 fechas factibles, las imprimimos y luego se simula
    primeras_15_fechas = calendarizacion(15)
    imprimir(15)
    resultados, instancia_inicial = crear_simulacion(primeras_15_fechas,
                                                     EQUIPOS)

    #FECHA 15
    instancia = copy.deepcopy(instancia_inicial)
    cal_factible = calendarizacion(7, primeras_15_fechas, resultados)

    #FECHA 20
    fechas_15_22 = cal_factible[:8]
    instancia.agregar_fechas(fechas_15_22[:5])
    fechas_21_22 = fechas_15_22[5:]
    imprimir(20)
    resultados, instancia = simulacion_unica(instancia)
    cal = min_var(rho, 3, fechas_21_22, instancia.calendario + fechas_21_22, resultados, prob_matrix(instancia), 20,clusters=False)
    if cal is not None:
        fechas_23_25, factible_26_30 = cal
    else:
        print ("Calendarizacion infactible")
        fechas_23_25, factible_26_30 = cal_factible[8:10], cal_factible[10:]

    #FECHA 24
    fechas_23_24 = fechas_23_25[:2]
    instancia.agregar_fechas(fechas_21_22 + fechas_23_24)
    imprimir(24)
    resultados, instancia = simulacion_unica(instancia)
    cal = min_var(rho, 3, fechas_23_25[1:], instancia.calendario + [fechas_23_25[-1]], resultados, prob_matrix(instancia), 24,clusters=False)
    if cal is not None:
        fechas_26_28, factible_29_30 = cal
    else:
        print ("Calendarizacion infactible")
        fechas_26_28, factible_29_30 = factible_26_30[:3], factible_26_30[3:]

    #FECHA 27
    fechas_25_27 = fechas_23_25[2:] + fechas_26_28[:2]
    instancia.agregar_fechas(fechas_25_27)
    imprimir(27)
    resultados, instancia = simulacion_unica(instancia)
    cal = min_var(rho, 2, fechas_26_28[1:], instancia.calendario + [fechas_26_28[-1]], resultados, prob_matrix(instancia), 27, False, 0.033)
    if cal is not None:
        fechas_29_30 = cal
    else:
        print ("Calendarizacion infactible")
        fechas_29_30 = factible_29_30

    #FECHA 30
    fechas_28_30 = fechas_26_28[2:] + fechas_29_30
    instancia.agregar_fechas(fechas_28_30)
    imprimir(30)
    resultados, instancia = simulacion_unica(instancia)
    return instancia.atractividad_por_fecha[str(len(instancia.atractividad_por_fecha))]



if __name__ == "__main__" :
    #comparacion_rho()
    modelo()
    #simular_campeonato_actual()


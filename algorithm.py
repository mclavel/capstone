from schedueling import *
from montecarlo import simulacion_montecarlo
from min_var import min_var
from simulation import simulacion_unica
from equipos import EQUIPOS, nombres


        

def prob_matrix(simulation):
    prob_matrix = {}
    for team in simulation.equipos:
        prob_matrix[team.nombre] = match_probs(team)
    return prob_matrix
        
def potencialmente_interesante(a):
    interesantes = 0
    for j in range(1, len(a)):
        if 1 < a[0].puntaje - a[j].puntaje <= 3:
            interesantes += 1
            print("El partido de {} es interesante porque si gana puede quedar primero".format(a[j].nombre))

        elif a[0].puntaje - a[j].puntaje == 1:
            interesantes += 1
            print("El partido de {} es interesante porque si empata o gana puede quedar primero".format(
                    a[j].nombre))

        elif 1 < a[5].puntaje - a[j].puntaje <= 3:
            interesantes += 1
            print(
                "El partido de {} es interesante porque si gana puede quedar en zona de clasificacion a torneo internacional".format(
                    a[j].nombre))

        elif a[5].puntaje - a[j].puntaje == 1:
            interesantes += 1
            print(
                "El partido de {} es interesante porque si empata o gana  puede quedar en zona de clasificacion a torneo internacional".format(
                    a[j].nombre))

        elif 1 < a[13].puntaje - a[j].puntaje <= 3:
            interesantes += 1
            print(
                "El partido de {} es interesante porque si gana puede salir de posicion de descenso".format(
                    a[j].nombre))

        elif a[13].puntaje - a[j].puntaje == 1:
            interesantes += 1
            print(
                "El partido de {} es interesante porque si empata o gana puede salir de posicion de descenso".format(
                    a[j].nombre))

def modelo():
    primeras_15_fechas = calendarizacion(15)
    sim_m = simulacion_montecarlo(primeras_15_fechas, True)
    print "Simulacion unica:"
    sim2, s = simulacion_unica(primeras_15_fechas, None,EQUIPOS,None)
    sim_2_sorted = sorted(sim2.items(), key=operator.itemgetter(1), reverse=True)
    segundas_7_fechas = calendarizacion(7, primeras_15_fechas, sim_2_sorted)
    s.agregar_fechas(segundas_7_fechas)
    sim2, s = simulacion_unica(primeras_15_fechas,None,EQUIPOS,s)
    #print(s.p_local(s.buscar_equipo('U. La Calera'),s.buscar_equipo('Colo Colo')))
    #print(s.p_local(s.buscar_equipo('Colo Colo'),s.buscar_equipo('U. La Calera')))
    #print(s.buscar_equipo('Colo Colo').jugados)
    #print(s.buscar_equipo('Colo Colo').partidos_visita)
    #print(s.buscar_equipo('Colo Colo').partidos_local)
    #print(s.no_jugados(s.buscar_equipo('Colo Colo')))

    #problems here Houston
    terceras_5_fechas = min_var(5, s.calendario, sim2)


if __name__ == "__main__" :
    modelo()



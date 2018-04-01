from prob import get_matrix, refresh_odds, ODDS, draw_odds, win_odds
from equipos import EQUIPOS
import random


ORD = sorted(EQUIPOS, key=lambda x: x.puntaje, reverse=True)
print(ORD)

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

potencialmente_interesante(ORD)



import random
import time

TAM = 5

GATO = "G"
RATON = "R"
LIBRE = "."

def crear_tablero():#Crear un tablero vacío
    tablero = []
    for fila in range(TAM):
        fila_actual = []
        for col in range(TAM):
            fila_actual.append(LIBRE)
        tablero.append(fila_actual)
    return tablero

def mostrar_tablero(gato, raton): #Mostrar el tablero con las posiciones del gato y el ratón
    tablero = crear_tablero()
    tablero[gato[0]][gato[1]] = GATO
    tablero[raton[0]][raton[1]] = RATON

    for fila in tablero: #Mostrar cada fila del tablero
        print(" ".join(fila))
    print()

def movimientos_posibles(pos):#Generar movimientos posibles
    fila, col = pos
    movimientos = []
    direcciones = [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(1,-1),(-1,1),(1,1)
    ]
    for df, dc in direcciones:#Iterar sobre las direcciones posibles
        nueva_fila = fila + df
        nueva_col = col + dc
        if 0 <= nueva_fila < TAM and 0 <= nueva_col < TAM:
            movimientos.append((nueva_fila, nueva_col))
    return movimientos

def evaluar(gato, raton):#Evaluar la distancia entre el gato y el ratón
    return abs(raton[0] - gato[0]) + abs(raton[1] - gato[1])

def minimax(gato, raton, profundidad, turno_raton):#Algoritmo Minimax
    if gato == raton:
        return -100, gato
    if profundidad == 0:
        return evaluar(gato, raton), raton

    if turno_raton:#Turno del ratón
        mejor_valor = -100
        mejor_movimiento = raton
        for mov in movimientos_posibles(raton):
            valor, _ = minimax(gato, mov, profundidad - 1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
        return mejor_valor, mejor_movimiento

    else:#Turno del gato
        mejor_valor = 100
        mejor_movimiento = gato
        for mov in movimientos_posibles(gato):
            valor, _ = minimax(mov, raton, profundidad - 1, True)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
        return mejor_valor, mejor_movimiento

def mover_raton_minimax(raton, gato):#Mover el ratón usando Minimax
    _, mov = minimax(gato, raton, 3, True)
    return mov

def mover_gato_minimax(gato, raton):#Mover el gato usando Minimax
    _, mov = minimax(gato, raton, 3, False)
    return mov

gato = (4, 4)
raton = (0, 0)

turnos = 0

while turnos < 15:#Límite de turnos
    print("Turno:", turnos + 1)
    mostrar_tablero(gato, raton)

    if gato == raton:
        print("El gato atrapó al ratón")
        break

    if turnos < 1:#Primer movimiento aleatorio del ratón
        raton = random.choice(movimientos_posibles(raton))
    else:
        raton = mover_raton_minimax(raton, gato)

    gato = mover_gato_minimax(gato, raton)

    turnos += 1
    time.sleep(1.5)

if turnos >= 15 and gato != raton:#El ratón escapó
    print("El ratón escapó")
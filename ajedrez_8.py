def imprimir_tablero(tablero):
    for fila in tablero:
        print('\t'.join(fila))
    print('\n')

def guardar_tablero_en_archivo(tablero, nombre_archivo):
    with open(nombre_archivo, 'ab') as archivo:
        for fila in tablero:
            fila_codificada = '\t'.join(fila).encode('utf-8')
            archivo.write(fila_codificada + b'\n')
        archivo.write(b'\n')

def es_movimiento_valido_torre(origen_fila, origen_columna, destino_fila, destino_columna):
    return origen_fila == destino_fila or origen_columna == destino_columna

def es_movimiento_valido_caballo(origen_fila, origen_columna, destino_fila, destino_columna):
    filas = abs(destino_fila - origen_fila)
    columnas = abs(destino_columna - origen_columna)
    return (filas == 2 and columnas == 1) or (filas == 1 and columnas == 2)

def es_movimiento_valido_alfil(origen_fila, origen_columna, destino_fila, destino_columna):
    return abs(destino_fila - origen_fila) == abs(destino_columna - origen_columna)

def es_movimiento_valido_reina(origen_fila, origen_columna, destino_fila, destino_columna):
    return es_movimiento_valido_torre(origen_fila, origen_columna, destino_fila, destino_columna) or \
           es_movimiento_valido_alfil(origen_fila, origen_columna, destino_fila, destino_columna)

def es_movimiento_valido_rey(origen_fila, origen_columna, destino_fila, destino_columna):
    return abs(destino_fila - origen_fila) <= 1 and abs(destino_columna - origen_columna) <= 1

def es_movimiento_valido_peon(origen_fila, origen_columna, destino_fila, destino_columna, tablero):
    # Los peones se mueven hacia adelante y capturan en diagonal
    pieza = tablero[origen_fila][origen_columna]
    direccion = 1 if pieza.islower() else -1

    if (
        (origen_fila + direccion == destino_fila or origen_fila + 2 * direccion == destino_fila)
        and origen_columna == destino_columna
        and tablero[destino_fila][destino_columna] == ' '
    ):
        return True

    if (
        origen_fila + direccion == destino_fila
        and abs(origen_columna - destino_columna) == 1
        and tablero[destino_fila][destino_columna] != ' '
    ):
        return True

    return False

def main():
    nombre_archivo = input("Ingrese el nombre del archivo para guardar la partida: ")

    tablero = [
        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
        [' '] * 8,
        [' '] * 8,
        [' '] * 8,
        [' '] * 8,
        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
        ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
    ]

    guardar_tablero_en_archivo(tablero, nombre_archivo)

    numero_movimiento = 1

    while True:
        imprimir_tablero(tablero)

        decision = input("¿Quieres hacer un movimiento? (Sí/No): ").lower()

        if decision != 'si':
            break

        origen_fila = int(input("Ingrese la fila de la pieza que quiere mover: "))
        origen_columna = int(input("Ingrese la columna de la pieza que quiere mover: "))
        destino_fila = int(input("Ingrese la fila a la que quiere mover la pieza: "))
        destino_columna = int(input("Ingrese la columna a la que quiere mover la pieza: "))

        # Validar el movimiento según la pieza seleccionada
        pieza = tablero[origen_fila][origen_columna]
        movimiento_valido = False

        if pieza == '♜' or pieza == '♖':
            movimiento_valido = es_movimiento_valido_torre(origen_fila, origen_columna, destino_fila, destino_columna)
        elif pieza == '♞' or pieza == '♘':
            movimiento_valido = es_movimiento_valido_caballo(origen_fila, origen_columna, destino_fila, destino_columna)
        elif pieza == '♝' or pieza == '♗':
            movimiento_valido = es_movimiento_valido_alfil(origen_fila, origen_columna, destino_fila, destino_columna)
        elif pieza == '♛' or pieza == '♕':
            movimiento_valido = es_movimiento_valido_reina(origen_fila, origen_columna, destino_fila, destino_columna)
        elif pieza == '♚' or pieza == '♔':
            movimiento_valido = es_movimiento_valido_rey(origen_fila, origen_columna, destino_fila, destino_columna)
        elif pieza == '♟' or pieza == '♙':
            movimiento_valido = es_movimiento_valido_peon(origen_fila, origen_columna, destino_fila, destino_columna, tablero)

        if movimiento_valido:
            tablero[destino_fila][destino_columna] = pieza
            tablero[origen_fila][origen_columna] = ' '

            guardar_tablero_en_archivo(tablero, nombre_archivo)
            numero_movimiento += 1
        else:
            print("Movimiento no válido. Inténtalo de nuevo.")

    movimiento_a_mostrar = int(input("Ingrese el número de movimiento que desea mostrar: "))
    if movimiento_a_mostrar <= numero_movimiento:
        with open(nombre_archivo, 'rb') as archivo:
            lineas = archivo.readlines()
            inicio = (movimiento_a_mostrar - 1) * 9
            fin = inicio + 8
            tablero_mostrado = [linea.decode('utf-8').strip().split('\t') for linea in lineas[inicio:fin]]
            imprimir_tablero(tablero_mostrado)
    else:
        print("Número de movimiento no válido.")

if __name__ == "__main__":
    main()
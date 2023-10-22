import os
import random
import time 
import json

#Limpiar consola
os.system('cls')

class Partida:
    def __init__(self, jugador1, movimiento1, jugador2, movimiento2, ganador, movimientos):
        self.jugador1 = jugador1
        self.movimiento1 = movimiento1
        self.jugador2 = jugador2
        self.movimiento2 = movimiento2
        self.ganador = ganador
        self.movimientos = movimientos
    
    def __str__(self):
        return f"{self.jugador1} ({self.movimiento1}) vs {self.jugador2} ({self.movimiento2}) -> Ganador: {self.ganador} en {self.movimientos} movimientos."

historial_partidas = []

def registrar_partida(jugador1, ficha1, jugador2, ficha2, ganador, movimientos):
    nueva_partida = Partida(jugador1, ficha1, jugador2, ficha2, ganador, movimientos)
    historial_partidas.append(nueva_partida)
    
def mostrar_historial():
    if not historial_partidas:
        print("No hay partidas registradas en el historial.")
        return

    for partida in historial_partidas:
        print(partida)


class Tablero:
    def __init__(self):
        self.casillas = [" "] * 10
        self.partidas_jugadas = 0
        self.puntuacion_jugador = 0
        self.empates = 0
        self.puntuacion_ia = 0
        self.combinaciones_ganadoras = [[1, 2, 3], [4, 5, 6], [7, 8, 9], # Horizontales
                                        [1, 4, 7], [2, 5, 8], [3, 6, 9], # Verticales
                                        [1, 5, 9], [3, 5, 7]]            # Diagonales
        
    def dibuja_tablero(self):
        print("Partidas jugadas: ", self.partidas_jugadas)
        print(f"Puntuación: > Jugador: {self.puntuacion_jugador} | IA: {self.puntuacion_ia}")
        print(f"Empates: > {self.empates} \n")
        print(f"{self.casillas[1]} | {self.casillas[2]} | {self.casillas[3]}")
        print("-" * 10)
        print(f"{self.casillas[4]} | {self.casillas[5]} | {self.casillas[6]}")
        print("-" * 10)
        print(f"{self.casillas[7]} | {self.casillas[8]} | {self.casillas[9]}")
    
    def actualizar_casillas(self, casilla_num, jugador):
        if self.casillas[casilla_num] == " ":
            self.casillas[casilla_num] = jugador
        else:
            raise ValueError("Ya hay una ficha en esa casilla. Elige otra casilla.")
    
    def reiniciar_tablero(self):
        self.casillas = [" "] * 10
        self.partidas_jugadas = 0
        self.puntuacion_jugador = 0
        self.empates = 0
        self.puntuacion_ia = 0

    def ganador(self, jugador):
        for combinaciones in self.combinaciones_ganadoras:
            resultado = all(self.casillas[casilla] == jugador for casilla in combinaciones)
            if resultado:
                return True
        return False
    
    def empate(self):
        casillas_llenas = sum(1 for casilla in self.casillas[1:] if casilla != " ")
        return casillas_llenas == 9
    
    def nueva_partida(self):
        self.casillas = [" "] * 10
        self.partidas_jugadas += 1
        
    def ia_turno(self, jugador):
        try:
            if jugador == "X":
                contrincante = "O"
            else:
                contrincante = "X"
                
            print("\nIA pensando...")
            time.sleep(0.5) 

            # Busca un movimiento ganador
            movimiento_ganador = self.movimiento_ganador(jugador)
            if movimiento_ganador:
                self.actualizar_casillas(movimiento_ganador, jugador)
                return

            # Bloquea al jugador humano
            movimiento_bloqueo = self.movimiento_ganador(contrincante)
            if movimiento_bloqueo:
                self.actualizar_casillas(movimiento_bloqueo, jugador)
                return

            # Ocupa el centro si está disponible
            if self.casillas[5] == " ":
                self.actualizar_casillas(5, jugador)
                return

            # Ocupa una esquina si está disponible
            esquinas_disponibles = [1, 3, 7, 9]
            esquinas_vacias = [esquina for esquina in esquinas_disponibles if self.casillas[esquina] == " "]
            if esquinas_vacias:
                self.actualizar_casillas(random.choice(esquinas_vacias), jugador)
                return random.choice(esquinas_vacias)

            # Ocupa un lado si no hay otras opciones
            lados_disponibles = [2, 4, 6, 8]
            lados_vacios = [lado for lado in lados_disponibles if self.casillas[lado] == " "]
            if lados_vacios:
                self.actualizar_casillas(random.choice(lados_vacios), jugador)
        except Exception as e:
            print(f"Error en la IA mejorada: {e}")
            
    def movimiento_ganador(self, jugador):
        for combinacion in self.combinaciones_ganadoras:
            casillas_jugador = [casilla for casilla in combinacion if self.casillas[casilla] == jugador]
            casillas_vacias = [casilla for casilla in combinacion if self.casillas[casilla] == " "]
            
            if len(casillas_jugador) == 2 and len(casillas_vacias) == 1:
                return casillas_vacias[0]
        
        return None
    
    
    def save_game_state(self):
        data = {
            'casillas': self.casillas,
            'partidas_jugadas': self.partidas_jugadas,
            'puntuacion_jugador': self.puntuacion_jugador,
            'empates': self.empates,
            'puntuacion_ia': self.puntuacion_ia
        }
        with open('game_state.json', 'w') as f:
            json.dump(data, f)
        
    def load_game_state(self):
        try:
            with open('game_state.json', 'r') as f:
                data = json.load(f)
                self.casillas = data['casillas']
                self.partidas_jugadas = data['partidas_jugadas']
                self.puntuacion_jugador = data['puntuacion_jugador']
                self.empates = data['empates']
                self.puntuacion_ia = data['puntuacion_ia']
        except FileNotFoundError:
            pass


tablero = Tablero()
tablero.load_game_state()

def partida_guardada_existe():
    return os.path.exists('game_state.json')
            
def turno_jugador():
    while True:
        try:
            jugador_humano = int(input("\n Jugador: Introduce un número del 1 al 9: >"))
            if 1 <= jugador_humano <= 9 and tablero.casillas[jugador_humano] == " ":
                return jugador_humano
            else:
                if not 1 <= jugador_humano <= 9:
                    print("Error: Debes ingresar un número del 1 al 9. >")
                else:
                    print("Error: La casilla seleccionada está ocupada. Elige otra casilla. >")
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            
def partida_nueva():
    while True:
        decision = input("¿Te atreves a jugar otra partida? [S | N] >").upper()
        if decision in ["S", "N"]:
            return decision
        else:
            print("Error: Debes ingresar 'S' para sí, 'N' para no >")

def titulo_juego():
    print("¡Bienvenido a The Tic-Tac-Toe GAME!")
    print("-" * 36 + "\n")
    
def limpia_pantalla():
    os.system("cls")
    titulo_juego()
    
def verificar_partida_guardada():
    if os.path.exists('game_state.json'):
        while True:
            respuesta = input('Se encontró una partida guardada.\n'
                              '¿Deseas cargar la partida anterior? [S | N] > ').lower()
            if respuesta == 's':
                with open('game_state.json', 'r') as file:
                    data = json.load(file)
                return data
            elif respuesta == 'n':
                try:
                    os.remove('game_state.json')  # Intenta eliminar la partida guardada.
                    print("Partida anterior eliminada exitosamente.")
                    tablero.reiniciar_tablero()  # Reinicia el tablero
                    break
                except PermissionError:
                    print("Error al eliminar la partida anterior. "
                          "El archivo está siendo utilizado por otro proceso.")
                    # Aquí puedes decidir si deseas volver a preguntar o simplemente continuar.
                    break
            else:
                print("Respuesta no válida. Por favor, responde con 'S' o 'N'.")
    return None
    
def elegir_ficha():
    """
    Permite al jugador elegir ser "X" o "O".
    Retorna una tupla (ficha_jugador_humano, ficha_ia).
    """
    while True:
        ficha = input("\n¿Quieres ser 'X' o 'O'? > ").upper()
        limpia_pantalla()
        if ficha == "X":
            return ("X", "O")
        elif ficha == "O":
            return ("O", "X")
        else:
            print("Error: Debes elegir 'X' o 'O'.")
def menu():
    while True:
        limpia_pantalla()
        
        print("1. Jugar")
        print("2. Mostrar historial de partidas")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            juego_principal()
        elif opcion == "2":
            mostrar_historial()
            input("\nPresiona Enter para volver al menú.")
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def juego_principal():
    
    limpia_pantalla()

    # Elegir ficha
    ficha_jugador_humano, ficha_ia = elegir_ficha()
    
    # Mostrar Tablero
    tablero.dibuja_tablero()

    # Si el jugador elige 'O', la IA juega primero.
    if ficha_jugador_humano == "O":
        tablero.ia_turno(ficha_ia)
        limpia_pantalla()
        tablero.dibuja_tablero()

    movimientos = 0

    while not (tablero.ganador(ficha_jugador_humano) or tablero.ganador(ficha_ia) or tablero.empate()):
            movimientos += 1
            # Turno del jugador humano
            jugador_humano = turno_jugador()
            tablero.actualizar_casillas(jugador_humano, ficha_jugador_humano)
            limpia_pantalla()
            tablero.dibuja_tablero()

            # Comprobar si el jugador humano ganó
            if tablero.ganador(ficha_jugador_humano):
                print("\n¡Felicidades! Has ganado.")
                tablero.puntuacion_jugador += 1
                registrar_partida("Jugador", ficha_jugador_humano, "IA", ficha_ia, ficha_jugador_humano, movimientos)
                break

            # Comprobar empate
            if tablero.empate():
                print("\n¡Es un empate!")
                tablero.empates += 1
                registrar_partida("Jugador", ficha_jugador_humano, "IA", ficha_ia, "Empate", movimientos)
                break

            movimientos += 1

            # Turno de la IA
            movimiento_ia = tablero.ia_turno(ficha_ia)
            limpia_pantalla()
            tablero.dibuja_tablero()

            # Comprobar si la IA ganó
            if tablero.ganador(ficha_ia):
                print("\nLa IA ha ganado.")
                tablero.puntuacion_ia += 1
                registrar_partida("Jugador", ficha_jugador_humano, "IA", ficha_ia, "IA", movimientos)
                break
            
            # Comprobar empate
            if tablero.empate():
                print("\n¡Es un empate!")
                tablero.empates += 1
                registrar_partida("Jugador", ficha_jugador_humano, "IA", ficha_ia, "Empate", movimientos)
                break

    # Preguntar si se quiere jugar otra partida
    tablero.save_game_state()
    decision = partida_nueva()
    if decision == "N":
        return
    else:
        tablero.nueva_partida()

verificar_partida_guardada()
menu()               

import unittest
from tic_tac_toe import Tablero

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        self.tablero = Tablero()

    def test_inicializacion_tablero(self):
        self.assertEqual(self.tablero.casillas, [" "] * 10)
        self.assertEqual(self.tablero.partidas_jugadas, 0)
        self.assertEqual(self.tablero.puntuacion_jugador, 0)
        self.assertEqual(self.tablero.empates, 0)
        self.assertEqual(self.tablero.puntuacion_ia, 0)

    def test_actualizar_casillas(self):
        self.tablero.actualizar_casillas(1, "X")
        self.assertEqual(self.tablero.casillas[1], "X")

    def test_ganador_horizontal_X(self):
        self.tablero.casillas[1:4] = ["X"] * 3
        self.assertTrue(self.tablero.ganador("X"))

    def test_ganador_vertical_X(self):
        for i in [1, 4, 7]:
            self.tablero.casillas[i] = "X"
        self.assertTrue(self.tablero.ganador("X"))

    def test_ganador_diagonal_X(self):
        for i in [1, 5, 9]:
            self.tablero.casillas[i] = "X"
        self.assertTrue(self.tablero.ganador("X"))

    def test_ganador_horizontal_O(self):
        self.tablero.casillas[1:4] = ["O"] * 3
        self.assertTrue(self.tablero.ganador("O"))

    def test_ganador_vertical_O(self):
        for i in [1, 4, 7]:
            self.tablero.casillas[i] = "O"
        self.assertTrue(self.tablero.ganador("O"))

    def test_ganador_diagonal_O(self):
        for i in [3, 5, 7]:
            self.tablero.casillas[i] = "O"
        self.assertTrue(self.tablero.ganador("O"))

    def test_tablero_vacio(self):
        self.assertFalse(self.tablero.ganador("X"))
        self.assertFalse(self.tablero.ganador("O"))
        self.assertFalse(self.tablero.empate())

    def test_empate(self):
        self.tablero.casillas[1:] = ["X", "X", "O", "X", "O", "X", "O", "X", "O", "X"]
        self.assertTrue(self.tablero.empate())

    def test_movimiento_ganador(self):
        self.tablero.casillas[1:3] = ["X", "X"]
        self.assertEqual(self.tablero.movimiento_ganador("X"), 3)
        
    def test_reiniciar_tablero(self):
        self.tablero.casillas[1] = "X"
        self.tablero.reiniciar_tablero()
        self.assertEqual(self.tablero.casillas, [" "] * 10)
        self.assertEqual(self.tablero.partidas_jugadas, 0)
        self.assertEqual(self.tablero.puntuacion_jugador, 0)
        self.assertEqual(self.tablero.empates, 0)
        self.assertEqual(self.tablero.puntuacion_ia, 0)


if __name__ == "__main__":
    unittest.main()

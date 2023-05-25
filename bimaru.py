# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0
    boats = {1 : 4, 2 : 3, 3 : 2, 4 : 1} # Barcos disponíveis
    boats_possible_actions = {1 : [], 2 : [], 3 : [], 4 : []}

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, rows, columns, grid) -> None:
        self.rows = rows
        self.columns = columns
        self.grid = grid

    def __str__(self) -> str:
        string = ""
        for i in range(10):
            string += ' '.join(self.grid[i]) + '   ' + str(self.rows[i]) + '\n'
        string += '\n'
        for i in range(10):
            string += str(self.columns[i]) + ' '
        return string

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or col < 0 or row > 9 or col > 9 or self.grid[row][col] == '.':
            return None
        return self.grid[row][col]
    
    def is_empty(self, row: int, col: int) -> bool:
        """ Devolve True se a posição estiver vazia, False caso contrário."""
        if row < 0 or col < 0 or row > 9 or col > 9:
            return False
        return self.grid[row][col] == '.'
    
    def set_value(self, row: int, col: int, value: str) -> None:
        """Define o valor na respetiva posição do tabuleiro."""
        if row < 0 or col < 0 or row > 9 or col > 9:
            return
        self.grid[row][col] = value

    def adjacent_vertical_values(self, row: int, col: int):# -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int):# -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col - 1), self.get_value(row + 1, col + 1))

    def get_row_pieces(self, row : int) -> int:
        """Devolve o número de peças na linha."""
        return 10 - self.grid[row].count('.') - self.grid[row].count('W') - self.grid[row].count('w')

    def get_column_pieces(self, col : int) -> int:
        """Devolve o número de peças na coluna."""
        return 10 - sum(1 for row in self.grid if row[col] in ('.', 'W', 'w'))
    
    def get_free_row_positions(self, row : int) -> int:
        """Devolve o número de posições livres na linha."""
        return self.grid[row].count('.')
    
    def get_free_column_positions(self, col : int) -> int:
        """Devolve o número de posições livres na coluna."""
        return sum(1 for row in self.grid if row[col] == '.')

    def is_row_complete(self, row : int) -> bool:
        """Devolve True se a linha estiver completa e False caso contrário."""
        return self.get_row_pieces(row) == self.rows[row]
    
    def is_column_complete(self, col : int) -> bool:
        """Devolve True se a coluna estiver completa e False caso contrário."""
        return self.get_column_pieces(col) == self.columns[col]

    def possible_n_boat_actions(self, n : int) -> list:
        """Devolve uma lista com as posições livres para colocar um barco de tamanho n."""
        actions = []

        for i in range(10):
            if self.get_free_row_positions(i) < n:
                continue
            for j in range(10 - n + 1):
                if self.get_value(i, j) in ('L', None) and \
                    self.get_value(i, j+n-1) in ('R', None) and \
                    self.get_value(i, j-1) in ('W', 'w', None) and \
                    self.get_value(i, j+n) in ('W', 'w', None) and \
                    self.get_value(i, j-2) != 'L' and \
                    self.get_value(i, j+n+1) != 'R':

                    if n > 2 and self.get_value(i, j+1) in ('M', None):
                        if n > 3 and self.get_value(i, j+2) in ('M', None):
                            actions += [((i, j), n, 'H')]
 
        for j in range(10):
            if self.get_free_column_positions(j) < n:
                continue
            for i in range(10 - n + 1):
                if self.get_value(i, j) in ('T', None) and \
                    self.get_value(i+n-1, j) in ('B', None) and \
                    self.get_value(i-1, j) in ('W', 'w', None) and \
                    self.get_value(i+n, j) in ('W', 'w', None) and \
                    self.get_value(i-2, j) != 'T' and \
                    self.get_value(i+n+1, j) != 'B':
                    
                    if n > 2 and self.get_value(i+1, j) in ('M', None):
                        if n > 3 and self.get_value(i+2, j) in ('M', None):
                            actions += [((i, j), n, 'V')]

        return actions

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        rows = sys.stdin.readline().split()[1:]
        rows = [eval(row) for row in rows]

        columns = sys.stdin.readline().split()[1:]
        columns = [eval(col) for col in columns]
        
        hints = eval(sys.stdin.readline().split()[0])

        grid = [['.'] * 10 for _ in range(10)]

        for _ in range(hints):
            hint = sys.stdin.readline().split()
            row = eval(hint[1])
            col = eval(hint[2])
            grid[row][col] = hint[3]

        return Board(rows, columns, grid)


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        self.initial_clear()
        self.initial_possible_actions()
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        for n in range(4, 0, -1):
            if state.boats[n] > 0:
                return state.boats_possible_actions(n)
        # TODO se sair do for loop estão todos colocados

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        # action = (row, col, boat, orientation)
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        for _ in range(10):
            if not state.board.is_row_complete() or not state.board.is_column_complete():
                return False
        
        for number in state.boats:
            if number > 0:
                return False
        # TODO verificar se as águas estão todas (?)
        
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    def initial_clear(self) -> None:
        board = self.initial.board
        
        # Preencher linhas e colunas maximizadas com água
        for i in range(10):
            if board.is_row_complete(i):
                for j in range(10):
                    if board.is_empty(i, j):
                        board.set_value(i, j, 'w')
            if board.is_column_complete(i):
                for j in range(10):
                    if board.is_empty(j ,i):
                        board.set_value(j, i, 'w')
        
        # Rodear barcos com água
        neighbours = []
        M_positions = []
        for i in range(10): # Encontrar posições triviais para colocar águas
            for j in range(10):
                if board.grid[i][j] == 'C':
                    neighbours += [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]
                if board.grid[i][j] == 'T':
                    neighbours += [(i-1, j), (i-1, j-1), (i, j-1), (i+1, j-1), (i+2, j-1), (i-1, j+1), (i, j+1), (i+1, j+1), (i+2, j+1)]
                if board.grid[i][j] == 'L':
                    neighbours += [(i, j-1), (i-1, j-1), (i-1, j), (i-1, j+1), (i-1, j+2), (i+1, j-1), (i+1, j), (i+1, j+1), (i+1, j+2)]
                if board.grid[i][j] == 'B':
                    neighbours += [(i+1, j), (i+1, j-1), (i, j-1), (i-1, j-1), (i-2, j-1), (i+1, j+1), (i, j+1), (i-1, j+1), (i-2, j+1)]
                if board.grid[i][j] == 'R':
                    neighbours += [(i, j+1), (i-1, j+1), (i-1, j), (i-1, j-1), (i-1, j-2), (i+1, j+1), (i+1, j), (i+1, j-1), (i+1, j-2)]
                if board.grid[i][j] == 'M':
                    neighbours += [(i-1, j-1), (i+1, j-1), (i+1, j+1), (i-1, j+1)]
                    M_positions += [(i, j)]
        
        for (neighbour_i, neighbour_j) in neighbours:
            if board.is_empty(neighbour_i, neighbour_j):
                board.set_value(neighbour_i, neighbour_j, 'w')
        neighbours = []
        
        for (i, j) in M_positions: # Encontrar posições triviais ao redor de peças centrais
            if i == 0 or board.grid[i-1][j] in ("W", "w"):
                neighbours += [(i+1, j-2), (i+1, j), (i+1, j+2)]
            if i == 10 or board.grid[i+1][j] in ("W", "w"):
                neighbours += [(i-1, j-2), (i-1, j), (i-1, j+2)]
            if j == 0 or board.grid[i][j-1] in ("W", "w"):
                neighbours += [(i-2, j+1), (i, j+1), (i+2, j+1)]
            if j == 10 or board.grid[i][j+1] in ("W", "w"):
                neighbours += [(i-2, j-1), (i, j-1), (i+2, j-1)]
        
        for (neighbour_i, neighbour_j) in neighbours:
            if board.is_empty(neighbour_i, neighbour_j):
                board.set_value(neighbour_i, neighbour_j, 'w')
    
    def initial_possible_actions(self) -> None:
        for i in range(1, 5):
            self.initial.boats_possible_actions[i] = board.possible_n_boat_actions(i)

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    print(board, '\n')
    problem = Bimaru(board)
    s0 = BimaruState(board)
    print(board)

    n = 4
    print(f"\n### {n}-boat ###")
    for action in s0.boats_possible_actions[n]:
        print(action)

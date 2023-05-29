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

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    boats = {1 : 4, 2 : 3, 3 : 2, 4 : 1} # Barcos disponíveis

    def __init__(self, rows, columns, grid) -> None:
        self.rows = rows
        self.columns = columns
        self.grid = grid

    def __str__(self) -> str:
        string = ""

        grid = [[v for v in row] for row in self.grid]
        for i in range(10):
            for j in range(10):
                if grid[i][j] == 'w':
                    grid[i][j] = '.'
        
        # Testes
        for i in range(10):
            string += ' '.join(grid[i]) + '   ' + str(self.rows[i]) + '\n'
        for i in range(10):
            string += str(self.columns[i]) + ' '
        string += '\n'

        # Mooshak
        string = '\n'.join([''.join(row) for row in grid])
    
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
        if value != 'w':
            self.rows[row] -= 1
            self.columns[col] -= 1

    def adjacent_vertical_values(self, row: int, col: int):# -> (str, str): TODO
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int):# -> (str, str): TODO
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
        return self.rows[row] == 0
    
    def is_column_complete(self, col : int) -> bool:
        """Devolve True se a coluna estiver completa e False caso contrário."""
        return self.columns[col] == 0

    def possible_n_boat_actions(self, n : int) -> list:
        """Devolve uma lista com as posições livres para colocar um barco de tamanho n."""
        actions = []

        if n == 1:
            for i in range(10):
                if n > self.rows[i]:
                    continue
                for j in range(10):
                    valid = True
                    if n > self.columns[j]:
                        continue
                    if self.get_value(i, j) == None:
                        for a in range(i-1, i+2):
                            for b in range(j-1, j+2):
                                if self.get_value(a, b) not in ('W', 'w', None):
                                    valid = False
                        if valid:
                            actions += [((i, j), n, 'H')]
            return actions

        for i in range(10):
            for j in range(10 - n + 1):
                valid = True
                new_in_row = n
                new_in_col = [1] * n
                if self.get_value(i, j) in ('L', None) and \
                    self.get_value(i, j+n-1) in ('R', None) and \
                    self.get_value(i, j-1) in ('W', 'w', None) and \
                    self.get_value(i, j+n) in ('W', 'w', None) and \
                    self.get_value(i, j-2) != 'L' and \
                    self.get_value(i, j+n+1) != 'R':

                    if self.get_value(i, j) == 'L':
                        new_in_row -= 1
                        new_in_col[0] = 0
                    if self.get_value(i, j+n-1) == 'R':
                        new_in_row -= 1
                        new_in_col[n-1] = 0

                    if n > 2:
                        if self.get_value(i, j+1) not in ('M', None):
                            continue
                        if self.get_value(i, j+1) == 'M':
                            new_in_row -= 1
                            new_in_col[1] = 0
                    if n > 3:
                        if self.get_value(i, j+2) not in ('M', None):
                            continue
                        if self.get_value(i, j+2) == 'M':
                            new_in_row -= 1
                            new_in_col[2] = 0

                    if self.rows[i] - new_in_row < 0:
                        continue
                    for col in range(j, j+n):
                        if self.columns[col] - new_in_col[col - j] < 0:
                            valid = False
                    
                    if valid: actions += [((i, j), n, 'H')]

        for j in range(10):
            for i in range(10 - n + 1):
                valid = True
                new_in_row = [1] * n
                new_in_col = n
                if self.get_value(i, j) in ('T', None) and \
                    self.get_value(i+n-1, j) in ('B', None) and \
                    self.get_value(i-1, j) in ('W', 'w', None) and \
                    self.get_value(i+n, j) in ('W', 'w', None) and \
                    self.get_value(i-2, j) != 'T' and \
                    self.get_value(i+n+1, j) != 'B':
                    
                    if self.get_value(i, j) == 'T':
                        new_in_col -= 1
                        new_in_row[0] = 0
                    if self.get_value(i+n-1, j) == 'B':
                        new_in_col -= 1
                        new_in_row[n-1] = 0

                    if n > 2:
                        if self.get_value(i+1, j) not in ('M', None):
                            continue
                        if self.get_value(i+1, j) == 'M':
                            new_in_col -= 1
                            new_in_row[1] = 0
                    if n > 3:
                        if self.get_value(i+2, j) not in ('M', None):
                            continue
                        if self.get_value(i+2, j) == 'M':
                            new_in_col -= 1
                            new_in_row[2] = 0

                    if self.columns[j] - new_in_col < 0:
                        continue
                    for row in range(i, i+n):
                        if self.rows[row] - new_in_row[row - i] < 0:
                            valid = False
                    
                    if valid: actions += [((i, j), n, 'V')]

        return actions
    
    def set_n_boat(self, row : int, col : int, n : int, orientation : str) -> None:
        """Insere um barco de tamanho n a começar nas coordenadas (row, col),
        com orientação horizontal ou vertical."""
        if n == 1:
            if self.get_value(row, col)         == None: self.set_value(row, col, 'c')
        elif n == 2:
            if orientation == 'H':
                if self.get_value(row, col)     == None: self.set_value(row, col, 'l')
                if self.get_value(row, col + 1) == None: self.set_value(row, col + 1, 'r')
            elif orientation == 'V':
                if self.get_value(row, col)     == None: self.set_value(row, col, 't')
                if self.get_value(row + 1, col) == None: self.set_value(row + 1, col, 'b')
        elif n == 3:
            if orientation == 'H':
                if self.get_value(row, col)     == None: self.set_value(row, col, 'l')
                if self.get_value(row, col + 1) == None: self.set_value(row, col + 1, 'm')
                if self.get_value(row, col + 2) == None: self.set_value(row, col + 2, 'r')
            elif orientation == 'V':
                if self.get_value(row, col)     == None: self.set_value(row, col, 't')
                if self.get_value(row + 1, col) == None: self.set_value(row + 1, col, 'm')
                if self.get_value(row + 2, col) == None: self.set_value(row + 2, col, 'b')
        elif n == 4:
            if orientation == 'H':
                if self.get_value(row, col)     == None: self.set_value(row, col, 'l')
                if self.get_value(row, col + 1) == None: self.set_value(row, col + 1, 'm')
                if self.get_value(row, col + 2) == None: self.set_value(row, col + 2, 'm')
                if self.get_value(row, col + 3) == None: self.set_value(row, col + 3, 'r')
            elif orientation == 'V':
                if self.get_value(row, col)     == None: self.set_value(row, col, 't')
                if self.get_value(row + 1, col) == None: self.set_value(row + 1, col, 'm')
                if self.get_value(row + 2, col) == None: self.set_value(row + 2, col, 'm')
                if self.get_value(row + 3, col) == None: self.set_value(row + 3, col, 'b')
        else: print("PROBLEMA no set_n_boat") # TODO remover

        if orientation == 'H':
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + n + 1):
                    if self.get_value(i, j) == None: self.set_value(i, j, 'w')
        elif orientation == 'V':
            for j in range(col - 1, col + 2):
                for i in range(row - 1, row + n + 1):
                    if self.get_value(i, j) == None: self.set_value(i, j, 'w')
        else: print("PROBLEMA no set_n_boat") # TODO remover


    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        Mooshak = True

        if Mooshak:
            rows = sys.stdin.readline().split()[1:]
        else:
            f = open("instances/instance01.txt", "r")
            rows = f.readline().split()[1:]
        
        rows = [eval(row) for row in rows]

        if Mooshak:
            columns = sys.stdin.readline().split()[1:]
        else:
            columns = f.readline().split()[1:]
        
        columns = [eval(col) for col in columns]
        
        if Mooshak:
            hints = eval(sys.stdin.readline().split()[0])
        else:
            hints = eval(f.readline().split()[0])

        grid = [['.'] * 10 for _ in range(10)]

        for _ in range(hints):
            if Mooshak:
                hint = sys.stdin.readline().split()
            else:
                hint = f.readline().split()
            row = eval(hint[1])
            col = eval(hint[2])
            grid[row][col] = hint[3]

        return Board(rows, columns, grid)


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        self.initial_clear()
        self.initial_boats()

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        for n in range(4, 0, -1):
            if state.board.boats[n] > 0:
                return state.board.possible_n_boat_actions(n)
        return []

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        i = action[0][0]
        j = action[0][1]
        n = action[1]
        orientation = action[2]

        board = Board([v for v in state.board.rows], [v for v in state.board.columns], [[v for v in row] for row in state.board.grid])
        board.set_n_boat(i, j, n, orientation)
        board.boats = {i : state.board.boats[i] for i in state.board.boats.keys()}
        board.boats[n] -= 1

        new_state = BimaruState(board)

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        for i in range(10):
            if not state.board.is_row_complete(i) or not state.board.is_column_complete(i):
                return False
        
        for number in state.board.boats.values():
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
        
        # Rodear peças com água
        neighbours = []
        M_positions = []
        for i in range(10): # Encontrar posições triviais para colocar águas
            if board.is_row_complete(i):
                continue
            for j in range(10):
                if board.is_column_complete(j):
                    continue
                board.rows[i] -= 1
                board.columns[j] -= 1
                if board.get_value(i, j) == 'C':
                    neighbours += [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]
                elif board.get_value(i, j) == 'T':
                    neighbours += [(i-1, j), (i-1, j-1), (i, j-1), (i+1, j-1), (i+2, j-1), (i-1, j+1), (i, j+1), (i+1, j+1), (i+2, j+1)]
                elif board.get_value(i, j) == 'L':
                    neighbours += [(i, j-1), (i-1, j-1), (i-1, j), (i-1, j+1), (i-1, j+2), (i+1, j-1), (i+1, j), (i+1, j+1), (i+1, j+2)]
                elif board.get_value(i, j) == 'B':
                    neighbours += [(i+1, j), (i+1, j-1), (i, j-1), (i-1, j-1), (i-2, j-1), (i+1, j+1), (i, j+1), (i-1, j+1), (i-2, j+1)]
                elif board.get_value(i, j) == 'R':
                    neighbours += [(i, j+1), (i-1, j+1), (i-1, j), (i-1, j-1), (i-1, j-2), (i+1, j+1), (i+1, j), (i+1, j-1), (i+1, j-2)]
                elif board.get_value(i, j) == 'M':
                    neighbours += [(i-1, j-1), (i+1, j-1), (i+1, j+1), (i-1, j+1)]
                    M_positions += [(i, j)]
                else:
                    board.rows[i] += 1
                    board.columns[j] += 1
        
        for (neighbour_i, neighbour_j) in neighbours:
            if board.is_empty(neighbour_i, neighbour_j):
                board.set_value(neighbour_i, neighbour_j, 'w')
        neighbours = []
        
        for (i, j) in M_positions: # Encontrar posições triviais ao redor de peças centrais
            if i == 0 or board.get_value(i-1, j) in ("W", "w"):
                neighbours += [(i+1, j-2), (i+1, j), (i+1, j+2)]
            if i == 10 or board.get_value(i+1, j) in ("W", "w"):
                neighbours += [(i-1, j-2), (i-1, j), (i-1, j+2)]
            if j == 0 or board.get_value(i, j-1) in ("W", "w"):
                neighbours += [(i-2, j+1), (i, j+1), (i+2, j+1)]
            if j == 10 or board.get_value(i, j+1) in ("W", "w"):
                neighbours += [(i-2, j-1), (i, j-1), (i+2, j-1)]
        
        for (neighbour_i, neighbour_j) in neighbours:
            if board.is_empty(neighbour_i, neighbour_j):
                board.set_value(neighbour_i, neighbour_j, 'w')
        # TODO tirar a repeticao de codigo anterior (?) e meter isto a correr de novo sempre que for feita alguma alteracao
        
        # Preencher linhas e colunas maximizadas com água
        for a in range(10):
            if board.is_row_complete(a):
                for b in range(10):
                    if board.is_empty(a, b):
                        board.set_value(a, b, 'w')
            if board.is_column_complete(a):
                for b in range(10):
                    if board.is_empty(b ,a):
                        board.set_value(b, a, 'w')
    
    def initial_boats(self) -> None:
        board = self.initial.board
        
        for i in range(10):
            for j in range(10):
                if board.get_value(i, j) == 'C':
                    board.boats[1] -= 1
                for n in range(2, 5):
                    if board.get_value(i, j) == 'L':
                        if board.get_value(i, j+n-1) == 'R':
                            if n > 2 and board.get_value(i, j+1) != 'M':
                                continue
                            if n > 3 and board.get_value(i, j+2) != 'M':
                                continue
                            board.boats[n] -= 1
                    elif board.get_value(i, j) == 'T':
                        if board.get_value(i+n-1, j) == 'B':
                            if n > 2 and board.get_value(i+1, j) != 'M':
                                continue
                            if n > 3 and board.get_value(i+2, j) != 'M':
                                continue
                            board.boats[n] -= 1

    # TODO: outros metodos da classe
    # TODO: rever incoerencia na utilizacao de (i, j) e (row, col)


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    # print(board, '\n')
    problem = Bimaru(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, sep = "")
    # print("Is goal?", problem.goal_test(goal_node.state))
    # print("Solution:\n", goal_node.state.board, sep="")

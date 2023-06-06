# bimaru.py: Projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 51:
# 102763 Afonso da Conceição Ribeiro
# 102756 Miguel Lopes Ramos do Monte e Freitas


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


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    # Dicionário que faz corresponder, a cada tamanho n, o número de barcos.
    boats = {1 : 4, 2 : 3, 3 : 2, 4 : 1}

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

        string = '\n'.join([''.join(row) for row in grid])

        return string

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or col < 0 or row > 9 or col > 9 or self.grid[row][col] == '.':
            return None
        return self.grid[row][col]

    def is_empty(self, row: int, col: int) -> bool:
        """Devolve True se a posição estiver vazia, False caso contrário."""
        if row < 0 or col < 0 or row > 9 or col > 9:
            return False
        return self.grid[row][col] == '.'

    def set_value(self, row: int, col: int, value: str) -> None:
        """Define o valor na respetiva posição do tabuleiro e, caso o valor seja
        uma peça, decrementa o número de peças restantes na linha e na coluna."""
        if row < 0 or col < 0 or row > 9 or col > 9:
            return
        self.grid[row][col] = value
        if value != 'w':
            self.rows[row] -= 1
            self.columns[col] -= 1

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # TODO
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # TODO
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col - 1), self.get_value(row + 1, col + 1))

    def is_row_complete(self, row : int) -> bool:
        """Devolve True se a linha estiver completa e False caso contrário."""
        return self.rows[row] == 0

    def is_column_complete(self, col : int) -> bool:
        """Devolve True se a coluna estiver completa e False caso contrário."""
        return self.columns[col] == 0

    def set_row_water(self, row : int) -> None:
        """Preenche as posições livres da linha com água."""
        for col in range(10):
            if self.get_value(row, col) == None: self.set_value(row, col, 'w')

    def set_column_water(self, col : int) -> None:
        """Preenche as posições livres da coluna com água."""
        for row in range(10):
            if self.get_value(row, col) == None: self.set_value(row, col, 'w')

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
                        for a in range(i - 1, i + 2):
                            for b in range(j - 1, j + 2):
                                if self.get_value(a, b) not in ('W', 'w', None):
                                    valid = False
                        if valid:
                            actions += [((i, j), n, 'H')]
            return actions

        for j in range(10 - n + 1):
            for i in range(10):
                valid = True
                new_in_row = n
                new_in_col = [1] * n
                if  self.get_value(i, j)     in ('L', None)      and \
                    self.get_value(i, j+n-1) in ('R', None)      and \
                    self.get_value(i, j-1)   in ('W', 'w', None) and \
                    self.get_value(i, j+n)   in ('W', 'w', None) and \
                    self.get_value(i, j-2)   != 'L'              and \
                    self.get_value(i, j+n+1) != 'R':

                    if self.get_value(i, j)     == 'L':
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

                    if valid: actions = [((i, j), n, 'H')] + actions

        for i in range(10 - n + 1):
            for j in range(10):
                valid = True
                new_in_row = [1] * n
                new_in_col = n
                if  self.get_value(i, j)     in ('T', None)      and \
                    self.get_value(i+n-1, j) in ('B', None)      and \
                    self.get_value(i-1, j)   in ('W', 'w', None) and \
                    self.get_value(i+n, j)   in ('W', 'w', None) and \
                    self.get_value(i-2, j)   != 'T'              and \
                    self.get_value(i+n+1, j) != 'B':

                    if self.get_value(i, j)     == 'T':
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

                    if valid: actions = [((i, j), n, 'V')] + actions

        return actions


    def set_n_boat(self, row : int, col : int, n : int, orientation : str) -> None:
        """Insere um barco de tamanho n a começar nas coordenadas (row, col),
        com orientação horizontal ou vertical."""
        if n == 1:
            if self.get_value(row, col)         == None: self.set_value(row, col,     'c')

        elif n == 2:
            if orientation == 'H':
                if self.get_value(row, col)     == None: self.set_value(row, col,     'l')
                if self.get_value(row, col + 1) == None: self.set_value(row, col + 1, 'r')
            elif orientation == 'V':
                if self.get_value(row, col)     == None: self.set_value(row,     col, 't')
                if self.get_value(row + 1, col) == None: self.set_value(row + 1, col, 'b')

        elif n == 3:
            if orientation == 'H':
                if self.get_value(row, col)     == None: self.set_value(row, col,     'l')
                if self.get_value(row, col + 1) == None: self.set_value(row, col + 1, 'm')
                if self.get_value(row, col + 2) == None: self.set_value(row, col + 2, 'r')
            elif orientation == 'V':
                if self.get_value(row, col)     == None: self.set_value(row,     col, 't')
                if self.get_value(row + 1, col) == None: self.set_value(row + 1, col, 'm')
                if self.get_value(row + 2, col) == None: self.set_value(row + 2, col, 'b')

        elif n == 4:
            if orientation == 'H':
                if self.get_value(row, col)     == None: self.set_value(row, col,     'l')
                if self.get_value(row, col + 1) == None: self.set_value(row, col + 1, 'm')
                if self.get_value(row, col + 2) == None: self.set_value(row, col + 2, 'm')
                if self.get_value(row, col + 3) == None: self.set_value(row, col + 3, 'r')
            elif orientation == 'V':
                if self.get_value(row, col)     == None: self.set_value(row,     col, 't')
                if self.get_value(row + 1, col) == None: self.set_value(row + 1, col, 'm')
                if self.get_value(row + 2, col) == None: self.set_value(row + 2, col, 'm')
                if self.get_value(row + 3, col) == None: self.set_value(row + 3, col, 'b')

        if orientation == 'H':
            for j in range(col - 1, col + n + 1):
                if j < 10 and self.is_column_complete(j):
                    self.set_column_water(j)
                for i in range(row - 1, row + 2):
                    if self.get_value(i, j) == None: self.set_value(i, j, 'w')

            if self.is_row_complete(row):
                self.set_row_water(row)

        elif orientation == 'V':
            for i in range(row - 1, row + n + 1):
                if i < 10 and self.is_row_complete(i):
                    self.set_row_water(i)
                for j in range(col - 1, col + 2):
                    if self.get_value(i, j) == None: self.set_value(i, j, 'w')

            if self.is_column_complete(col):
                self.set_column_water(col)


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

        board = Board(state.board.rows.copy(), state.board.columns.copy(), [row.copy() for row in state.board.grid])
        board.set_n_boat(i, j, n, orientation)
        board.boats = state.board.boats.copy()
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

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass
    
    def initial_clear(self) -> None:
        """Coloca água em todas as posições do tabuleiro inicial que não podem
        ser ocupadas por peças de barcos. Ao reconhecer peças de barcos,
        atualiza as contagens de peças por linha e coluna"""
        board = self.initial.board

        # 1. Rodear peças com água
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

        for (i, j) in neighbours:
            if board.is_empty(i, j): board.set_value(i, j, 'w')

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

        for (i, j) in neighbours:
            if board.is_empty(i, j): board.set_value(i, j, 'w')

        # 2. Preencher linhas e colunas maximizadas com água
        for i in range(10):
            if board.is_row_complete(i):
                for j in range(10):
                    if board.is_empty(i, j):
                        board.set_value(i, j, 'w')
            if board.is_column_complete(i):
                for j in range(10):
                    if board.is_empty(j ,i):
                        board.set_value(j, i, 'w')
    
    def initial_boats(self) -> None:
        """Reconhece barcos de tamanho presentes no tabuleiro inicial e atualiza
        as suas contagens."""
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


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    problem = Bimaru(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, sep = "")

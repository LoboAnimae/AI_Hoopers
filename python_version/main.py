import numpy as np


class Piece:
    def __init__(self, color):
        self.color = color


class Game:
    def __init__(self, turn=1):
        self.turn = turn

    def take_turn(self, turn=1):
        x_coord = int(input('X_coord: '))
        y_coord = int(input('Y_coord: '))


class Table:
    def __init__(self):
        self.table = [[0 for x in range(10)] for x in range(10)]

    def __str__(self):
        print('     0 1 2 3 4 5 6 7 8 9')
        print('     ====================')
        for index, i in enumerate(self.table):
            print(9 - index, end=' || ')
            for j in i:
                print(j, end=' ')
            print()

        return ''


# If we think about how a single cell can move, it
# has the possibility to move around using a transitive property,
# such as in Discrete mathematics. In such a case, the game could
# end up in a loop, where the starting position is also the ending
# position. For this, the starting position cannot be part of the
# ending positions.
def find_possible_moves(top: Table, cords: list):
    x_cords, y_cords = cords
    try:
        if top.table[x_cords][y_cords] == 0:
            raise Exception('No piece')
        return True
    except Exception as e:
        return e


def fill_rows(table, from_column, to_column, from_row, cell_type):
    top = table
    i = from_column - 1
    while i < to_column:
        top.table[from_row - 1][i] = cell_type
        i += 1
    return top


def create_board():
    top = Table()
    # Simulate C for loop
    i = 5
    while i >= 1:
        top = fill_rows(top, 1, i, i + 5, 1)
        top = fill_rows(top, i + 5, 10, i, 2)
        i -= 1
    return top


# def main():
#     board = create_board()
#     print(board)

board = create_board()
# board.table[9][4] = 0
# board.table[8][4] = 1
# i = 0
# j = 0

board.table[0][0] = 9
board.table[9][9] = 8
board.table[0][9] = 7

board.table.reverse()
# for i in board.table:
#     i.reverse()

# result = find_possible_moves(board, [9, 4])
# print(result)
print(board)
# main()

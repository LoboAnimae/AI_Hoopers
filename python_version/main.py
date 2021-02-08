import numpy as np


class Piece:
    def __init__( self, color ):
        self.color = color


class Game:
    def __init__( self, turn = 1 ):
        self.turn = turn

    def take_turn( self, turn = 1 ):
        x_coord = int( input( 'X_coord: ' ) )
        y_coord = int( input( 'Y_coord: ' ) )


class Table:
    def __init__( self ):
        self.table = [ [ 0 for x in range( 10 ) ] for x in range( 10 ) ]

    def __str__( self ):
        print( '\n\n' )
        i = 9
        while i >= 0:
            print( '%d || ' % i, end = '' )
            for j in self.table[ i ]:
                print( '%d ' % j, end = '' )
            print()
            i -= 1
        # for index, i in enumerate( self.table ):
        #     print( 9 - index, end = ' || ' )
        #     for j in i:
        #         print( j, end = ' ' )
        #     print()
        print( '     ====================' )
        print( '     0 1 2 3 4 5 6 7 8 9' )
        return ''


# If we think about how a single cell can move, it
# has the possibility to move around using a transitive property,
# such as in Discrete mathematics. In such a case, the game could
# end up in a loop, where the starting position is also the ending
# position. For this, the starting position cannot be part of the
# ending positions.
def find_possible_moves( top: Table, cords: list, original_cord = None ):
    x_cords, y_cords = cords
    original_cords = None
    possible_cords = [ ]
    if original_cord is None:
        original_cords = cords
    try:
        if top.table[ x_cords ][ y_cords ] == 0:
            raise Exception( 'No piece' )
        if cords == original_cords and original_cord is not None:
            raise Exception( 'Original' )

        around_cords = [
            [ x_cords - 1, y_cords + 1 ], [ x_cords, y_cords + 1 ], [ x_cords + 1, y_cords + 1 ],
            [ x_cords - 1, y_cords ], [ x_cords + 1, y_cords ],
            [ x_cords - 1, y_cords - 1 ], [ x_cords, y_cords - 1 ], [ x_cords + 1, y_cords - 1 ]
        ]
        for i in around_cords:
            x, y = i
            if x < 0 or x > 9 or y < 0 or y > 9: continue
            if top.table[ x ][ y ] == 0:
                possible_cords.append( [ x, y ] )

        for i in around_cords:
            x, y = i
            if x < 0 or x > 9 or y < 0 or y > 9: continue
            if top.table[ x ][ y ] == 1:
                for i in find_possible_moves( top, [x, y], original_cords ):
                    x, y = i
                    possible_cords.append( [ x, i ] )
        return possible_cords
    except Exception as e:
        print (e)
        return possible_cords


def fill_rows():
    top = Table()
    # i = from_column - 1
    top.table = [ [ 0, 0, 0, 0, 0, 2, 2, 2, 2, 2 ],
                  [ 0, 0, 0, 0, 0, 0, 2, 2, 2, 2 ],
                  [ 0, 0, 0, 0, 0, 0, 0, 2, 2, 2 ],
                  [ 0, 0, 0, 0, 0, 0, 0, 0, 2, 2 ],
                  [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 2 ],
                  [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
                  [ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ],
                  [ 1, 1, 1, 0, 0, 0, 0, 0, 0, 0 ],
                  [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0 ],
                  [ 1, 1, 1, 1, 1, 0, 0, 0, 0, 0 ],
                  ]
    # while i < to_column:
    #     top.table[ from_row - 1 ][ i ] = cell_type
    #     i += 1
    return top


# def create_board():
#     top = Table()
#     # Simulate C for loop
#     i = 5
#     while i >= 1:
#         top = fill_rows( top, 1, i, i + 5, 1 )
#         top = fill_rows( top, i + 5, 10, i, 2 )
#         i -= 1
#     return top


# def main():
#     board = create_board()
#     print(board)


# Cords: (y, x)
def main():
    board = fill_rows()
    # board.table.reverse()
    result = find_possible_moves( board, [ 3, 9 ] )
    print( board )
    print( result )


main()

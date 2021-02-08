import numpy as np


class Piece:
    def __init__( self, color ):
        self.color = color


class Table:
    def __init__( self ):
        self.table = [ [ 0 for x in range( 10 ) ] for x in range( 10 ) ]

    def __str__( self ):
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

def game():
    board = fill_rows()
    print( 'Current board status: ' )
    print( board )

    turn = 1
    running = True
    while running:
        x = int( input( 'Piece from (X-Cord): ' ) )
        y = int( input( 'Piece from (Y-Cord): ' ) )
        x, y = y, x
        result = find_possible_moves( board.table, x, y, turn )
        print( result )


class Node:
    def __init__( self, x, y, player ):
        self.x = x
        self.y = y
        self.objective = [ 0, 9 ] if player == 1 else [ 9, 0 ]
        self.children = [ ]

    def add_node( self, node ) -> None:
        self.children.append( node )

    def __str__( self ):
        description = 'Node %s with the following children:\n' % str( [ self.y, self.x ] )
        children = ''
        for i in self.children:
            children += '- %s \n' % str( i ) if i is not None else ''
        if children == '':
            return 'Node %s with no children.' % str( [ self.y, self.x ] )
        return description + children


def has_piece( top, x, y ):
    if top[ x ][ y ] == 0:
        return False
    return True


def is_current_player_piece( top, x, y, player ):
    return top[ x ][ y ] == player


def find_possible_moves( top: list, x: int, y: int, player: int, is_root = True, depth = 0 ) -> list:
    if depth == 4:
        return None
    root = Node( x, y, player = player )
    objective = [ 9, 0 ] if player == 1 else [ 9, 0 ]
    goes_to_objective = False
    if is_current_player_piece( top, x, y, player ):
        goes_to_objective = True

    around_cords = [
        [ x - 1, y + 1 ], [ x, y + 1 ], [ x + 1, y + 1 ],
        [ x - 1, y ], [ x + 1, y ],
        [ x - 1, y - 1 ], [ x, y - 1 ], [ x + 1, y - 1 ]
    ]

    for cord in around_cords:
        try:
            x_cord, y_cord = cord
            exists = has_piece( top, x_cord, y_cord )
            if not exists and is_root:
                root.add_node( Node( x_cord, y_cord, player ) )
            elif exists:
                new_x = (2 * x_cord) - x
                new_y = (2 * y_cord) - y
                if has_piece( top, new_x, new_y ):
                    continue
                root.add_node( find_possible_moves( top, new_x, new_y, player, False, depth + 1 ) )
        except:
            pass
    return root

    # original_cords = None


# possible_cords = [ ]
# if parent is None:
#     original_cords = cords
# try:
#     if top.table[ x_cords ][ y_cords ] == 0:
#         raise Exception( 'No piece' )
#     if cords == original_cords and parent is not None:
#         raise Exception( 'Original' )
#
#     around_cords = [
#         [ x_cords - 1, y_cords + 1 ], [ x_cords, y_cords + 1 ], [ x_cords + 1, y_cords + 1 ],
#         [ x_cords - 1, y_cords ], [ x_cords + 1, y_cords ],
#         [ x_cords - 1, y_cords - 1 ], [ x_cords, y_cords - 1 ], [ x_cords + 1, y_cords - 1 ]
#     ]
#     for i in around_cords:
#         x, y = i
#         if x < 0 or x > 9 or y < 0 or y > 9: continue
#         if top.table[ x ][ y ] == 0:
#             possible_cords.append( [ x, y ] )
#
#     for i in around_cords:
#         x, y = i
#         if x < 0 or x > 9 or y < 0 or y > 9: continue
#         if top.table[ x ][ y ] == 1:
#             for i in find_possible_moves( top, [ x, y ], original_cords ):
#                 x, y = i
#                 possible_cords.append( [ x, i ] )
#     return possible_cords
# except Exception as e:
#     print( e )
#     return possible_cords


def fill_rows():
    top = Table()
    # i = from_column - 1
    top.table = [
        [ 0, 0, 0, 0, 0, 2, 2, 2, 2, 2 ],
        [ 0, 0, 0, 0, 0, 0, 0, 2, 2, 2 ],
        [ 0, 0, 0, 0, 0, 2, 0, 2, 2, 2 ],
        [ 0, 0, 0, 1, 0, 0, 0, 0, 2, 2 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 2 ],
        [ 1, 0, 0, 1, 0, 0, 0, 0, 0, 0 ],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 0, 1, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 1, 0, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 1, 1, 1, 0, 0, 0, 0, 0 ]
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
    game()


main()

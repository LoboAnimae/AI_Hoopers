from math import pow, sqrt

MAX_DEPTH = 12
CHANGE_PARAMETER = 5
LAST_VISITED = [ -1, -1 ]
OPTIMAL_PLAY = None
OPTIMAL_MAGNITUDE = None
OBJECTIVE = {
    1: [ 0, 9 ],
    2: [ 9, 0 ],
}
WIN_CELLS = {
    1: [
        [ 5, 0 ], [ 6, 0 ], [ 7, 0 ], [ 8, 0 ], [ 9, 0 ],
        [ 6, 1 ], [ 7, 1 ], [ 8, 1 ], [ 9, 1 ], [ 7, 2 ],
        [ 8, 2 ], [ 9, 2 ], [ 8, 3 ], [ 9, 3 ], [ 9, 4 ]
    ],
    2: [
        [ 0, 9 ], [ 0, 8 ], [ 0, 7 ], [ 0, 6 ], [ 0, 5 ],
        [ 1, 9 ], [ 1, 8 ], [ 1, 7 ], [ 1, 6 ], [ 2, 9 ],
        [ 2, 8 ], [ 2, 7 ], [ 3, 9 ], [ 3, 8 ], [ 4, 9 ],
    ]
}


# Classes
# class Piece:
#     def __init__( self, color ):
#         self.color = color


class NodeClass:
    def __init__( self, x, y, player, parent = None ):
        self.x = x
        self.y = y
        self.children = [ ]
        self.parent = parent

    def add_node( self, node ) -> None:
        self.children.append( node )

    def __str__( self ):
        description = 'Node %s ' % str( [ self.y, self.x ] )
        parent = 'is a root node '
        if self.parent is not None:
            parent = ' has parent %s ' % str( [ self.parent[ 1 ], self.parent[ 0 ] ] )
        children = 'and is parent to nodes'
        for i in self.children:
            children += ' %s ' % str( [ i.x, i.y ] )
        if children == 'and is parent to nodes':
            return 'and no children'
        return description + parent + children + '.'


#

class Table:
    def __init__( self ):
        self.table = [ [ 0 for x in range( 10 ) ] for x in range( 10 ) ]

    def __str__( self ):
        i = 9
        while i >= 0:
            print( '%d || ' % i, end = '' )
            for j in self.table[ i ]:
                print( '%s ' % j, end = '' )
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


# Methods
def explore_children( root, parent = None, tab_arg = 1, depth = 0, original_cords = None ):
    if root is None:
        return 10000000, -1, [ 0, 0 ]
    for cord in WIN_CELLS:
        if cord == [ root.y, root.x ]:
            return 0.01, 12, [ root.y, root.x ]
    console = '(Depth %d) %s' % (depth, [ root.y, root.x ])
    tab = tab_arg
    if parent is not None:
        tabulator = ' ' * tab
        console = tabulator + console
        tab = tab + 1
    if original_cords is None:
        original_cords = { 'x': root.x, 'y': root.y }

    new_magnitude, magnitude_change = calculate_magnitude( original_cords, root, { 'x': 0, 'y': 9 } )

    # print( console + ' ' + str( new_magnitude ) + ' (changed ' + str( magnitude_change ) + ')' )
    node = [ ]
    if len( root.children ) != 0:
        for child in root.children:
            child_magnitude, magnitude_sub_change, new_node = explore_children( child, root, tab, depth = depth + 1,
                                                                                original_cords = original_cords )
            if new_magnitude:
                if new_magnitude > child_magnitude or magnitude_sub_change > CHANGE_PARAMETER:
                    new_magnitude = child_magnitude
                    node = new_node
                    magnitude_change = magnitude_sub_change

    return new_magnitude, magnitude_change, node if len( node ) != 0 else [ root.y, root.x ]


# The AI has to try to go forward, no matter what
# If the AI finds itself a large magnitude, it could
# be going back and forth in a plane, never going towards
# the objective.
# To solve this, the magnitude has ALWAYS to be decreasing.
def calculate_magnitude( original_cords, new_cord, objective ):
    if [ original_cords[ 'x' ], original_cords[ 'y' ] ] == [ new_cord.x, new_cord.y ]:
        return 1000000000000, -1
    # This is a mess of optimization
    current_magnitude = sqrt(
            pow( (original_cords[ 'x' ] - objective[ 'x' ]), 2 ) + pow( (original_cords[ 'y' ] - objective[ 'y' ]),
                                                                        2 ) )
    viable = sqrt( pow( (new_cord.x - objective[ 'x' ]), 2 ) + pow( (new_cord.y - objective[ 'y' ]), 2 ) )
    if not (viable < current_magnitude):
        return 10000000000000, -1
    return viable, current_magnitude - viable


# If we think about how a single cell can move, it
# has the possibility to move around using a transitive property,
# such as in Discrete mathematics. In such a case, the game could
# end up in a loop, where the starting position is also the ending
# position. For this, the starting position cannot be part of the
# ending positions.

def calculate_move( top, turn = 1 ):
    search_results = [ ]
    pieces = [ ]

    for index_y, y in enumerate( top ):
        for index_x, x in enumerate( y ):
            if x == turn:
                pieces.append( [ index_x, index_y ] )

    for piece in pieces:
        result = find_possible_moves( top, piece[ 1 ], piece[ 0 ], turn )
        result = explore_children( result )
        search_results.append( [ piece, result ] )
    for result in search_results:
        if result[ 1 ][ 0 ] > 25:
            search_results.remove( result )
    from_cord = [ ]
    to_cord = [ ]
    best_magnitude = 12
    for result in search_results:
        if (len( from_cord ) == 0 or best_magnitude < result[ 1 ][ 1 ]) and best_magnitude:
            from_cord = result[ 0 ]
            to_cord = result[ 1 ][ 2 ]
            best_magnitude = result[ 1 ][ 1 ]

    magnitudes = [ ]
    for result in search_results:
        if result[ 1 ][ 0 ] < 10:
            magnitudes.append( result[ 1 ][ 0 ] )

    magnitudes.sort()

    difference = magnitudes[ -1 ] - magnitudes[ -2 ]

    if difference > 0.5 or difference == 0:
        for result in search_results:
            if magnitudes[ -1 ] == result[ 1 ][ 0 ]:
                from_cord = result[ 0 ]
                to_cord = result[ 1 ][ 2 ]
                best_magnitude = result[ 1 ][ 1 ]

    from_cord.reverse()
    to_cord.reverse()
    top = make_move( top, from_cord, to_cord, turn )
    return top


def game():
    board = fill_rows()
    print( 'Current board status: ' )
    print( board )

    turn = 2
    running = True
    while running:
        if turn == 1:
            board.table = calculate_move( board.table, 1 )
            turn = 2
        else:
            try:
                x = int( input( 'Piece from (X-Cord): ' ) )
                y = int( input( 'Piece from (Y-Cord): ' ) )
                new_x = int( input( 'Piece to (X-Cord): ' ) )
                new_y = int( input( 'Piece to (Y-Cord): ' ) )
            except:
                x = 0
                y = 0
                new_x = 0
                new_y = 0

            x, y = y, x
            new_x, new_y = new_y, new_x
            board.table = make_move( board.table, [ x, y ], [ new_x, new_y ], 2 )
            turn = 1

        print( board )


def make_move( top, old_cord, new_cord, player ):
    old_x, old_y = old_cord
    new_x, new_y = new_cord

    top[ old_x ][ old_y ] = '.'
    top[ new_x ][ new_y ] = player
    return top


def return_possible_moves_array( node ):
    if len( node.children ) != 0:
        result = [ ]
        for sub_node in node.children:
            if len( sub_node.children ) != 0:
                children = return_possible_moves_array( sub_node )
                result.append( children )


def has_piece( top, x, y ):
    if top[ x ][ y ] == '.':
        return False
    return True


def is_current_player_piece( top, x, y, player ):
    return top[ x ][ y ] == player


def find_possible_moves( top: list, x: int, y: int, player: int, is_root = True, depth = 0, parent = None ) -> list:
    if depth == MAX_DEPTH:
        return None
    root = NodeClass( x, y, player = player, parent = parent )
    around_cords = [
        [ x - 1, y + 1 ], [ x, y + 1 ], [ x + 1, y + 1 ],
        [ x - 1, y ], [ x + 1, y ],
        [ x - 1, y - 1 ], [ x, y - 1 ], [ x + 1, y - 1 ]
    ]
    for cord in around_cords:
        if cord == [ root.x, root.y ]:
            continue
        try:
            x_cord, y_cord = cord
            exists = has_piece( top, x_cord, y_cord )
            if not exists and is_root:
                root.add_node( NodeClass( x_cord, y_cord, player ) )
            elif exists:
                new_x = (2 * x_cord) - x
                new_y = (2 * y_cord) - y
                if [ new_x, new_y ] == parent:
                    continue
                if has_piece( top, new_x, new_y ):
                    continue
                root.add_node(
                        find_possible_moves( top, new_x, new_y, player, False, depth + 1,
                                             parent = [ root.x, root.y ] ) )
        except:
            pass
    return root


# Cords: (y, x)
def fill_rows():
    top = Table()
    # i = from_column - 1
    top.table = [
        [ '.', '.', '.', '.', '.', 2, 2, 2, 2, 2 ],
        [ '.', '.', '.', '.', '.', '.', 2, 2, 2, 2 ],
        [ '.', '.', '.', '.', '.', '.', '.', 2, 2, 2 ],
        [ '.', '.', '.', '.', '.', '.', '.', '.', 2, 2 ],
        [ '.', '.', '.', '.', '.', '.', '.', '.', '.', 2 ],
        [ 1, '.', '.', '.', '.', '.', '.', '.', '.', '.' ],
        [ 1, 1, '.', '.', '.', '.', '.', '.', '.', '.' ],
        [ 1, 1, 1, '.', '.', '.', '.', '.', '.', '.' ],
        [ 1, 1, 1, 1, '.', '.', '.', '.', '.', '.' ],
        [ 1, 1, 1, 1, 1, '.', '.', '.', '.', '.' ]
    ]
    # while i < to_column:
    #     top.table[ from_row - 1 ][ i ] = cell_type
    #     i += 1
    return top


def main():
    game()


if __name__ == '__main__':
    main()
else:
    print( 'Not available as a module.' )

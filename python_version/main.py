from math import pow, sqrt

MAX_DEPTH = 12
LAST_VISITED = [ -1, -1 ]
OPTIMAL_PLAY = None
OPTIMAL_MAGNITUDE = None


# Classes
class Piece:
    def __init__( self, color ):
        self.color = color


class Node:
    def __init__( self, x, y, player, parent = None ):
        self.x = x
        self.y = y
        self.objective = [ 0, 9 ] if player == 1 else [ 9, 0 ]
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


# Methods
def explore_children( root, parent = None, tab_arg = 1, depth = 0, original_cords = None ):
    console = '(Depth %d) %s' % (depth, [ root.y, root.x ])
    tab = tab_arg
    if parent is not None:
        tabulator = ' ' * tab
        console = tabulator + console
        tab = tab + 1
    if original_cords is None:
        original_cords = { 'x': root.x, 'y': root.y }

    magnitude_change = calculate_magnitude( original_cords, root, { 'x': 0, 'y': 9 } )
    print( console + ' ' + str(magnitude_change))
    node = [ ]
    if len( root.children ) != 0:
        for child in root.children:
            child_magnitude, new_node = explore_children( child, root, tab, depth = depth + 1,
                                                          original_cords = original_cords )
            if magnitude_change:
                if magnitude_change > child_magnitude:
                    magnitude_change = child_magnitude
                    node = new_node

    return magnitude_change, node if len(node) != 0 else [root.x, root.y]


# The AI has to try to go forward, no matter what
# If the AI finds itself a large magnitude, it could
# be going back and forth in a plane, never going towards
# the objective.
# To solve this, the magnitude has ALWAYS to be decreasing.
def calculate_magnitude( original_cords, new_cord, objective ):
    if [ original_cords[ 'x' ], original_cords[ 'y' ] ] == [ new_cord.x, new_cord.y ]:
        return 1000000000000
    # This is a mess of optimization
    current_magnitude = sqrt(
            pow( (original_cords[ 'x' ] - objective[ 'x' ]), 2 ) + pow( (original_cords[ 'y' ] - objective[ 'y' ]),
                                                                        2 ) )
    viable = sqrt( pow( (new_cord.x - objective[ 'x' ]), 2 ) + pow( (new_cord.y - objective[ 'y' ]), 2 ) )
    if not (viable < current_magnitude):
        return 10000000000000
    return viable


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
        result = explore_children( result )
        print( result )


def has_piece( top, x, y ):
    if top[ x ][ y ] == 0:
        return False
    return True


def is_current_player_piece( top, x, y, player ):
    return top[ x ][ y ] == player


def find_possible_moves( top: list, x: int, y: int, player: int, is_root = True, depth = 0, parent = None ) -> list:
    if depth == MAX_DEPTH:
        return None
    root = Node( x, y, player = player, parent = parent )
    # objective = [ 9, 0 ] if player == 1 else [ 9, 0 ]
    # goes_to_objective = False
    # if is_current_player_piece( top, x, y, player ):
    #     goes_to_objective = True

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
                root.add_node( Node( x_cord, y_cord, player ) )
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
        [ 0, 0, 0, 0, 0, 2, 2, 2, 2, 2 ],
        [ 0, 0, 0, 0, 0, 0, 0, 2, 2, 2 ],
        [ 0, 0, 0, 0, 0, 2, 0, 2, 2, 2 ],
        [ 0, 0, 0, 1, 0, 0, 0, 0, 2, 2 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 2 ],
        [ 1, 0, 0, 1, 0, 0, 0, 0, 0, 0 ],
        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 0, 1, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 1, 1, 0, 0, 0, 0, 0, 0 ],
        [ 1, 1, 1, 1, 1, 0, 0, 0, 0, 0 ]
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

'''
RILEY ANDERSON
08/26/2025
Class definition for array of cells for minesweeper game
'''

from cell import Cell

class Grid():
    def __init__(self, size=10):
        #initialize a grid of cells, default size 10
        self.size = size
        self._grid = [[Cell() for cell in range(size)] for row in range(size)]

    def coord(self, x, y):
        #return cell at coordinate (x, y), where (0,0) is upper leftmost cell
        return self._grid[y][x]
    
        
    def bomb(self, coords):
        #allow passing of single tuple of bomb coords, or a list of tuples of bomb coords
        #idea is a list can be passed for initialization
        if type(coords) != list:
            coords = [coords]
        
        for bomb_position_x, bomb_position_y in coords:
            cell = self.coord(bomb_position_x, bomb_position_y)
            cell.bomb = True

    def reveal(self, coords):
        #allow passing of single tuple of reveal coords, or a list of tuples of reveal coords
        if type(coords) != list:
            coords = [coords]
        
        for reveal_position_x, reveal_position_y in coords:
            cell = self.coord(reveal_position_x, reveal_position_y)
            cell.revealed = True

    def flag(self, x, y, state: bool):
        #flag a cell
        cell = self.coord(x, y)
        cell.flagged = state

    def check_coord(self, coord):
        #return True if coord exists
        x, y = coord
        if x >= self.size or y >= self.size:
            return False
        return True

    def print_debug(self):
        #print grid to terminal for dbugging
        print_str = ''
        for row in self._grid:
            for cell in row:
                print_str += str(cell) + ' | '
            print_str += '\n'
        print(print_str)

#test / demo logic
test = Grid()
#print grid pretty
test.print_debug()
#add list of bombs
test.bomb([(0,3), (8,5)])
#reveal list of cells
test.reveal([(0,3), (9, 2), (6, 5)])
#reveal single cell
test.reveal((0, 0))
#flag single cell
test.flag(9, 0, True)
#print grid pretty to check
test.print_debug()
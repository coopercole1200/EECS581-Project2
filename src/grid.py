'''
RILEY ANDERSON & HANNAH SMITH 
CREATED: 08/26/2025
Last Edited: 8/28/2025
Class definition for array of cells for minesweeper game
'''
import random
from cell import Cell

class Grid():
    def __init__(self, size=10):
        #initialize a grid of cells, default size 10
        self.size = size
        self._grid = [[Cell() for cell in range(size)] for row in range(size)]

    def get_cell(self, x, y=None):
        #return cell at coordinate (x, y), where (0,0) is upper leftmost cell
        if type(x) == tuple:
            x, y = x
        return self._grid[y][x]
    
        
    def apply_bomb(self, coords):
        #allow passing of single tuple of bomb coords, or a list of tuples of bomb coords
        #idea is a list can be passed for initialization
        if type(coords) != list:
            coords = [coords]
        
        for bomb_position_x, bomb_position_y in coords:
            cell = self.get_cell(bomb_position_x, bomb_position_y)
            cell.bomb = True
            #add to bomb count of neighboring cells
            self.add_nearby((bomb_position_x, bomb_position_y))

    def reveal(self, coords):
        #allow passing of single tuple of reveal coords, or a list of tuples of reveal coords
        if type(coords) != list:
            coords = [coords]
        
        for reveal_position_x, reveal_position_y in coords:
            cell = self.get_cell(reveal_position_x, reveal_position_y)
            cell.revealed = True

    def flag(self, x, y, state: bool):
        #flag a cell
        cell = self.get_cell(x, y)
        cell.flagged = state

    def check_coord(self, coord):
        #return True if coord exists
        x, y = coord
        if (0 > x or x >= self.size) or (0 > y or y >= self.size):
            return False
        return True
    def check_bomb(self, coord):
        #return true is cell is marked as bomb
        if self.get_cell(coord).bomb:
            return True
        return False 
    
    def check_nearby(self, coord):
        #return true if cell's assigned nearby is strictly larger than 0
        if self.get_cell(coord).nearby > 0:
            return True
        return False

    def print_debug(self):
        #print grid to terminal for debugging
        print_str = ''
        for row in self._grid:
            for cell in row:
                print_str += str(cell) + ' | '
            print_str += '\n'
        print(print_str)

    def add_nearby(self, cell_coord):
        #calculates the nearby function -- this might have an error didn't dig in
        adjacent_transformations = [(-1, -1), (0, -1), (1, -1),
                                    (-1, 0),           (1, 0),
                                    (-1, 1),  (0, 1),  (1, 1)]
        for t in adjacent_transformations:
            if self.check_coord((cell_coord[0] + t[0], cell_coord[1] + t[1])):
                cell = self.get_cell((cell_coord[0] + t[0], cell_coord[1] + t[1]))
                cell.nearby += 1

    def place_bombs(self, firstClick_coord, bomb_amount = 10):
        #randomly places bombs on board outside of save zone
        #safe zone defined as 3X3 area around the first click 
        options = {(i, j) for i in range(self.size) for j in range(self.size)}
        x,y = firstClick_coord
        safe_zone = {(i, j) for i in range(x-1,x+2) for j in range(y-1, y+2)}
        options = {coord for coord in options if coord not in safe_zone}
        bomb_list = random.sample(options, k=bomb_amount)
        self.apply_bomb(bomb_list)

    def _flood_helper(self, coords, reveal_list):
        #recursive helper function to fill the board
        #returns if outside of boundaries, already checked, is a bomb
        #reveals any squares with nearbys larger than 0, but does not explore further 
        if not self.check_coord(coords):
            return
        if coords in reveal_list:
            return
        if self.check_bomb(coords):
            return
        reveal_list.append(coords) 
        if self.check_nearby(coords):
            return
        x, y = coords
        self._flood_helper((x, y-1), reveal_list)
        self._flood_helper((x+1, y), reveal_list)
        self._flood_helper((x, y+1), reveal_list)
        self._flood_helper((x-1, y), reveal_list)

    
    def flood_revel(self, coords):
        #public reveal function that calls recursive function and 
        # then also passes list to reveal
        revel_list = []
        self._flood_helper(coords, revel_list)
        self.reveal(revel_list)

#test / demo logic
test = Grid()
#print grid pretty
test.print_debug()
#add list of bombs
test.apply_bomb([(0,3), (8,5)])
#reveal list of cells
test.reveal([(0,3), (9, 2), (6, 5)])
#reveal single cell
test.reveal((0, 0))
#flag single cell
test.flag(9, 0, True)
#print grid pretty to check
test.print_debug()

#test / demo logic
test = Grid(8)
#print grid pretty
test.print_debug()
#test is bombs randomly applied to grid
test.place_bombs((5,5))
#prints grid pretty to reference and check
test.print_debug()
#test flood function 
test.flood_revel((5,5))
#print grid pretty to check
test.print_debug()
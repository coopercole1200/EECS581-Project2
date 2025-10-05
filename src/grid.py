"""
New Team
Description: Grid Class for Minesweeper Game.
Authors: Cole Cooper, Manu Redd, Riley England, Jackson Yanek, Evans Chigweshe
External Sources: Generative AI, Pygame documentation, NumPy documentation
"""


'''
Functions: 
make_grid -> allows for coordination between mouse coordinates and cell coordinates 
get_cell -> return cell at coordinate (x, y), where (0,0) is upper leftmost cell,
can take in seperate x, y OR a tuple (x, y)
mouse_coord -> translate event coords into mouse coords that are helpful to us
apply_bomb -> allow passing of single tuple of bomb coords, or a list of tuples of bomb coords
idea is a list can be passed for initialization
reveal -> allow passing of single tuple of reveal coords, or a list of tuples of reveal coords
flag -> flag a cell
check_coord -> return True if coord exists
check_bomb -> return true is cell is marked as bomb
check_nearby -> return true if cell's assigned nearby is strictly larger than 0
check_win ->  return true only if all the cells are revealed that are not bombs 
check_lose -> check for losing state
print_debug -> print grid to terminal for debugging
add_nearby -> calculates how many bombs are nearby a tile 
place_bombs -> randomly places bombs on board outside of save zone
_flood_helper -> recursive helper function to flood fill the board
flood_revel -> public reveal function that calls recursive function

Inputs:
the size of the board, assumed that it will be vXv
Outputs: 
A grid class that will easily allow for manipulation 
and storage for the minesweeper game. 

Outside sources: minor chatpgt and github copilot 
Authors: RILEY ANDERSON & HANNAH SMITH 
CREATED: 08/26/2025
'''
import random
import math
from cell import Cell

class Grid():
    def __init__(self, size=10):
        #initialize a grid of cells, default size 10
        self.size = size
        self._grid = [[] for row in range(size)]
        self.first = False

    def make_grid(self, mouse_coords):
        #allows for coordination between mouse coordinates and cell coordinates 
        self.cell_list = []
        for coord in mouse_coords:
            target_cell = Cell(coord[0], coord[1])  # x, y order
            self.cell_list.append(target_cell)
        for i in range((self.size**2)):
            self._grid[math.floor(i/self.size)].append(self.cell_list[i])

    def get_cell(self, x, y=None):
        #return cell at coordinate (x, y), where (0,0) is upper leftmost cell
        #can take in seperate x, y OR a tuple (x, y)
        if type(x) == tuple:
            x, y = x

        if self.check_coord((x, y)):
            return self._grid[y][x]
        
    def mouse_coord(self, coords):
        #translate event coords into mouse coords that are helpful to us
        x, y = coords
        padding = 50
        width = 50
        if (padding < x < (width * 10)+padding) and (padding < y < (width * 10)+padding):
            return((x-padding) // width, (y-padding) // width)
        return None
    
        
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

    def reveal(self, coords=None):
        #allow passing of single tuple of reveal coords, or a list of tuples of reveal coords
        if type(coords) != list and coords is not None:
            coords = [coords]
        
        if coords is None:
            for row in self._grid:
                for cell in row:
                    cell.revealed = True
        
        else:
            for reveal_position_x, reveal_position_y in coords:
                cell = self.get_cell(reveal_position_x, reveal_position_y)
                cell.revealed = True

    def flag(self, x, y=None):
        #flag a cell
        if type(x) == tuple:
            x, y = x

        cell = self.get_cell(x, y)
        state = not cell.flagged
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

    def check_win(self):
        #return true only if all the cells are revealed that are not bombs 
        for row in self._grid:
            for cell in row:
                    if not cell.bomb and not cell.revealed:
                        return False
        return True
    def check_lose(self):
        #check for losing state

        # Losing occurs when any bomb cell has been revealed (user clicked a bomb).
        for row in self._grid:
            for cell in row:
                if cell.bomb and cell.revealed:
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
        #calculates the nearby function
        adjacent_transformations = [(-1, -1), (0, -1), (1, -1),
                                    (-1, 0),           (1, 0),
                                    (-1, 1),  (0, 1),  (1, 1)]
        for t in adjacent_transformations:
            if self.check_coord((cell_coord[0] + t[0], cell_coord[1] + t[1])):
                cell = self.get_cell((cell_coord[0] + t[0], cell_coord[1] + t[1]))
                cell.nearby += 1

    def place_bombs(self, firstClick_coord, bomb_amount):
        #randomly places bombs on board outside of save zone
        #safe zone defined as 3X3 area around the first click 
        options = {(i, j) for i in range(self.size) for j in range(self.size)}
        x,y = firstClick_coord
        safe_zone = {(i, j) for i in range(x-1,x+2) for j in range(y-1, y+2)}
        options = {coord for coord in options if coord not in safe_zone}
        bomb_list = random.sample(sorted(options), k=bomb_amount)
        self.apply_bomb(bomb_list)

    def _flood_helper(self, coords, reveal_list):
        #recursive helper function to flood fill the board
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
        self._flood_helper((x-1, y-1), reveal_list) 
        self._flood_helper((x+1, y-1), reveal_list) 
        self._flood_helper((x+1, y+1), reveal_list) 
        self._flood_helper((x-1, y+1), reveal_list)

    
    def flood_revel(self, coords, bomb_amount=10):
        #public reveal function that calls recursive function and 
        # then also passes list to reveal
        if not self.first:
            self.place_bombs(coords, bomb_amount)
            self.first = True
        cell = self.get_cell(coords)
        if cell.flagged:
            return
        if cell.bomb:
            self.reveal()
        revel_list = []
        self._flood_helper(coords, revel_list)
        self.reveal(revel_list)
        # self.print_debug()

# #test / demo logic
# test = Grid()
# #print grid pretty
# test.print_debug()
# #add list of bombs
# test.bomb([(0,3), (8,5), (10,10)])
# #reveal list of cells
# test.reveal([(0,3), (9, 2), (6, 5)])
# #reveal single cell
# test.reveal((0, 0))
# #flag single cell
# test.flag(9, 0, True)
# #print grid pretty to check
# test.print_debug()

#test / demo logic
# test = Grid(10)
# #print grid pretty
# test.print_debug()
# #test is bombs randomly applied to grid
# test.place_bombs((5,5))
# #prints grid pretty to reference and check
# test.print_debug()
# #test flood function 
# test.flood_revel((5,5))
# #print grid pretty to check
# test.print_debug()
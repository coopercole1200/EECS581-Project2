"""
Description: Implements AI Solver feature.
Authors: Riley England, Jackson Yanek, Evan Chigweshe, Manu Redd, Cole Cooper
External Sources: Generative AI, Pygame documentation, NumPy documentation
"""

import random
import time

class AISolver:
    def __init__(self, grid, difficulty='easy'):
        """
        Initialize AI Solver
        Easy is default
        """
        # take in given grid and difficulty choice
        self.grid = grid
        self.difficulty = difficulty.lower()
        # time between moves
        self.last_move_time = 0
        self.move_delay = 1.0
        
    def can_make_move(self):
        #Check time between moves
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
            return True
        return False
    
    def get_unrevealed_cells(self):
        #Get list of unrevealed and unflagged cell coordinates
        unrevealed = []
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                cell = self.grid.get_cell(x, y)
                if cell and not cell.revealed and not cell.flagged:
                    unrevealed.append((x, y))
        return unrevealed
    
    def get_revealed_cells(self):
        #Get list of revealed cell coordinates
        revealed = []
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                cell = self.grid.get_cell(x, y)
                if cell and cell.revealed:
                    revealed.append((x, y))
        return revealed
    
    def easy_move(self):
        """
        Easy AI: Random cell selection
        Uncovers cells randomly, avoids flagged or already uncovered cells
        """
        unrevealed = self.get_unrevealed_cells()
        
        if not unrevealed:
            return None
        
        #Select random unrevealed cell
        selected_coord = random.choice(unrevealed)
        return selected_coord
    
    def medium_move(self):
        """
        Medium AI: Strategic play after finding safe cells
        Uncovers randomly until a safe cell (zero adjacent mines) is revealed
        then uncovers adjacent cells strategically using revealed numbers and flags
        also flags cells when remaining surrounding cells equals cell number
        """
        # Auto flag bomb locations
        self._auto_flag()
        # Check for strategic moves based on revealed cells
        strategic_move = self._find_strategic_move()
        if strategic_move:
            return strategic_move   
        # Otherwise make a random move
        return self.easy_move()

    def _auto_flag(self):
        """
        Auto-flag cells that must be bombs
        If a revealed cell's number equals the count of surrounding unrevealed cells,
        all those unrevealed cells must be bombs
        """
        revealed = self.get_revealed_cells()
        for coord in revealed:
            cell = self.grid.get_cell(coord)
            if cell and cell.revealed and cell.nearby > 0:
                adjacent_unrevealed = self._get_adjacent_unrevealed(coord)
                adjacent_flagged = self._get_adjacent_flagged(coord) 
                # If number of unrevealed + flagged equals cell's number,
                # and there are unrevealed cells, flag them
                if len(adjacent_unrevealed) + len(adjacent_flagged) == cell.nearby:
                    for flag_coord in adjacent_unrevealed:
                        self.grid.flag(flag_coord)
    
    def _find_strategic_move(self):
        """
        Find a strategic move based on revealed cells and flags 
        Returns a safe cell or None
        """
        revealed = self.get_revealed_cells()
        
        # Base Case: Find cells adjacent to revealed zeros
        for coord in revealed:
            cell = self.grid.get_cell(coord)
            if cell and cell.revealed and cell.nearby == 0:
                # Find a cell with 0 adjacent mines
                # Get adjacent unrevealed cells
                adjacent = self._get_adjacent_unrevealed(coord)
                if adjacent:
                    return random.choice(adjacent)
        
        # Look for cells where safe move can be found
        for coord in revealed:
            cell = self.grid.get_cell(coord)
            # If number of flagged cells equals the cell's value,
            # all other adjacent cells are safe
            if cell and cell.revealed and cell.nearby > 0:
                adjacent_unrevealed = self._get_adjacent_unrevealed(coord)
                adjacent_flagged = self._get_adjacent_flagged(coord) 
                if len(adjacent_flagged) == cell.nearby and adjacent_unrevealed:
                    return random.choice(adjacent_unrevealed)
        
        return None
    
    def _get_adjacent_unrevealed(self, coord):
        "Get adjacent unrevealed and unflagged cells"
        adjacent = []
        x, y = coord
        
        # Check all 8 adjacent positions
        adjacent_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        
        for dx, dy in adjacent_offsets:
            new_x, new_y = x + dx, y + dy
            if self.grid.check_coord((new_x, new_y)):
                adj_cell = self.grid.get_cell(new_x, new_y)
                if adj_cell and not adj_cell.revealed and not adj_cell.flagged:
                    adjacent.append((new_x, new_y))
        
        return adjacent
    
    def _get_adjacent_flagged(self, coord):
        "Get adjacent flagged cells"
        adjacent = []
        x, y = coord
        
        # Check all 8 adjacent positions
        adjacent_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        
        for dx, dy in adjacent_offsets:
            new_x, new_y = x + dx, y + dy
            if self.grid.check_coord((new_x, new_y)):
                adj_cell = self.grid.get_cell(new_x, new_y)
                if adj_cell and adj_cell.flagged:
                    adjacent.append((new_x, new_y))
        
        return adjacent
    
    def hard_move(self):
        """
        Hard AI: Perfect play
        Always uncovers a safe cell
        """
        unrevealed = self.get_unrevealed_cells()
        
        if not unrevealed:
            return None
        
        # Find all safe cells
        safe_cells = []
        for coord in unrevealed:
            cell = self.grid.get_cell(coord)
            if cell and not cell.bomb:
                safe_cells.append(coord)
        
        if safe_cells:
            # Prioritize cells with nearby == 0 for faster solving
            zero_cells = []
            for coord in safe_cells:
                cell = self.grid.get_cell(coord)
                if cell.nearby == 0:
                    zero_cells.append(coord)
            
            if zero_cells:
                return random.choice(zero_cells)
            else:
                return random.choice(safe_cells)
        
        # If no safe cells available 
        return None
    
    def make_move(self):
        """
        Make a move based on the current difficulty
        Returns the coordinate to uncover (in grid coords), or None if no move possible
        """
        if not self.can_make_move():
            return None
        
        if self.difficulty == 'easy':
            return self.easy_move()
        elif self.difficulty == 'medium':
            return self.medium_move()
        elif self.difficulty == 'hard':
            return self.hard_move()
        else:
            return self.easy_move()
    
    def grid_to_mouse_coords(self, grid_coord):
        """
        Convert grid coordinates to mouse coordinates
        Takes: grid_coord: tuple (x, y) in grid coordinates
        Returns: tuple (mouse_x, mouse_y) in pixel coordinates
        """
        if grid_coord is None:
            return None
        
        x, y = grid_coord
        padding = 50
        width = 50
        
        # Calculate mouse coordinates from grid coordinates
        mouse_x = x * width + padding + width // 2
        mouse_y = y * width + padding + width // 2
        
        return (mouse_x, mouse_y)
    
    def set_difficulty(self, difficulty):
        """Change AI difficulty"""
        self.difficulty = difficulty.lower()
    
    def set_move_delay(self, delay):
        """Set delay between AI moves in seconds"""
        self.move_delay = delay

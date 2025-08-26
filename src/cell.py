'''
RILEY ANDERSON
08/26/2025
Class definition for individual cell of minesweeper game'''

class Cell():
    def __init__(self):
        self.bomb = False
        self.flagged = False
        self.revealed = False

    def __str__(self):
        #overload for pretty printing
        return f'b:{self.tf(self.bomb)}, f:{self.tf(self.flagged)}, r:{self.tf(self.revealed)}'
    
    def tf(self, bool):
        if bool:
            return 'T'
        return 'F'
'''
RILEY ANDERSON
08/26/2025
Class definition for individual cell of minesweeper game'''

class Cell():
    def __init__(self):
        self.bomb = False
        self.flagged = False
        self.revealed = False
        self.nearby = 0

    def __str__(self):
        #overload for pretty printing
        #uncomment for mode (full info vs nearby + bombs)
        # return f'b:{self.tf(self.bomb)}, f:{self.tf(self.flagged)}, r:{self.tf(self.revealed)}'
        return f'{self.nearby if not self.bomb else "B"}'
    
    def tf(self, bool):
        if bool:
            return 'T'
        return 'F'
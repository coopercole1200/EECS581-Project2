'''
RILEY ANDERSON
08/26/2025
Class definition for individual cell of minesweeper game'''

import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.bomb = False
        self.flagged = False
        self.revealed = False
        self.nearby = 0

        #pygame init
        super().__init__()  # Initialize the parent Sprite class
        self.image = pygame.image.load('textures\\Unrevealed_Tile.png').convert_alpha()  # Load the sprite image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Get the rectangle for collision and positioning
        self.rect.topleft = (x, y)  # Set the initial position
    
    def update(self):
        #funct that updates sprite image based on state
        if not self.revealed:
            pass
        else:
            if self.bomb:
                self.image = pygame.image.load('textures\\Bomb_Tile.png').convert_alpha()
            elif self.flagged:
                self.image = pygame.image.load('textures\\Flagged_Tile.png').convert_alpha()
            elif self.nearby != 0:
                self.image = pygame.image.load('textures\\Number_Tile.png').convert_alpha()
            else:
                self.image = pygame.image.load('textures\\Revealed_Tile.png').convert_alpha()

        self.image = pygame.transform.scale(self.image, (50, 50))

    def __str__(self):
        #overload for pretty printing
        #uncomment for mode (full info vs bomb,nearby,revealed vs nearby + bombs)
        # return f'b:{self.tf(self.bomb)}, f:{self.tf(self.flagged)}, r:{self.tf(self.revealed)}'
        #return f'b:{self.tf(self.bomb)}, n:{self.nearby} r:{self.tf(self.revealed)}'
        return f'{(self.nearby if self.revealed else "X") if not self.bomb else "B"}'
    
    def tf(self, bool):
        if bool:
            return 'T'
        return 'F'
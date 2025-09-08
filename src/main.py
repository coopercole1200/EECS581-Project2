import pygame
from grid import Grid
from cell import Cell

pygame.init()

# render variables 
padding = 200
gameHeight = 10
gameWidth = 10
gameSize = 500
padding = 50
displaySize = gameSize + padding * 2
cellSize = gameSize // gameWidth

#sprite group
all_cells = pygame.sprite.Group()
#Grid class
grid = Grid()

def draw_gameboard():
    # fill whole screen with gray 
    gameDisplay.fill((200, 200, 200)) 

    # draw white background
    pygame.draw.rect(gameDisplay, (255, 255, 255),
                        (padding, padding, gameSize, gameSize))

    # draw grid
    x_corner = []
    y_corner = []

    for x in range(0, gameSize + 1, cellSize):
        pygame.draw.line(gameDisplay, (0, 0, 0), (padding + x, padding), (padding + x, padding + gameSize))
        x_corner.append(padding + x)
    for y in range(0, gameSize + 1, cellSize):
        pygame.draw.line(gameDisplay, (0, 0, 0), (padding, padding + y), (padding + gameSize, padding + y))
        y_corner.append(padding + y)

    mouse_coords = []
    for x in x_corner[:10]:
        for y in y_corner[:10]:
            mouse_coords.append((x, y))
    
    grid.make_grid(mouse_coords)
    for cell in grid.cell_list:
        all_cells.add(cell)

    all_cells.draw(gameDisplay)

# display
gameDisplay = pygame.display.set_mode((displaySize, displaySize)) #display
pygame.display.set_caption("Minesweeper")  
draw_gameboard()

running = True
while running:
    # grid =[]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            if event.button == 1:
                grid.flood_revel(grid.mouse_coord(event.pos))
            if event.button == 3:
                grid.flag(grid.mouse_coord(event.pos))
    
    all_cells.clear(gameDisplay, gameDisplay)
    all_cells.update()
    all_cells.draw(gameDisplay)

    pygame.display.flip()

pygame.quit()
"""
Functions: 
drawStartMenu -> draws the start page
drawGameboard -> after player starts the game this function draws the main grid
drawEndScreen -> display the winning screen
drawGameOver -> display the game over screen
startGame -> initialize the game
Inputs: User will select the number of bombs on the start page 
Outputs: Playable minesweeper front end 
Authors: Colin Treanor, Riley Anderson, Hannah Smith
"""

import pygame
import pygame_widgets
from grid import Grid
from pygame_widgets.dropdown import Dropdown

# --- header imports ---
from header import init_header, draw_header
import time

pygame.init()

# --- header and render variables ---
HEADER_HEIGHT = 150
gameHeight = 10
gameWidth = 10
gameSize = 500
padding = 50
cellSize = gameSize // gameWidth
displaySize = gameSize + padding * 2
WINDOW_HEIGHT = HEADER_HEIGHT + displaySize
stop_time = 0  # to freeze timer on win/lose

#sprite group
all_cells = pygame.sprite.Group()
#Grid class
grid = Grid()

gameDisplay = pygame.display.set_mode((displaySize, WINDOW_HEIGHT)) #display
pygame.display.set_caption("Minesweeper") 

# dropdown component for the number of bombs selected (shifted below header)
dropdown = Dropdown(
    gameDisplay, (displaySize//2)+100, HEADER_HEIGHT + (displaySize//2)-175, 60, 40,
    name='Bombs',
    choices=['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
    borderRadius=3,
    colour=(255,255,255),
    direction='down',
    textHAlign='left'
)

MENU = True
GAME = False
GAMEOVER = False
WIN = False

# button (shifted below header)
startButton = pygame.Rect((displaySize//2)-125, HEADER_HEIGHT + 125, 200, 60)

# # --- header state ---
# buoys_left = 10
# start_time = 0.0

# header setup
init_header(displaySize, HEADER_HEIGHT)  # load/scale header assets once

# draw the start page
def drawStartMenu(): 
    title = pygame.font.SysFont('Impact', 60)
    title = title.render("Minesweeper", True, (0,0,0))
    startText = pygame.font.SysFont('Impact', 30)
    startText = startText.render("Start", True, (0,0,0))
    
    # Background of the play area
    gameDisplay.fill((200, 200, 200))
    # pygame.draw.rect(gameDisplay, (220, 220, 220),
    #                  (0, HEADER_HEIGHT, displaySize, displaySize))

    mouse_pos = pygame.mouse.get_pos()
    if startButton.collidepoint(mouse_pos):
        pygame.draw.rect(gameDisplay, (0, 150, 255), startButton)
    else:
        pygame.draw.rect(gameDisplay, (0, 100, 255), startButton)

    gameDisplay.blit(title,(displaySize//2 - title.get_width()//2, HEADER_HEIGHT + 25))
    gameDisplay.blit(startText, (startButton.centerx - startText.get_width()//2, startButton.centery - startText.get_height()//2))

# draw the main grid
def drawGameboard():
    gameDisplay.fill((200, 200, 200))
    font = pygame.font.SysFont('Comic Sans MS', 16)
    # Fill play area background
    pygame.draw.rect(gameDisplay, (255, 255, 255),
                        (padding, HEADER_HEIGHT + padding, gameSize, gameSize))

    # draw grid
    for x in range(0, gameSize + 1, cellSize):
        pygame.draw.line(gameDisplay, (0, 0, 0), (padding + x, HEADER_HEIGHT + padding), (padding + x, HEADER_HEIGHT + padding + gameSize))
    for y in range(0, gameSize + 1, cellSize):
        pygame.draw.line(gameDisplay, (0, 0, 0), (padding, HEADER_HEIGHT + padding + y), (padding + gameSize, HEADER_HEIGHT + padding + y))
    
    # add column labels (A-J)
    for i in range(10):
        label = chr(ord('A') + i)
        text_surface = font.render(label, True, (0, 0, 0))
        x_pos = padding + (i * cellSize) + (cellSize // 2) - (text_surface.get_width() // 2)
        y_pos = HEADER_HEIGHT + padding - 20 
        gameDisplay.blit(text_surface, (x_pos, y_pos))

    # add row labels (1-10)
    for i in range(10):
        label = str(i + 1)
        text_surface = font.render(label, True, (0, 0, 0))
        x_pos = padding - 30 
        y_pos = HEADER_HEIGHT + padding + (i * cellSize) + (cellSize // 2) - (text_surface.get_height() // 2)
        gameDisplay.blit(text_surface, (x_pos, y_pos))

# draw you win page
def drawEndScreen():
    # fill screen with gray
    gameDisplay.fill((200, 200, 200)) # maybe remove this - just added it in case we need to draw over the game board
    text = pygame.font.Font(None, 60).render("YOU WIN", True, (0,0,0))
    gameDisplay.blit(text, (displaySize//2 - 125, HEADER_HEIGHT + displaySize//2))

# draw game over page
def drawGameOver():
    text = pygame.font.Font(None, 60).render("GAME OVER", True, (0,0,0))
    gameDisplay.blit(text, (displaySize//2 - 125, HEADER_HEIGHT + displaySize//2))

# initialize the game
def startGame():
    global all_cells, start_time, buoys_left
    all_cells.empty()
    mouse_coords = []
    for y in range(padding, padding + gameSize, cellSize):
        for x in range(padding, padding + gameSize, cellSize):
            mouse_coords.append((x, HEADER_HEIGHT + y))  # x first, then y with header offset

    grid.make_grid(mouse_coords)
    for cell in grid.cell_list:
        all_cells.add(cell)

    # header state
    start_time = time.time()
    buoys_left = 10

# fill screen with gray
gameDisplay.fill((200, 200, 200))

# main loop
running = True
numBombs = None

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if MENU: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(event.pos):
                    numBombs = dropdown.getSelected()
                    dropdown = None
                    startGame()
                    drawGameboard()
                    MENU = False
                    GAME = True
                    if numBombs is not None:
                        buoys_left = int(numBombs)
        elif GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                adj_pos = (event.pos[0], event.pos[1] - HEADER_HEIGHT)
                if event.button == 1:
                    mc = grid.mouse_coord(adj_pos)
                    if mc is not None:
                        if numBombs is not None:
                            grid.flood_revel(mc, int(numBombs))
                        else:
                            grid.flood_revel(mc)
                if event.button == 3:
                    mc = grid.mouse_coord(adj_pos)
                    if mc is not None:
                        cell = grid.get_cell(mc)
                        was_flagged = cell.flagged
                        grid.flag(mc)
                        if not was_flagged and cell.flagged:
                            buoys_left -= 1
                        elif was_flagged and not cell.flagged:
                            buoys_left += 1
    
    if MENU: 
        drawStartMenu()
        pygame_widgets.update(events)
    elif GAMEOVER:
        drawGameOver()
    elif WIN:
        drawEndScreen()
    else:
        if grid.check_win():
            WIN = True
            GAME = False
        elif grid.check_lose():
            GAMEOVER = True
            GAME = False
        all_cells.clear(gameDisplay, gameDisplay)
        all_cells.update()
        all_cells.draw(gameDisplay)

    # Always draw the header last so it stays on top
    if not MENU:
        elapsed = int(time.time() - start_time)
        stop_time = elapsed if not (GAMEOVER or WIN) else stop_time
        draw_header(gameDisplay, buoys_left, start_time, displaySize, HEADER_HEIGHT, GAMEOVER or WIN, stop_time)

    pygame.display.flip()

pygame.quit()
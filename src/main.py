"""
Description: Implements Minesweeper Game.
Authors: Riley England, Jackson Yanek, Evan Chigweshe, Manu Redd, Cole Cooper
External Sources: Generative AI, Pygame documentation, NumPy documentation
"""

import pygame
import pygame_widgets
from grid import Grid
from pygame_widgets.dropdown import Dropdown
from ai_solver import AISolver

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

# AI difficulty dropdown
ai_dropdown = Dropdown(
    gameDisplay, (displaySize//2)-200, HEADER_HEIGHT + (displaySize//2)-175, 80, 40,
    name='AI',
    choices=['None', 'Easy', 'Medium', 'Hard'],
    borderRadius=3,
    colour=(255,255,255),
    direction='down',
    textHAlign='left'
)

# AI mode dropdown (Auto vs Interactive)
mode_dropdown = Dropdown(
    gameDisplay, (displaySize//2)-200, HEADER_HEIGHT + (displaySize//2)-110, 100, 40,
    name='Mode',
    choices=['Auto', 'Interactive'],
    borderRadius=3,
    colour=(255,255,255),
    direction='down',
    textHAlign='left'
)

MENU = True
GAME = False
GAMEOVER = False
WIN = False

# AI variables
ai_solver = None
ai_mode = None
game_mode = 'Auto'
player_turn = True

# button (shifted below header)
startButton = pygame.Rect((displaySize//2)-125, HEADER_HEIGHT + 125, 200, 60)

# header setup
init_header(displaySize, HEADER_HEIGHT)  # load/scale header assets once

# draw the start page
def drawStartMenu(): 
    title = pygame.font.SysFont('Impact', 60)
    title = title.render("Minesweeper", True, (0,0,0))
    startText = pygame.font.SysFont('Impact', 30)
    startText = startText.render("Start", True, (0,0,0))
    
    # Labels for dropdowns
    labelFont = pygame.font.SysFont('Impact', 20)
    bombLabel = labelFont.render("Bombs:", True, (0,0,0))
    aiLabel = labelFont.render("AI Mode:", True, (0,0,0))
    modeLabel = labelFont.render("Game Mode:", True, (0,0,0))
    
    # Background of the play area
    gameDisplay.fill((200, 200, 200))

    mouse_pos = pygame.mouse.get_pos()
    if startButton.collidepoint(mouse_pos):
        pygame.draw.rect(gameDisplay, (0, 150, 255), startButton)
    else:
        pygame.draw.rect(gameDisplay, (0, 100, 255), startButton)

    gameDisplay.blit(title,(displaySize//2 - title.get_width()//2, HEADER_HEIGHT + 25))
    gameDisplay.blit(startText, (startButton.centerx - startText.get_width()//2, startButton.centery - startText.get_height()//2))
    
    # Draw labels
    gameDisplay.blit(aiLabel, ((displaySize//2)-200, HEADER_HEIGHT + (displaySize//2)-200))
    gameDisplay.blit(modeLabel, ((displaySize//2)-200, HEADER_HEIGHT + (displaySize//2)-135))
    gameDisplay.blit(bombLabel, ((displaySize//2)+100, HEADER_HEIGHT + (displaySize//2)-200))

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
    gameDisplay.fill((200, 200, 200)) 
    image = pygame.image.load('textures/Win_Screen.png').convert_alpha()
    gameDisplay.blit(image, (displaySize//2 - image.get_width()//2, HEADER_HEIGHT + displaySize//2 - image.get_height()//2))
    text = pygame.font.Font(None, 60).render("YOU WIN", True, (0,0,0))
    gameDisplay.blit(text, (displaySize//2 - 125, HEADER_HEIGHT + displaySize//2))    
    
# draw game over page
def drawGameOver():
    gameDisplay.fill((200, 200, 200))
    image = pygame.image.load('textures/Lose_Screen.png').convert_alpha()
    gameDisplay.blit(image, (displaySize//2 - image.get_width()//2, HEADER_HEIGHT + displaySize//2 - image.get_height()//2))
    text = pygame.font.Font(None, 60).render("GAME OVER", True, (0,0,0))
    gameDisplay.blit(text, (displaySize//2 - 125, HEADER_HEIGHT + displaySize//2))

# initialize the game
def startGame():
    global all_cells, start_time, buoys_left, ai_solver, player_turn
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
    # Player always goes first in interactive mode
    player_turn = True
    
    # Initialize AI if mode is selected
    if ai_mode and ai_mode != 'None':
        ai_solver = AISolver(grid, ai_mode)
        # Delay to allow player to see AI choice
        if game_mode == 'Auto':
            ai_solver.set_move_delay(1.0)
        else:
            ai_solver.set_move_delay(1.5)

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
                    ai_mode = ai_dropdown.getSelected()
                    game_mode = mode_dropdown.getSelected() if ai_mode != 'None' else 'Auto'
                    dropdown = None
                    ai_dropdown = None
                    mode_dropdown = None
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
                # Only allow player input if None AI selected or Interactive mode and it's player's turn
                can_play = (ai_mode == 'None') or (game_mode == 'Interactive' and player_turn)
                
                if can_play:
                    adj_pos = (event.pos[0], event.pos[1] - HEADER_HEIGHT)
                    
                    if event.button == 1:  # Left click - reveals cells
                        mc = grid.mouse_coord(adj_pos)
                        if mc is not None:
                            if numBombs is not None:
                                grid.flood_revel(mc, int(numBombs))
                            else:
                                grid.flood_revel(mc)
                            
                            # Switch turn to AI
                            if game_mode == 'Interactive' and ai_mode != 'None':
                                player_turn = False
                                ai_solver.last_move_time = time.time()
                    
                    if event.button == 3:  # Right click - flags cells
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
        # AI Turns
        # Only in Auto or Interactive mode
        should_ai_move = False
        if ai_solver and ai_mode != 'None':
            if game_mode == 'Auto':
                should_ai_move = True
            elif game_mode == 'Interactive' and not player_turn:
                should_ai_move = True
        
        if should_ai_move:
            # Gets coords of AI's choice
            ai_grid_coord = ai_solver.make_move()
            if ai_grid_coord:
                # Reveals AI's choice on the board
                if numBombs is not None:
                    grid.flood_revel(ai_grid_coord, int(numBombs))
                else:
                    grid.flood_revel(ai_grid_coord)
                
                # Switch turn back to player in interactive mode
                if game_mode == 'Interactive':
                    player_turn = True
        
        if grid.check_win():
            WIN = True
            GAME = False
        elif grid.check_lose():
            GAMEOVER = True
            GAME = False
        
        drawGameboard()  # Redraw board each frame
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

import pygame
import pygame_widgets
from grid import Grid
from cell import Cell
from pygame_widgets.button import Button 
from pygame_widgets.dropdown import Dropdown

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

gameDisplay = pygame.display.set_mode((displaySize, displaySize)) #display
pygame.display.set_caption("Minesweeper") 

# dropdown
dropdown = Dropdown(
    gameDisplay, (displaySize//2)+100, (displaySize//2)-175, 60, 40,
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

# button
startButton = pygame.Rect((displaySize//2)-125, 125, 200, 60)

def drawStartMenu(): 
    title = pygame.font.SysFont('Impact', 60)
    title = title.render("Minesweeper", True, (0,0,0))
    startText = pygame.font.SysFont('Impact', 30)
    startText = startText.render("Start", True, (0,0,0))
    
    gameDisplay.blit(title,(displaySize//2 - title.get_width()//2, 25))
    
    mouse_pos = pygame.mouse.get_pos()
    if startButton.collidepoint(mouse_pos):
        pygame.draw.rect(gameDisplay, (0, 150, 255), startButton)
    else:
        pygame.draw.rect(gameDisplay, (0, 100, 255), startButton)

    gameDisplay.blit(startText, (startButton.centerx - startText.get_width()//2, startButton.centery - startText.get_height()//2))

def draw_gameboard():
    font = pygame.font.SysFont('Comic Sans MS', 16)
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
    
        # add column labels (A-J)
    # for i in range(10):
    #     label = chr(ord('A') + i)
    #     text_surface = font.render(label, True, (0, 0, 0))
    #     x_pos = padding + (i * cellSize) + (cellSize // 2) - (text_surface.get_width() // 2)
    #     y_pos = padding - 20 
    #     gameDisplay.blit(text_surface, (x_pos, y_pos))

    # # add row labels (1-10)
    # for i in range(10):
    #     label = str(i + 1)
    #     text_surface = font.render(label, True, (0, 0, 0))
    #     x_pos = padding - 30 
    #     y_pos = padding + (i * cellSize) + (cellSize // 2) - (text_surface.get_height() // 2)
    #     gameDisplay.blit(text_surface, (x_pos, y_pos))

def drawEndScreen():
    # fill screen with gray
    gameDisplay.fill((200, 200, 200)) # maybe remove this - just added it in case we need to draw over the game board
    text = pygame.font.Font(None, 60).render("YOU WIN", True, (0,0,0))
    gameDisplay.blit(text, (displaySize//2 - 125, displaySize//2))

def drawGameOver():
    print("HIIIIIIIIIIIIIIIIIII Hannah")
    text = pygame.font.Font(None, 60).render("GAME OVER", True, (0,0,0))
    gameDisplay.blit(text, (displaySize//2 - 125, displaySize//2))

def startGame():
    global all_cells
    all_cells.empty()
    mouse_coords = []
    for x in range(padding, padding + gameSize, cellSize):
        for y in range(padding, padding + gameSize, cellSize):
            mouse_coords.append((x, y))

    grid.make_grid(mouse_coords)
    for cell in grid.cell_list:
        all_cells.add(cell)
    #all_cells.draw(gameDisplay)

# fill screen with gray
gameDisplay.fill((200, 200, 200))

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if MENU: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(event.pos):
                    # store number of bombs user selects 
                    numBombs = dropdown.getSelected()
                    dropdown = None
                    startGame()
                    draw_gameboard()
                    MENU = False
                    GAME = True
                    break
        elif GAME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if event.button == 1:
                    if numBombs != None:
                        grid.flood_revel(grid.mouse_coord(event.pos), int(numBombs))
                    else:
                        grid.flood_revel(grid.mouse_coord(event.pos))
                        if grid.check_win():
                            WIN = True
                            GAME = False
                        elif grid.check_lose():
                            print("Hi HANNAH")
                            GAMEOVER = True
                            GAME = False
                if event.button == 3:
                    grid.flag(grid.mouse_coord(event.pos))

    if MENU: 
        drawStartMenu()
        # update widgets
        pygame_widgets.update(events)
    elif GAMEOVER:
        print("HIIIIIII HANNAH")
        drawGameOver()
    elif WIN:
        drawEndScreen()
    else:
        all_cells.clear(gameDisplay, gameDisplay)
        all_cells.update()
        all_cells.draw(gameDisplay)

    pygame.display.flip()

pygame.quit()
import pygame

pygame.init()

# render variables 
padding = 200
gameHeight = 10
gameWidth = 10
gameSize = 500
padding = 50
displaySize = gameSize + padding * 2
cellSize = gameSize // gameWidth

# display
gameDisplay = pygame.display.set_mode((displaySize, displaySize)) #display
pygame.display.set_caption("Minesweeper")  

running = True
while running:
    grid =[]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # fill whole screen with gray 
    gameDisplay.fill((200, 200, 200)) 

    # draw white background
    pygame.draw.rect(gameDisplay, (255, 255, 255),
                     (padding, padding, gameSize, gameSize))
    
    # draw grid
    for x in range(0, gameSize + 1, cellSize):
        pygame.draw.line(gameDisplay, (0, 0, 0), (padding + x, padding), (padding + x, padding + gameSize))
    for y in range(0, gameSize + 1, cellSize):
        pygame.draw.line(gameDisplay, (0, 0, 0), (padding, padding + y), (padding + gameSize, padding + y))

    pygame.display.flip()

pygame.quit()
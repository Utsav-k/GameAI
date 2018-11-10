# Basic Image Movements


import pygame
pygame.init()

# Defining variables.
# Measurments
display_width = 800
display_height = 600

# Colours: RGB colour code.
black=(0,0,0)
white=(255,255,255)

# Necessary stuff.
gameDisplay = pygame.display.set_mode( (display_width,display_height) )
pygame.display.set_caption('The Doom')
clock = pygame.time.Clock()

# Insert image
ballImg = pygame.image.load('ball.jpg')
ballImg = pygame.transform.scale(ballImg,(50,50))


def ball(x,y):
	gameDisplay.blit(ballImg,(x,y))

x = (display_width*0.45)
y = (display_height*0.9)

x_change = 0

# Game Loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x_change = -10
			elif event.key == pygame.K_RIGHT:
				x_change = 10
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				x_change = 0

	x+=x_change
	gameDisplay.fill(black)
	ball(x,y)
	pygame.display.flip()
	clock.tick(50)		# FPS = 20.

pygame.quit()
quit()
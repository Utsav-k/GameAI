# Adding boundaries..

import sys
import pygame
import time
import random

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
ballImg = pygame.transform.scale(ballImg,(100,5))

# Adding Obstacles 
def things(thing_x,thing_y,thing_w,thing_h,color):
	pygame.draw.rect(gameDisplay,color,[thing_x,thing_y,thing_w,thing_h])


def ball(x,y):
	gameDisplay.blit(ballImg,(x,y))

def textObjects(text,font):
	text_surface = font.render(text,True,white)
	return text_surface, text_surface.get_rect()

def crash():
	messageDisplay('You Crashed!')

def messageDisplay(text):
	
	large_text = pygame.font.Font('freesansbold.ttf', 60)
	text_surf, text_rect = textObjects(text,large_text)
	text_rect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(text_surf,text_rect)

	pygame.display.update()
	time.sleep(2)
	gameLoop()

def gameLoop():
	x = (display_width*0.45)
	y = (display_height*0.95)

	x_change = 0


	# Starting Obstacles

	thing_startx = random.randrange(0,display_width)
	thing_starty = -600
	thing_speed = 20
	thing_width = random.randrange(15,50)
	thing_height = 30

	game_exit = False
	while not game_exit:
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

		# things(thing_x,thing_y,thing_w,thing_h,color)
		things(thing_startx, thing_starty, thing_width,thing_height, white)

		thing_starty += thing_speed


		ball(x,y)

		if x>display_width-50 or x<0:
			crash()

		if thing_starty > display_height:
			thing_starty = 0-thing_height
			thing_startx = random.randrange(0,display_width)
			thing_width = random.randrange(15,80)

		if y<thing_starty+thing_height:
			print('Step 1')
			if x > thing_startx and x < thing_startx+thing_width or (x+100) > thing_startx and (x+100)<thing_startx+thing_width:
				print("Crossover")
				crash()

		pygame.display.update()
		clock.tick(60)

gameLoop()
pygame.quit()
quit()
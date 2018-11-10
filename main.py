import sys
import pygame

pygame.init()

size = (800,600)
gameDisplay = pygame.display.set_mode(size)


pygame.display.set_caption('THE D00M')		# Setting title name.

clock = pygame.time.Clock()		# Setting up game clock.


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		print(event)
	pygame.display.update()
	clock.tick(60)		# FPS = 60.

pygame.quit()
quit()
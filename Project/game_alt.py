# Import Modules 
import pygame
import time
import random
import sys


score = 0
health = 100
pygame.init()

win_size = (800,600)

# Colours: RGB colour code.
black=(0,0,0)
white=(255,255,255)

# Display Window.
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("THE D00M")

barImg = pygame.image.load('ball.jpg') 
barImg = pygame.transform.scale(barImg,(20,5))

# pygame Clock.
clock = pygame.time.Clock()

class Player(object):
	def __init__(self,x,width,height):
		self.x=x
		self.height=height
		self.width=width
		self.vel=10
		
	def draw(self,win):
		win.blit(barImg,(self.x,585))
		



class Bullet(object):
	def __init__(self,x,y,radius,colour):
		self.x=x
		self.y=y
		self.radius=radius
		self.colour=colour
		self.vel=10
		self.hitbox = (self.x,self.y,self.radius,white)
	
	def draw(self,win):
		pygame.draw.circle(win,self.colour,(self.x,self.y),self.radius)
		self.hitbox = (self.x,self.y,self.radius,white)



class Obstacle(object):
	def __init__(self,x,y,width,height,colour):
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.colour=colour
		self.vel=3
		self.hitbox = (self.x,self.y,40,10)
	def draw(self,win):
		pygame.draw.rect(win,white,[self.x,self.y,self.width,self.height])
		self.hitbox = (self.x,self.y,40,10)
		pygame.draw.rect(win,(255,0,0),self.hitbox,2)

	def hit(self):
		pass

def redrawGameWindow():
	doom.draw(win)
	score_text=font.render('Score:'+ str(score),1,(0,200,55))
	win.blit(score_text,(700,10))
	
	health_text=font.render('Health:'+str(health),1,(0,200,55))
	win.blit(health_text,(100,10))
	for bullet in bullets:
		bullet.draw(win)
	for obstacle in obstacles:
		obstacle.draw(win)
	pygame.display.update()

doom = Player(390,20,5)

bullets = []
bul = 0
obstacles = []

run = True

font = pygame.font.SysFont('freesansbold.ttf',30)
#mainloop
def play():
	bul=0
	score=0
	health=100
	while run:

		if bul > 0:
			bul+=1
		if bul>4:
			bul=0

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
		
		for bullet in bullets:
			for obstacle in obstacles:
				if bullet.x-bullet.radius < obstacle.hitbox[0]+obstacle.hitbox[2] and bullet.x+bullet.radius>obstacle.hitbox[0]:
					if bullet.y + bullet.radius > obstacle.hitbox[1] and bullet.y-bullet.radius < obstacle.hitbox[1]+ obstacle.hitbox[3]:
						obstacle.hit()
						score+=5
						bullets.pop(bullets.index(bullet))
						obstacles.pop(obstacles.index(obstacle))

			if bullet.y>0:
				bullet.y-=bullet.vel
			else:
				bullets.pop(bullets.index(bullet))

		for obstacle in obstacles:
			if obstacle.y<800:
				obstacle.y+=obstacle.vel
			else:

				obstacles.pop(obstacles.index(obstacle))
				health -= 10

		win.fill(black)


		x_pos = random.randrange(5,760)

		if len(obstacles)<5:
			obstacles.append( Obstacle(x_pos,0,40,10,white) )


		keys = pygame.key.get_pressed()

		if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE] and bul==0:
			if len(bullets)<4:
				bullets.append( Bullet( round(doom.x+doom.width//2), 585, 3, (0,0,255)) )
		
			bul = 1

		if event.type==pygame.KEYDOWN and keys[pygame.K_LEFT] and doom.x>doom.vel-5:
			doom.x-=doom.vel
		elif event.type==pygame.KEYDOWN and keys[pygame.K_RIGHT] and doom.x<800-doom.width-doom.vel+5:
			doom.x+=doom.vel
		

		clock.tick(60)
		redrawGameWindow()
play()
pygame.quit()






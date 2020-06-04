#Name=Tushar
#Roll No.:2018201
#Section-A
#Group:1
import pygame
import sys
import random
from pygame.locals import *
from numpy import loadtxt
import numpy as np

#Constants for the game
pacImg = pygame.image.load('assets/pacman.png')
enImg = pygame.image.load('assets/enemy.png')
coinImg = pygame.image.load('assets/fruit.png')
wallImg = pygame.image.load('assets/wall1.jpeg')
goImg= pygame.image.load("assets/go.png")
goImg=pygame.transform.scale(goImg,(640,640))
wallImg=pygame.transform.scale(wallImg,(32,32))
pacImg=pygame.transform.scale(pacImg,(32,32))
coinImg=pygame.transform.scale(coinImg,(32,32))
enImg=pygame.transform.scale(enImg,(32,32))

WIDTH, HEIGHT = (32, 32)
BLUE = pygame.Color(0, 0, 255, 255) # BLUE
RED = pygame.Color(255, 0, 0, 255) # RED
YELLOW = pygame.Color(255, 255, 0, 255) # RED
WHITE=pygame.Color(255,255,255,255)
BLACK=pygame.Color(0,0,0,0)
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
NONE= (0,0)
DIR=[TOP,DOWN,RIGHT,LEFT]
clock=pygame.time.Clock()

screen = pygame.display.set_mode((640,640), 0, 32)
#Draws a rectangle for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	screen.blit(wallImg, [pixels, (WIDTH, HEIGHT)])


#Draws a rectangle for the player
def draw_pacman(screen, pos):
	pixels = pixels_from_points(pos)
	screen.blit(pacImg, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the coin
def draw_coin(screen, pos):
	pixels = pixels_from_points(pos)
	screen.blit(coinImg, [pixels, (WIDTH, HEIGHT)])
def draw_enemies(screen,pos):
	pixels = pixels_from_points(pos)
	screen.blit(enImg, [pixels, (WIDTH, HEIGHT)])

#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)


#Initializing pygame
pygame.init()


background = pygame.surface.Surface((320,320)).convert()
pygame.font.init() # you have to call this at the start,

myfont = pygame.font.SysFont('Comic Sans MS', 30)

time=0
#Initializing variables
layout = loadtxt('assets/layout.txt', dtype=str)
rows, cols = layout.shape
pacman_position = (1,1)
background.fill((0,0,0))
move_directio=NONE
move_direction=NONE
myfont = pygame.font.SysFont("monospace", 16)
score=0
X=[]
Y=[]
enemycount=0
while enemycount<4:


	enemycount=0
	for i in range (5,len(layout)):
		for j in range (4,len(layout[i])):
			c=random.randint(1,10)
			if enemycount<6:
				if c==4 and layout[i][j]==".":
					enemycount+=1
					layout[i][j]="e"
					X.append(i)
					Y.append(j)

countcoin=1
# Main game loop
while True  :


	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	screen.fill(BLACK)
	if countcoin==0:

		screen.blit(goImg, [(0,0),(640, 640)])
		textsurface = myfont.render('Score %d' % (score + 1), False, WHITE, (0, 0, 0))
		screen.blit(textsurface, (0, 0))
		textsurface1 = myfont.render('Time %d s' % time, False, WHITE, (0, 0, 0))
		screen.blit(textsurface1, (550, 0))
		pygame.display.update()

		# Wait for a while, computers are very fast.
		clock.tick(10)

	else:
		#Draw board from the 2d layout array.
		#In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins
		for col in range(cols):
			for row in range(rows):
				value = layout[col][row]
				pos = (col, row)
				if value == 'w':
					draw_wall(screen, pos)
				elif value == 'c':
					draw_coin(screen, pos)
				elif value == 'e':
					draw_enemies(screen, pos)

		# Draw the player
		draw_pacman(screen, pacman_position)

		textsurface = myfont.render('Score %d' %score, False,WHITE, (0, 0, 0))
		screen.blit(textsurface, (0, 0))
		textsurface1 = myfont.render('Time %d s' %time , False,WHITE, (0, 0, 0))
		screen.blit(textsurface1, (550, 0))
		time+=0.1





		#TODO: Take input from the user and update pacman moving direction, Currently hardcoded to always move down
		keys_pressed = pygame.key.get_pressed()
		if pygame.key.get_focused()==False:
			move_directio=NONE

		elif keys_pressed[K_LEFT]:
			move_directio = LEFT

		elif keys_pressed[K_RIGHT]:
			move_directio = RIGHT

		elif keys_pressed[K_UP]:
			move_directio = TOP

		elif keys_pressed[K_DOWN]:
			move_directio = DOWN

		kola=0
		x,y=add_to_pos(pacman_position, move_directio)
		flag=0
		if layout[x][y]=="w":
			flag=1
			move_directio=NONE

		z=0
		if x in X and y in Y:
			if X.index(x) == Y.index(y):
				z=1
				kola=1

				flag=1
				if pacman_position!=(1,1):
					score-=1
					pacman_position=(1,1)
					move_directio = NONE
		if z==0 and layout[x][y]=="c":
			layout[x][y]="."
			score+=1


			# Update player position based on movement.
		if flag != 1:
			pacman_position = add_to_pos(pacman_position, move_directio)

		for i in range(len(X)):
			enemy_position=(X[i],Y[i])
			c=random.randint(0,3)
			d=random.randint(0,3)
			if c==d:
				move_direction=DIR[c]

			p,q = add_to_pos(enemy_position, move_direction)

			if (p,q)==pacman_position:
				if kola!=1:
					if pacman_position!=(1,1):
						score-=1
						pacman_position = (1, 1)
						move_directio = NONE
					layout[X[i]][Y[i]] = "."
					X[i], Y[i] = add_to_pos(enemy_position, move_direction)
					layout[X[i]][Y[i]] = "e"

			elif layout[p][q] == "w":

				move_direction = NONE
				X[i], Y[i] = add_to_pos(enemy_position, move_direction)
			elif layout[p][q]=="c" :
				layout[X[i]][Y[i]] = "."
				X[i], Y[i] = add_to_pos(enemy_position, move_direction)
				layout[X[i]][Y[i]] = "c"
				draw_enemies(screen,(p,q))
			elif layout[X[i]][Y[i]]=="c":
				layout[X[i]][Y[i]] = "c"
				X[i], Y[i] = add_to_pos(enemy_position, move_direction)
				layout[X[i]][Y[i]] = "e"


			else:
				layout[X[i]][Y[i]] = "."
				X[i], Y[i] = add_to_pos(enemy_position, move_direction)
				layout[X[i]][Y[i]] = "e"
			countcoin = 0
			for i in range(len(layout)):
				for j in range(len(layout[i])):
					if layout[i][j] == "c":
						countcoin += 1





		#TODO: Check if player ate any coin, or collided with the wall by using the layout array.
		# player should stop when colliding with a wall
		# coin should dissapear when eating, i.e update the layout array

		#Update the display
		pygame.display.update()



		#Wait for a while, computers are very fast.
		clock.tick(10)


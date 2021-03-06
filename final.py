"""Emily Yeh and Lydia Zuehsow"""

"""This program allows a person to wave a green "wand" to cast spells, Harry Potter-style!"""

"""For future reference, here's a link to our Google doc: https://docs.google.com/document/d/1daGjz8CWycfev0Fs96ru-Na5JNtqs2nVE1fHZ1ydhX0/edit?usp=sharing"""

# ****************** IMPORTED STUFF ****************** #

from collections import deque
import cv2
import imutils
import os, sys
import argparse
import pygame
from pygame.locals import *
import time
import numpy as np
import random

# ****************** CLASSES ****************** #

class WebCam(object):
	"""Runs the webcam and identifies green objects.
		return: center coordinates"""

	def __init__(self, bufsize = 100, counter = 0):
		self.camera = cv2.VideoCapture(0)
		self.ap = argparse.ArgumentParser()
		self.ap.add_argument("-v","--video",
			help="path to the(optional) video file")
		self.bufsize = bufsize
		self.ap.add_argument("-b", "--buffer", type=int, default = 100,
			help="max buffer size")
		self.pts = deque(maxlen=bufsize)
		self.rad = []
		self.counter = counter

		self.calpts = deque(maxlen=bufsize)
		self.calrad = []
		self.calcounter = counter

	def getcenter(self, greenLower, greenUpper):
		self.args = vars(self.ap.parse_args())
		(self.grabbed, self.frame) = self.camera.read() # Grabs the current frame
		
		# Resizes the frame, blurs the frame, converts to HSV color space
		self.frame = imutils.resize(self.frame, width=600)
		blurred = cv2.GaussianBlur(self.frame,(11,11),0)
		hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)

		# Constructs a mask for "green" objects, performs dilations and erosions to remove erroneous parts of the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask,None,iterations=1)

		# Finds contours in the mask, initializes the current (x,y) center
		self.cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]

		# Only continue if at least one contour is found
		if len(self.cnts) > 0:
			# Find the largest contour in the mask, use it to compute the minimum enclosing circle and centroid for that contour
			c = max(self.cnts,key=cv2.contourArea)
			M = cv2.moments(c)
			(center,radius) = cv2.minEnclosingCircle(c)
			Mlist= [M["m10"], M["m00"],M["m01"],M["m00"]]

			if any(Mlist) == 0:
				return None
			else:
				center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
				return [center,radius]

	def update_webcam(self, center):
		# Draw a grid on the webcam stream for spell-casting
		cv2.line(webcam.frame, (0,0), (0,450), blueColor, 1)
		cv2.line(webcam.frame, (200,0), (200,450), blueColor, 1)
		cv2.line(webcam.frame, (400,0), (400,450), blueColor, 1)
		cv2.line(webcam.frame, (600,0), (600,450), blueColor, 1)
		cv2.line(webcam.frame, (0,0), (600,0), blueColor, 1)
		cv2.line(webcam.frame, (0,150), (600,150), blueColor, 1)
		cv2.line(webcam.frame, (0,300), (600,300), blueColor, 1)

		if model.grid1flag == True:
			cv2.rectangle(webcam.frame,(400,0),(600,150),greenColor,5)
		if model.grid2flag == True:
			cv2.rectangle(webcam.frame,(200,0),(400,150),greenColor,5)
		if model.grid3flag == True:
			cv2.rectangle(webcam.frame,(0,0),(200,150),greenColor,5)
		if model.grid4flag == True:
			cv2.rectangle(webcam.frame,(400,150),(600,300),greenColor,5)
		if model.grid5flag == True:
			cv2.rectangle(webcam.frame,(200,150),(400,300),greenColor,5)
		if model.grid6flag == True:
			cv2.rectangle(webcam.frame,(0,150),(200,300),greenColor,5)
		if model.grid7flag == True:
			cv2.rectangle(webcam.frame,(400,300),(600,450),greenColor,5)
		if model.grid8flag == True:
			cv2.rectangle(webcam.frame,(200,300),(400,450),greenColor,5)
		if model.grid9flag == True:
			cv2.rectangle(webcam.frame,(0,300),(200,450),greenColor,5)

		# Draw a dot to represent the wand's coordinates
		cv2.circle(webcam.frame, center, 5, redColor, -1)

		# What happens next depends on whether the player is still alive or not
		if player.hp <= 0:
			enemy.hp = 100
			enemy.x = -800
			enemy.y = -200
			screen.fill((49,79,79))
			view.sprite = pygame.transform.scale(view.sprite, (2100,2300))
			cv2.rectangle(webcam.frame, (0,0), (600,450), blackColor, -1)
			cv2.putText(webcam.frame,GameOverText1,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),3)
			cv2.putText(webcam.frame,GameOverText2,(200,100),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),3)
			cv2.putText(webcam.frame,GameOverText3,(10,300),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),3)
			webcam.frame = cv2.flip(webcam.frame, 1)
			# img = cv2.imread('gameover.jpg')
			# cv2.imshow('Game Over', img)
# ffff
		else:
			cv2.rectangle(webcam.frame, (50,10), (550,30), greenColor, -1)
			cv2.rectangle(webcam.frame, (50,10), ((550 - player.hp),30), redColor, -1)

class Calibration(object):
	"""Performs calibration of the 'green thing' and represents the calibrated original "green object" """
	def __init__(self):
		self.loading = pygame.image.load('loadingscreen.gif').convert()
		self.loading = pygame.transform.scale(self.loading, (screenwidth,screenheight))

	def startup(self,greenLower,greenUpper):

		calibrating = True
		count = 0
		calradi = 0
		calx = 0
		caly = 0
		calxs=[]
		calys=[]

		while calibrating:
			screen.blit(self.loading,(0,0))
			pygame.display.update()

			califind = webcam.getcenter(greenLower, greenUpper)
			cv2.rectangle(webcam.frame, (0,0), (600,450), blackColor, -1)

			A = "Please hold your wand very still!"
			B =	"The Dueling Association is assembling."

			cv2.putText(webcam.frame,A,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),3)
			cv2.putText(webcam.frame,B,(10,100),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),3)

			if califind == None:
				pass
			else:
				calicenter = califind[0]
				caliradius = califind[1]

				if caliradius > 20:
				#if radius is above a certain size we count it
					webcam.calpts.append(calicenter)
					webcam.calrad.append(caliradius)
					count = count + 1
					calcounter = webcam.calcounter
			buf = 10

			cv2.imshow("Frame",webcam.frame)
			key = cv2.waitKey(1) & 0xFF

			#Eliminates accidental infinity loops by setting a frame limit on runtime.

			if count > 50:
				calradi = np.mean(webcam.calrad)
				calibrating = False
				return calradi


class Player(object):
	"""Represents you, the player!"""

	def __init__(self):
		self.hp = 500
		self.hit = False

	def DamageTaken(self,dmg):
		self.hp -= dmg

class Enemy(object):
	"""Represents your opponent."""

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.hp = 100
		self.hit = False

	def Move(self, newx, newy):
		self.x = newx
		self.y = newy

	def DamageTaken(self,dmg):
		self.hp = self.hp - dmg

	def DamageDealt(self):
		self.damage = 10


class DesktopModel(object):
	"""Stores the fake desktop state."""

	def __init__(self):
		self.grid1flag = False
		self.grid2flag = False
		self.grid3flag = False
		self.grid4flag = False
		self.grid5flag = False
		self.grid6flag = False
		self.grid7flag = False
		self.grid8flag = False
		self.grid9flag = False
		self.randominteger = random.randint(0,3)

	def spell_check(self):
		if (self.grid1flag and self.grid4flag and self.grid7flag) and (self.grid2flag == False and self.grid3flag == False and self.grid5flag == False and self.grid6flag == False and self.grid8flag == False and self.grid9flag == False) and (spell_frame <= 10):		
			enemy.hit = True
			return 0
			# Flipendo
		# fffff
		elif (self.grid3flag and self.grid6flag and self.grid9flag) and (self.grid1flag == False and self.grid2flag == False and self.grid4flag == False and self.grid5flag == False and self.grid7flag == False and self.grid8flag == False) and (spell_frame <= 10):
			enemy.hit = True
			return 1
			# Wingardium Leviosa

		elif (self.grid1flag and self.grid2flag and self.grid4flag and self.grid5flag) and (self.grid3flag == False and self.grid6flag == False and self.grid7flag == False and self.grid8flag == False and self.grid9flag == False) and (spell_frame <= 10):
			enemy.hit = True
			return 2
			# Incendio

		elif (self.grid2flag and self.grid4flag and self.grid5flag and self.grid6flag and self.grid8flag) and (self.grid1flag == False and self.grid3flag == False and self.grid7flag == False and self.grid9flag == False) and (spell_frame <= 10):
			enemy.hit = True
			return 3
			# Avada Kedavra

		elif (self.grid3flag and self.grid4flag and self.grid5flag and self.grid6flag and self.grid7flag) and (self.grid1flag == False and self.grid2flag == False and self.grid8flag == False and self.grid9flag == False) and (spell_frame <= 10):
			enemy.hit = True
			return 4
			# Stupefy

		elif (self.grid3flag and self.grid5flag and self.grid6flag and self.grid7flag and self.grid8flag) and (self.grid1flag == False and self.grid2flag == False and self.grid4flag == False and self.grid9flag == False) and (spell_frame <= 10):
			enemy.hit = True
			return 5
			# Expelliarmus

		else:
			enemy.hit = False
			if player.hp > 0 and menu.gamerunning == True:
				opponent = ["Voldemort", "Umbridge", "Malfoy", "Bellatrix"]
				dialogue = ["{} takes a stab at you!".format(opponent[self.randominteger]), "{} casts a spell-- it narrowly misses you!".format(opponent[self.randominteger]), "{} screams something unintelligible and hits you with a weak spell!".format(opponent[self.randominteger]), "{} unleashes a stream of curses! They're not very effective.".format(opponent[self.randominteger]), "{} calls forth an army of dementors, but they swarm around {} excitedly like a bunch of puppies.".format(opponent[self.randominteger], opponent[self.randominteger]), "{} yells a hurtful insult at you!".format(opponent[self.randominteger]), "{} bends down to pick up a tiny pebble and flings it at you! It hits you squarely in the stomach.".format(opponent[self.randominteger]), "{} throws Nagini at you! Nagini is displeased.".format(opponent[self.randominteger]), "You tell {} you just want to be friends. {} gives you a scalding glare.".format(opponent[self.randominteger], opponent[self.randominteger])]

				if self.randominteger == 0: # Voldemort
					if random.randint(0,100) == 5:
						player.hit = True
						player.DamageTaken(125)
						pygame.mixer.music.load('require.mp3')
						pygame.mixer.music.play(0)
						dialogue_choose = dialogue[random.randint(0,8)]
						print dialogue_choose

				if self.randominteger == 1: # Umbridge
					if random.randint(0,100) == 5:
						player.hit = True
						player.DamageTaken(50)
						pygame.mixer.music.load('goodbye.mp3')
						pygame.mixer.music.play(0)
						dialogue_choose = dialogue[random.randint(0,8)]
						print dialogue_choose

				if self.randominteger == 2: # Malfoy
					if random.randint(0,100) == 5:
						player.hit = True
						player.DamageTaken(20)
						pygame.mixer.music.load('horror_demonic_laugh.mp3')
						pygame.mixer.music.play(0)
						dialogue_choose = dialogue[random.randint(0,8)]
						print dialogue_choose

				if self.randominteger == 3: # Bellatrix
					if random.randint(0,100) == 5:
						player.hit = True
						player.DamageTaken(100)
						pygame.mixer.music.load('giggle.mp3')
						pygame.mixer.music.play(0)
						dialogue_choose = dialogue[random.randint(0,8)]
						print dialogue_choose

	def spell_clear(self):
		model.grid1flag = False
		model.grid2flag = False
		model.grid3flag = False
		model.grid4flag = False
		model.grid5flag = False
		model.grid6flag = False
		model.grid7flag = False
		model.grid8flag = False
		model.grid9flag = False


class Menu(object):
	def __init__(self):
		self.screen = screen.fill((173,216,230))
		self.font = pygame.font.SysFont("monospace", 15)

		logo = pygame.image.load('logo.png').convert_alpha()
		logo = pygame.transform.scale(logo, (300,300))
		screen.blit(logo,(300,100))


		self.cursorcolor = blueColor

		self.gamerunning = False
		self.tutorielrunning = False # The thought of exercise fills you with... determination!

	def Button(self, x, y, color, text = "Text"):
		self.x = x
		self.y = y
		self.width = 200
		self.height = 50

		self.text = self.font.render(text, 20, blackColor)

		screen.fill(color,Rect(self.x,self.y,self.width,self.height))

	def update(self):
		gamebutton = menu.Button(25,25,whiteColor, "Random Mode")
		screen.blit(self.text, (self.x + 10, self.y + 10))

		tutorielbutton = menu.Button(25,125,(100,149,237), "Tutorial Mode")
		screen.blit(self.text, (self.x + 10, self.y + 10))

		quitbutton = menu.Button(25,225,(70,130,180), "Quit")
		screen.blit(self.text, (self.x + 10, self.y + 10))

		pygame.display.update()


class PygameView(object):
	"""Visualizes a fake desktop in a pygame window."""

	def __init__(self,model,screen,background, winscreen, sprite, explosion):
		"""Initialise the view with a specific model."""
		self.model = model
		self.screen = screen.fill(whiteColor)

		# Load background png and post to screen
		background = pygame.image.load(background).convert()
		self.background = pygame.transform.scale(background, (screenwidth,screenheight))
		screen.blit(self.background,(0,0))

		# Lead the win screen
		self.winscreen = pygame.image.load(winscreen).convert()
		self.winscreen = pygame.transform.scale(self.winscreen, (screenwidth,screenheight))

		# Load enemy sprite png
		self.sprite = pygame.image.load(sprite).convert_alpha()
		self.sprite = pygame.transform.scale(self.sprite, (600,450))

		# Load spell damage animation png
		self.explosion = pygame.image.load(explosion).convert_alpha()
		self.explosion = pygame.transform.scale(self.explosion, (150,150))
		# self.explosion = self.color_surface(self.explosion, 120, 78, 240)
		# ffffff

		# Draw the enemy's HP bar
		screen.fill((0,255,0),Rect(10,10,100,20))

		# Update game display
		pygame.display.update()

	# def color_surface(self, surface, red, green, blue):
	# 	"""Changes the color of images"""
	# 	arr = pygame.surfarray.pixels3d(surface)
	# 	arr[:,:,0] = red
	# 	arr[:,:,1] = green
	# 	arr[:,:,2] = blue

	def update(self):
		"""Draw the game state to the screen"""
		# Enemy spell damage animation
		if enemy.hit and (spell_frame <= 10):
			screen.blit(self.explosion,(enemy.x + 230,enemy.y + 110))
		else:
			screen.blit(self.sprite,(enemy.x,enemy.y))

		# Update the enemy's HP bar
		if enemy.hit and (spell_frame == 1) and enemy.hp > 0:
			screen.fill((255,0,0),Rect(10,10,(150 - enemy.hp),20))
		else:
			pass

		pygame.display.update()

	def wongame(self):
		"""Displays the win game screen"""
		screen.blit(self.winscreen,(0,0))
		pygame.display.update()


class Controller(object):
	"""Your controller is your green wand. Its position determines if you cast a spell or what spell you cast."""
	def __init__(self,model):
		self.model = model
		self.selected = False

	def process_events(self):
 		"""Process all of the events in the queue"""
 		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == GRID:
				(x,y) = center
				if x <= 200 and y <= 150:
					# print 'Grid 3'
					model.grid3flag = True
				if (x >= 200 and x <= 400) and y <=150:
					# print 'Grid 2'
					model.grid2flag = True
				if x >= 400 and y <= 150:
					# print 'Grid 1'
					model.grid1flag = True
				if x <= 200 and (y >= 150 and y <=300):
					# print 'Grid 6'
					model.grid6flag = True
				if (x >= 200 and x <= 400) and (y >= 150 and y <=300):
					# print 'Grid 5'
					model.grid5flag = True
				if x >= 400 and (y >= 150 and y <= 300):
					# print 'Grid 4'
					model.grid4flag = True
				if x <= 200 and y >= 300:
					# print 'Grid 9'
					model.grid9flag = True
				if (x >= 200 and x <= 400) and y >= 300:
					# print 'Grid 8'
					model.grid8flag = True
				if x >= 400 and y >= 300:
					# print 'Grid 7'
					model.grid7flag = True

			elif event.type == BUTTON:
				(x,y) = center

				if x > 375 and x < 575 and y > 25 and y < 75:
					if menu.tutorielrunning == False:
						menu.gamerunning = True
				elif x > 375 and x < 575 and y > 125 and y < 175:
					if menu.gamerunning == False:
						menu.tutorielrunning = True
				elif x > 375 and x < 575 and y > 225 and y < 275:
					if menu.gamerunning == False and menu.tutorielrunning == False:
						running = False

						# Release the camera, close open windows
						webcam.camera.release()
						cv2.destroyAllWindows()
						master.close()
		pygame.event.clear()

	def close(self):
		pygame.display.quit()
		pygame.quit()

if __name__ == '__main__':

# ****************** INITIALIZING STUFF ****************** #

	# Initialize pygame
	pygame.init()

	# Define some colors
	redColor = pygame.Color(0,0,255)
	greenColor = pygame.Color(0,255,0)
	blueColor = pygame.Color(255,0,0)
	whiteColor = pygame.Color(255,255,255)
	blackColor = pygame.Color(0,0,0)

	# Set pygame fake desktop size
	screenwidth = 600
	screenheight = 450

	size = (screenwidth, screenheight)
	screen = pygame.display.set_mode(size)

	greenLower = (29,86,6)
	greenUpper = (64,255,255)

	check = 0
	frame = 0
	spell_frame = 0
	eventcount = 0
	center = 0

	webcam = WebCam()
	calibrate = Calibration()
	calradi = calibrate.startup(greenLower,greenUpper)

	menu = Menu()
	model = DesktopModel()
	master = Controller(model)

	pygame.mixer.music.load('hogwartsmarch.mp3')
	pygame.mixer.music.play(0)

	GameOverText1 = "You and all of your friends are dead."
	GameOverText2 = "Congrats."
	GameOverText3 = "Press R to ressurect and try again."

	# running = False
	# running = True

	GRID = pygame.USEREVENT+2
	grid_event = pygame.event.Event(GRID)

	BUTTON = pygame.USEREVENT+3
	button_event = pygame.event.Event(BUTTON)

	# Makes sure only the events we want are on the event queue
	allowed_events = [QUIT,GRID,BUTTON]
	pygame.event.set_allowed(allowed_events)

	
# ****************** RUNTIME LOOP ****************** #
	# This is the main loop of the program. 

	while True:

		if menu.gamerunning == True:
			break
		elif menu.tutorielrunning == True:
			break

		gotcenter = webcam.getcenter(greenLower, greenUpper)

		if gotcenter == None:
			master.selected = False
		else:
			center = gotcenter[0]
			radius = gotcenter[1]

			(x,y) = center

			pygame.draw.circle(screen,menu.cursorcolor,(600-x,y),3,0)

			if radius >= calradi + 15:
				pygame.event.post(button_event)
				menu.cursorcolor = redColor
			else:
				menu.cursorcolor = blueColor

		menu.update()
		webcam.frame = cv2.flip(webcam.frame, 1)
		cv2.circle(webcam.frame, (600-x,y), 5, blueColor, -1)
		cv2.imshow("Frame",webcam.frame)
		key = cv2.waitKey(1) & 0xFF

		master.process_events()
		frame += 1

		if key == ord("q"):
			# Release the camera, close open windows
			webcam.camera.release()
			cv2.destroyAllWindows()
			master.close()
			pygame.quit()

		time.sleep(.001)

	if menu.tutorielrunning == True:
		background = 'house.jpg'
		opponent = 'gnome.png'
		view = PygameView(model, screen, background, 'win.png', opponent, 'flame.png')
		player = Player()
		enemy = Enemy(25, 100)

		spells = ['Flipendo!', 'Wingardium Leviosa', 'Incendio', 'Avada Kedavra', 'Stupefy', 'Expelliarmus']

		directions = menu.font.render("Press q to quit", 40, blackColor)
		screen.blit(directions, (300, 15))

		directions = menu.font.render("Press c to start casting again", 40, blackColor)
		screen.blit(directions, (300, 35))

	if menu.gamerunning == True:
		background = ['chamberofsecrets.png', 'forbiddenforest.jpeg', 'greathall.png', 'ministryofmagicatrium.png', 'umbridgeoffice.png']
		opponent = ['voldemort.png', 'umbridge.png', 'malfoy.png', 'bellatrix.png']
		view = PygameView(model, screen, background[random.randint(0,4)], 'win.png', opponent[model.randominteger], 'flame.png')
		player = Player()
		enemy = Enemy(25, 100)

		spells = ['Flipendo!', 'Wingardium Leviosa', 'Incendio', 'Avada Kedavra', 'Stupefy', 'Expelliarmus']


	while menu.gamerunning or menu.tutorielrunning:
		# print enemy.hp
		if player.hp <= 0:
			check += 1
			if check == 1:
				pygame.mixer.music.load('Voldemort.mp3')
				pygame.mixer.music.set_volume(1.0)
				pygame.mixer.music.play(0)

		if enemy.hp <= 0:
			check += 1
			view.wongame()
			if check == 1:
				pygame.mixer.music.load('win.mp3')
				pygame.mixer.music.set_volume(1.0)
				pygame.mixer.music.play(0)
		else:
			# fffff
			view.update()

			spellnum = model.spell_check()
			if spell_frame == 1:
				print 'You cast ', spells[spellnum]
			
				if 0 <= spellnum and spellnum <= 1:
					enemy.DamageTaken(25)
					pygame.mixer.music.load('Swooshing.mp3')
				if spellnum == 2:
					enemy.DamageTaken(50)
					pygame.mixer.music.load('SmallFireball.mp3')
				if 3 <= spellnum and spellnum <= 5:
					enemy.DamageTaken(100)
					pygame.mixer.music.load('Gun.mp3')

				pygame.mixer.music.set_volume(1.0)
				pygame.mixer.music.play(0)

		# Check for spells
			if enemy.hit: #if a player's offensive spell is detected, add one to spell frame count
				spell_frame += 1
				if spell_frame > 3: #if a spell has finished firing, reset spell frame counter and clear all grid flags.
					model.spell_clear()
					spell_frame = 0
				else:
					pass
			else:
				pass

		# Find the center of any green objects' contours
		gotcenter = webcam.getcenter(greenLower, greenUpper)
		if gotcenter == None:
			webcam.update_webcam((300, 225))
		else:
			center = gotcenter[0]
			radius = gotcenter[1]
			webcam.update_webcam(center)
			if radius > 20:
				# If the radius is above a certain size we count it
				webcam.pts.append(center)
				webcam.rad.append(radius)
				webcam.counter = webcam.counter + 1
				(x,y) = center
				if (x >= 0 and x <= 600) and (y >= 0 and y <= 450):
					pygame.event.post(grid_event)

			master.process_events()

		# Update the frames of the webcam video
		webcam.frame = cv2.flip(webcam.frame, 1)
		cv2.imshow("Frame",webcam.frame)
		key = cv2.waitKey(1) & 0xFF
		frame = frame + 1
		time.sleep(.001)
		if key == ord("q"):
			# Release the camera, close open windows
			webcam.camera.release()
			cv2.destroyAllWindows()
			master.close()
			pygame.quit()
		if key == ord("c"):
			# Clear spell chain
			model.spell_clear()
		if key == ord("r"):
			# Reset game
			check = 0
			enemy.x = 25
			enemy.y = 100
			enemy.hp = 100
			player.hp = 500

			model.spell_clear()
			view.sprite = pygame.transform.scale(view.sprite, (600,450))
			screen.blit(view.background,(0,0))
			screen.fill((0,255,0),Rect(10,10,100,20))

			if menu.tutorielrunning == True:
				directions = menu.font.render("Press q to quit", 40, blackColor)
				screen.blit(directions, (300, 15))

				directions = menu.font.render("Press c to start casting again", 40, blackColor)
				screen.blit(directions, (300, 35))

			pygame.display.update()
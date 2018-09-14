#coding=utf-8

import sys, random, pygame, time
from pygame.locals import *


#BASIC VAR
FPS = 30
WINDOWSWIDTH = 600
WINDOWSHEIGHT = 500
BUTTONSIZE = 40
BUTTONGAPSIZE = 10

# COLOR = (R,   G,   B)
WHITE = (255, 255, 255)
BLUE = (0, 0, 155)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BGCOLOR = BLUE
baseboard = [1, 0, 0, 0]

# FUNC

def terminate():
	pygame.quit()
	sys.exit(0)


def getxymargin(row = 4, clumn = 4):
	XMARGIN = int((WINDOWSWIDTH - (clumn * BUTTONSIZE) -  (clumn - 1) * BUTTONGAPSIZE) / 2)
	YMARGIN = int((WINDOWSHEIGHT - (row * BUTTONSIZE) - (row - 1) * BUTTONGAPSIZE) / 2)
	return (XMARGIN, YMARGIN)

def creatnewboard(baseboard, row = 2, clumn = 2):
	board = []
	for x in xrange(row):
		for y in xrange(clumn):
			random.shuffle(baseboard)
			board.append(baseboard[:])

	return board

def gettopleft(XMARGIN, YMARGIN,boxx, boxy):

	left = XMARGIN + (boxy * (BUTTONSIZE + BUTTONGAPSIZE))
	top = YMARGIN + (boxx * (BUTTONSIZE + BUTTONGAPSIZE))

	return (left, top)

def drawboard(color, left, top, str = None):
	
	pygame.draw.rect(DISPLAYSURF, color, (left, top, BUTTONSIZE, BUTTONSIZE))
	
def creatnewgame(board, XMARGIN, YMARGIN):

	for x in xrange(len(board)):
		for y in xrange(len(board[x])):
			left_x, top_y = gettopleft(XMARGIN, YMARGIN,x, y)
			if board[x][y]:
				drawboard(YELLOW, left_x, top_y)
			else:
				drawboard(WHITE, left_x, top_y)


def getboom(mainboard):

	return [(item_x, item_y) for item_x in xrange(len(mainboard))\
	for item_y in xrange(len(mainboard[item_x]))\
	if mainboard[item_x][item_y] == 1]

def mark(mainboard, mouse_x, mouse_y,  XMARGIN, YMARGIN):
	
	for x in xrange(len(mainboard)):
		for y in xrange(len(mainboard[x])):
			left, top = gettopleft(XMARGIN, YMARGIN,x, y)
			boxRect = pygame.Rect(left, top, BUTTONSIZE, BUTTONSIZE)
			if boxRect.collidepoint(mouse_x, mouse_y):
				return (x, y)
	return (None, None)

def checkhaswon(mainboard, wonlist):
	boomlist = getboom(mainboard)
	clicklist = list(set(wonlist))
	if len(boomlist) == len(clicklist):
		if False not in  map(lambda x : x in boomlist, clicklist):
			return True
		return False
	else:
		return False
		

def changebgcolor(board, XMARGIN, YMARGIN):
	global BGCOLOR
	if (int(time.time() - STARTTIME) % 5 == 0):
		BGCOLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		DISPLAYSURF.fill(BGCOLOR)
		creatnewgame(board, XMARGIN, YMARGIN)
		pygame.time.wait(300)
	else:
		creatnewgame(board, XMARGIN, YMARGIN)

def newgame(row, clumn, mainboard):

	global mouseclick, clicklist
	xmargin, ymargin = getxymargin(row, clumn)
	creatnewgame(mainboard, xmargin, ymargin)
	
	if mouseclick:
		
		mouse_x, mouse_y = pygame.mouse.get_pos()
		boxx, boxy = mark(mainboard, mouse_x, mouse_y, xmargin, ymargin)
		if (boxx, boxy) != (None, None):
			BEEP.play()
			clicklist.append((boxx, boxy))

	mouseclick = None

	if clicklist:
		for boxx, boxy in clicklist:
			left, top = gettopleft(xmargin, ymargin, boxx, boxy)
			drawboard(RED, left, top)
		
	
def gamewon(mainboard, row = 6, clumn = 5, animationSpeed = 20):
	origSurf = DISPLAYSURF.copy()
	flashSurf = pygame.Surface(DISPLAYSURF.get_size())
	flashSurf = flashSurf.convert_alpha()
	r, g, b = (200, 1, 0)
	xmargin, ymargin = getxymargin(9, 6)
	for i in xrange(3):
		for start, end, step in ((0, 255, 1), (255, 0, -1)):
			for alpha in xrange(start, end, animationSpeed * step):
				flashSurf.fill((r, g, b, alpha))
				DISPLAYSURF.blit(origSurf, (0, 0))
				DISPLAYSURF.blit(flashSurf, (0, 0))
				creatnewgame(mainboard, xmargin, ymargin)
				pygame.display.update()
				FPSCLOCK.tick(FPS)


def button(BASICFONT):

	buttonSurf = pygame.Rect(WINDOWSWIDTH - 70, WINDOWSHEIGHT - 20, 60, 40)

	textSurf = BASICFONT.render('restart', True, WHITE)
	textRect = buttonSurf.copy()
	textRect.topleft = (WINDOWSWIDTH - 70, WINDOWSHEIGHT - 20)
	DISPLAYSURF.blit(textSurf, textRect)
	return buttonSurf

def click_button(clicklist, buttonSurf):

	global buttonclick
	mouse_x, mouse_y = pygame.mouse.get_pos()
	if buttonclick:
		if buttonSurf.collidepoint(mouse_x, mouse_y):
			if clicklist:
				clicklist.pop(-1)

	buttonclick = None
			

def main():
	global DISPLAYSURF, FLAG, STARTTIME, FPSCLOCK, mouseclick, buttonclick, clicklist, BEEP, baseboard
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))
	pygame.display.set_caption('click')
	mainboard = creatnewboard(baseboard, 2, 2)
	STARTTIME = time.time()
	BEEP = pygame.mixer.Sound('beep1.ogg')
	mouseclick, buttonclick = None, None
	FLAG = 1
	clicklist = []
	BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
	infoSurf = BASICFONT.render('click the yellow box', True, WHITE)
	infoRect = infoSurf.get_rect()
	infoRect.topleft = (10, 10)
	
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		DISPLAYSURF.blit(infoSurf, infoRect)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			if event.type == MOUSEBUTTONUP:
				mouseclick, buttonclick = True, True
					
		buttonSurf = button(BASICFONT)
		scoreSurf = BASICFONT.render('FLAG:{}'.format(FLAG), True, WHITE)
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (WINDOWSWIDTH - 100, 10)
		DISPLAYSURF.blit(scoreSurf, scoreRect)
		boomlist = getboom(mainboard)
		clickSurf = BASICFONT.render('boom:{}'.format(len(boomlist) - len(list(filter(lambda x: x in boomlist, list(set(clicklist)))))), True, WHITE)
		clickRect = clickSurf.get_rect()
		clickRect.center = (int(WINDOWSWIDTH / 2), 20)
		DISPLAYSURF.blit(clickSurf, clickRect)
		
		if FLAG == 1:
			newgame(4, 4, mainboard)
			if checkhaswon(mainboard, clicklist):
				pygame.time.wait(300)
				clicklist = []
				FLAG += 1
				baseboard.append(random.choice([0, 1]))
				mainboard = creatnewboard(baseboard, 2 ,3)
				
		elif FLAG == 2:
			newgame(6, 5, mainboard)
			if checkhaswon(mainboard, clicklist):
				pygame.time.wait(300)
				clicklist = []
				FLAG += 1
				baseboard.append(random.choice([0, 1]))
				mainboard = creatnewboard(baseboard, 3 ,3)

		elif FLAG == 3:
			newgame(9, 6, mainboard)
			if checkhaswon(mainboard, clicklist):
				pygame.time.wait(300)
				clicklist = []
				gamewon(mainboard)
				baseboard = [1, 0, 0, 0]
				mainboard = creatnewboard(baseboard, 2, 2)
				FLAG = 1
				
		click_button(clicklist, buttonSurf)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	main()

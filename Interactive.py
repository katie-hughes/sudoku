import pygame
from pygame.locals import *
import time
import numpy as np
import argparse

"""
I need to do this outside the class, because if the class is called
more than once, the screen size becomes updated to the window size, which is
smaller than the screen. Then the new window created becomes tiny.
Is there a way around this...?
"""
pygame.init()
screen_info = pygame.display.Info()
global screen_width
screen_width = screen_info.current_w
pygame.quit()


class Msg:
	def __init__(self, message, width, height, color=None):
		self.m = message
		self.w = width
		self.h = height
		self.c = color


class Draw:
	def __init__(self, size):
		pygame.init()
		self.fps = 500
		self.fpsClock = pygame.time.Clock()
		self.width = int((screen_width)/3.)
		print(f"WINDOW WIDTH: {self.width}")
		self.window = pygame.display.set_mode((self.width, (int(self.width*1.2))))
		pygame.display.set_caption("Sudoku Solver :)")
		self.done = False

		self.msg_size = int(screen_width/60.)#32
		self.msg_font = pygame.font.SysFont('UbuntuMono',self.msg_size)
		self.large_size = int((screen_width)/30.)
		self.large_font = pygame.font.SysFont('UbuntuMono',self.large_size)

		# Defining some commonly used colors
		self.white = (255,255,255)
		self.gray = (150,150,150)
		self.black = (0,0,0)
		self.lightblue = (179,242,255)
		self.lightyellow = (255,255,153)
		self.lightgreen = (153,255,170)
		self.purple = (184,143,205)
		self.pink = (245,137,209)

		self.window.fill(self.white)

		self.buff = int(self.width/15.) #50
		self.size = size
		if self.size == 0:
			self.choose_size()
			self.window.fill(self.white)

		self.sqt = int(np.sqrt(self.size))
		self.sq_size = int((self.width-2*self.buff)/self.size)
		# Number font:
		self.font = pygame.font.SysFont('UbuntuMono', int(0.8*self.sq_size))   #pygame.font.get_default_font()

		# Defining the board border (lol) sizes
		# If the board has more squares the lines are thinner.
		self.line = int(screen_width/(25*self.size))
		self.halfline = int(0.5*self.line)


		self.board = np.zeros((self.size, self.size), dtype=int)

		# Drawing a gray box to surround each number space.
		for r in range(self.size):
			for c in range(0, self.size):
				x = self.buff+c*self.sq_size
				y = self.buff+r*self.sq_size
				rect = pygame.Rect(x, y, self.sq_size, self.sq_size)
				pygame.draw.rect(self.window, self.gray, rect, self.halfline)

		# Drawing the dark black boarders around squares and the edges.
		for r in range(self.sqt+1):
			x = self.buff+(r*self.sqt)*self.sq_size
			y1 = self.buff - self.halfline
			y2 = self.buff+self.size*self.sq_size + self.halfline
			pygame.draw.line(self.window, self.black, (x,y1), (x,y2), self.line)

		for c in range(self.sqt+1):
			x1 = self.buff #- self.halfline
			x2 = self.buff+self.size*self.sq_size #+ self.halfline
			y = self.buff+(c*self.sqt)*self.sq_size
			pygame.draw.line(self.window, self.black, (x1,y), (x2,y), self.line)

		## putting some legend messages for the color coded boxes
		startmsg = "Starting"
		logicmsg = "Logic-ed"
		bfmsg = "Brute Forced"

		sw,sh = self.msg_font.size(startmsg)
		lw,lh = self.msg_font.size(logicmsg)
		bw,bh = self.msg_font.size(bfmsg)

		freespace = self.width - sw - lw - bw
		d = freespace/4

		start = Msg(startmsg, d, self.width*1.1, self.lightblue) #{'msg':startmsg, 'w':d, 'h':self.width*1.1, 'c':self.lightblue}
		logic = Msg(logicmsg, sw+2*d, self.width*1.1, self.lightgreen) #{'msg':logicmsg, 'w':sw+2*d, 'h':self.width*1.1, 'c':self.lightgreen}
		bf = Msg(bfmsg, 3*d+sw+lw, self.width*1.1, self.pink) #{'msg':bfmsg, 'w':3*d+sw+lw, 'h':self.width*1.1, 'c':self.pink}

		self.print_msg(start)
		self.print_msg(logic)
		self.print_msg(bf)

		self.update()

	def update(self):
		pygame.display.update()
		self.fpsClock.tick(self.fps)

	def choose_size(self):
		four = Msg('4', self.buff, self.width/2, self.purple) #{'msg':'4', 'w':self.buff, 'h':self.width/2}
		nine = Msg('9', self.width/2-self.buff, self.width/2, self.purple)#{'msg':'9', 'w':self.width/2-self.buff, 'h':self.width/2}
		sixteen = Msg('16', self.width-4*self.buff, self.width/2, self.purple) #{'msg':'16', 'w':self.width-4*self.buff, 'h':self.width/2}
		infomsg = "Choose your board size!"
		info = Msg(infomsg, self.centermsg(infomsg), self.width*0.25) #{'msg':infomsg, 'w':self.centermsg(infomsg), 'h':self.width*0.25, 'c':None}
		self.print_msg(info)
		self.print_large(four)
		self.print_large(nine)
		self.print_large(sixteen)
		sizeBool = True
		while sizeBool:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					x,y = event.pos
					if self.large_isclicked(four, (x,y)):
						self.size = 4
						sizeBool = False
						break
					elif self.large_isclicked(nine, (x,y)):
						self.size = 9
						sizeBool = False
						break
					elif self.large_isclicked(sixteen, (x,y)):
						self.size = 16
						sizeBool = False
						break

	def print_large(self, msg):
		w,h = self.large_font.size(msg.m)
		s = (w if w>h else h)
		s *= 1.2
		if msg.c is not None:
			box = pygame.Rect(msg.w, msg.h, s, s)
			outline = pygame.Rect(msg.w, msg.h, s, s)
			pygame.draw.rect(self.window, msg.c, box)
			pygame.draw.rect(self.window, self.black, outline, 2)
		self.window.blit(self.large_font.render(msg.m, True, self.black), (msg.w-(w-s)/2, msg.h))
		self.update()

	def large_isclicked(self, msg, pos):
		x,y = pos
		w,h = self.large_font.size(msg.m)
		s = (w if w>h else h)
		bw = msg.w
		bh = msg.h
		return ((bw <= x <= bw+s) and (bh <= y <= bh+s))

	def print_msg(self, msg):
		w,h = self.msg_font.size(msg.m)
		if msg.c is not None:
			box = pygame.Rect(msg.w, msg.h, w, h)
			pygame.draw.rect(self.window, msg.c, box)
		self.window.blit(self.msg_font.render(msg.m, True, self.black), (msg.w, msg.h))
		self.update()

	def cover(self, msg):
		w,h = self.msg_font.size(msg.m)
		box = pygame.Rect(msg.w, msg.h, w, h)
		pygame.draw.rect(self.window, self.white, box)
		self.update()

	def centermsg(self, msg):
		mw, mh = self.msg_font.size(msg)
		msg_width = (self.window.get_size()[0] - mw)*0.5
		return msg_width

	def FillFromScratch(self, board=None, mistake_box=False):
		print("we are filling from scratch!")
		infomsg = "Click to input the starting numbers."
		donemsg = "Press Enter to start solving!"
		mistakemsg = "U have a mistake. Pls fix"
		txt_height = self.msg_font.size(infomsg)[1]
		info = Msg(infomsg, self.centermsg(infomsg), self.width) #{'msg':infomsg, 'w':self.centermsg(infomsg), 'h':self.width, 'c':None}
		done = Msg(donemsg, self.centermsg(donemsg), self.width+txt_height) #{'msg':donemsg, 'w':self.centermsg(donemsg), 'h':self.width+txt_height, 'c':None}
		mistake = Msg(mistakemsg, self.centermsg(mistakemsg), self.width+2*txt_height) #{'msg':mistakemsg, 'w':self.centermsg(mistakemsg), 'h':self.width+2*txt_height, 'c':None}
		self.print_msg(info)
		self.print_msg(done)

		b = True
		while b:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					x,y = event.pos
					#Next highlight this square
					r = (y-self.buff)//self.sq_size
					c = (x-self.buff)//self.sq_size
					x = self.buff+c*self.sq_size
					y = self.buff+r*self.sq_size
					if 0<=r<self.size and 0<=c<self.size:
						if mistake_box is True:
							self.cover(mistake)
							mistake_box = False
						#highlight the clicked square:
						rect = pygame.Rect(x+self.halfline, y+self.halfline, self.sq_size-self.line, self.sq_size-self.line)
						pygame.draw.rect(self.window, self.lightyellow, rect)
						self.update()
						pygame.event.clear()
						brk = False
						while not brk:
							pygame.event.wait()
							for event in pygame.event.get():
								try:
									num = int(event.text)
									#cover up the highlight
									if num != 0:
										#add the number entered
										w,h = self.font.size(str(num))
										w_add = (self.sq_size - w)*0.5
										h_add = (self.sq_size - h)*0.5
										pygame.draw.rect(self.window, self.lightblue, rect)
										self.window.blit(self.font.render(str(num), True, self.black), (x+w_add, y+h_add))
									else:
										# clear square
										pygame.draw.rect(self.window, self.white, rect)
									self.board[r][c] = num
									self.update()
									brk = True
									break
								except ValueError:
									pass
								except AttributeError:
									pass
				elif event.type == 768:   #RETURN KEY. for some reason pygame.K_RETURN does not work...
					b = False
					break
		self.cover(info)
		self.cover(done)
		#self.update()
		return self.board

	def enterNumber(self, num, r, c, color=None, update=True):
		if color is None:
			color = self.lightblue
		x = (c*self.sq_size)+self.buff
		y = (r*self.sq_size)+self.buff
		rect = pygame.Rect(x+self.halfline, y+self.halfline, self.sq_size-self.line, self.sq_size-self.line)
		pygame.draw.rect(self.window, color, rect)
		if num != 0:
			w,h = self.font.size(str(num))
			w_add = (self.sq_size - w)*0.5
			h_add = (self.sq_size - h)*0.5
			self.window.blit(self.font.render(str(num), True, self.black), (x+w_add, y+h_add))
		if update is True:
			self.update()

	def FillFromBoard(self, newboard, update=True):
		self.board = newboard
		for r in range(self.size):
			for c in range(self.size):
				num = self.board[r][c]
				if num != 0:
					self.enterNumber(num, r, c, color=None, update=update)

	def spin(self):
		infomsg = "Press ESC or click the X to exit."
		info = Msg(infomsg, self.centermsg(infomsg), self.width) #{'msg':infomsg, 'w':self.centermsg(infomsg), 'h':self.width, 'c':None}
		self.print_msg(info)
		while not self.done:
			pressed = pygame.key.get_pressed()
			if pressed[K_ESCAPE]:
				self.done = True
			for event in pygame.event.get():
				 if event.type == pygame.QUIT:
					 self.done = True
			pygame.event.pump()
			self.fpsClock.tick(self.fps)
		print("Goodbye!")
		pygame.quit()

import pygame
from pygame.locals import *
import time
import numpy as np
import argparse
import thread6

import CurrentPlace


class Draw:
	def __init__(self, size):
		pygame.init()
		self.fps = 60
		self.fpsClock = pygame.time.Clock()
		self.width = 800
		self.window = pygame.display.set_mode((self.width, (int(self.width*1.2))))
		pygame.display.set_caption("Sudoku Solver :)")
		self.size = size
		self.sqt = int(np.sqrt(size))
		self.buff = 50
		self.sq_size = int((self.width-2*self.buff)/self.size)
		self.font = pygame.font.Font(pygame.font.get_default_font(), int(0.8*self.sq_size))
		self.msg_size = 24
		self.msg_font = pygame.font.SysFont('ubuntu',self.msg_size)
		self.done = False

		self.board = np.zeros((self.size, self.size), dtype=int)
		#self.BO = BoardOps(self.board)

		self.white = (255,255,255)
		self.gray = (150,150,150)
		self.black = (0,0,0)
		self.lightblue = (179,242,255)
		self.lightyellow = (255,255,153)
		self.lightgreen = (153,255,170)
		self.purple = (184,143,205)
		self.pink = (245,137,209)

		self.line = 6
		self.halfline = 0.5*self.line

		self.window.fill(self.white)

		for r in range(self.size):
			for c in range(0, self.size):
				x = self.buff+c*self.sq_size
				y = self.buff+r*self.sq_size
				rect = pygame.Rect(x, y, self.sq_size, self.sq_size)
				pygame.draw.rect(self.window, self.gray, rect, self.line)

		for r in range(self.sqt+1):
			x1 = self.buff+(r*self.sqt)*self.sq_size
			x2 = self.buff+(r*self.sqt)*self.sq_size
			y1 = self.buff
			y2 = self.buff+self.size*self.sq_size
			pygame.draw.line(self.window, self.black, (x1,y1), (x2,y2), self.line)

		for c in range(self.sqt+1):
			x1 = self.buff
			x2 = self.buff+self.size*self.sq_size
			y1 = self.buff+(c*self.sqt)*self.sq_size
			y2 = self.buff+(c*self.sqt)*self.sq_size
			pygame.draw.line(self.window, self.black, (x1,y1), (x2,y2), self.line)

		self.update()

	def update(self):
		pygame.display.update()
		self.fpsClock.tick(self.fps)

	def print_msg(self, msg, color=None):
		w,h = self.msg_font.size(msg['msg'])
		if color is not None:
			box = pygame.Rect(msg['w'], msg['h'], w, h)
			pygame.draw.rect(self.window, color, box)
		self.window.blit(self.msg_font.render(msg['msg'], True, self.black), (msg['w'], msg['h']))
		self.update()

	def cover(self, msg):
		w,h = self.msg_font.size(msg['msg'])
		box = pygame.Rect(msg['w'], msg['h'], w, h)
		pygame.draw.rect(self.window, self.white, box)
		self.update()

	def centermsg(self, msg):
		mw, mh = self.msg_font.size(msg)
		msg_width = (self.window.get_size()[0] - mw)*0.5
		return msg_width

	def FillFromScratch(self, board=None, mistake_box=False):
		infomsg = "Click on the boxes and enter your numbers."
		donemsg = "Press Enter To Continue!"
		mistakemsg = "U have a mistake. Pls fix"
		txt_height = self.msg_font.size(infomsg)[1]
		info = {'msg':infomsg, 'w':self.centermsg(infomsg), 'h':self.width, 'c':None}
		done = {'msg':donemsg, 'w':self.centermsg(donemsg), 'h':self.width+txt_height, 'c':None}
		mistake = {'msg':mistakemsg, 'w':self.centermsg(mistakemsg), 'h':self.width+2*txt_height, 'c':None}
		self.print_msg(info, color=info['c'])
		self.print_msg(done, color=done['c'])

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

	def run(self):
		#M = Methods(self.board,verbose=False)
		#M.go()
		#self.BO.update(self.board)
		while not self.done:
			pressed = pygame.key.get_pressed()
			if pressed[K_ESCAPE]:
				self.done = True
			for event in pygame.event.get():
				 if event.type == pygame.QUIT:
					 self.done = True

			if len(CurrentPlace.current)!=0:
				fst = CurrentPlace.current[0]
				r, c, n = fst
				CurrentPlace.current = CurrentPlace.current[1:]
				print(fst)
				self.enterNumber(n, r, c, color=self.lightgreen)
			else:
				if self.BO.isdone():
					print("DONE!")
			pygame.event.pump()
			self.fpsClock.tick(self.fps)
		print("Goodbye!")



"""
parser = argparse.ArgumentParser(description='Solve a sudoku!')
parser.add_argument('-n', '--nums', type=int, nargs='+', help='Numbers of the sudoku from top-left to bottom-right. Empty spaces should be denoted as 0. If not inputted, you will fill it out manually in a second!')
args = parser.parse_args()
if args.nums is not None:
	nums = np.array(args.nums)
	l = len(nums)
	if (int(np.sqrt(l)))**2 != l:
		print(f"Size must be a square. You inputted {l} numbers.")
		exit()
	size = int(np.sqrt(l))
	if nums.max()>size or nums.min()<0:
		print(f"All numbers must be within range of 0 - {size}!")
		exit()
	board = nums.reshape(size, size)
	d = Draw(size)
	d.FillFromBoard(board)
	BF = Brute(board, verbose=True,threaded=True)
	print("Hi")
	thread6.run_threaded(d.bf_wrap())
	thread6.run_threaded(BF.go())

else:
	d = Draw(9)
	b = d.FillFromScratch()
"""

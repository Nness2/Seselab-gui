# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
from probe  import Probe
from memory import Memory
from cpu import CPU
import tkinter
import tkinter.font as tkFont
import sys
import linecache
import random
import time

def splitInfos(space, contents): # make space betwin differents elements
	text = contents
	size = len(text)
	while size < space:
		text = text + ' '
		size += 1
	return text

def getProgram (k, program): 
	t = ''
	for i in program[k][0]:
		for j in i:
			if j == 'reg':
				t = t+' r'
			if j == 'imm':
				t = t+' #'
			if j == 'mem':
				t = t+' @'
			if j != 'reg' and j != 'imm' and j != 'mem':
				t = t+str(j)
	return t

def getInfos (program, i):
	takeAll = ''
	file = program[i][1][0]
	line =program[i][1][1]
	if line < 0:
		line = program[i][0][1][1]
		file = program[i][1][2]+'.asm'
	code = linecache.getline(file, line)
	code = code.replace('\t','')
	code = code.replace('\n','')
	takeAll = splitInfos(20, getProgram(i,program))+splitInfos(20, code)+file+'  L.'+str(line)
	return takeAll

def stackInfos(program):
	i = 0
	instrs = []
	for instr in program:
		instrs.append(getInfos(program,i))
		i += 1
	instrs.append("end")
	instrs.append("")
	return instrs

class Interface:

	def __init__(self, code):
		self._i = 0
		self._ip = 0 # init instruction pointer
		self.flag = 0
		self._code = code
		self._ram = Memory(1048576)
		self._reg = Memory(32)
		self.__ra = 32 - 1
		self.__sp = 32 - 2
		self._probe = Probe(sys.argv[2])
		self._root = Tk()
		self._current = 0
		self.openRegList()
		self._root.title('Seselab')
		self._dm = 1
		# self._root.geometry("490x250")
		self._infos = stackInfos(code)
		default_font = tkFont.nametofont("TkFixedFont")
		default_font.configure(size=15)
		self._lab1 = Label(self._root, text='', bg='white', width=60, anchor='w',font="TkFixedFont")
		self._lab2 = Label(self._root, text=self._infos[0], bg='yellow', width=60, anchor='w',font="TkFixedFont")
		self._lab3 = Label(self._root, text=self._infos[1], bg='white', width=60, anchor='w',font="TkFixedFont")
		self._lab1.grid(column = 1, row = 1, columnspan=8, sticky='w')
		self._lab2.grid(column = 1, row = 2, columnspan=8, sticky='w')
		self._lab3.grid(column = 1, row = 3, columnspan=8, sticky='w')
		self._space = Label(self._root, text='', bg='white', width=60, anchor='w', font="TkFixedFont").grid(column = 1, row = 4, columnspan=8, sticky='w', )
		self._step = Button(self._root, text="Step", command=self.step, width = 10).grid(column=9, row=1, sticky='nesw')
		self._run = Button(self._root, text="Run", command=self.run, width = 10).grid(column=9, row=2, sticky='nesw')
		self._breaK = Button(self._root, text="Break", command=self.breaK, width = 10).grid(column=9, row=3, sticky='nesw')
		self._reset = Button(self._root, text="Reset", command=self.breaK, width = 10).grid(column=9, row=4, sticky='nesw')
		# self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=1, row=9, sticky='we', pady = 4)
 	
	def openRegList (self):
		self._regLst = []
		i = 0
		for j in range(4):
			for k in range(8):
				l = Button(self._root, text='r'+str(i)+': '+str(self._reg[i]), bg='white', width = 5,command=lambda x=i : self.select(x))
				l.grid(column = k+1, row = j+5, sticky='we')
				self._regLst.append(l)
				i += 1
		self._regLst[0].config(bg='yellow')
		fault = Button(self._root, text="Inject fault", command=self.injctRand, width = 10).grid(column=1, row=9, sticky='we', pady = 4, columnspan=2)
		zero = Button(self._root, text="Set to zero", command=self.SetToZero, width = 10).grid(column=3 , row=9, sticky='we', pady = 4, columnspan=2)

	def select (self, x):
		self._regLst[self._current].config(bg='white')
		self._regLst[x].config(bg='yellow')
		self._current = x

	def SetToZero (self):
		self._regLst[self._current].config(text='r'+str(self._current)+': 0')
		self._reg[self._current] = 0
		cpu._reg[self._current] = 0


	def injctRand (self):
		r = random.randint(0,255)
		self._regLst[self._current].config(text='r'+str(self._current)+': '+str(r))
		self._reg[self._current] = r
		cpu._reg[self._current] = r

	def change (self):
		self._lab1.config(text=self._infos[self._i])
		self._lab2.config(text=self._infos[self._i+1])
		self._lab3.config(text=self._infos[self._i+2])
		self._i += 1
		self.runC()

	def tempo(self):
		self.change()
		for i in range (32):
			self._regLst[i].config(text='r'+str(i)+': '+str(cpu._reg[i]))
		if self._infos[self._i] != 'end':
			if self.flag > 0: 
				self._root.after(50,self.tempo)

	def run(self):	
		if self.flag == 0:
			self.flag = 1
			self.tempo()
		self.runC()

	def step(self):
		if self._infos[self._i] != 'end':
			self._lab1.config(text=self._infos[self._i])
			self._lab2.config(text=self._infos[self._i+1])
			self._lab3.config(text=self._infos[self._i+2])
			self._i += 1
			self.runC()
		for i in range (32):
			self._regLst[i].config(text='r'+str(i)+': '+str(cpu._reg[i]))
			
	def breaK(self):
		if self._infos[self._i] != 'end':
			self.flag = 0

	def runC (self):
		init = 1
		if init == 1:
			max_ip = len(self._code)
			self._reg[self.__sp] = self._ram._size # init stack pointer
			self._reg[self.__ra] = max_ip # init return address
			init = 0
		try:
			if self._ip >= 0 and self._ip < max_ip:
				ip = cpu.cycle(self._ip)
				if ip is not None:
					self._ip = ip
				else:
					self._ip += 1
				self._probe.read(self._ram.get_activity())
				self._probe.read(self._reg.get_activity())
				self._probe.output_activity()
				sys.stdout.flush()
				
		except AddrError as e:
			print('Invalid address ' + str(e.addr) + cpu.dbg(self._ip))
		except ValError as e:
			print('Invalid value ' + str(e.val) + cpu.dbg(self._ip))
		except WriteError:
			print('Invalid write ' + cpu.dbg(self._ip))


program = Compiler().compile(sys.argv[1])
cpu = CPU(1048576, 32, program, sys.argv[2])
main = Interface(program)
mainloop()


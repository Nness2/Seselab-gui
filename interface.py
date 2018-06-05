# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
from probe  import Probe
from memory import Memory
from cpu import CPU
from tkinter import filedialog
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

	def __init__(self):
		self._i = 0
		self._ip = 0 # init instruction pointer
		self.flag = 0
		# self._root.geometry("490x250")
		self._root = Tk()
		self._current = 0
		self._root.title('Seselab')
		self._dm = 1
		self.openRegList()
		font = tkFont.nametofont("TkFixedFont")
		font.configure(size=17)

		#LABEL
		self._space = Label(self._root, text='', bg=None).grid(column = 1, row = 5)
		self._injectFault = Label(self._root, text='Inject fault:', bg=None, width=10, font=('helvetic', 11, 'bold'))
		self._lab1 = Label(self._root, text='', bg='white', width=61, anchor='w',font="TkFixedFont")
		self._lab2 = Label(self._root, text='', bg='white', width=61, anchor='w',font="TkFixedFont")
		self._lab3 = Label(self._root, text='', bg='white', width=61, anchor='w',font="TkFixedFont")
		self._lab1.grid(column = 1, row = 2, columnspan=7, sticky='w', padx = 1)
		self._lab2.grid(column = 1, row = 3, columnspan=7, sticky='w', padx = 1)
		self._lab3.grid(column = 1, row = 4, columnspan=7, sticky='w', padx = 1)
		self._injectFault.grid(column = 1, row = 11, columnspan=8, sticky='w', padx = 8)
		#BUTTON
		self._step = Button(self._root, text="Step", command=self.step, width = 6, font=('helvetic', 10), state='disabled')
		self._step.grid(column=8, row=2, sticky='nesw', padx=2)
		self._breaK = Button(self._root, text="Break", command=self.breaK, width = 6, font=('helvetic', 10), state='disabled')
		self._breaK.grid(column=8, row=4, sticky='nesw', padx=2)
		self._run = Button(self._root, text="Run", command=self.run, width = 6, font=('helvetic', 10), state='disabled')
		self._run.grid(column=8, row=3, sticky='nesw', padx=2)
		self._toRand = Button(self._root, text="Random", command=self.setRand, width = 6, font=('helvetic', 11), state='disabled')
		self._toRand.grid(column=2, row=11, sticky='we', pady = 4)
		self._toZero = Button(self._root, text="Zero", command=self.setToZero, width = 6, font=('helvetic', 11), state='disabled')
		self._toZero.grid(column=3 , row=11, sticky='we', pady = 4)
		self._reset = Button(self._root, text="Reset", command=self.load, width = 6, font=('helvetic', 11), state='disabled')
		self._reset.grid(column=5, row=0, sticky='nesw', pady=2)
		self._quit = Button(self._root, text="Close", command=self._root.quit, width = 6, font=('helvetic', 11)).grid(column=7, row=11, sticky='we', columnspan=2)
		self._open = Button(self._root, text="Open file", command=self.openFile, width = 6, font=('helvetic', 11)).grid(column=3, row=0, sticky='nesw', pady=2)
		self._load = Button(self._root, text="Load", command=self.load, width = 6, font=('helvetic', 11)).grid(column=4, row=0, sticky='nesw', pady=2)
		self.whichFile()
		# value = StringVar() 
		# value.set('50 ms')
		# self._entree = Entry(self._root, text=value, width=5)
		# self._entree.grid(column=9, row=3, sticky='w', padx = 2)
		# self._reset = Button(self._root, text="Reset", command=self.breaK, width = 10).grid(column=8, row=4, sticky='nesw', padx=0, pady=0)

	def openFile (self):
		filename =  filedialog.askopenfilename(initialdir = "/home",title = "Select file",filetypes = (("asm files","*.asm"),("all files","*.*")))
		self._file.delete(0,17)
		self._file.insert(0,filename)

	def whichFile (self):
		value = StringVar() 
		try:
			value.set(sys.argv[1])
			self._file = Entry(self._root, text=value, width=25, font=('helvetic', 12))
			self._file.grid(column=1, row=0, sticky='w', padx = 7, pady = 5, columnspan=2)
			self.load()
		except:
			value.set('Choose a file ...')
			self._file = Entry(self._root, text=value, width=25, font=('helvetic', 12))
			self._file.grid(column=1, row=0, sticky='w', padx = 7, pady = 5, columnspan=2)

	def load (self):
		self._code = Compiler().compile(self._file.get())
		self.cpu = CPU(1048576, 32, self._code, '/dev/null')
		self._ram = Memory(1048576)
		self._reg = Memory(32)
		self.__ra = 32 - 1
		self.__sp = 32 - 2
		self._ip = 0
		self._i = 0
		self._probe = Probe('/dev/null')
		self._infos = stackInfos(self._code)
		self._step.config(state='normal')
		self._breaK.config(state='normal')
		self._run.config(state='normal')
		self._toRand.config(state='normal')
		self._toZero.config(state='normal')
		self._reset.config(state='normal')
		self._lab1.config(text='')
		self._lab2.config(text=self._infos[0],bg='yellow')
		self._lab3.config(text=self._infos[1])
		self.flag = 0
		for i in range (32):
			self._regLst[i].config(text='r'+str(i)+': '+'0')

	def select (self, x):
		self._regLst[self._current].config(bg='white')
		self._regLst[x].config(bg='yellow')
		self._current = x

	def openRegList (self):
		self._regLst = []
		i = 0
		for j in range(4):
			for k in range(8):
				l = Button(self._root, text='r'+str(i)+': '+str(0), bg='white', width = 9,command=lambda x=i : self.select(x), font=('helvetic', 11))
				l.grid(column = k+1, row = j+7, sticky='we')
				self._regLst.append(l)
				i += 1
		self._regLst[0].config(bg='yellow')

	def setToZero (self):
		self._regLst[self._current].config(text='r'+str(self._current)+': 0')
		self.cpu._reg[self._current] = 0


	def setRand (self):
		r = random.randint(0,255)
		self._regLst[self._current].config(text='r'+str(self._current)+': '+str(r))
		self.cpu._reg[self._current] = r

	def change (self):
		for i in range (32):
			self._regLst[i].config(text='r'+str(i)+': '+str(self.cpu._reg[i]))
		self._lab1.config(text=self._infos[self._i])
		self._lab2.config(text=self._infos[self._i+1])
		self._lab3.config(text=self._infos[self._i+2])
		self._i += 1
		self.runC()

	def step (self):
		if self._infos[self._i] != 'end':
			self.change()
 
	def tempo (self):
		if self.flag == 1: 
			if self._infos[self._i] != 'end':
				self.change()
				self._root.after(50,self.tempo)

	def run (self):
		if self.flag == 0:
			self.flag = 1
			self.tempo()
			self._toRand.config(state='disabled')
			self._toZero.config(state='disabled')
			self.runC()
			
	def breaK (self):
		self.flag = 0
		self._toRand.config(state='normal')
		self._toZero.config(state='normal')

	def runC (self):
		init = 1
		if init == 1:
			max_ip = len(self._code)
			self._reg[self.__sp] = self._ram._size # init stack pointer
			self._reg[self.__ra] = max_ip # init return address
			init = 0
		try:
			if self._ip >= 0 and self._ip < max_ip:
				ip = self.cpu.cycle(self._ip)
				if ip is not None:
					self._ip = ip
				else:
					self._ip += 1
				self._probe.read(self._ram.get_activity())
				self._probe.read(self._reg.get_activity())
				self._probe.output_activity()
				sys.stdout.flush()
				
		except AddrError as e:
			print('Invalid address ' + str(e.addr) + self.cpu.dbg(self._ip))
		except ValError as e:
			print('Invalid value ' + str(e.val) + self.cpu.dbg(self._ip))
		except WriteError:
			print('Invalid write ' + self.cpu.dbg(self._ip))



main = Interface()
mainloop()


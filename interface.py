# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
from cpu import CPU
import linecache
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

def getInfos (program,i):
	takeAll = ''
	file = program[i][1][0]
	line =program[i][1][1]
	if line < 0:
		line = program[i][0][1][1]
		file = program[i][1][2]+'.asm'
	code = linecache.getline(file, line)
	code = code.replace('\t','')
	code = code.replace('\n','')
	takeAll = splitInfos(25, getProgram(i,program))+splitInfos(20, code)+file+'  L.'+str(line)
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
		self.f = 0
		self._i = 0
		self._ip = 1
		self._root = Tk()
		self._root.title('Seselab') 
		self._root.geometry("490x160")
		self._infos = stackInfos(code)
		self._lab1 = Label(self._root, text='', bg='white', width=60, anchor='w')
		self._lab2 = Label(self._root, text=self._infos[0], bg='yellow', width=60, anchor='w')
		self._lab3 = Label(self._root, text=self._infos[1]+'\n', bg='white', width=60, anchor='w')
		self._lab1.grid(column = 1, row = 1, columnspan=6)
		self._lab2.grid(column = 1, row = 2, columnspan=6)
		self._lab3.grid(column = 1, row = 3, columnspan=6)
		self._step = Button(self._root, text="Step", command=self.step).grid(column=1, row=4, sticky='we')
		self._run = Button(self._root, text="Run", command=self.run).grid(column=2, row=4, sticky='we')
		self._breaK = Button(self._root, text="Break", command=self.breaK).grid(column=3, row=4, sticky='we')
		self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=1, row=6, sticky='we', pady = 4)

	def change(self):
		self._lab1.config(text=self._infos[self._i])
		self._lab2.config(text=self._infos[self._i+1])
		self._lab3.config(text=self._infos[self._i+2]+'\n')
		cpu.run(self._ip)
		self._ip += 1

	def step(self):
		if self._infos[self._i] != 'end':
			self.change()
			self._i += 1

	def run(self):
		while self._infos[self._i] != 'end':
			self.change()
			self._i += 1
			i = 0

	def breaK(self):
		print(':)')


if sys.argv[1] == '-i':
    signal.signal(signal.SIGINT, inject)
    sys.argv.pop(1)

program = Compiler().compile(sys.argv[1])
cpu = CPU(1048576, 32, program, sys.argv[2])
main = Interface(program)
mainloop()


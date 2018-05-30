# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
import linecache

def splitInfos(space, contents):
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

def getInfo (program,i):
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

def getInfos(program):
	i = 0
	instrs = []
	for instr in program:
		instrs.append(getInfo(program,i))
		i += 1
	instrs.append("end")
	instrs.append("")
	return instrs

class Interface:

	def __init__(self, code):
		self._i = 0
		self._root = Tk()
		self._root.title('Seselab') 
		self._root.geometry("520x160")
		self._infos = getInfos(code)
		self._lab1 = Label(self._root, text='', bg='white', width=60, anchor='w')
		self._lab2 = Label(self._root, text=self._infos[0], bg='yellow', width=60, anchor='w')
		self._lab3 = Label(self._root, text=self._infos[1]+'\n', bg='white', width=60, anchor='w')
		self._lab1.grid(column = 1, row = 1)
		self._lab2.grid(column = 1, row = 2)
		self._lab3.grid(column = 1, row = 3)
		self._step = Button(self._root, text="Step by step", command=self.stepByStep).grid(column=1, row=4, sticky='w')
		self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=1, row=7, sticky='w', pady = 4)

	def change(self, i):
		self._lab1.config(text=self._infos[self._i])
		self._lab2.config(text=self._infos[self._i+1])
		self._lab3.config(text=self._infos[self._i+2]+'\n')

	def stepByStep(self):
		if self._infos[self._i] != 'end':
			self.change(self._i)
			self._i += 1




program = Compiler().compile(sys.argv[1])
main = Interface(program)
mainloop()


# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
import linecache

def getProgram (k, program):
	t = ''
	for i in program[k][0]:
		for j in i:
			if j == 'reg':
				t = t+' r'
			if j == 'imm':
				t = t+' #'
			if j != 'reg' and j != 'imm':
				t = t + str(j)
	return t

def getInfo (program,i):
	file = program[i][1][0]
	line =program[i][1][1]
	code = linecache.getline(file, line)
	code = code.replace('\t','')
	code = code.replace('\n','')
	takeAll = """{code} {file} {line} {prog} 
	""".format(code=code, file=program[i][1][0] , line=program[i][1][1]-1, prog=getProgram(i,program))
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
		self._root.geometry("480x160")
		self._infos = getInfos(code)
		self._lab1 = Label(self._root, text='', bg='white', width=50, anchor='w')
		self._lab2 = Label(self._root, text=str(self._infos[1]), bg='yellow', width=50, anchor='w')
		self._lab3 = Label(self._root, text=str(self._infos[2]), bg='white', width=50, anchor='w')
		self._lab1.grid(column = 1, row = 1)
		self._lab2.grid(column = 1, row = 2)
		self._lab3.grid(column = 1, row = 3)
		self._step = Button(self._root, text="Step by step", command=self.stepByStep).grid(column=1, row=4, sticky='w')
		self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=1, row=7, sticky='w', pady = 4)

	def change(self, i):
		self._lab1.config(text=str(self._infos[self._i+1]))
		self._lab2.config(text=str(self._infos[self._i+2]))
		self._lab3.config(text=str(self._infos[self._i+3]))

	def stepByStep(self):
		if self._infos[self._i] != 'end':
			self.change(self._i)
			self._i += 1




program = Compiler().compile(sys.argv[1])
main = Interface(program)
mainloop()


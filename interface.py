# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
import linecache


def getInfo (program,i):
	file = program[i][1][0]
	line =program[i][1][1]-1
	code = linecache.getline(file, line)
	code = code.replace('\t','')
	code = code.replace('\n','')
	return [code,file,line]

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
		self._root.geometry("680x240")
		self._code = code
		self._infos = getInfos(self._code)
		self._lab1 = Label(self._root, text=' ', bg='white', width=80)
		self._lab2 = Label(self._root, text=str(self._infos[1])+"\t"+str(code[0][0]), bg='white', width=80)
		self._lab3 = Label(self._root, text=str(self._infos[2])+"\t"+str(code[1][0]), bg='white', width=80)
		self._lab1.grid(padx=10, pady=10, column = 1, row = 1)
		self._lab2.grid(padx=10, pady=10, column = 1, row = 2)
		self._lab3.grid(padx=10, pady=10, column = 1, row = 3)
		self._step = Button(self._root, text="Step by step", command=self.stepByStep).grid(column=1, row=4, sticky='ew')
		self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=1, row=7, sticky='ew', pady = 4)

	def change(self, i):
		self._lab1.config(text=str(self._infos[self._i+1])+'\t'+str(self._code[i][0]))
		self._lab2.config(text=str(self._infos[self._i+2])+'\t'+str(self._code[i+1][0]))
		self._lab3.config(text=str(self._infos[self._i+3])+'\t'+str(self._code[i+2][0]))

	def stepByStep(self):
		if self._infos[self._i] != 'end':
			self.change(self._i)
			self._i += 1




program = Compiler().compile(sys.argv[1])
main = Interface(program)
mainloop()


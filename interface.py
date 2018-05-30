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

		self._t = Text(self._root,height=6, width=45)
		self._t.grid(padx=10, pady=10, column = 2, row = 1)
		self._t.insert(END,'\n\n\n'+str(self._infos[1])+'\n\n'+str(self._infos[2])+'\n')
		self._t.config(state='disabled')

		self._t2 = Text(self._root,height=6, width=45)
		self._t2.grid(padx=10, pady=10, column = 1, row = 1)
		self._t2.insert(END,'\n\n\n'+str(code[0][0])+'\n\n'+str(code[1][0])+'\n')
		self._t2.config(state='disabled')

		self._step = Button(self._root, text="Step by step", command=self.stepByStep).grid(column=1, row=4, sticky='ew')
		self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=1, row=7, sticky='ew', pady = 4)

	def change(self, i):
		self._t.config(state='normal')
		self._t.delete('1.0', END)
		self._t.insert(END, '\n'+str(self._infos[i+1])+'\n\n'+str(self._infos[i+2])+'\n\n'+str(self._infos[i+3])+'\n')
		self._t.config(state='disabled')
		self._t2.config(state='normal')
		self._t2.delete('1.0', END)
		self._t2.insert(END, '\n'+str(self._code[i][0])+'\n\n'+str(self._code[i+1][0])+'\n\n'+str(self._code[i+2][0])+'\n')
		self._t2.config(state='disabled')

	def stepByStep(self):
		if self._infos[self._i] != 'end':
			self.change(self._i)
			self._i += 1




program = Compiler().compile(sys.argv[1])
main = Interface(program)
mainloop()


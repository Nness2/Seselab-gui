# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 

def getLines(file):
	instrs = []
	with open(file) as instr :
		for line in instr :
			instrs.append(line.strip())
	instr.close()
	return instrs

class Interface:

	def __init__(self):
		self._i = 0
		self._fenetre = Tk()
		self._lines = getLines(sys.argv[1])
		self._lab1 = Label(self._fenetre, text='', bg='white', width=25, anchor='w')
		self._lab1.pack()
		self._lab2 = Label(self._fenetre,text='-> '+self._lines[0], bg='white', width=25, anchor='w')
		self._lab2.pack()
		self._lab3 = Label(self._fenetre, text=' '+self._lines[1], bg='white', width=25, anchor='w')
		self._lab3.pack()
		self._b = Button(self._fenetre, text="Pas-à-pas", command=self.stepByStep).pack(padx=10, pady=10, side = LEFT)
		self._b = Button(self._fenetre, text="Sans interruption").pack(padx=10, pady=10, side = RIGHT)

	def stepByStep(self):
		self._lab1.config(text=' '+self._lines[self._i])
		self._lab2.config(text='-> '+self._lines[self._i+1])
		self._lab3.config(text=' '+self._lines[self._i+2])
		self._i += 1

program = Interface()
mainloop()
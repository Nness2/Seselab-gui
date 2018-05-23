# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 

def getLines(file):
	instrs = []
	with open(file) as instr :
		for line in instr :
			if line != '\n':
				instrs.append(line.strip())
	instr.close()
	instrs.append('end')
	instrs.append('')
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
		self._sb = Button(self._fenetre, text="Pas-à-pas", command=self.stepByStep).pack(padx=10, pady=10, side=LEFT)
		self._ns = Button(self._fenetre, text="Trois par trois", command=self.nStep).pack(padx=10, pady=10, side=LEFT)
		# self._os = Button(self._fenetre, text="Sans interruption").pack(padx=10, pady=10, side=LEFT)
		self._quit=Button(self._fenetre, text="Fermer", command=self._fenetre.quit).pack(padx=10, pady=10, side=BOTTOM)
	
	def stepByStep(self):
		if self._lines[self._i] != 'end':
			self._lab1.config(text=' '+self._lines[self._i])
			self._lab2.config(text='-> '+self._lines[self._i+1])
			self._lab3.config(text=' '+self._lines[self._i+2])
			self._i += 1

	def nStep(self):
		i = 0
		while i < 3:
			if self._lines[self._i] != 'end':
				self._lab1.config(text=' '+self._lines[self._i])
				self._lab2.config(text='-> '+self._lines[self._i+1])
				self._lab3.config(text=' '+self._lines[self._i+2])
				self._i += 1
				i += 1


program = Interface()
mainloop()
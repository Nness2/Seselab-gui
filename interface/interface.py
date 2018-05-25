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
		self._root = Tk()
		self._root.title('Seselab') 
		# self._root.geometry("250x150")
		self._lines = getLines(sys.argv[1])
		self._lab1 = Label(self._root, text=' ', bg='white', width=25, anchor='w')
		self._lab2 = Label(self._root,text='-> '+self._lines[0], bg='white', width=25, anchor='w')
		self._lab3 = Label(self._root, text=' '+self._lines[1], bg='white', width=25, anchor='w')
		self._lab1.grid(columnspan=4, column=1, row=1, padx = 10)
		self._lab2.grid(columnspan=4, column=1, row=2, padx = 10)
		self._lab3.grid(columnspan=4, column=1, row=3, padx = 10)
		self._oneStep = Button(self._root, text="Step by step", command=self.stepByStep).grid(column=1, row=4, sticky='w', padx = 10)
		self._nStep = Button(self._root, text="Jump",width=5 ,command=self.nStep).grid(column=1, row=5, sticky='E', padx = 10)
		self._quit=Button(self._root, text="Close", command=self._root.quit).grid(column = 1,row=6,sticky='w', padx = 10)
		self._value = StringVar() 
		self._value.set('Step')
		self._entree = Entry(self._root, text=self._value, width=6)
		self._entree.grid(column=1, row=5, sticky = 'w', padx = 10)
	
	def stepByStep(self):
		if self._lines[self._i] != 'end':
			self._lab1.config(text=' '+self._lines[self._i])
			self._lab2.config(text='-> '+self._lines[self._i+1])
			self._lab3.config(text=' '+self._lines[self._i+2])
			self._i += 1

	def nStep(self):
		i = 0
		n = self._entree.get()
		while i < int(n[0]):	#gérer les erreurs
			if self._lines[self._i] != 'end':
				self._lab1.config(text=' '+self._lines[self._i])
				self._lab2.config(text='-> '+self._lines[self._i+1])
				self._lab3.config(text=' '+self._lines[self._i+2])
				self._i += 1
			i += 1	


program = Interface()
mainloop()
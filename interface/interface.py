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
		self._root.geometry("450x240")
		self._lines = getLines(sys.argv[1])
		self._t = Text(self._root,height=6, width=60)
		self._t.grid(columnspan=15, padx=10, pady=10, column = 1, row = 1)
		self._t.insert(END,'\n\n\n-> '+self._lines[0]+'\n\n '+self._lines[1]+'\n')
		self._t.config(state='disabled')
		self._oneStep = Button(self._root, text="Step by step", command=self.stepByStep).grid(column=1, row=4, sticky='ew')
		self._nStep = Button(self._root, text="Jump", width=5, command=self.nStep).grid(column=1, row=5, sticky='ew')
		self._rstr = Button(self._root, text="Restart", width=5, command=self.restart).grid(column=1, row=6, sticky='ew')
		self._quit = Button(self._root, text="Close", command=self._root.quit).grid(column=3, row=7, sticky='ew', pady = 4)
		self._value = StringVar() 
		self._value.set('Step')
		self._entree = Entry(self._root, text=self._value, width=5)
		self._entree.grid(column=2, row=5, sticky='ew')
	
	def change(self, i):
		self._t.config(state='normal')
		self._t.delete('1.0', END)
		self._t.insert(END, '\n'+self._lines[i]+'\n\n-> '+self._lines[i+1]+'\n\n '+self._lines[i+2]+'\n')
		self._t.config(state='disabled')

	def restart(self):
		self._i = 0
		self.change(self._i-1)

	def stepByStep(self):
		if self._lines[self._i] != 'end':
			self.change(self._i)
			self._i += 1

	def nStep(self):
		i = 0
		n = self._entree.get()
		while i < int(n[0]):	#gérer les erreurs
			if self._lines[self._i] != 'end':
				self.change(self._i)
				self._i += 1
			i += 1	


program = Interface()
mainloop()

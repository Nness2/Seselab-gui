# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
import linecache

# def getLines(file):
# 	instrs = []
# 	with open(file) as instr :
# 		for line in instr :
# 			if line != '\n':
# 				instrs.append(line.strip())
# 	instr.close()
# 	instrs.append('end')
# 	instrs.append('')
# 	return instrs

def getInfo (l,i):
	file = l[i][1][0]
	line =l[i][1][1]-1
	code = linecache.getline(file, line)
	code = code.replace('\t','')
	code = code.replace('\n','')
	return [code,file,line]

class Interface:

	def __init__(self, code):
		self._i = 0
		self._root = Tk()
		self._root.title('Seselab') 
		self._root.geometry("680x240")
		self._code = code
		self._infos = self.getInfos(self._code)
		# self._lines = getLines(sys.argv[1])

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
		# self._rstr = Button(self._root, text="Restart", width=5, command=self.nStep).grid(column=1, row=6, sticky='ew')
		# self._nStep = Button(self._root, text="Jump", width=5, command=self.nStep).grid(column=1, row=5, sticky='ew')
		# self._value = StringVar() 
		# self._value.set('Step')
		# self._entree = Entry(self._root, text=self._value, width=5)
		# self._entree.grid(column=2, row=5, sticky='ew')

	def getInfos(self, program):
		i = 0
		instrs = []
		for instr in program:
			instrs.append(getInfo(program,i))
			i += 1
		instrs.append("end")
		instrs.append("")
		return instrs

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

	# def restart(self):
	# 	self._i = 0
	# 	self.change(self._i-1)

	# def nStep(self):
	# 	i = 0
	# 	n = self._entree.get()
	# 	while i < int(n[0]):	#gérer les erreurs
	# 		if self._lines[self._i] != 'end':
	# 			self.change(self._i)
	# 			self._i += 1
	# 		i += 1	


program = Compiler().compile(sys.argv[1])
main = Interface(program)
mainloop()


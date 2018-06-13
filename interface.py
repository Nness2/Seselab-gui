# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
from probe  import Probe
from memory import Memory
from cpu import CPU
from instr import Instr
from tkinter import filedialog
import tkinter as tk
import os
import tkinter.font as tkFont
import sys
import random

class Interface:

    def __init__(self):
        self._i = 0
        self.flag = 0
        self._root = Tk()
        self._root.resizable(False, False)
        self._current = 33
        self._root.title('Seselab')
        self._dm = 1
        self.open_reglist()
        self.font = tkFont.nametofont("TkFixedFont")
        self.font.configure(size=14)
        self.which_file()
        self._inject_fault = Label(self._root, text = 'Inject fault:', bg = None, width = 10, font = ('helvetic', 11, 'bold'))
        self._inject_fault.grid(column = 1, row = 10, columnspan = 8, sticky = 'w', padx = 8)
        self._step = self.creat_button(self._root, 'Step', self.event_step, 'disabled', 8, 1)
        self._run = self.creat_button(self._root, 'Run', self.event_run, 'disabled', 8, 2)
        self._run_slow = self.creat_button(self._root, 'Run slowly', self.event_run_slow, 'disabled', 8, 3)
        self._pause = self.creat_button(self._root, 'Pause', self.event_pause, 'disabled', 8, 4)
        self._skip = self.creat_button(self._root, 'Skip', self.event_skip, 'disabled', 8, 5)
        self._to_rand = self.creat_button(self._root, 'Random', self.event_set_rand, 'disabled', 2, 10)
        self._to_zero = self.creat_button(self._root, 'Zero', self.event_set_zero, 'disabled', 3, 10)
        self._reset = self.creat_button(self._root, 'Reset', self.load, 'disabled', 5, 0)
        self._quit= self.creat_button(self._root, 'Close', self._root.quit, 'normal', 8, 12)
        self._pick_file = self.creat_button(self._root, 'Pick file', self.pick_file, 'normal', 3, 0)
        self._load = self.creat_button(self._root, 'Load', self.load, 'normal', 4, 0)

        self._canvas = Canvas(self._root, borderwidth = 0, height = 150, background="#ffffff")
        self._frame = Frame(self._canvas, background = "#ffffff")
        self._vsb = Scrollbar(self._root, orient = "vertical", command = self._canvas.yview)
        self._canvas.configure(yscrollcommand = self._vsb.set)
        self._vsb.grid(rowspan = 5, column = 7, row = 1, sticky = 'nse')
        self._canvas.grid(rowspan = 5, columnspan = 7,column = 1, row = 1, sticky = 'nesw')
        self._canvas.create_window((4,4), window=self._frame, anchor="ne")
        self._frame.bind("<Configure>", lambda event, canvas = self._canvas: self.on_frame_configure(self._canvas))
        self._op = Label(self._root, text = '', anchor = 'w', bg = 'white', width = 85, height = 5, font = self.font, relief = SUNKEN)
        self._op.grid(sticky = 'w',row = 11, column = 1, columnspan = 8, padx = 5,pady = 5)

    def populate(self): 
        self._istr_lst = []
        for row in range(len(self._infos)-1):
            t = self._infos[row]
            l = Label(self._frame, 
                      text = t, 
                      anchor = 'w', 
                      bg = 'white',
                      font = self.font)
            l.grid(row = row, 
                   column = 1)
            self._istr_lst.append(l)

    def on_frame_configure (self, canvas):
        self._canvas.configure(scrollregion = self._canvas.bbox("all"))

    def creat_button (self, root, text, command, state, c, r):
        button = Button(self._root, 
            text = text, 
            command = command, 
            width = 6, font = ('helvetic', 11), 
            state = state)
        button.grid(column = c, 
            row = r, 
            sticky = 'we', 
            pady = 0, 
            padx = 2)
        return button

    def pick_file (self):
        filename = filedialog.askopenfilename(initialdir = os.getcwd(), 
            title = "Select file", 
            filetypes = (("asm files", "*.asm"), ("all files", "*.*")))
        self._file.delete(0, END)
        self._file.insert(0, filename)

    def which_file (self):
        value = StringVar() 
        try:
            value.set(sys.argv[1])
            self._file = Entry(self._root, text = value, width = 22, font = ('helvetic', 12))
            self._file.grid(column = 1, row = 0, sticky = 'w', padx = 7, pady = 5, columnspan = 3)
        except:
            value.set('Choose a file ...')
            self._file = Entry(self._root, text=value, width = 22, font = ('helvetic', 12))
            self._file.grid(column = 1, row = 0, sticky = 'w', padx = 7, pady = 5, columnspan = 3)

    def event_reset (self):
        self._i = 0
        self.cpu = CPU(1048576, 32, self._code, '/dev/null')
        self.cpu._ip += 1
        self._infos = Instr().stack_infos(self._code)
        self.populate()
        self.update_display()
        self.update_reglist()
        self.flag = 0

    def load (self):
        self._i = 0
        self._sortie = ''
        self._code = Compiler().compile(self._file.get())
        self.cpu = CPU(1048576, 32, self._code, '/dev/null')
        self.cpu._ip += 1
        self._infos = Instr().stack_infos(self._code)
        self.populate()
        self.update_display()
        self.button_state('normal')
        self._pause.config(state = 'normal')
        self._reset.config(state = 'normal')
        self.update_reglist()
        self.flag = 0

    def select (self, x):
        if self._current == 33:
            self._reg_lst[x].config(bg = 'yellow')
            self._current = x
            self._to_rand.config(state = 'normal')
            self._to_zero.config(state = 'normal')
        elif self._current == x:
            self._reg_lst[self._current].config(bg = 'white')
            self._current = 33
            self._to_rand.config(state = 'disabled')
            self._to_zero.config(state = 'disabled')
        else:
            self._reg_lst[self._current].config(bg = 'white')
            self._reg_lst[x].config(bg = 'yellow')
            self._current = x
            self._to_rand.config(state = 'normal')
            self._to_zero.config(state = 'normal')

    def open_reglist (self):
        self._reg_lst = []
        i = 0
        for j in range(4):
            for k in range(8):
                l = Button(self._root, 
                    text = 'r'+str(i)+': 0', 
                    bg = 'white', 
                    width = 9, 
                    command = lambda x = i : 
                    self.select(x), 
                    font = ('helvetic', 11))
                l.grid(column = k+1, 
                    row = j+6, 
                    sticky='we')
                self._reg_lst.append(l)
                i += 1

    def update_reglist (self):
        for i in range (32):
            self._reg_lst[i].config(text = 'r'+str(i)+': '+str(self.cpu._reg[i]))

    def update_display (self):
        for i in range (32):
            self._reg_lst[i].config(text='r'+str(i)+': '+str(self.cpu._reg[i]))
            self._canvas.yview_scroll(-2*i,'units')
        if self._i < 3:
            self._istr_lst[self._i].config(bg = 'white')
            self._istr_lst[self._i+1].config(bg = 'yellow')
        elif self._i >= len(self._infos)-4:
            self._istr_lst[self._i].config(bg = 'white')
            self._istr_lst[self._i+1].config(bg = 'yellow')
        else:
            self._istr_lst[self._i-3].destroy()
            self._istr_lst[self._i].config(bg = 'white')
            self._istr_lst[self._i+1].config(bg = 'yellow')
        self._i += 1

    def event_set_zero (self):
        if self._current < 33:
            self._reg_lst[self._current].config(text = 'r'+str(self._current)+': 0')
            self.cpu._reg[self._current] = 0

    def event_set_rand (self):
        if self._current < 33:
            r = random.randint(0,255)
        self._reg_lst[self._current].config(text='r'+str(self._current)+': '+str(r))
        self.cpu._reg[self._current] = r

    def event_step (self):
        if self.cpu.cycle():
            self.output()
            self.update_display()
            pass
        else:
            self.button_state('disabled')
            self._pause.config(state = 'disabled')
 
    def event_tempo (self):
        if self.flag == 1:
            if self.cpu.cycle():
                self.output()
                self.update_display()
                self._root.after(500,self.event_tempo)
                pass

    def event_run (self):
        self._speed = 0
        while self.cpu.cycle():
            self.output()
            self.update_display()
            pass
        else:
            self.button_state('disabled')
            self._pause.config(state = 'disabled')
    
    def event_run_slow (self):
        if self.flag == 0:
            self.flag = 1
            self.button_state('disabled')
            self._reset.config(state = 'disabled')
            self._load.config(state = 'disabled')
            self.event_tempo()
        else:
            self.button_state('disabled')
            self._pause.config(state = 'disabled')

    def event_pause (self):
        self.flag = 0
        self.button_state('normal')
        self._reset.config(state = 'normal')
        self._load.config(state = 'normal')

    def event_skip (self):
        try:
            self.cpu._ip += 1 
            self.update_display() 
        except:
            self.button_state('disabled')
            self._pause.config(state = 'disabled')

    def button_state (self, state):
        self._to_rand.config(state = state)
        self._to_zero.config(state = state)
        self._step.config(state = state)
        self._run.config(state = state)
        self._run_slow.config(state = state)
        self._skip.config(state = state)

    def output (self):
        instr = self._code[self.cpu._ip-1][0]
        opcode = instr[0]
        dst = instr[1]
        if opcode == 'prn':
            self._sortie = self._sortie+str(self.cpu.value(dst))
            self._op.config(text = self._sortie)
        elif opcode == 'prx':
            self._sortie = self._sortie+format(self.cpu.value(dst), '02x')
            self._op.config(text = self._sortie)
        elif opcode == 'prX':
            self._sortie = self._sortie+format(self.cpu.value(dst), '04x')
            self._op.config(text = self._sortie)
        elif opcode == 'prc':
            self._sortie = self._sortie+chr(self.cpu.value(dst))
            self._op.config(text = self._sortie)
        else:
            pass

main = Interface()
mainloop()
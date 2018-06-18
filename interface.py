# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
from probe  import Probe
from memory import Memory
from cpu import CPU
from instr import Instr
from tkinter import filedialog
import linecache
import tkinter as tk
import os
import tkinter.font as tkFont
import sys
import random

class Interface:

    def __init__(self):
        self.rr = ''
        self._i = 0
        self.flag = 0
        self._root = Tk()
        self._root.resizable(False, False)
        self._current = 33
        self._root.title('Seselab')
        self._dm = 1
        self._ret_line = 1
        self.otp = []
        self.creat_reglist()
        self.font = tkFont.nametofont("TkFixedFont")
        self.font.configure(size=14)
        self.which_file()
        log = open('log.txt', 'w')
        bak = sys.stdout # on sauvegarde l'ancien stdout
        sys.stdout = log
        # log.close()
        # sys.stdout = bak 
        self._step = self.creat_button(self._root, 'Step', self.event_step, 'disabled', 8, 1)
        self._run = self.creat_button(self._root, 'Run', self.event_run, 'disabled', 8, 2)
        self._run_slow = self.creat_button(self._root, 'Run slowly', self.event_run_slow, 'disabled', 8, 3)
        self._pause = self.creat_button(self._root, 'Pause', self.event_pause, 'disabled', 8, 4)
        self._skip = self.creat_button(self._root, 'Skip', self.event_skip, 'disabled', 8, 5)
        self._to_rand = self.creat_button(self._root, 'Random', self.event_set_rand, 'disabled', 2, 10)
        self._to_zero = self.creat_button(self._root, 'Zero', self.event_set_zero, 'disabled', 3, 10)
        self._reset = self.creat_button(self._root, 'Reset', self.event_reset, 'disabled', 5, 0)
        self._quit= self.creat_button(self._root, 'Close', self._root.quit, 'normal', 8, 17)
        self._pick_file = self.creat_button(self._root, 'Pick file', self.pick_file, 'normal', 3, 0)
        self._load = self.creat_button(self._root, 'Load', self.event_load, 'normal', 4, 0)

        self._inject_fault = Label(self._root, text = 'Inject fault:', bg = None, width = 10, font = ('helvetic', 11, 'bold'))
        self._inject_fault.grid(column = 1, row = 10, columnspan = 8, sticky = 'w', padx = 8)
        self._breth = Label(self._root, text = '', bg = 'white', width = 97, font = ('helvetic', 11, 'bold'), relief = SUNKEN)
        self._breth.grid(column = 1, row = 16, columnspan = 8, sticky = 'w', padx = 8, pady = 5)
        
        self._instr_list = Canvas(self._root, borderwidth = 0, height = 150, background="#ffffff")
        self._frame = Frame(self._instr_list, background = "#ffffff")
        self._vsb = Scrollbar(self._root, orient = "vertical", command = self._instr_list.yview)
        self._instr_list.configure(yscrollcommand = self._vsb.set)
        self._vsb.grid(rowspan = 5, column = 7, row = 1, sticky = 'nse')
        self._instr_list.grid(rowspan = 5, columnspan = 7, column = 1, row = 1, sticky = 'nesw', pady = 5, padx = 5)
        self._instr_list.create_window((4,4), window=self._frame, anchor="ne")
        self._frame.bind("<Configure>", lambda event, canvas = self._instr_list: self.on_frame_configure(self._instr_list))

        self._instr_list2 = Canvas(self._root, borderwidth = 0, height = 150, background="#ffffff")
        self._frame2 = Frame(self._instr_list2, background = "#ffffff")
        self._vsb2 = Scrollbar(self._root, orient = "vertical", command = self._instr_list2.yview)
        self._instr_list2.configure(yscrollcommand = self._vsb2.set)
        self._vsb2.grid(rowspan = 5, column = 8, row = 11, sticky = 'nse')
        self._instr_list2.grid(rowspan = 5, columnspan = 8, column = 1, row = 11, sticky = 'nesw', pady = 5, padx = 5)
        self._instr_list2.create_window((4,4), window=self._frame2, anchor="ne")
        self._frame2.bind("<Configure>", lambda event, canvas = self._instr_list2: self.on_frame_configure(self._instr_list2))
        # self._op = Label(self._root, text = '', anchor = 'sw', bg = 'white', width = 85, height = 5, font = self.font, relief = SUNKEN)
        # self._op.grid(sticky = 'sw',row = 11, column = 1, columnspan = 8, padx = 5, pady = 5)

    def add_line (self):
        l = Label(self._frame2, 
            text = '', 
            anchor = 'nw', 
            bg = 'white',
            height = 1,
            font = self.font)
        l.grid(row = self._ret_line, 
            column = 1, 
            sticky = 'w')
        self.otp.append(l)

    def fill_canvas (self): 
        self._istr_lst = []
        for row in range(len(self._infos)-1):
            t = self._infos[row]
            l = Label(self._frame, 
                      text = t, 
                      anchor = 'w', 
                      bg = 'white',
                      font = self.font)
            l.grid(row = row, 
                   column = 1,
                   pady = 2)
            self._istr_lst.append(l)

    def on_frame_configure (self, canvas):
        self._instr_list.configure(scrollregion = self._instr_list.bbox("all"))
        self._instr_list2.configure(scrollregion = self._instr_list2.bbox("all"))

    def creat_button (self, root, text, command, state, c, r):
        button = Button(self._root, 
            text = text, 
            command = command, 
            width = 6, font = ('helvetic', 11), 
            state = state)
        button.grid(column = c, 
            row = r, 
            sticky = 'we', 
            padx = 5)
        return button

    def pick_file (self):
        filename = filedialog.askopenfilename(initialdir = os.getcwd(), 
            title = "Select file", 
            filetypes = (("asm files", "*.asm"), ("all files", "*.*")))
        if len(filename) > 0:
            self._file.delete(0, END)
            self._file.insert(0, filename)

    def which_file (self):
        value = StringVar() 
        try:
            value.set(sys.argv[1])
            self._file = Entry(self._root, 
            	text = value, 
            	width = 22, 
            	font = ('helvetic', 12))
            self._file.grid(column = 1, 
            	row = 0, 
            	sticky = 'w', 
            	padx = 7, 
            	pady = 5, 
            	columnspan = 3)
        except:
            value.set('Choose a file ...')
            self._file = Entry(self._root, 
            	text=value, 
            	width = 22, 
            	font = ('helvetic', 12))
            self._file.grid(column = 1, 
            	row = 0, 
            	sticky = 'w', 
            	padx = 7, 
            	pady = 5, 
            	columnspan = 3)

    def event_reset (self):
        self._i = 0
        # self._sortie = ''
        self.cpu = CPU(1048576, 32, self._code, '/dev/null')
        self.cpu._ip += 1
        self._infos = Instr().stack_infos(self._code)
        self._instr_list.yview_scroll(-2*len(self._infos),'units')
        self.fill_canvas()
        self.update_display()
        self.button_state('normal')
        self._pause.config(state = 'normal')
        self._reset.config(state = 'normal')
        self.update_reglist()
        self.flag = 0


    def event_load (self):
        self._i = 0
        # self._sortie = ''
        self._code = Compiler().compile(self._file.get())
        self.cpu = CPU(1048576, 32, self._code, '/dev/null')
        self.cpu._ip += 1
        self._infos = Instr().stack_infos(self._code)
        self._instr_list.yview_scroll(-2*len(self._infos),'units')
        self.add_line()
        self.fill_canvas()
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

    def creat_reglist (self):
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
        self._instr_list.yview_scroll(-2*len(self._infos),'units')
        if self._i < 2:
            self._istr_lst[self._i].config(bg = 'white')
            self._istr_lst[self._i+1].config(bg = 'yellow')
        elif self._i >= len(self._infos)-2:
            self._istr_lst[self._i].config(bg = 'white')
            self._istr_lst[self._i+1].config(bg = 'yellow')
        else:
            self._instr_list.yview_scroll(2*self._i-2,'units')
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
            else:
                self._load.config(state = 'normal')
                self._reset.config(state = 'normal')

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
        linecache.clearcache()
        if 'prc #10 ' in self._infos[self.cpu._ip-1]:
            self._ret_line += 1
            self.add_line()
            self._instr_list2.yview_scroll(2,'units')
        else:
            sortie = linecache.getline('log.txt', self._ret_line)
            self.otp[self._ret_line-1].config(text = sortie)

main = Interface()
mainloop()
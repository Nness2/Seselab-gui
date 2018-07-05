# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from tkinter import * 
from compiler import Compiler
from cpu import CPU
from consumption import Consumption
from instr import Instr
from tkinter import filedialog
import tempfile
import tkinter.font as tkFont
import os
import sys
import random

class Interface:

    def __init__(self):
        self._root = Tk()
        self._root.title('Seselab')
        self._root.resizable(False, False)
        self._root.protocol("WM_DELETE_WINDOW", self.event_close)

        self.creat_reglist()
        self.fill_text_field()
        self.creat_widget()
        self.cpu = None

        self._consum_file = tempfile.NamedTemporaryFile()
        self._output_file = tempfile.NamedTemporaryFile()

        self._output = open(self._output_file.name, 'w')
        sys.stdout = self._output
        self._stdout_back = sys.stdout 

    def event_load (self):
        self.destroy_canvas()
        self._instr_lab_list = []
        self._code = Compiler().compile(self._file.get())
        self._infos = Instr().stack_infos(self._code)
        self.fill_canvas()
        self.event_reset()

    def event_reset (self):    
        # self._output = open(self._output_file.name, 'w')
        self._pause_flag = 0
        self._brdcrb_list = ['main']
        self._brdcrb.config(text = '')
        self.cpu = CPU(1048576, 32, self._code, self._consum_file.name)
        self.update_display()
        self.button_state('normal')
        self._pause.config(state = 'normal')
        self._reset.config(state = 'normal')
        self._root.after(1, self.event_step)


    def pick_file (self):
        filename = filedialog.askopenfilename(initialdir = os.getcwd(),
            title = "Select file", 
            filetypes = (("asm files", "*.asm"), ("all files", "*.*")))
        if len(filename) > 0:
            self._file.delete(0, END)
            self._file.insert(0, filename)

    def fill_text_field (self):
        if len(sys.argv) > 1:
            if sys.argv[1][-4:] == '.asm':
                text_field = sys.argv[1]
            else:
                text_field = 'Choose file…'
        else:
            text_field = 'Choose file…'

        value = StringVar()
        value.set(text_field)
        self._file = Entry(self._root, text = value, width = 25, font = ('helvetic', 12))
        self._file.grid(column = 1, row = 0, sticky = 'w', padx = 5, pady = 5, columnspan = 3)

    def creat_button (self, root, text, command, state, c, r, px, py):
        button = Button(self._root, text = text, command = command, 
            width = 6, font = ('helvetic', 11), state = state)
        button.grid(column = c, row = r, sticky = 'we', padx = px, pady = py)
        return button

    def creat_reglist (self):
        self._curt_reg = None
        self._reg_lst = []
        reg_num = 0
        for j in range(4):
            for k in range(8):
                l = Button(self._root, text = 'r' + str(reg_num) + ': 0', bg = 'white', width = 9,
                    command = lambda x = reg_num : self.select(x), font = ('helvetic', 11))
                l.grid(column = k + 1, row = j + 6, sticky = 'we')
                self._reg_lst.append(l)
                reg_num += 1

    def update_reglist (self):
        for i in range (32):
            self._reg_lst[i].config(
                text = 'r' + str(i) + ': ' + str(self.cpu._reg[i]))

    def event_close(self):
        self._consum_file.close()
        self._output_file.close()
        self._output.close()
        sys.stdout = self._stdout_back
        self._root.destroy()

    def fill_canvas (self):
        self._previous_ip = 0
        font = tkFont.nametofont("TkFixedFont")
        font.configure(size = 14)
        for row in range(len(self._infos) - 1):
            t = self._infos[row]
            l = Label(self._frame, text = t, width = 85, anchor = 'w', bg = 'white', font = font)
            l.grid(row = row, column = 1, pady = 2)
            self._instr_lab_list.append(l)
            self.bind_scrollbar(l)
        self._instr_lab_list[0].grid_forget()

    def event_step (self):
        if self.cpu.cycle():
            self.update_display()
            self.output()
            return True
        else:
            self.button_state('disabled')
            self._pause.config(state = 'disabled')
            self._consumption.config(state = 'normal')
            self.output()
            return False

    def event_run (self, speed):
        if self._pause_flag == 0:
            self._pause_flag = 1
            self.button_state('disabled')
            self._reset.config(state = 'disabled')
            self._load.config(state = 'disabled')
            self._speed = speed
            self.tempo_run()

    def tempo_run (self):
        if self._pause_flag == 1:
            if self.event_step():
                self._root.after(self._speed, self.tempo_run)
            else:
                self._load.config(state = 'normal')
                self._reset.config(state = 'normal')

    def event_pause (self):
        self._pause_flag = 0
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

    def event_set_zero (self):
        if self._curt_reg is not None:
            self._reg_lst[self._curt_reg].config(
                text = 'r' + str(self._curt_reg) + ': 0')
            self.cpu._reg[self._curt_reg] = 0

    def event_set_rand (self):
        if self._curt_reg is not None:
            r = random.randint(0,255)
            self._reg_lst[self._curt_reg].config(
                text = 'r' + str(self._curt_reg) + ': ' + str(r))
            self.cpu._reg[self._curt_reg] = r

    def select (self, x):
        if self._curt_reg is None:
            self._reg_lst[x].config(bg = 'yellow')
            self._curt_reg = x
        elif self._curt_reg == x:
            self._reg_lst[self._curt_reg].config(bg = 'white')
            self._curt_reg = None
        else:
            self._reg_lst[self._curt_reg].config(bg = 'white')
            self._reg_lst[x].config(bg = 'yellow')
            self._curt_reg = x

        if self.cpu is not None and self._curt_reg is not None:
            self._to_rand.config(state = 'normal')
            self._to_zero.config(state = 'normal')

    def update_display (self):
        self.update_reglist()
        self._instr_display.yview_scroll(-2 * len(self._infos), 'units')
        self._instr_display.yview_scroll(2 * self.cpu._ip - 6, 'units')
        self._instr_lab_list[self._previous_ip].config(bg = 'white')
        self._instr_lab_list[self.cpu._ip].config(bg = 'yellow')
        self._previous_ip = self.cpu._ip
        self.breadcrumb()

    def breadcrumb (self):
        text = ''
        if self._code[self.cpu._ip][0][0] == 'cal':
            self._brdcrb_list.insert(0, self._code[self.cpu._ip][1][2])
        elif self._code[self.cpu._ip][0][0] == 'ret':
            if self._brdcrb_list:
                self._brdcrb_list.pop(0)
        for e in self._brdcrb_list:
            text = text + e + ' ← '
        self._brdcrb.config(text = text)

    def destroy_canvas (self):
        for obj in self._instr_lab_list:
            obj.destroy()

    def button_state (self, state):
        self._to_rand.config(state = state)
        self._to_zero.config(state = state)
        self._consumption.config(state = state)
        self._step.config(state = state)
        self._run.config(state = state)
        self._run_slow.config(state = state)
        self._skip.config(state = state)

    def output (self):
        self._output_text = ''
        fd = open(self._output_file.name, "r")
        self._output_text = fd.read()
        self._output_text = self.return_line(self._output_text)
        self._outpt.config(text = self._output_text)
        self._root.after(1, self._output_display.yview_scroll(2, "units"))
        fd.close()

    def return_line(self, text):
        cmp = 0
        for i in range(len(text)):
            if cmp < 94 and text[i] != '\n': #and text[i] != '\n':
                cmp += 1
            elif text[i] == '\n':
            	cmp = 0
            else:
                cmp = 0
                text = text[:i]+ '\n' + text [i:]
        return text

    def mouse_scroll(self, event):
        wdg = event.widget
        while wdg != self._root:
            prev_wdg = wdg
            wdg = wdg.master
        if event.num == 5:
            prev_wdg.yview_scroll(1, "units")
        else:
            prev_wdg.yview_scroll(-1, "units")

    def bind_scrollbar (self, wd):
        wd.bind_all("<MouseWheel>", self.mouse_scroll)
        wd.bind("<Button-4>", self.mouse_scroll)
        wd.bind("<Button-5>", self.mouse_scroll)

    def on_frame_configure (self, canvas):
        canvas.configure(
            scrollregion = canvas.bbox("all"))

    def consumption (self):
        self.cpu._probe._probe.flush()
        Consumption(self._consum_file.name).creat_plot()

    def creat_widget (self):
        font_text = tkFont.nametofont("TkFixedFont")
        font_text.configure(size=14)
        # Frame 1
        self._instr_display = Canvas(self._root, borderwidth = 0, height = 150, bg = "white")
        self._frame = Frame(self._instr_display, bg = "white")
        self._vsb = Scrollbar(self._root, orient = "vertical", command = self._instr_display.yview)
        self._instr_display.configure(yscrollcommand = self._vsb.set)
        self._vsb.grid(rowspan = 5, column = 7, row = 1, sticky = 'nse')
        self._instr_display.grid(rowspan = 5, columnspan = 7, column = 1, row = 1, sticky = 'nesw', pady = 5, padx = 5)
        self._instr_display.create_window((4, 4), window = self._frame, anchor = "ne")
        self._frame.bind("<Configure>", lambda event, canvas = self._instr_display: 
            self.on_frame_configure(canvas))
        self.bind_scrollbar(self._frame)
        self._instr_lab_list = []

        # Frame 2
        self._output_display = Canvas(self._root, borderwidth = 0, height = 150, bg = "white")
        self._frame2 = Frame(self._output_display, bg = "white")
        self._vsb2 = Scrollbar(self._root, orient = "vertical", command = self._output_display.yview)
        self._output_display.configure(yscrollcommand = self._vsb2.set)
        self._vsb2.grid(rowspan = 5, column = 8, row = 11, sticky = 'nse')
        self._output_display.grid(rowspan = 5, columnspan = 8, column = 1, row = 11, sticky = 'nesw', pady = 5, padx = 5)
        self._output_display.create_window((4, 4), window = self._frame2, anchor="ne")
        self._frame2.bind("<Configure>", lambda event, canvas = self._output_display: 
            self.on_frame_configure(canvas))
        self._outpt = Label(self._frame2, width = 94, anchor = 'nw', justify = 'left', bg = 'white', font = font_text)
        self._outpt.grid(row = 1, column = 1, pady = 2, sticky = 'w')
        self.bind_scrollbar(self._outpt)

        # Button
        self._step = self.creat_button(self._root, 'Step', self.event_step, 'disabled', 8, 1, 5, 0)
        self._run = self.creat_button(self._root, 'Run', lambda: self.event_run(1), 'disabled', 8, 2, 5, 0)
        self._run_slow = self.creat_button(self._root, 'Run slowly', lambda: self.event_run(500), 'disabled', 8, 3, 5, 0)
        self._pause = self.creat_button(self._root, 'Pause', self.event_pause, 'disabled', 8, 4, 5, 0)
        self._skip = self.creat_button(self._root, 'Skip', self.event_skip, 'disabled', 8, 5, 5, 0)
        self._to_rand = self.creat_button(self._root, 'Random', self.event_set_rand, 'disabled', 2, 10, 5, 0)
        self._to_zero = self.creat_button(self._root, 'Zero', self.event_set_zero, 'disabled', 3, 10, 5, 0)
        self._reset = self.creat_button(self._root, 'Reset', self.event_reset, 'disabled', 5, 0, 5, 0)
        self._pick_file = self.creat_button(self._root, 'Pick file', self.pick_file, 'normal', 3, 0, 5, 0)
        self._load = self.creat_button(self._root, 'Load', self.event_load, 'normal', 4, 0, 5, 0)
        self._quit= self.creat_button(self._root, 'Close', self.event_close, 'normal', 8, 17, 5, 5)
        self._consumption = self.creat_button(self._root, 'Consumption', self.consumption, 'normal', 7, 17, 5, 5)
        self._consumption.config(state = 'disabled')
        self.bind_scrollbar(self._output_display)
        # Text
        self._inject_fault = Label(self._root, anchor = 'e', text = 'Inject fault:', g = None, width = 10,
            font = ('helvetic', 12))
        self._inject_fault.grid(column = 1, row = 10, columnspan = 8, sticky = 'w', padx = 8)

        # Call list
        self._brdcrb = Label(self._root, text = '', anchor = 'w', bg = 'white', width = 97,
            font = font_text, relief = SUNKEN)
        self._brdcrb.grid(column = 1, row = 16, columnspan = 8, sticky = 'w', padx = 8, pady = 5)



main = Interface()
mainloop()

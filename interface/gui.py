#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tkinter import * 
import tkinter as tk

def test():
	print(2)

fenetre = Tk()

label = Label(fenetre, text="mov r23 #3", bg="white", width=25, anchor='w')
label.pack()
label = Label(fenetre,text="-> "+"prn r23", bg="white", width=25, anchor='w')
label.pack()
label = Label(fenetre, text="add r22 #3 #2", bg="white", width=25, anchor='w')
label.pack()

# b = Button(fenetre, text ='test').pack(side=LEFT, padx=5, pady=5)
# b.bind('test','<Button-1>', test)
# b.pack()

# canvas = Canvas(fenetre, width=70, height=20)
# txt = canvas.create_text(5, 10, text="Pas-à-pas", fill="black", anchor='w')
# canvas.focus_set()
# canvas.bind("<Button-1>", test)
# canvas.pack()

# Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
# Frame1.pack(side=LEFT, padx=30, pady=30)
# b = Label(Frame1, text="Frame 1").pack(padx=10, pady=10)
# b.bind("<Button-1", test)

b = Button(fenetre, text="Pas-à-pas", command=test).pack(padx=10, pady=10, side = LEFT)

b = Button(fenetre, text="Sans interruption", command=test).pack(padx=10, pady=10, side = RIGHT)


fenetre.mainloop()
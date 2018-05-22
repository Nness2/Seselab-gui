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


b = Button(fenetre, text="Pas-à-pas", command=test).pack(padx=10, pady=10, side = LEFT)
b = Button(fenetre, text="Sans interruption", command=test).pack(padx=10, pady=10, side = RIGHT)


fenetre.mainloop()
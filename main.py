#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from vue import *
from modele import *
from controleur import *


main=Tk()
main.title("Ultimate Traffic Simulator of Doom")
main.iconbitmap(default = icon)

def start():
	interface = Interface(main)
	
	simulationLoop(interface,0)
	interface.mainloop()

start()



			



#!/usr/bin/env python
# coding: utf-8
from tkinter import *
from vue import *
from modele import *
import platform

if platform.system()=='Windows':
	import winsound





##Retourne un élément aléatoire dans une liste L
def randomSelection(L) :
	return L[randint(0,len(L)-1)]
	

def spawn(road, speedFactor) :
	vehicle = Vehicle(lane=0, speed=randomSelection(speeds) * speedFactor, color=randomSelection(colours), road=road)
	vehicle.spawn()
	

def simulationLoop(interface, x) :
	#Fonction normale:
	road = interface.var_road

	#On veut que les vehicules apparaissent toutes les 20*interface.var_traffic ms, afin de pouvoir gerer la densité du traffic.
	if x % interface.var_traffic.get() == 0:
		spawn(road, interface.var_speed.get())
	x += 1

	#On fait rouler tous les véhicules de la route
	for index in range(len(road.listVehiclesLane)):
		for vehicle in road.listVehiclesLane[index]:
			vehicle.roule()

	#Bonus sons
	if platform.system()=='Windows' and interface.var_sound.get() == True:
		if x == 1:
			winsound.PlaySound("Sounds/Intro.wav", winsound.SND_ASYNC)
		elif x % 1200 == 0:
			winsound.PlaySound(randomSelection(sounds), winsound.SND_ASYNC)

	road.zone.after(interface.var_time.get(), simulationLoop, interface,x)





	


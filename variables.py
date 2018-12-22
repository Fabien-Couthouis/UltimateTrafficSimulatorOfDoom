#!/usr/bin/env python
# coding: utf-8



#Fenetre
height=1000 #hauteur fenetre
width=1000   #largeur fenetre

#Icone
icon='icon.ico'

#Sons
sounds = ["Sounds/Eternuement.wav", "Sounds/Arrivee.wav", "Sounds/Carambolage.wav", "Sounds/Favoris.wav", "Sounds/Rabattement.wav", "Sounds/Non.wav",\
		  "Sounds/Rabattement.wav", "Sounds/Tuttut.wav", "Sounds/Valeurs.wav", "Sounds/Vroum.wav"]

#Vehicule
colours=['red', 'blue', 'green', 'deeppink', 'purple', 'orange', 'black', "yellow"]
speeds=[2,2.5,3,4,3.5]

#couleurs routes
class Color():
	def __init__(self):
		self.roadColor = 'grey'        #bitume
		self.markingColor = 'white'    #marquage au sol
		self.edgeColor = 'black'       #contours de la route
		self.areaColor = 'green'       #region hors route





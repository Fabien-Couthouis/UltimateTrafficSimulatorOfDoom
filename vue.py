#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from math import *
from JCVD import *
from variables import *

color=Color()

######################################################## INTERFACE ########################################################################################################################
class Interface(Frame):

	def __init__(self, window):
		Frame.__init__(self, window, width=width, height=height)
		self.window = window

		self.initialize()
		self.pack(fill=BOTH)

	#Fonction comprenant tout ce que l'interface doit contenir lors de son initialisation 
	def initialize(self):

		#Simulateur et zone de simulation (caneva ou sont affichées route et voitures)
		self.simulator = LabelFrame(self, text='Simulateur')
		self.zone = Canvas(self.simulator, width=width, height=height, bg=color.areaColor)
		self.zone.pack()
		self.simulator.pack(side=LEFT,expand=Y, fill=BOTH, pady=2, padx=2)
		self.var_road = RouteVirage(nbOfLanes=2, zone = self.zone)
		self.var_road.draw(self.zone)

		#Variables modifiables par l utilisateur
		self.var_time = IntVar()
		self.var_time.set(20)  # valeur par défaut

		self.var_traffic = IntVar()
		self.var_traffic.set(30) 

		self.var_nbOfLanes = IntVar()
		self.var_nbOfLanes.set(2) 

		self.var_speed = DoubleVar()
		self.var_speed.set(1) 

		self.var_roadName = StringVar()
		self.var_roadName.set('RouteVirage') 
		self.var_road = RouteVirage(zone=self.zone, nbOfLanes=self.var_nbOfLanes.get())

		self.var_sound = BooleanVar()
		self.var_sound.set(True)

		self.var_modeMalozieux = BooleanVar()
		self.var_modeMalozieux.set(False)

		#Interface utilisateur : controles
		self.controles = LabelFrame(self, text='Controles')
		self.controles.pack(side=RIGHT, expand=Y, fill=BOTH, pady=2, padx=2)
		self.displayControles()
		

		#Menu haut
		self.menubar = Menu(self)

		self.optionmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Options", menu=self.optionmenu)
		self.optionmenu.insert_checkbutton(1,label="Mode malozieux", variable=self.var_modeMalozieux, command=self.selectColorMod)
		self.optionmenu.insert_checkbutton(1,label="Activer/Désactiver les sons", variable=self.var_sound)

		self.helpmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Aide", menu=self.helpmenu)
		self.helpmenu.add_command(label="À propos", command=self.popJCVD )

		self.menubar.add_command(label="Quitter", command=quit)
		self.window.config(menu=self.menubar)


	#Afficher l'UI
	def displayControles(self) :

		controles = self.controles

		#"Temps"
		scale_time=Scale(controles, from_=2, to=40, resolution=2, length=300, orient=HORIZONTAL, label='Fréquence de rafraîchissement (ms)', variable=self.var_time)
		scale_time.pack()

		#Vitesse
		scale_speed=Scale(controles, from_=0.5, to=2, resolution=0.1, length=300, orient=HORIZONTAL, label="Multiplicateur de vitesse à l'apparition", variable=self.var_speed)
		scale_speed.pack()

		#Traffic
		traffic = LabelFrame(controles, text='Traffic')
		values = [1000000, 50, 30, 10]
		texts = ['presque surement rien', 'peu dense', 'dense', 'très dense']

		for i in range(len(values)):
			b = Radiobutton(traffic, variable=self.var_traffic, text=texts[i], value=values[i])
			b.pack(side=LEFT, expand=1)

		traffic.pack()

		#Menu selection (pour les routes)
		roads = ['RouteVirage', 'RouteOvale', 'RouteDroite']
		roadFrame = LabelFrame(controles, text='Type de route')
		routeMenu = OptionMenu(roadFrame, self.var_roadName, * roads, command = self.resetZone)
		routeMenu.pack()
		roadFrame.pack()

		#Nombre de voies
		nbOfLanes = LabelFrame(controles, text='Nombre de voies')
		lanes = [1, 2, 3]
		lanesMenu = OptionMenu(nbOfLanes, self.var_nbOfLanes, * lanes, command = self.resetZone)
		nbOfLanes.pack()
		lanesMenu.pack(side=LEFT)


	# Affiche un popup sur lequel est inscrit une citation de Jean-Claude Van Damme
	def popJCVD(self):
		top = Toplevel()
		top.title("À propos de Jean Claude Van Damme ...")
		msg = Message(top, text=randomPhrase(JCVD) + "  - JCVD")
		msg.pack()
		button = Button(top, text="Ok Jean-Claude", command=top.destroy)
		button.pack()


	def selectColorMod(self):
		if self.var_modeMalozieux.get()==False:
			color.roadColor = 'grey'      
			color.markingColor = 'white' 
			color.edgeColor = 'black'
			color.areaColor = 'green'
			self.resetZone(0)    
		else:
			color.roadColor = "yellow"     
			color.markingColor = "deeppink"   
			color.edgeColor = "orange"     
			color.areaColor = "purple" 
			self.resetZone(0)     
	
	def resetZone(self,var):
		roads = {'RouteVirage':RouteVirage, 'RouteOvale':RouteOvale, 'RouteDroite':RouteDroite}
		self.var_road = roads.get(self.var_roadName.get())(zone=self.zone, nbOfLanes=self.var_nbOfLanes.get())
		self.zone.delete(ALL)
		self.zone.configure(bg=color.areaColor)
		self.var_road.draw(self.zone)
		self.zone.pack()
		


		
			
##########################################################################################################################################################################################







############################################# ROUTES ######################################################################################################################################

class Route():

	def __init__(self, speedMax = 130, nbOfLanes = 2, zone = None):
		self.zone = zone
		self.speedMax = speedMax
		self.nbOfLanes = nbOfLanes           #nombre de voies sur la route

		#Création d'une liste de listes : cette liste contient les listes des véhicules sur une voie
		#Exemple : listVehiclesLane[1] renverra la liste de tous les véhicules situées sur la voie 2 
		self.listVehiclesLane = []
		for i in range(nbOfLanes):
			self.listVehiclesLane.append([])

		

class RouteDroite(Route):
	
	def draw(self, zone) :
		self.listVehiclesLane.append([]) #lane -1 est la voie d'insertion
		
		Canvas.create_rectangle(zone, 400,0, 490,1002, fill=color.roadColor, outline=color.edgeColor)
		Canvas.create_line(zone, 430, 0, 430,1002, fill = color.markingColor, dash=(5,3))
		Canvas.create_line(zone, 460, 0, 460,1002, fill = color.markingColor, dash=(5,3))

		Canvas.create_rectangle(zone, 400 + self.nbOfLanes*30,-1, 1002, 1002, fill=color.areaColor, outline=color.edgeColor)

		#sortie
		Canvas.create_rectangle(zone, 0,950, 350,920, fill=color.roadColor, outline=color.edgeColor)
		Canvas.create_rectangle(zone, 370,670, 400,900, fill=color.roadColor, outline=color.roadColor)
		Canvas.create_line(zone, 370,670, 370,900, fill=color.edgeColor)

		Canvas.create_arc(zone, 300,850, 400, 950, start=0, extent=-90, fill=color.roadColor, outline=color.roadColor, style='pieslice')
		Canvas.create_arc(zone, 300,850, 400, 950, start=0, extent=-90, fill=color.roadColor, outline=color.edgeColor, style='arc')

		Canvas.create_arc(zone, 330,880, 370, 920, start=0, extent=-90, fill=color.areaColor, outline=color.areaColor, style='pieslice')
		Canvas.create_arc(zone, 330,880, 370, 920, start=0, extent=-90, fill=color.areaColor, outline=color.edgeColor, style='arc')

		ptsTriangle2 = [(370,670), (400,670),    (400,650)]
		Canvas.create_polygon(zone, ptsTriangle2, fill=color.roadColor, outline=color.roadColor)
		Canvas.create_line(zone, 370,670, 401,649, fill=color.edgeColor)

		Canvas.create_line(zone, 400,652, 400,899, fill=color.markingColor, dash=(3,3))


	def convert(self, t, lane, segment) :
		if lane < 0 :
			
			if t>=100 and t<=400 :
				X = 415 + 30*lane
				Y = t
				segment = 3

			if t<100 :
				X = 100 + 35*cos((t-50)/(40*pi)-pi/2)
				Y = 100 + 35*sin((t-50)/(40*pi)-pi/2)
				segment = 2

			if t<50 :
				X = t*350/50
				Y = 65
				segment = 2

			if t>=650 and t<=900 :
				X = 415 + 30*lane
				Y = t
				segment = 4
			
			if t>900 :
				X = 350 + 35*cos((t-900)/(10*pi))
				Y = 900 + 35*sin((t-900)/(10*pi))
				segment = 4

			if t>950 :
				X = 350-(t-950)*350/50
				Y = 935
				segment = 4

		elif lane >= 0 :
			X = 415 + lane*30
			Y = t
			segment = 1

		if t > 1001 :
			segment = 0
		
		return(X,Y,segment)


class RouteVirage(Route):

	######## fonction de dessin de la route ################################
	def draw(self, zone) :
		#3 routes droites
		Canvas.create_rectangle(zone, 0,10+(3-self.nbOfLanes)*30, 800,100, fill=color.roadColor, outline=color.edgeColor)
		Canvas.create_rectangle(zone, 820,120, 910-(3-self.nbOfLanes)*30,820, fill=color.roadColor, outline=color.edgeColor)
		Canvas.create_rectangle(zone, 0,840, 800,930-(3-self.nbOfLanes)*30, fill=color.roadColor, outline=color.edgeColor)
		
		
		#virage haut droite
		Canvas.create_arc(zone, 780-self.nbOfLanes*30,100-self.nbOfLanes*30, 820+self.nbOfLanes*30,140+self.nbOfLanes*30 , start=0, extent=90, fill=color.roadColor, outline=color.roadColor, style='pieslice') #route
		Canvas.create_arc(zone, 780,100, 820,140 , start=0, extent=90, fill=color.areaColor, outline=color.areaColor, style='pieslice') #cache virage
		Canvas.create_arc(zone, 780-self.nbOfLanes*30,100-self.nbOfLanes*30, 820+self.nbOfLanes*30,140+self.nbOfLanes*30 , start=0, extent=90, fill=color.roadColor, outline=color.edgeColor, style='arc') #bord ext
		Canvas.create_arc(zone, 780,100, 820,140 , start=0, extent=90, fill=color.areaColor, outline=color.edgeColor, style='arc') #bord int
		#virage bas droite
		Canvas.create_arc(zone, 780-self.nbOfLanes*30,800-self.nbOfLanes*30, 820+self.nbOfLanes*30,840+self.nbOfLanes*30 , start=270, extent=90, fill=color.roadColor, outline=color.roadColor, style='pieslice')
		Canvas.create_arc(zone, 780,800, 820,840 , start=270, extent=90, fill=color.areaColor, outline=color.areaColor, style='pieslice')
		Canvas.create_arc(zone, 780-self.nbOfLanes*30,800-self.nbOfLanes*30, 820+self.nbOfLanes*30,840+self.nbOfLanes*30 , start=270, extent=90, fill=color.roadColor, outline=color.edgeColor, style='arc')
		Canvas.create_arc(zone, 780,800, 820,840 , start=270, extent=90, fill=color.areaColor, outline=color.edgeColor, style='arc')
		
		#marquages		
		#for i in range(self.nbOfLanes)	
		if self.nbOfLanes>=2 :
			Canvas.create_line(zone, 0,70, 800,70, fill=color.markingColor, dash=(5,3), width=1)
			Canvas.create_line(zone, 850,120, 850,820, fill=color.markingColor, dash=(5,3), width=1)
			Canvas.create_line(zone, 0,870, 800,870, fill=color.markingColor, dash=(5,3), width=1)
			
			Canvas.create_arc(zone, 750,70, 850,170 , start=0, extent=90, fill=color.roadColor, outline=color.markingColor, style='arc', dash=(5,3))
			Canvas.create_arc(zone, 850,870, 750,770 , start=270, extent=90, fill=color.roadColor, outline=color.markingColor, style='arc', dash=(5,3))
			
				
		if self.nbOfLanes==3 :
			Canvas.create_line(zone, 0,40, 800,40, fill=color.markingColor, dash=(5,3), width=1)
			Canvas.create_line(zone, 880,120, 880,820, fill=color.markingColor, dash=(5,3), width=1)
			Canvas.create_line(zone, 0,900, 800,900, fill=color.markingColor, dash=(5,3), width=1)
			
			Canvas.create_arc(zone, 720,40, 880,200 , start=0, extent=90, fill=color.roadColor, outline=color.markingColor, style='arc', dash=(5,3))
			Canvas.create_arc(zone, 880,900, 720,740 , start=270, extent=90, fill=color.roadColor, outline=color.markingColor, style='arc', dash=(5,3))


	####### Converti t en couple X,Y ######
	def convert(self, t, lane, segment) : 
		
		if segment==1 :
		# morceau 1 (droite horizontale)
			X = t
			Y = 55 + (1-lane)*30
		
			if X>=800 :
				segment = 2
	
		if segment==2 :
		#morceau 2 (arc1)
			X = 800 + (35+(lane)*30)* cos((t-800)/(20*pi)-pi/2)
			Y = 120 + (35+(lane)*30)* sin((t-800)/(20*pi)-pi/2)
		
			if Y>=125 :
				segment = 3
		
		if segment==3 :
		#morceau 3 (droite verticale)
			X = 835 + lane*30
			Y = (t-903) + 120
		
			if Y>=825 :
				segment = 4
			
		if segment==4 :
		#morceau 4 (arc2)
			X = 800 + (35+lane*30)* cos((t-1605)/(20*pi)+0.1)
			Y = 820 + (35+lane*30)* sin((t-1605)/(20*pi)+0.1)
		
			if X<=800 :
				segment = 5
					
		if segment==5 :
		#morceau 5 (droite horizontale)
			X = (-t+1697) + 800
			Y = 855 + lane*30
		
			if X<=0 :
				segment = 0
		
		
		return (X,Y,segment)

class RouteOvale(Route) :
	
	def draw(self,zone) :
		nbVoies=self.nbOfLanes
		Canvas.create_oval(zone, 40,40, 960,960, width=1, fill=color.roadColor)
		for i in range (nbVoies):
			Canvas.create_oval(zone, 70 + 30 * i,70 + 30 * i, 930 - 30 * i,930 - 30 * i, width=1, outline=color.markingColor, dash=(3,5))
		Canvas.create_oval(zone, 40+30*nbVoies,40+30*nbVoies, 960-30*nbVoies,960-30*nbVoies, width=1, fill=color.areaColor)
	
	def convert(self, t, posLine, segment) :
		#on met ça parce que le dessin en fonction des voies est plus long à faire sinon, et donc voilàààà
		if self.nbOfLanes == 1 :
			posLine += 2
		elif self.nbOfLanes == 2 :
			posLine += 1

		#un cercle classique, avec le - au sinus pour tourner dans le bon sens (on est pas des anglais hein)
		X = 500 + (385+30*(posLine))* cos(t/(100*pi))
		Y = 500	+ (385+30*(posLine))* sin(-t/(100*pi))

		#Segment = 10 une fois un tour effectué, pour le reset un peu buggé
		if t >= 1975 :
			segment = 10
		else :
			segment = 1

		return (X,Y,segment)		
	




##########################################################################################################################################################################################

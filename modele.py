#!/usr/bin/env python
# coding: utf-8
from vue import *

#Retourne la position du vehicule dans la nouvelle liste, en fonction de t, par recherche dichotomique
def returnPosInList(vehicle,L):
	i = 0
	j = len(L)

	if j==0:
		return 0
	if vehicle.t > L[j-1].t :
		return j
	while i!=j:
		k=(i+j)//2
		if vehicle.t <= L[k].t:
			j=k
		else:
			i=k+1
	return i

class Vehicle():
	
	def __init__(self, road=RouteVirage, list=None, t=0, lane=0, speed=2, color="blue", segment=1):
		self.road = road
		self.t = t

		self._list = self.road.listVehiclesLane[lane]
		self._list.insert(returnPosInList(self,self.list),self)
		self.lane = lane
		
		self.segment = segment
		
		self.speedMax = road.speedMax
		self._speed = speed
		self.wantedSpeed = speed
		
		self.color = color


## Propriété speed
	
	def _set_speed(self,value):
		if value>0:
			self._speed= min(value, self.speedMax)

	def _get_speed(self):
		return self._speed
		
	speed=property(_get_speed,_set_speed)
##


## Propriété list 
	
	def _set_list(self, newList):
		self._list.remove(self)		
		self._list = newList
		self._list.insert(returnPosInList(self,self.list), self)

	def _get_list(self):
		return self._list
		
	list = property(_get_list, _set_list)
###


## Retourne la voie dans laquelle se situe le véhicule au niveau des listes. C'est l index de la liste de la liste des véhicules par voies.
	def returnListNumber(self):
		if type(self.road) == RouteDroite :  #si c'est la route droite et qu'on est sur la voie d'insertion
			if self.road.listVehiclesLane.index(self._list) > self.road.nbOfLanes-1 :
				return -1

		return self.road.listVehiclesLane.index(self._list)


## Création	du vehicule
	def spawn(self) :
		rectang = Canvas.create_rectangle(self.road.zone, 0, 45, 20,65, fill=self.color, outline="black")
		self.rectang = rectang
	

## Déplacement	
	def roule(self) :
		#Le roulage	
		self.t += self.speed
		(X,Y,self.segment) = self.road.convert(self.t,self.lane,self.segment)
		self.road.zone.coords(self.rectang, X-7,Y-7, X+7,Y+7)
		
		self.speed += 0.2*( (self.wantedSpeed - self.speed) + self.returnListNumber())

		#Comportement du véhicule	
		self.behavior()

		#Pour la route ovale, on reset quand on a fait un tour
		if type(self.road) == RouteOvale and self.segment == 10 :
			print(self.t)
			self.t -= 1972
			self.list = self.list

		#Détruire ou rouler, telle est la question
		if self.segment==0 :
			self.list.remove(self)	
			self.road.zone.delete(self.rectang)
		
		
## Comportement du véhicule : changement de trajectoire en fonction des autres
	def behavior(self) :
		#Position du véhicule dans la liste des véhicules de sa voie	
		posInList = self.list.index(self)
		#Indice de la liste dans laquelle se trouve le véhicule dans la liste des voies.
		#\C'est en fait le numéro de la voie dans laquelle sera la voiture une fois le depassement/rabattage terminé.
		listNumber = self.returnListNumber()

		##fonction de voie de sortie
		if type(self.road)==RouteDroite and self.t>650 and self.t<850 and listNumber<=0  and listNumber>-1 and randint(0,1000)>997 :
			self.lane -= 0.00002
			if self.canCutIn() :
				self.list = self.road.listVehiclesLane[listNumber - 1]
				self.cutIn()
		

		#Voitures en fin de liste (sans voiture devant elle) : on les fait terminer leur manoeuvre en cours puis elles se rabattent si elles le peuvent
		elif posInList + 1 >= len (self.list) :
			if self.lane > listNumber:
				self.cutIn() 
			elif self.lane < listNumber:
				self.overtake()
			elif self.canCutIn() :
				self.list = self.road.listVehiclesLane[listNumber - 1]
				self.cutIn()

		#Si le véhicule est en cours de dépassement, continuer
		elif self.lane < listNumber:
			self.overtake()

		#Y a t il un véhicule plus lent situé juste devant ?  
		elif self.t + self.speed >= self.list[posInList + 1].t + self.list[posInList + 1].speed  - 50:   
			#Si oui et que le véhicule peut dépasser, commencer le dépassement 
			if self.canOvertake() :   
				self.list = self.road.listVehiclesLane[listNumber + 1]	
				self.overtake()		
			#Sinon, on reste urbain et on freine
			else :
				self.brake(posInList)	
		
		#Le vehicule est civilisé se rabat, s'il a déja commencé ou s'il peut se rabattre :
		elif self.lane > listNumber:
			self.cutIn()    
		elif self.canCutIn() :  
			self.list = self.road.listVehiclesLane[listNumber - 1] 
			self.cutIn()   


##Freinage professionnel
	def brake(self, posInList) :
		self.speed = 0.5*self.speed
		#Si le véhicule est trop près de celui situé devant lui, on réduit sa vitesse afin de rétablir une distance de sécurité minimale
		if (self.t + self.speed) >= self.list[posInList + 1].t +self.list[posInList + 1].speed  - 20 :
			self.speed -= 0.5
		#Si la vitesse du véhicule atteint celle du véhicule situé devant, on arrête de freiner et on reste à cette vitesse
		elif self.speed  <= self.list[posInList + 1].speed  :
			self.speed = self.list[posInList + 1].speed
		
##Est-il possible de dépasser ?
	def canOvertake(self) :
		#ON PEUT PAS DEPASSER SI Y A PAS DE VOIE PLUS A GAUCHE HEIN, OUI, ON EST D ACCORD !
		#et puis on va pas s'inserrrer si on le peut pas encore ce serait dommage
		if self.lane == self.road.nbOfLanes - 1 or (self.lane<0 and self.t>600) :
			return False
		else :
			newList=self.road.listVehiclesLane[int(self.lane) + 1]

		#Si nouvelle liste vide, on s embete pas a verifier et squalala on depasse !
		if len(newList) == 0:
			return True

		#Sinon	on compare la position de la voiture avec celles de la voie d'à coté et on voit si y a moyen de s insérer 
		else :
			newPos = returnPosInList(self, newList)
			r = 55   #rayon (suivant t) de l'intervalle de vérification (55 est bien après tests)
			for otherVehicle in newList:
				if (otherVehicle.t < self.t + r) and (otherVehicle.t > self.t - r) :
					return False
			
		#Aucune condition n'empêche le changement de voie alors c'est partiiiiiiiiiiiiiiiii
		return True


##Est-il possible de se rabattre ?
	def canCutIn(self):
		#On va pas se rabattre sur la voie d arret d urgence non plus, on est pas des sauvages (ni sur la voie d'insertion)
		if self.lane == 0 or self.lane == -1:
			return False
		else : 
			newList=self.road.listVehiclesLane[int(self.lane) - 1]

		if len(newList) == 0:
			return True

		else :
			newPos = returnPosInList(self, newList)
			r = 55   #rayon (suivant t) de l'intervalle de vérification (50 est pas mal apres tests)
			for otherVehicle in newList:
				if (otherVehicle.t < self.t + r) and (otherVehicle.t > self.t - r) :
					return False

		return True


##Dépassement
	def overtake(self) :
		self.lane += 0.02*self.speed
		if self.lane >= self.returnListNumber() :
			self.lane = self.returnListNumber()


##Se rabattre
	def cutIn(self) :
		self.lane -= 0.02*self.speed
		if self.lane <= self.returnListNumber() :
			self.lane = self.returnListNumber()




			

				
		
		
		












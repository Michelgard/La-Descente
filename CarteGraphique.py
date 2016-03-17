# -*- coding: cp1252 -*-

from pygame import *

class CarteGraphique(Rect,object):
	valeurs = (None, 'AS', 2 ,3, 4, 5, 6, 7 ,8, 9, 10, 'Valet', 'Cavalier', 'Dame', 'Roi')
	couleurs = ('Coeur', 'Trèfle', 'Carreau', 'Pique', 'Atout', 'Excuse')
	
	def __init__(self, img = False, valeur = False, couleur = False):
		self.img     = img
		self.valeur  = valeur
		self.couleur = couleur
		if valeur    == False:
			self.fixe = True
		else:
			self.fixe  = False
		self.selected = False
		self.released = False
		
	def __str__(self):
		if self.couleur == 4:  
			return str(self.valeur)+ " d "+CarteGraphique.couleurs[self.couleur]
		elif self.couleur == 5:
			return "L Excuse"
		else:
			return str(CarteGraphique.valeurs[self.valeur])+ ' de ' + CarteGraphique.couleurs[self.couleur]
	
	def placer(self, fenetre, **arg):
		self.fenetre = fenetre
		self.rect = Rect.__init__(self, self.img.get_rect(**arg))
		
	def placerR(self, rotation):
		self.img = transform.rotate(self.img, rotation)

		
	def update(self,ev):
		if self.released:
			self.released = False
			
		if ev.type == MOUSEBUTTONDOWN and ev.button == 1 and self.collidepoint(ev.pos) and self.fixe == False:
			x, y = ev.pos
			self.selected = True
				
		elif ev.type == MOUSEBUTTONUP and ev.button == 1 and self.collidepoint(ev.pos) and self.fixe == False:
			self.selected = False
			self.released = True

		elif ev.type == MOUSEMOTION and self.selected:
			relx,rely = ev.rel
			self.x += relx
			self.y += rely
			
		else:   
			return False
		return True
		
	@property
	def pos(self):
		return self.topleft

	@pos.setter
	def pos(self,coord):
		self.topleft = coord
		
	def __lt__(self, cartePaquetArrive):
		if cartePaquetArrive == None:
			return False
		couleurDepart, valeurDepart = int(self.couleur), int(self.valeur)
		couleurArrive, valeurArrive = int(cartePaquetArrive.couleur), int(cartePaquetArrive.valeur)
		#descente des atouts
		if couleurArrive == 4 and couleurDepart == 4:
			if valeurArrive == (valeurDepart + 1):
				return True
		if couleurArrive == 0 and ((couleurDepart - 1) == 0 or (couleurDepart - 3) == 0):
			if valeurArrive == (valeurDepart + 1):
				return True
		if couleurArrive == 1 and ((couleurDepart - 1) == 1 or (couleurDepart + 1) == 1):
			if valeurArrive == (valeurDepart + 1):
				return True
		if couleurArrive == 2 and ((couleurDepart - 1) == 2 or (couleurDepart + 1) == 2):
			if valeurArrive == (valeurDepart + 1):
				return True
		if couleurArrive == 3 and ((couleurDepart + 3) == 3 or (couleurDepart + 1) == 3):
			if valeurArrive == (valeurDepart + 1):
				return True
		return False
		
	def __gt__(self, cartePaquetArrive):
		if cartePaquetArrive == None:
			return False
		couleurDepart, valeurDepart = int(self.couleur), int(self.valeur)
		couleurArrive, valeurArrive = int(cartePaquetArrive.couleur), int(cartePaquetArrive.valeur)
		#descente des atouts
		if couleurArrive == couleurDepart:
			if valeurArrive == (valeurDepart - 1):
				return True
		return False
	
	def __eq__(self, autreCarte):
		if autreCarte == None:
			return False
		if (self.couleur == autreCarte.couleur) and (self.valeur == autreCarte.valeur):
			return True
		return False

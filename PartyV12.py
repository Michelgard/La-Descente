# -*- coding: cp1252 -*-

import random
from CarteGraphique import CarteGraphique
from JeuCartesGraphiques import JeuCartesGraphiques
from PaquetGraphique import PaquetGraphique
import sys, pygame
from time import sleep
from pygame.locals import *

class PartieV12 :
	def __init__(self):
	
		self.WINSIZE = [1000, 600]
		pygame.init()
		self.fenetre = pygame.display.set_mode(self.WINSIZE)
		pygame.display.set_caption('La descente')
	
		#Cartes fixes crées et placées
		self.cartesFixes = JeuCartesGraphiques(fixe = True, fenetre = self.fenetre)
	
		#Changement images des mains
		self.carteMainSud = CarteGraphique(pygame.image.load("images/main-sud.gif").convert())
		self.carteMainNord = CarteGraphique(pygame.image.load("images/main-nord.gif").convert())
		
		icon_32x32 = pygame.image.load("images/icone.gif").convert_alpha()
		pygame.display.set_icon(icon_32x32)
		
		#Difinition de la position des paquets sur le jeu
		self.positionPaquet =[(292,180),(392,180),(492,180),(592,180),(692,180),(
			280,50),(400,31),(520,30),(400,444),(520,443),(640,420),(
			55,102),(55,182),(55,262),(55,342),(55,422), ]		
			
		self.modeJeu = 1
		self.niveauJeu = [0, 0, 1, 0, 0]
		
		self.timer = pygame.time.Clock()
		
		self.demarrer = False

	def redraw(self): #placement de la liste images en 2 temps (images fixes et images en mouvement)
		self.fenetre.fill((0, 0, 0))
		
		for j, i in enumerate(self.cartesFixes.cartes):
			self.fenetre.blit(i.img,i.pos)
			
		for t in reversed(self.listeCartes):	
			self.fenetre.blit(t.img,t.pos)
		
		pygame.display.flip()	
		
	def demarrerPartie(self):
		self.demarrer = True
		self.listeCartes = []
		#Jeu de tarot créé et mélangé
		self.jeuDeTarot = JeuCartesGraphiques()
		self.melanger()
		#Le joueur SUD commence
		self.joueurSud = True
		self.joueurNord = False
		self.paquet = [None]
		for i in self.positionPaquet:
			self.paquet.append(PaquetGraphique(topleft = i))
			
		self.cartesFixes.cartes[1] = (CarteGraphique(img = pygame.image.load("images/dos-carte.jpg").convert()))
		self.cartesFixes.cartes[2] = (CarteGraphique(img = pygame.image.load("images/dos-carte.jpg").convert()))
		self.cartesFixes.cartes[1].placer(fenetre = self.fenetre, topleft=(520,30))
		self.cartesFixes.cartes[2].placer(fenetre = self.fenetre, topleft=(400,444))
		
		self.distribuer()
		
		#Mise en place de la main SUD pour commencer
		self.listeCartes.insert(0, self.carteMainSud)
		self.listeCartes[0].placer(fenetre = self.fenetre, topleft=(670,522))
		
		self.redraw()
		
		while 1:
			self.timer.tick(20)
			self.ev = pygame.event.wait()
		
			if self.ev.type == QUIT:
				break
			elif self.ev.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):	
				for self.indice, carte in enumerate(self.listeCartes):
					if carte.update(self.ev):
						if self.ev.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
								if self.mouvementCartes(carte):
									break
				
				self.jouerCartesNordSud(self.ev)	
				if self.menu(self.ev):
					break
			self.redraw()	
			if self.parcoursPaquet():#placement automatique des cartes
				self.parcoursPaquet()
			else:
				self.rangementPaquetCote()	
			
			if (len(self.paquet[7].cartes) == 0) and (len(self.paquet[8].cartes) == 0) and (len(self.paquet[6].cartes) == 0):
				self.gagnant("NORD")
				if self.menu(self.ev):
					break
		
			if (len(self.paquet[9].cartes) == 0) and (len(self.paquet[10].cartes) == 0) and (len(self.paquet[11].cartes) == 0):
				self.gagnant("SUD")
				if self.menu(self.ev):
					break
		pygame.quit()
		sys.exit()

	def gagnant(self, gagneur):
		text_size = 30
		bg_col = [0,0,0]
		text_col = [255,255,255]
		
		myfont = pygame.font.Font("Roboto-Regular.ttf", text_size)
		pygame.draw.rect(self.fenetre, 0, (0,25,1000,575))
		
		texte = 	"LE JOUEUR " + gagneur + " GAGNE LA PARTIE"
		bulle = Rect(200,250,500,350)
		x,y = bulle.topleft
		
		for ligne in texte.splitlines():
			x,y = self.fenetre.blit(myfont.render(ligne, True, text_col, bg_col),(x,y)).bottomleft
			
		pygame.display.flip()	
		while 1:
					
			ev = pygame.event.wait()
			if ev.type == QUIT:
				pygame.quit()
				return True
			if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
				if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
					if (self.cartesFixes.cartes[15].collidepoint(ev.pos)):
						self.demarrer = False
						self.affichageMenu()
		
	def retournerCarte(self, paquet, carte, indicePaquet):
		self.paquet[paquet].ajouterCarte(carte)
		self.paquet[indicePaquet].tirerCarteFace()
		self.mouvementCartesSeules(carte, self.paquet[paquet].pos, True)
		carte.pos = self.paquet[paquet].pos
		return True
	
	def mouvementCartesSeules(self, carte, posArrive, rotation):
		index = self.rechercheDansListe(self.listeCartes, carte)
		if  index < 0:
			self.listeCartes.insert(0, carte)
		else:
			self.listeCartes.insert(0, self.listeCartes[index])
			self.listeCartes[index + 1 : index + 2] = []
		pasX = (posArrive[0] - carte.x) / float(90)
		pasY = (posArrive[1] - carte.y) / float(90)
		if rotation:
			carte.placerR(90)
		for i in range(1,80):
			carte.x = carte.x + int(round(pasX, 0))
			carte.y = carte.y + int(round(pasY, 0))
			self.redraw()
			sleep(0.01)
	
	def parcoursPaquet(self):
		mouvement = False
		for indicePaquet in range (1, 12):
			if indicePaquet <> 8 and indicePaquet <> 9:
				carte = self.paquet[indicePaquet].derniereCarte()
				if carte <> None:
					if carte.couleur == 5: # placement excuse
						mouvement =  self.retournerCarte(16, carte, indicePaquet)
						break
					elif carte.couleur == 4:
						carteDessus = self.paquet[16].derniereCarte()
						if carteDessus <> None:
							if carte.valeur == 1:
								mouvement =  self.retournerCarte(16, carte, indicePaquet)
								break
							elif carte > carteDessus:
								mouvement =  self.retournerCarte(16, carte, indicePaquet) 
								break
								
					elif carte.couleur == 3:
						carteDessous = self.paquet[15].derniereCarte()
						if carteDessous <> None:
							if carte > carteDessous:
								mouvement =  self.retournerCarte(15, carte, indicePaquet)
								break
						else:
							if carte.valeur == 1:
								mouvement =  self.retournerCarte(15, carte, indicePaquet) 
								break
							
					elif carte.couleur == 2:
						carteDessus = self.paquet[12].derniereCarte()
						if carteDessus <> None:
							if carte > carteDessus:
								mouvement =  self.retournerCarte(12, carte, indicePaquet)
								break
						else:
							if carte.valeur == 1:
								mouvement = self.retournerCarte(12, carte, indicePaquet)
								break
								
					elif carte.couleur == 1:
						carteDessus = self.paquet[14].derniereCarte()
						if carteDessus <> None:
							if carte > carteDessus:
								mouvement =  self.retournerCarte(14, carte, indicePaquet)
								break
						else:
							if carte.valeur == 1:
								mouvement =  self.retournerCarte(14, carte, indicePaquet)
								break
								
					elif carte.couleur == 0:
						carteDessus = self.paquet[13].derniereCarte()
						if carteDessus <> None:
							if carte > carteDessus:
								mouvement = self.retournerCarte(13, carte, indicePaquet)
								break
						else:
							if carte.valeur == 1:
								mouvement = self.retournerCarte(13, carte, indicePaquet)
								break
		return mouvement						
		
	def mouvementCartes(self, cartePrise):
		if self.ev.type == MOUSEBUTTONDOWN:
			self.cartePaquetDepart, self.indiceCarteDepart = None, None
			fin = False
			for i , j in enumerate(self.paquet):
				if i > 0 and i <> 9 and i <> 8:
					for j, carte in enumerate(self.paquet[i]):
						if carte == cartePrise:
							self.indicePaquetDepart = i
							self.indiceCarteDepart = j
							fin = True
							break
				if fin == True : break
			self.cartePaquetDepart = cartePrise
			self.positionDepart = self.cartePaquetDepart.pos
			self.listeCartes.insert(0, self.cartePaquetDepart) # déplacement de l'image cliquée au debut de la liste image non fixe
			self.listeCartes[self.indice +1 : self.indice + 2] = []
			self.move = True
			return True
		elif self.move:
			self.cartePaquetArrive, self.indiceArrive = None, None
			for i , j in enumerate(self.paquet):
				if i > 0 and i <> 6 and i <> 11 and i <> 9 and i <> 8:
					if self.paquet[i].collidepoint(self.ev.pos):
						self.cartePaquetArrive = self.paquet[i].derniereCarte()
						self.indiceArrive = i
						break
						
			if not self.mainSurPaquetNordSud():
				if (self.cartePaquetArrive == None) and (self.indiceArrive <> None)\
					and (self.indiceArrive < 12) : # pas de carte arrivé mais paquet
					#déplacement de plusieurs cartes sur paquet cental
					self.deplacementMultiCarte()
					if self.indiceArrive > 0 and self.indiceArrive < 6:
						self.rangementPaquetCentre()
				else :
					self.cartePaquetDepart.pos = self.positionDepart
					if self.indicePaquetDepart > 0 and self.indicePaquetDepart < 6:
						self.rangementPaquetCentre()
				
				if self.cartePaquetArrive <> None and self.indiceArrive <> None: 
					if (self.cartePaquetDepart.couleur == 4) and \
						 ((self.indiceArrive == 7) or (self.indiceArrive == 10)) and \
						  (self.paquet[16].premiereCarte() == None):
						self.cartePaquetDepart.pos = self.positionDepart
						self.rangementPaquetCentre()
					
					# vérification si descente carte
					elif not (self.cartePaquetDepart < self.cartePaquetArrive): #compare si carte plus petite et couleur inverse
						self.cartePaquetDepart.pos = self.positionDepart
						if self.indiceArrive > 0 and self.indiceArrive < 6:
							self.rangementPaquetCentre()
					else:	
						#déplacement de plusieurs cartes sur paquet cental
						self.deplacementMultiCarte()	
						if self.indiceArrive > 0 and self.indiceArrive < 6:
							self.rangementPaquetCentre()
			if self.joueurSud == True: # la main toujours au dessus
				index = self.rechercheDansListe(self.listeCartes, self.carteMainSud)
			else:
				index = self.rechercheDansListe(self.listeCartes, self.carteMainNord)
			self.listeCartes.insert(0, self.listeCartes[index])
			self.listeCartes[index + 1 : index + 2] = []
			self.move = False
			
	def deplacementMultiCarte(self):
		for d in range(self.indiceCarteDepart, len(self.paquet[self.indicePaquetDepart].cartes)):
			self.paquet[self.indiceArrive].ajouterCarte(self.paquet[self.indicePaquetDepart].cartes[d])
			self.paquet[self.indicePaquetDepart].cartes[d].pos = self.paquet[self.indiceArrive].pos
		for d in range(self.indiceCarteDepart, len(self.paquet[self.indicePaquetDepart].cartes)):
			finPaquet = len(self.paquet[self.indicePaquetDepart].cartes) 
			self.paquet[self.indicePaquetDepart].cartes[finPaquet -1 : finPaquet] = []
	
	def mainSurPaquetNordSud(self):
		if self.indicePaquetDepart == 6 and self.indiceArrive == 7: # tirage carte paquet Nord
			carte = self.paquet[self.indicePaquetDepart].tirerCarte()
			if carte <> None:
				self.paquet[self.indiceArrive].ajouterCarte(carte)
				carte.pos = self.paquet[7].pos
				
				index = self.rechercheDansListe(self.listeCartes, self.carteMainNord)
				self.listeCartes[index : index +1] = []
				self.joueurNord = False 
				self.joueurSud = True
				index = self.rechercheDansListe(self.listeCartes, self.carteMainSud)
				if  index < 0:
					self.listeCartes.insert(0, self.carteMainSud)
					self.listeCartes[0].placer(fenetre = self.fenetre, topleft=(670,522))
				else:
					self.listeCartes.insert(0, self.listeCartes[index])
					self.listeCartes[index + 1 : index + 2] = []
				return True
		elif self.indicePaquetDepart == 11 and self.indiceArrive == 10: # tirage carte paquet Sud
			carte = self.paquet[self.indicePaquetDepart].tirerCarte()
			if carte <> None:
				self.paquet[self.indiceArrive].ajouterCarte(carte)
				carte.pos = self.paquet[10].pos
				
				index = self.rechercheDansListe(self.listeCartes, self.carteMainSud)
				self.listeCartes[index : index +1] = []
				self.joueurNord = True
				self.joueurSud = False 
				index = self.rechercheDansListe(self.listeCartes, self.carteMainNord)
				if  index < 0:
					self.listeCartes.insert(0, self.carteMainNord)
					self.listeCartes[0].placer(fenetre = self.fenetre, topleft=(230,00))
				else:
					self.listeCartes.insert(0, self.listeCartes[index])
					self.listeCartes[index + 1 : index + 2] = []
					
				if self.modeJeu == 1:
					self.jeuOrdi()
					#jeuOrdi(self.paquet, self.listeCartes, self.cartesFixes, self.fenetre, self.carteMainNord, self.carteMainSud)
					self.joueurNord = False 
					self.joueurSud = True
				return True
		else:
			return False			
	
	def rangementPaquetCentre(self):
		for k in range(1,6):
			val = 0
			if len(self.paquet[k].cartes) > 6:
				i = 10
			else :
				i = 18
			for carte in self.paquet[k]:
				index = self.listeCartes.index(carte)
				self.listeCartes.insert(0, carte)
				self.listeCartes[index +1 : index + 2] = []
				carte.pos = self.paquet[k].pos
				carte.x = carte.x + 10
				carte.y = carte.y + val
				val = val + i
				
	def rangementPaquetCote(self):
		for k in range(12,17):
			for carte in self.paquet[k]:
				index = self.listeCartes.index(carte)
				self.listeCartes.insert(0, carte)
				self.listeCartes[index +1 : index + 2] = []
			
	def verificationValiditer2Cartes(self):
		if self.cartePaquetArrive == None:
			return False
		couleurDepart, valeurDepart = int(self.cartePaquetDepart.couleur), int(self.cartePaquetDepart.valeur)
		couleurArrive, valeurArrive = int(self.cartePaquetArrive.couleur), int(self.cartePaquetArrive.valeur)
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
		
	def rechercheDansListe(self, liste, carte):
		try:
			index = liste.index(carte)
			return index
		except:
			return -1
	
	def menu(self, ev):
		if ev.type == QUIT:
			pygame.quit()
			return True
		if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
			if (self.cartesFixes.cartes[15].collidepoint(ev.pos)):
				return self.affichageMenu()
		return False
	
	def affichageMenu(self):
		imageMenu = []
		text_size = 12
		bg_col = [0,0,0]
		text_col = [255,255,255]
		
		myfont = pygame.font.Font("Roboto-Regular.ttf", text_size)
		#pygame.draw.rect(self.fenetre, 0, (0,25,1000,575))
		
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/mode-joueur.gif").convert())))
		imageMenu[0].placer(fenetre = self.fenetre, topleft=(96,60))
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/un-joueur.gif").convert()))
		imageMenu[1].placer(fenetre = self.fenetre, topleft=(96,100))
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/deux-joueurs.gif").convert()))
		imageMenu[2].placer(fenetre = self.fenetre, topleft=(100,130))
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/case-a-cocher.gif").convert()))
		if self.modeJeu == 1:
			imageMenu[3].placer(fenetre = self.fenetre, topleft=(200,95))
		else :
			imageMenu[3].placer(fenetre = self.fenetre, topleft=(200,130))
		
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/niveau-jeu-ordi.gif").convert())))
		imageMenu[4].placer(fenetre = self.fenetre, topleft=(96,210))
		
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/niveau-expert.gif").convert())))
		imageMenu[5].placer(fenetre = self.fenetre, topleft=(96,240))
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/niveau-tres-bon.gif").convert())))
		imageMenu[6].placer(fenetre = self.fenetre, topleft=(96,270))
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/niveau-bon.gif").convert())))
		imageMenu[7].placer(fenetre = self.fenetre, topleft=(96,300))
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/niveau-moyen.gif").convert())))
		imageMenu[8].placer(fenetre = self.fenetre, topleft=(96,330))
		imageMenu.append((CarteGraphique(img = pygame.image.load("images/niveau-mauvais.gif").convert())))
		imageMenu[9].placer(fenetre = self.fenetre, topleft=(96,360))
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/case-a-cocher.gif").convert()))
		for indice, val in enumerate(self.niveauJeu):
			if val == 1 :
				topleft = (200, imageMenu[indice + 5].y)
				imageMenu[10].placer(fenetre = self.fenetre, topleft = topleft)
				break
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/menu-regle.gif").convert()))
		imageMenu[11].placer(fenetre = self.fenetre, topleft=(96,440))
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/menu-a-propos.gif").convert()))
		imageMenu[12].placer(fenetre = self.fenetre, topleft=(96,480))
		
		imageMenu.append(CarteGraphique(img = pygame.image.load("images/menu-lancer-partie.gif").convert()))
		imageMenu[13].placer(fenetre = self.fenetre, topleft=(500,150))
		
		if self.demarrer == True :
			imageMenu.append(CarteGraphique(img = pygame.image.load("images/menu-continuer-partie.gif").convert()))
			imageMenu[14].placer(fenetre = self.fenetre, topleft=(500,350))
		
		self.boucleAffichageMenu(imageMenu)
		while 1:		
			ev = pygame.event.wait()
			if ev.type == QUIT:
				pygame.quit()
				return True
			if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
				if (imageMenu[1].collidepoint(ev.pos)):
					self.modeJeu = 1
					imageMenu[3].pos = (200,95)
					self.boucleAffichageMenu(imageMenu)
				if (imageMenu[2].collidepoint(ev.pos)):
					self.modeJeu = 2
					imageMenu[3].pos = (200,130)
					self.boucleAffichageMenu(imageMenu)
					
				if (imageMenu[5].collidepoint(ev.pos)):
					self.niveauJeu = [1, 0, 0, 0, 0]
					imageMenu[10].pos = (200,240)
					self.boucleAffichageMenu(imageMenu)
				if (imageMenu[6].collidepoint(ev.pos)):
					self.niveauJeu = [0, 1, 0, 0, 0]
					imageMenu[10].pos = (200,270)
					self.boucleAffichageMenu(imageMenu)
				if (imageMenu[7].collidepoint(ev.pos)):
					self.niveauJeu = [0, 0, 1, 0, 0]
					imageMenu[10].pos = (200,300)
					self.boucleAffichageMenu(imageMenu)
				if (imageMenu[8].collidepoint(ev.pos)):
					self.niveauJeu = [0, 0, 0, 1, 0]
					imageMenu[10].pos = (200,330)
					self.boucleAffichageMenu(imageMenu)
				if (imageMenu[9].collidepoint(ev.pos)):
					self.niveauJeu = [0, 0, 0, 0, 1]
					imageMenu[10].pos = (200,360)
					self.boucleAffichageMenu(imageMenu)
				
				if (imageMenu[11].collidepoint(ev.pos)):
					 self.regleDuJeu()
					 
				if (imageMenu[12].collidepoint(ev.pos)):
					 self.aPropos()
					 
				if (imageMenu[13].collidepoint(ev.pos)):	 
					self.move = False
					self.demarrerPartie()
				if self.demarrer == True :	
					if (imageMenu[14].collidepoint(ev.pos)):
						return False
					 
	def boucleAffichageMenu(self, imageMenu):
		pygame.draw.rect(self.fenetre, 0, (0,25,1000,575))
		self.fenetre.blit(self.cartesFixes.cartes[15].img, self.cartesFixes.cartes[15].pos)
		for j, i in enumerate(imageMenu):
			self.fenetre.blit(i.img,i.pos)
		pygame.display.flip()				
	
	def regleDuJeu(self):
		text_size = 12
		bg_col = [0,0,0]
		text_col = [255,255,255]
		
		myfont = pygame.font.Font("Roboto-Regular.ttf", text_size)
		pygame.draw.rect(self.fenetre, 0, (0,25,1000,575))
		with open('les-regles-du-jeu.txt', 'r') as mon_fichier:
			texte = mon_fichier.read()
		
		bulle = Rect(40,60,600,600)
		x,y = bulle.topleft
		
		for ligne in texte.splitlines():
			x,y = self.fenetre.blit(myfont.render(ligne, True, text_col, bg_col),(x,y)).bottomleft
		
		pygame.display.flip()	
		while 1:
							
			ev = pygame.event.wait()
			if ev.type == QUIT:
				pygame.quit()
				return True
			if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
				if (self.cartesFixes.cartes[15].collidepoint(ev.pos)):
					self.affichageMenu()
			
	
	def aPropos(self):
		text_size = 30
		bg_col = [0,0,0]
		text_col = [255,255,255]
		
		myfont = pygame.font.Font("Roboto-Regular.ttf", text_size)
		pygame.draw.rect(self.fenetre, 0, (0,25,1000,575))
		with open('a-propos.txt', 'r') as mon_fichier:
			texte = mon_fichier.read()
		
		bulle = Rect(500,225,500,350)
		x,y = bulle.topleft
		
		for ligne in texte.splitlines():
			x,y = self.fenetre.blit(myfont.render(ligne, True, text_col, bg_col),(x,y)).bottomleft
			
		pygame.display.flip()	
		while 1:
			ev = pygame.event.wait()
			if ev.type == QUIT:
				pygame.quit()
				return True
			if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
				if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
					if (self.cartesFixes.cartes[15].collidepoint(ev.pos)):
						self.affichageMenu()
		
	def jouerCartesNordSud(self, ev):
		if ev.type == MOUSEBUTTONDOWN  and ev.button == 1:
			if (self.cartesFixes.cartes[1].collidepoint(ev.pos)) and \
				(self.paquet[11].premiereCarte()== None) and \
				(self.paquet[6].premiereCarte() == None) and \
				self.joueurSud == False:
				carte = self.paquet[8].tirerCarte()
				if carte <> None:							
					self.paquet[6].ajouterCarte(carte)
					self.listeCartes.insert(0, carte)
					self.paquet[6].cartes[0].placer(fenetre = self.fenetre, topleft=self.paquet[6].pos)
					
					index = self.rechercheDansListe(self.listeCartes, self.carteMainNord)
					if  index < 0:
						self.listeCartes.insert(0, self.carteMainNord)
						self.listeCartes[0].placer(fenetre = self.fenetre, topleft=(230,00))
					else:
						self.listeCartes.insert(0, self.listeCartes[index])
						self.listeCartes[index + 1 : index + 2] = []
					
					if self.paquet[8].premiereCarte()== None:
						self.cartesFixes.cartes[1]=(CarteGraphique(pygame.image.load("images/carte-transparente.gif").convert()))
						self.cartesFixes.cartes[1].placer(fenetre = self.fenetre, topleft=(520,30))
			elif (self.cartesFixes.cartes[2].collidepoint(ev.pos)) and \
				(self.paquet[6].premiereCarte()== None) and \
				(self.paquet[11].premiereCarte() == None) and \
				self.joueurNord == False:
				carte = self.paquet[9].tirerCarte()
				if carte <> None:
					self.paquet[11].ajouterCarte(carte)
					self.listeCartes.insert(0, carte)
					self.paquet[11].cartes[0].placer(fenetre = self.fenetre, topleft=self.paquet[11].pos)
					
					index = self.rechercheDansListe(self.listeCartes, self.carteMainSud)
					if  index < 0:
						self.listeCartes.insert(0, self.carteMainSud)
						self.listeCartes[0].placer(fenetre = self.fenetre, topleft=(670,522))
					else:
						self.listeCartes.insert(0, self.listeCartes[index])
						self.listeCartes[index + 1 : index + 2] = []
						
					if self.paquet[9].premiereCarte()== None:
						self.cartesFixes.cartes[2]=(CarteGraphique(pygame.image.load("images/carte-transparente.gif").convert()))
						self.cartesFixes.cartes[2].placer(fenetre = self.fenetre, topleft=(400,444))
		if ev.type == MOUSEBUTTONDOWN and ev.button == 3:
			if (self.cartesFixes.cartes[1].collidepoint(ev.pos)) and \
				(self.paquet[11].premiereCarte()== None) and \
				(self.paquet[6].premiereCarte() == None) and \
				(self.paquet[8].premiereCarte()== None) and \
				 (self.joueurNord == True):
					m = 0
					carte = self.paquet[7].tirerCarte()
					while carte <> None:
						index = self.listeCartes.index(carte)
						self.listeCartes[index : index + 1] = []
						if m == 0:
							self.paquet[8].ajouterCarte(carte)
							m = 1
						else:
							self.paquet[8].ajouterCarteDebut(carte)
							m = 0
						carte = self.paquet[7].tirerCarte()
					self.cartesFixes.cartes[1]=(CarteGraphique(pygame.image.load("images/dos-carte.jpg").convert()))	
					self.cartesFixes.cartes[1].placer(fenetre = self.fenetre, topleft=(520,30))
			
			elif (self.cartesFixes.cartes[2].collidepoint(ev.pos)) and \
			(self.paquet[6].premiereCarte()== None) and \
			(self.paquet[11].premiereCarte() == None) and \
			(self.paquet[9].premiereCarte()== None) and \
			 (self.joueurSud == True):
				m = 0
				carte = self.paquet[10].tirerCarte()
				h = 0
				while carte <> None:
					index = self.listeCartes.index(carte)
					self.listeCartes[index : index + 1] = []
					if m == 0:
						self.paquet[9].ajouterCarte(carte)
						m = 1
					else:
						self.paquet[9].ajouterCarteDebut(carte)
						m = 0
					carte = self.paquet[10].tirerCarte()
					h = h + 1
				self.cartesFixes.cartes[2]=(CarteGraphique(pygame.image.load("images/dos-carte.jpg").convert()))	
				self.cartesFixes.cartes[2].placer(fenetre = self.fenetre, topleft=(400,444))	
	
	def melanger(self):
		self.jeuDeTarot.melanger()
		
	def distribuer(self):
		pourTable = set()
		while len(pourTable) < 5:
			aleatoire = random.randint(1,76)
			pourTable.add(aleatoire)
		n = 1
		j = 0
		debut = 302
		for i in range(len(self.jeuDeTarot.cartes)):
			carte = self.jeuDeTarot.tirerCarte()
			if i in pourTable: #Placement des cartes centrales dans les paquets et sur table
				self.paquet[n].ajouterCarte(carte)
				self.paquet[n].cartes[0].placer(fenetre = self.fenetre, topleft=(debut,180))
				debut += 100
				n=n+1
				self.listeCartes.append(carte)
			elif j == 1: #placement cartes joueur nord paquet8 = cartes de dos
				self.paquet[8].ajouterCarte(carte)
				j = 0
			else: #placement cartes joueur sud paquet10 = cartes de dos
				self.paquet[9].ajouterCarte(carte)
				j = 1	
#########################################################################################
################### jeu ordinateur ######################################################
#########################################################################################

	def jeuOrdi(self):
	
		joueurSuivant = True
		while joueurSuivant:
			mouveCarte = False
			boucle = True
			while boucle:
				if self.recherche1(7) or self.recherche2() or self.mouvementDansPaquet() or \
					self.rechercheSiCarteVaSurCentre(7): #  recherche si carte de l'ordi va sur carte joueur SUD
					self.rechercheCarteCoteGauche()
					boucle = True
				else : 
					boucle = False
			
			if self.paquet[6].derniereCarte() == None:
				if self.paquet[8].derniereCarte() == None:
					if not self.melangerPaquet():
						self.verifivationSiNordGagne()
				self.tirerCarteNord()
			
			while self.rechercheCarteCoteGauche():
				if self.paquet[6].derniereCarte() == None:
					if self.paquet[8].derniereCarte() == None:
						if not self.melangerPaquet():
							self.verifivationSiNordGagne()
					self.tirerCarteNord()
			
						
			if self.paquet[7].derniereCarte() <> None and \
				(self.paquet[7].derniereCarte().valeur == 14 or \
				self.paquet[7].derniereCarte().valeur > self.paquet[6].derniereCarte().valeur):
					nbPaquet = 7
			else:
				nbPaquet = 6
				
			while self.recherchePaquetVide(nbPaquet):
				if self.paquet[6].derniereCarte() == None:
					if self.paquet[8].derniereCarte() == None:
						if not self.melangerPaquet():
							self.verifivationSiNordGagne()
					self.tirerCarteNord()
				while self.rechercheCarteCoteGauche():
					if self.paquet[6].derniereCarte() == None:
						if self.paquet[8].derniereCarte() == None:
							if not self.melangerPaquet():
								self.verifivationSiNordGagne()
						self.tirerCarteNord()
				mouveCarte = True
				
			while self.recherche1(6) or self.rechercheSiCarteVaSurCentre(6):
				self.tirerCarteNord()
				while self.rechercheCarteCoteGauche():
					if self.paquet[6].derniereCarte() <> None:
						if self.paquet[8].derniereCarte() == None:
							if not self.melangerPaquet():
								self.verifivationSiNordGagne()
						self.tirerCarteNord()
				mouveCarte = True
			
			if mouveCarte == True:
				joueurSuivant = True
			else:
				self.carteNordSurNord()# retour carte et changement joueur
				joueurSuivant = False				
	
	def niveauJeuOrdi(self):
		aleatoire = random.randint(0,4)
		#niveau expert
		if self.niveauJeu[0] == 1 :
			return True
		#niveau tres bon
		elif self.niveauJeu[1] == 1 and (aleatoire == 0 or aleatoire == 2 or aleatoire == 4 or aleatoire == 3):
			return True
		#niveau bon
		elif self.niveauJeu[2] == 1 and (aleatoire == 0 or aleatoire == 2 or aleatoire == 4):
			return True
		#niveau moyen
		elif self.niveauJeu[3] == 1 and (aleatoire == 1 or aleatoire == 3):
			return True
		#niveau mauvais
		elif self.niveauJeu[4] == 1 and (aleatoire == 4):
			return True
		return False
	
	def verifivationSiNordGagne(self):
		if (len(self.paquet[7].cartes) == 0) and (len(self.paquet[8].cartes) == 0) and (len(self.paquet[6].cartes) == 0):
			self.gagnant("NORD")
			if self.menu(self.ev):
				return True
	
	# si carte Nord va sur paquet centre
	def rechercheSiCarteVaSurCentre(self, nbPaquet):
		if self.niveauJeuOrdi():
			for k in range(1,6):
				if self.paquet[k].derniereCarte() <> None:
					carteChercheUn, carteCherchedeux = self.recherche2CartesPossible(self.paquet[k].derniereCarte())
					if self.paquet[nbPaquet].derniereCarte() == carteChercheUn or self.paquet[nbPaquet].derniereCarte() == carteCherchedeux:
						if self.paquet[nbPaquet].derniereCarte() <> None:
							self.mouvementCartesSeules(self.paquet[nbPaquet].derniereCarte(), self.paquet[k].pos, False)
							self.paquet[nbPaquet].derniereCarte().pos = self.paquet[k].pos
							self.paquet[nbPaquet].derniereCarte().x = self.paquet[nbPaquet].derniereCarte().x + 10
							self.paquet[k].ajouterCarte(self.paquet[nbPaquet].tirerCarteFace())
							self.rangementPaquetCentre()
							return True
			return False
		else : return False
		
	# melange paquet si plus de carte
	def melangerPaquet(self):
		m = 0
		carte = self.paquet[7].tirerCarte()
		if carte == None :
			return False
		while carte <> None:
			
			index = self.listeCartes.index(carte)
			self.listeCartes[index : index + 1] = []
			if m == 0:
				self.paquet[8].ajouterCarte(carte)
				m = 1
			else:
				self.paquet[8].ajouterCarteDebut(carte)
				m = 0
			carte = self.paquet[7].tirerCarte()
		self.cartesFixes.cartes[1]=(CarteGraphique(pygame.image.load("images/dos-carte.jpg").convert()))	
		self.cartesFixes.cartes[1].placer(fenetre = self.fenetre, topleft = (520,30))
		return True
		
	##### recherche paquet vide
	def recherchePaquetVide(self, paquetNord):
		if self.niveauJeuOrdi():
			for k in range(1,6):
				if len(self.paquet[k].cartes) == 0:
					self.paquet[k].ajouterCarte(self.paquet[paquetNord].tirerCarteFace())
					self.mouvementCartesSeules(self.paquet[k].derniereCarte(), self.paquet[k].pos, False)
					self.paquet[k].derniereCarte().pos = self.paquet[k].pos
					self.paquet[k].derniereCarte().x = self.paquet[k].derniereCarte().x + 10
					self.rangementPaquetCentre()
					return True
				else: False
		else: return False
		
	### carte nord sur paquet nord
	def carteNordSurNord(self):
		if self.paquet[6].derniereCarte <> None:
			self.paquet[7].ajouterCarte(self.paquet[6].tirerCarteFace())
			if self.paquet[7].derniereCarte() <> None:
				self.mouvementCartesSeules(self.paquet[7].derniereCarte(), self.paquet[7].pos, False)
				self.paquet[7].derniereCarte().pos = self.paquet[7].pos
				
				index = self.rechercheDansListe(self.listeCartes, self.carteMainNord)
				self.listeCartes[index : index +1] = []
				
				index = self.rechercheDansListe(self.listeCartes, self.carteMainSud)
				if  index < 0:
					self.listeCartes.insert(0, self.carteMainSud)
					self.listeCartes[0].placer(fenetre = self.fenetre, topleft = (670,522))
				else:
					self.listeCartes.insert(0, self.listeCartes[index])
					self.listeCartes[index + 1 : index + 2] = []
	
	### tirage carte nord ###################################
	def tirerCarteNord(self):
		carte = self.paquet[8].tirerCarte()
		if carte <> None:							
			self.paquet[6].ajouterCarte(carte)
			self.listeCartes.insert(0, carte)
			self.paquet[6].cartes[0].placer(fenetre = self.fenetre, topleft = self.paquet[6].pos)
			
			index = self.rechercheDansListe(self.listeCartes, self.carteMainNord)
			if  index < 0:
				self.listeCartes.insert(0, self.carteMainNord)
				self.listeCartes[0].placer(fenetre = self.fenetre, topleft = (230,00))
			else:
				self.listeCartes.insert(0, self.listeCartes[index])
				self.listeCartes[index + 1 : index + 2] = []
			
			if self.paquet[8].premiereCarte()== None:
				self.cartesFixes.cartes[1]=(CarteGraphique(pygame.image.load("images/carte-transparente.gif").convert()))
				self.cartesFixes.cartes[1].placer(fenetre = self.fenetre, topleft = (520,30))
	
	############ Vérifier si mouvement paquet possible    ###############
	def mouvementDansPaquet(self):	
		if self.niveauJeuOrdi():
			for k in range(1,6):
				if self.paquet[k].derniereCarte() <> None:
					carteChercheUn, carteCherchedeux = self.recherche2CartesPossible(self.paquet[k].derniereCarte())
					for l in range(1,6):
						if self.paquet[l].premiereCarte() <> None and \
						((self.paquet[l].premiereCarte() == carteChercheUn or self.paquet[l].premiereCarte() == carteCherchedeux)) and \
							l <> k:
							trouveCarte = (False, 0, l, 0)
							self.indiceCarteDepart = 0
							self.indicePaquetDepart = l
							self.indiceArrive = k
							self.deplacementMultiCarte()
							self.rangementPaquetCentre()
							return True
			return False
		else: return False
					
	def rechercheCarteCoteGauche(self):	
		if self.parcoursPaquet():#placement automatique des cartes
			self.parcoursPaquet()
			return True
		else:
			self.rangementPaquetCote()
			return False
			
			###########  recherche si carte de l'ordi va sur carte joueur SUD  ################	
	def recherche1(self, paquetNord):
		if self.niveauJeuOrdi():
			if self.paquet[10].derniereCarte() <> None:
				carteChercheUn, carteCherchedeux = self.recherche2CartesPossible(self.paquet[10].derniereCarte())
				carte = self.paquet[10].derniereCarte()
				if len(self.paquet[16].cartes) == 0 and carte.couleur == 4:
					return False
				if self.paquet[paquetNord].derniereCarte() == carteChercheUn or self.paquet[paquetNord].derniereCarte() == carteCherchedeux:
					self.paquet[10].ajouterCarte(self.paquet[paquetNord].tirerCarteFace())
					if self.paquet[10].derniereCarte() <> None:
						self.mouvementCartesSeules(self.paquet[10].derniereCarte(), self.paquet[10].pos, False)
						self.paquet[10].derniereCarte().pos = self.paquet[10].pos
					return True
				else : False
		else : return False
					
		###########  Recherche si cartes du centre va sur paquet SUD  ######################
	def recherche2(self):
		if self.niveauJeuOrdi():
			if self.paquet[10].derniereCarte() <> None:
				carte = self.paquet[10].derniereCarte()
				if len(self.paquet[16].cartes) == 0 and carte.couleur == 4:
					return False
				carteChercheUn, carteCherchedeux = self.recherche2CartesPossible(self.paquet[10].derniereCarte())
				trouveCarte1 = self.recherchePaquetCentre(carteChercheUn)
				trouveCarte2 = self.recherchePaquetCentre(carteCherchedeux)
				
				if trouveCarte1[0] and not trouveCarte2[0]:
					self.indiceCarteDepart = trouveCarte1[3]
					self.indicePaquetDepart = trouveCarte1[2]
					self.indiceArrive = 10
					self.deplacementMultiCarte()
					self.rangementPaquet()
					return True
					
				elif not trouveCarte1[0] and trouveCarte2[0]:
					self.indiceCarteDepart = trouveCarte2[3]
					self.indicePaquetDepart = trouveCarte2[2]
					self.indiceArrive = 10
					self.deplacementMultiCarte()
					self.rangementPaquet()
					return True
					
				elif trouveCarte1[0] and trouveCarte2[0]:
					if trouveCarte1[1] >= trouveCarte2[1]:
						self.indiceCarteDepart = trouveCarte1[3]
						self.indicePaquetDepart = trouveCarte1[2]
						self.indiceArrive = 10
						self.deplacementMultiCarte()
						self.rangementPaquet()
						return True
					else:
						self.indiceCarteDepart = trouveCarte2[3]
						self.indicePaquetDepart = trouveCarte2[2]
						self.indiceArrive = 10
						self.deplacementMultiCarte()
						self.rangementPaquet()
						return True
			return False
		else : return False
		
	def recherche2CartesPossible(self, carteJoueur):
		carteChercheUn, carteCherchedeux = None, None
		if carteJoueur.couleur == 0:
			carteChercheUn = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 1)
			carteCherchedeux = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 3)
			
		elif carteJoueur.couleur == 1:
			carteChercheUn = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 0)
			carteCherchedeux = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 2)
			
		elif carteJoueur.couleur == 2:
			carteChercheUn = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 1)
			carteCherchedeux = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 3)
			
		elif carteJoueur.couleur == 3:
			carteChercheUn = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 0)
			carteCherchedeux = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 2)
		
		elif carteJoueur.couleur == 4:
			carteChercheUn = CarteGraphique(valeur = (carteJoueur.valeur - 1), couleur = 4)
			carteCherchedeux = None
		
		return carteChercheUn, carteCherchedeux
		
	def recherchePaquetCentre(self, carteCherche):
		trouve = False
		nbCarte = 0
		for k in range(1,6):
			for indice, carte in enumerate(self.paquet[k]):
				if carte == carteCherche:
					trouve = True
					indiceCarte = indice
				if trouve:
					nbCarte = nbCarte + 1
			if trouve :
				return trouve, nbCarte, k , indiceCarte 	
		return trouve, nbCarte, k
	
	def rangementPaquet(self):
		for carte in self.paquet[10]:
			if carte <> None:
				index = self.listeCartes.index(carte)
				self.listeCartes.insert(0, carte)
				self.listeCartes[index +1 : index + 2] = []
		

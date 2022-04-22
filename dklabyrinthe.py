#-*-coding:utf-8 -*-
# cd N:\dk_labyrinthe_v1

'''
Created on 10 sept. 2019

@author: JORDAN
'''

"""
Jeu Donkey Kong Labyrinthe
Jeu dans lequel on doit d�placer DK jusqu'aux bananes � travers un labyrinthe.

Script Python
Fichiers : dklabyrinthe.py, classes.py, constantes.py,fonctions.py, n1, n2 + images
"""

#importation des bibliotheques
import pygame
import os
import time

#importation des modules
from constantes import *
import fonctions
from classes import *


#initialisation de pygame
pygame.init()

#titre
pygame.display.set_caption(titre)

#fenetre principale
fenetre = pygame.display.set_mode(resolution,pygame.DOUBLEBUF | pygame.HWSURFACE)

#On limite le nombre d'images par tour de boucle
clock  = pygame.time.Clock()

#on met a jour l'affichage
pygame.display.flip()

#initialisation des images

images_dk = {
            "img_dk_bas" : pygame.image.load(chemin_img_dk_bas).convert_alpha(),
            "img_dk_haut" : pygame.image.load(chemin_img_dk_haut).convert_alpha(),
            "img_dk_gauche" : pygame.image.load(chemin_img_dk_gauche).convert_alpha(),
            "img_dk_droite" : pygame.image.load(chemin_img_dk_droite).convert_alpha()
            }
 
images_fond = [
             pygame.image.load(chemin_img_fond1).convert_alpha(),
             pygame.image.load(chemin_img_fond2).convert_alpha()
             ]
   
img_acceuil = pygame.image.load(chemin_img_acceuil).convert_alpha()
img_arrivee = pygame.image.load(chemin_img_arrivee).convert_alpha()
img_depart = pygame.image.load(chemin_img_depart).convert_alpha()
img_mur = pygame.image.load(chemin_img_mur).convert_alpha()

#initialisation des sons
musique2 = pygame.mixer.Sound("sons/dk1.mp4") 
musique1 = pygame.mixer.Sound("sons/dk2.mkv") 
musique1.play()
       
continuer = True
lancer_menu = True
lancer_jeu = True

#boucle principale
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
                
    #initialise les fps
    clock.tick(fps)
    
    #On gere l'appui prolongé d'une touche
    pygame.key.set_repeat(400,40)
    num_labyrinthe = 1
    #boucle du menu
    while lancer_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lancer_menu = False
                continuer = False
                lancer_jeu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1 or event.key == pygame.K_F2:
                    if event.key == pygame.K_F1:
                        num_labyrinthe = 1
                    elif event.key == pygame.K_F2:
                        num_labyrinthe = 2
                    #on lance la musique
                    musique1.stop()
                    musique2.play()
                    musique2.set_volume(0.5)
                    lancer_menu = False
                    lancer_jeu = True
        #initialise les fps
        clock.tick(fps)
       
        fenetre.blit(img_acceuil,[0,0])
        
        #On actualise la fenetre
        pygame.display.flip()
    
    
    #On redimensionne la fenetre en fonction du niveau 
    if num_labyrinthe == 1:
        resolution = (600,600)
        pygame.display.set_mode(resolution)
    
    elif num_labyrinthe == 2 :
        resolution = (690,690)
        pygame.display.set_mode(resolution)
        
#Partie jeu   
   
    #On charge les niveaux
    cartes = []
    grille = {}
    for nom_fichier in os.listdir("niveaux"):
        if nom_fichier.endswith(".txt"):
            if nom_fichier == "n" + str(num_labyrinthe) + ".txt":
                chemin = os.path.join("niveaux", nom_fichier)
                nom_niveau = nom_fichier[:-3].lower()
                with open(chemin, "r") as fichier:
                    structure = fichier.read()
                    cartes.append(Niveau(structure))
                fichier.close()
    
    grille =  cartes[0].transform_grille()
    
    #création  du perso
    perso = Perso(grille,obstacle,arrivee,perso_lab)
    #position du perso
    pos_perso = (30,0)
    direc = "right"    
    obstacles = []
    cases_libres = []    
    resx,resy = resolution  
    #boucle du jeu
    while lancer_jeu:
        #initialise les fps
        clock.tick(fps)
        #On affiche l'mage de fond du jeu
        fenetre.blit(images_fond[num_labyrinthe - 1],[0,0])
        #Le joueur ne tombe pas
        tombe = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                lancer_jeu = False
            
            elif event.type == pygame.KEYDOWN:
                clock.tick(20)
                if (event.key== pygame.K_LEFT) and (event.key == pygame.K_UP) :
                    posx,posy = pos_perso
                    pos_perso = posx - taille_sprite,posy - taille_sprite 
                
                if  (event.key == pygame.K_RIGHT) and (event.key == pygame.K_UP):
                    posx,posy = pos_perso
                    pos_perso = posx + taille_sprite,posy - taille_sprite 
                               
                if event.key == pygame.K_UP:
                    direc = "up"
                    posx,posy = pos_perso
                    rec_perso = pygame.Rect(posx , posy - taille_sprite, taille_sprite, taille_sprite)
                    collision = False
                    if (rec_perso.y >= 0) :
                        tombe = False
                        for rec in iter(obstacles):
                            if (rec_perso.x == rec.x) and (rec_perso.y == rec.y):
                                collision = True
                        if not collision:
                            pos_perso = posx,posy - taille_sprite * 2
                            #a = 1  
                elif event.key == pygame.K_DOWN:
                    direc = "down"
                    posx,posy = pos_perso
                    rec_perso = pygame.Rect(posx , posy + taille_sprite, taille_sprite, taille_sprite)
                    collision = False
                    if (rec_perso.y <= resy - taille_sprite):
                        for rec in iter(obstacles):
                            if (rec_perso.x == rec.x) and (rec_perso.y == rec.y):
                                collision = True
                                
                        if not collision:
                            pos_perso = posx,posy + taille_sprite
                          
                elif event.key == pygame.K_LEFT:
                    direc = "left"
                    posx,posy = pos_perso
                    rec_perso = pygame.Rect(posx - taille_sprite, posy, taille_sprite, taille_sprite)
                    collision = False
                    if rec_perso.x  >= 0:
                        for rec in iter(obstacles):
                            if (rec_perso.x == rec.x) and (rec_perso.y == rec.y):
                                collision = True
                        if not collision:
                            pos_perso = posx - taille_sprite,posy
                             
                elif event.key == pygame.K_RIGHT:
                    direc = "right"
                    posx,posy = pos_perso
                    rec_perso = pygame.Rect(posx + taille_sprite , posy, taille_sprite, taille_sprite)
                    collision = False
                    if (rec_perso.x <= resy - taille_sprite):
                        for rec in iter(obstacles):
                            if (rec_perso.x == rec.x) and (rec_perso.y == rec.y):
                                collision = True
                       
                        if not collision:
                            pos_perso = posx + taille_sprite,posy
         
        #affichage du perso selon la touche de direction
        if(direc == "right"):
            fenetre.blit(images_dk["img_dk_droite"],pos_perso)
        elif direc == "left":
            fenetre.blit(images_dk["img_dk_gauche"],pos_perso)
        elif direc == "down":
            fenetre.blit(images_dk["img_dk_bas"],pos_perso)
        elif direc == "up":
            fenetre.blit(images_dk["img_dk_haut"],pos_perso)

        #affichage du labyrinhe
        # on inverse les positions de i et j car l'incrémentation est successive
        #c'est a dire que lorsque on parcour un dictionnaire avec la boucle for  il increment dabord
        #la premiere cle avant la seconde
        
        for (i,j) in iter(grille):
            if grille[i,j] == 'd':
                fenetre.blit(img_depart,[j * taille_sprite, i * taille_sprite])
                rec = pygame.Rect(j * taille_sprite, i * taille_sprite,30,30)
                obstacles.append(rec)
            elif grille[i,j] == 'm':
                fenetre.blit(img_mur,[j * taille_sprite, i * taille_sprite])
                rec = pygame.Rect(j * taille_sprite, i * taille_sprite,30,30)
                obstacles.append(rec)
            elif grille[i,j] == '0':
                rec = pygame.Rect(j * taille_sprite, i * taille_sprite,30,30)
                cases_libres.append(rec)
                 
            elif grille[i,j] == "a":
                fenetre.blit(img_arrivee,[j * taille_sprite, i * taille_sprite])
                
        posx,posy = pos_perso

        #On gere la velocite :  DK doit tombe si il n'est pas sur un block 
        for libre in iter(cases_libres):
            if (posy + taille_sprite == libre.y) and (posx == libre.x):
                tombe = True
        if tombe:
            clock.tick(15)
            pos_perso = posx,posy + 30
               
         
        if (posx == (resx - taille_sprite)) and (posy == (resy - taille_sprite)):
            lancer_jeu = False
            lancer_menu = True
            musique1.play()
            musique2.stop()
            pygame.display.set_mode([450,450])
    
        pygame.display.flip()
        
    pygame.display.flip()
    
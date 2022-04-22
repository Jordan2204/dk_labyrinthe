#-*-coding:utf-8
'''
Created on 10 sept. 2019

@author: JORDAN
'''

class Niveau():
    '''
    Cette classe permet de d�finir la structure du labyrinthe
    '''


    def __init__(self, structure):
        '''
        Constructor
        '''
        self.structure = structure
        self.grille = {}
    
    def transform_grille(self):
        """Cette methode transforme une chaine recu en un tableau a deux dimension
        
        """
        i = 0
        j = -1
        for lettre in self.structure:
            if lettre == '\n':
                i +=1
                j = -1
            else :
                j +=1
                self.grille[i,j] = lettre
            
              
        return self.grille
    
    #def affiche_niveau(self,grille,structure):
        
        
class Perso():
    '''
    Classe qui gere le personnage
    '''


    def __init__(self, grille,obstacle,arrivee,perso_lab):
        '''
            
        '''
        self.grille = grille
        self.obstacle = obstacle
        self.arrivee = arrivee
        self.perso_lab = perso_lab
        self.libre = '0'
    
   
    def trouve_pos(self):
        """On va determiné la position de notre robot.
        """
        #On recupere la position x et y du robot
        posx,posy = 0,0
        for i,j in iter(self.grille):
            if self.grille[i,j] == self.perso_lab:
                posx,posy = i,j
                pos_perso_lab = posx,posy
        return pos_perso_lab
    
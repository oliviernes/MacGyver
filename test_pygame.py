#! /usr/bin/env python3
# coding: utf-8

import pygame
from pygame.locals import *

pygame.init()

# Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((750, 750))

# Chargement et collage du fond
fond = pygame.image.load("sources/images/fond.jpg").convert()
fenetre.blit(fond, (0, 0))

# Chargement et collage du personnage
perso = pygame.image.load("sources/images/DK.png").convert_alpha()
position_perso = perso.get_rect()
fenetre.blit(perso, position_perso)

# Rafraîchissement de l'écran
pygame.display.flip()

# BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():  # Attente des événements

        if event.type == QUIT:
            continuer = 0

        # Down
        if event.type == KEYDOWN:
            if event.key == K_DOWN:

                position_perso = position_perso.move(0, 50)
        #
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                position_perso = position_perso.move(-50, 0)
        #
        if event.type == KEYDOWN:
            if event.key == K_UP:
                position_perso = position_perso.move(0, -50)
        #
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                position_perso = position_perso.move(50, 0)

    # Re-collage
    fenetre.blit(fond, (0, 0))
    fenetre.blit(perso, position_perso)

    # Rafraichissement
    pygame.display.flip()

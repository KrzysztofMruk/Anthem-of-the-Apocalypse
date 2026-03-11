import pygame, os, sys, random
from core import CONST as cst
from core.CONST import ButtonCONST as BC



#Powierzchnie przycisków
textures = {}
for img in os.listdir("../AOA/img"):
    texture = pygame.image.load("img/" + img)
    textures[img.replace(".png", "")] = texture

class ButtonSurfaces():

    #Przyciski menu
    mbs = BC.MENU_BUTTON_SIZE
    button_menu_surface = textures['red_button']
    button_menu_surface = pygame.transform.scale(button_menu_surface, mbs)
    button_menu_change_surface = textures['white_button']
    button_menu_change_surface = pygame.transform.scale(button_menu_change_surface, mbs)


    #Przycyski w pliku settings.py
    sbs = BC.SETTINGS_BUTTON_SIZE
    button_settings_surface = textures['red_button']
    button_settings_surface = pygame.transform.scale(button_settings_surface, sbs)
    button_change_settings_surface = textures['white_button']
    button_change_settings_surface = pygame.transform.scale(button_change_settings_surface, sbs)


    # Przycyski w pliku game.py
    sabs = BC.SAFE_BUTTON_SIZE
    button_safe_surface = textures['sejf_czerwony']
    button_safe_surface = pygame.transform.scale(button_safe_surface, sabs)
    button_safe_change_surface = textures['sejf_czerwony_c']
    button_safe_change_surface = pygame.transform.scale(button_safe_change_surface, sabs)

    button_EWO_1_surface = textures['EWO1']
    button_EWO_1_surface = pygame.transform.scale(button_EWO_1_surface, sabs)
    button_EWO_1_change_surface = textures['EWO1c']
    button_EWO_1_change_surface = pygame.transform.scale(button_EWO_1_change_surface, sabs)

    button_EWO_2_surface = textures['EWO2']
    button_EWO_2_surface = pygame.transform.scale(button_EWO_2_surface, sabs)
    button_EWO_2_change_surface = textures['EWO2c']
    button_EWO_2_change_surface = pygame.transform.scale(button_EWO_2_change_surface, sabs)

    ccbs = BC.CC_BUTTON_SIZE #valve button
    button_cc_surface = textures['valve']
    button_cc_surface = pygame.transform.scale(button_cc_surface, ccbs)
    button_cc_change_surface = textures['valve_c']
    button_cc_change_surface = pygame.transform.scale(button_cc_change_surface, ccbs)
    button_cc_true_surface = textures['valveT']
    button_cc_true_surface = pygame.transform.scale(button_cc_true_surface, ccbs)

    nks = BC.NUKE_KEY_SIZE
    button_nuke_key_surface = textures['klucz1']
    button_nuke_key_surface = pygame.transform.scale(button_nuke_key_surface, nks)
    button_nuke_key_change_surface = textures['klucz2']
    button_nuke_key_change_surface = pygame.transform.scale(button_nuke_key_change_surface, nks)

    #przyciski w pliku EWO.py
    abs = BC.ARROW_BUTTON_SIZE
    button_arrow_left_surface = textures['arrowL']
    button_arrow_left_surface = pygame.transform.scale(button_arrow_left_surface, abs)
    button_arrow_left_change_surface = textures['arrowLc']
    button_arrow_left_change_surface = pygame.transform.scale(button_arrow_left_change_surface, abs)

    button_arrow_right_surface = textures['arrowR']
    button_arrow_right_surface = pygame.transform.scale(button_arrow_right_surface, abs)
    button_arrow_right_change_surface = textures['arrowRc']
    button_arrow_right_change_surface = pygame.transform.scale(button_arrow_right_change_surface, abs)



class StaticImageSurface():

   #static image w pliku game.py
   llis =  BC.LAUNCH_LIGHT_IMAGE_SIZE # kontrolki gotowości do startu
   launch_disable_light_image_surface = textures['launch_disable']
   launch_disable_light_image_surface = pygame.transform.scale(launch_disable_light_image_surface, llis)

   launch_enable_light_image_surface = textures['launch_enable']
   launch_enable_light_image_surface = pygame.transform.scale(launch_enable_light_image_surface, llis)

   # static image w pliku safe.py
   cis = BC.COVER_IMAGE_SIZE # koperty
   cover_image_surface = textures['cover']
   cover_image_surface = pygame.transform.scale(cover_image_surface, cis)

   cois = BC.COOKIE_IMAGE_SIZE
   cookie_image_surface = textures['cookie']
   cookie_image_surface = pygame.transform.scale(cookie_image_surface, cois)

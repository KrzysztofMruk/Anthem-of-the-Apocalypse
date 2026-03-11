import pygame.font, json, zoneinfo
from datetime import datetime, timezone
from core import database as db


#połączenie z bazą danych
conn = db.create_connection('../baseAOA.db')


#sprawdzanie, czy ma być fullscreen
def screen():
    global SCREEN, SCREEN_MODE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_SIZE, HALF_SCREEN #, EWO_CARD_SIZE, CC_CARD_SIZE
    #dbScreenSize = db.get_screen_size(conn)
    #print(dbScreenSize[0][0], dbScreenSize[0][1])

    # właściwości ekranu
    with open('core/json/screen_parameters.json', 'r') as plik_screen_parameters:
        screen_parameters = json.load(plik_screen_parameters)

        for screen in screen_parameters['screen']:
            if screen['id'] == 0:
                SCREEN_WIDTH = screen['width']  # 1280
                SCREEN_HEIGHT = screen['height']  # 720
                SCREEN_MODE_B = screen['mode']  # 0
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    #EWO_CARD_SIZE = (SCREEN_WIDTH/2, SCREEN_HEIGHT)
    #CC_CARD_SIZE = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.75)

    if (SCREEN_MODE_B == 1):
        SCREEN_MODE = "Fullscreen"
        SCREEN = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
    else:
        SCREEN_MODE = "Window"
        SCREEN = pygame.display.set_mode((SCREEN_SIZE),pygame.RESIZABLE)

    HALF_SCREEN = pygame.display.set_mode((SCREEN_SIZE), pygame.RESIZABLE)


def music_and_sounds():
    global MASTER_MUSIC_VOLUME

    with open('../AOA/core/json/music_and_sound_volume.json', 'r') as plik_volume:
        volume = json.load(plik_volume)
        for music in volume['music']:
            if music['name'] == 'master':
                MASTER_MUSIC_VOLUME = (music['volume'])
                print(MASTER_MUSIC_VOLUME)

def get_current_date():
        local_timezone = datetime.now().astimezone().tzinfo  # Pobranie lokalnej strefy czasowej
        return datetime.now(local_timezone)

class ButtonCONST(): #klasa odpowiedzialna za parametry buttona
    #def __init__(self):
    #    screen()
    #    self.MENU_BUTTON_SIZE = ((SCREEN_WIDTH / 6), (SCREEN_HEIGHT / 12))
#
    #    self.MENU_BUTTON_FONT = "cambria"
#
    #    self.MENU_BUTTON_FONT_SIZE = round(SCREEN_HEIGHT / 40)
#
    #    self.SETTINGS_BUTTON_SIZE = ((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 12))
#
    #    self.SAFE_BUTTON_SIZE = ((SCREEN_WIDTH / 8), (SCREEN_WIDTH / 8))
#
    #    self.ARROW_BUTTON_SIZE = ((SCREEN_WIDTH / 16), (SCREEN_HEIGHT / 16))
#
    #    self.LAUNCH_LIGHT_IMAGE_SIZE = ((SCREEN_WIDTH / 12), (SCREEN_WIDTH / 14))
#
    #    self.CC_BUTTON_SIZE = ((SCREEN_WIDTH / 8), (SCREEN_HEIGHT/ 8))
#
    #    self.COVER_IMAGE_SIZE = ((SCREEN_WIDTH / 12), (SCREEN_HEIGHT/ 4))
#
    #    self.COOKIE_IMAGE_SIZE = self.COVER_IMAGE_SIZE
#
    #    self.EWO_CARD_SIZE = (SCREEN_WIDTH/2, SCREEN_HEIGHT)
#
    #    self.CC_CARD_SIZE = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.75)
#
    #    self.NUKE_KEY_SIZE = ((SCREEN_WIDTH / 14), (SCREEN_WIDTH / 14))
    screen()
    MENU_BUTTON_SIZE = ((SCREEN_WIDTH / 6), (SCREEN_HEIGHT / 12))

    MENU_BUTTON_FONT = "cambria"

    MENU_BUTTON_FONT_SIZE = round(SCREEN_HEIGHT / 40)

    SETTINGS_BUTTON_SIZE = ((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 12))

    SAFE_BUTTON_SIZE = ((SCREEN_WIDTH / 8), (SCREEN_WIDTH / 8))

    ARROW_BUTTON_SIZE = ((SCREEN_WIDTH / 16), (SCREEN_HEIGHT / 16))

    LAUNCH_LIGHT_IMAGE_SIZE = ((SCREEN_WIDTH / 12), (SCREEN_WIDTH / 14))

    CC_BUTTON_SIZE = ((SCREEN_WIDTH / 8), (SCREEN_HEIGHT/ 8))

    COVER_IMAGE_SIZE = ((SCREEN_WIDTH / 12), (SCREEN_HEIGHT/ 4))

    COOKIE_IMAGE_SIZE = COVER_IMAGE_SIZE

    EWO_CARD_SIZE = (SCREEN_WIDTH/2, SCREEN_HEIGHT)

    CC_CARD_SIZE = (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.75)

    NUKE_KEY_SIZE = ((SCREEN_WIDTH / 14), (SCREEN_WIDTH / 14))

screen()
music_and_sounds()
#limit k/s
FRAMERATE = 60

#główna czcionka
MAIN_FONT = "arial"



#kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)




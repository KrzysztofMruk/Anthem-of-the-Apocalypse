import pygame, sys, os
from core import buttons as bt, CONST as cst
from ui import main as mn, settings as sett
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.surfaces import ButtonSurfaces as BS
from core.surfaces import StaticImageSurface as SIS


class EscMenu:
    def __init__(self, mainPY, textures, previousScreen):
        self.mainPY = mainPY

        self.screen = cst.SCREEN
        self.screen_width = cst.SCREEN_WIDTH
        self.screen_height = cst.SCREEN_HEIGHT
        self.textures = textures

        self.MUSIC_END = pygame.USEREVENT + 1  # Ustawienie eventu dla końca muzyki
        pygame.mixer.music.set_endevent(self.MUSIC_END)  # Konfiguracja nasłuchiwania zakończenia utworu

        self.previous_screen = previousScreen
        self.background_image()

        self.main_esc_menu()

    def main_esc_menu(self):
        while True:
            self.fbuttons()

            self.background_image()
            bt.Button_one.bgChangeButton(self,self.buttons_menu)

            self.check_events()
            pygame.display.update()
    def fbuttons(self):
        #Przyciski na tej stronie.


        bms = BS.button_menu_surface
        bmcs = BS.button_menu_change_surface

        self.buttons_menu = [
            bt.Button_one(bms, bmcs, (self.screen_width / 2), (self.screen_height * 0.2), "Settings", 0, self.screen),
            bt.Button_one(bms, bmcs, (self.screen_width / 2), (self.screen_height * 0.4), "Back to Main Menu", 1, self.screen),
            bt.Button_one(bms, bmcs, (self.screen_width / 2), (self.screen_height * 0.6), "Back to Game", 2, self.screen),
        ]
    def background_image(self): #ustawnienie tła
        background_image = self.textures['esc_menu_background']
        background_image = pygame.transform.scale(background_image, cst.SCREEN_SIZE)
        self.screen.blit(background_image, (0, 0))


    def check_events(self): #sprawdzanie wydarzeń
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EscMenu.close(self)
            elif event.type == self.MUSIC_END:  # MUSIC_END
                mn.Main.next_track(self.mainPY)  # Przejście do kolejnego utworu ALLELUJA

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Przechodzę do poprzedniej strony.")
                    self.previous_screen()
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons_menu:
                    if button.checkForInput(mouse_pos):
                        if button.id == 0: #przejście do ustawień
                            self.start_settings()
                        elif button.id == 1: #powrót do strony głównej
                            mn.start_main()
                        elif button.id == 2: #przejście do strony, z której menu wywołano
                            print("Wracam do rozgrywki.")
                            self.previous_screen()
                            #return False
    def show_main_esc(self): #funkcja odpowiedająca za możliwość powrotu do tej strony, jest przerzucana jako zmienna previousScreen
        self.screen.fill((255, 255, 255))
        pygame.display.update()
        esc_menu = EscMenu(self.screen, self.textures, self.previous_screen)
        EscMenu(esc_menu.screen, esc_menu.textures, esc_menu.previous_screen)

    def start_settings(self): #funkcja odpowiadająca za przejście do pliku settings
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        sett.Settings(self.mainPY, self.textures, self.show_main_esc)

    def close(self): #koniec programu
        pygame.quit()
        sys.exit(0)
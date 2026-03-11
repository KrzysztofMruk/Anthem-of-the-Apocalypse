import pygame, sys, json,os
from core import buttons as bt, CONST as cst, database as db
from ui import main as mn
# Dodaj ścieżkę do katalogu nadrzędnego
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.surfaces import ButtonSurfaces as BS

class Settings:

    def __init__(self,mainPY, textures, previousScreen):
        self.msc_snd_vol_path = '../AOA/core//json/music_and_sound_volume.json' #ścieżka do pliku z ustawiniami dźwięku
        self.scrn_par_path = '../AOA/core/json/screen_parameters.json' #ścieżka do pliku z ustawiniami ekranu
        self.mainPY = mainPY #zaimportowana klasa Main()

        self.screen = cst.SCREEN
        self.textures = textures
        self.previous_screen = previousScreen


        self.master_volume = cst.MASTER_MUSIC_VOLUME
        self.MUSIC_END = pygame.USEREVENT + 1  # Ustawienie eventu dla końca muzyki
        pygame.mixer.music.set_endevent(self.MUSIC_END)  # Konfiguracja nasłuchiwania zakończenia utworu


        self.screen_mode = cst.SCREEN_MODE
        self.screen_width = cst.SCREEN_WIDTH
        self.screen_height = cst.SCREEN_HEIGHT

        self.background_image()

        self.main_settings()

    def main_settings(self):
        while True:
            self.fbuttons()
            self.background_image()

            bt.Button_one.bgChangeButton(self,self.buttons_menu)
            #for button in self.buttons_menu:
            #    button.changeButton(pygame.mouse.get_pos())  # Zmiana wyglądu przycisku po najechaniu na niego
            #    button.update()

            pygame.display.update()
            self.check_events()

    def background_image(self):
        #Wyświetlanie tła.
        background_image = self.textures['settings']
        background_image = pygame.transform.scale(background_image, cst.SCREEN_SIZE)
        self.screen.blit(background_image, (0, 0))

    def fbuttons(self):
        #Przyciski na tej stronie.

        bms = BS.button_menu_surface
        bmcs = BS.button_menu_change_surface

        bss = BS.button_settings_surface
        bcss = BS.button_change_settings_surface

        self.buttons_menu = [
            bt.Button_one(bms, bmcs, (self.screen_width / 11), (self.screen_height * 0.9), "Back", 0, self.screen),
            bt.Button_one(bss, bcss, (self.screen_width / 3) * 2, (self.screen_height / 3), f"Window size: {self.screen_width}x{self.screen_height}px" , 1, self.screen),
            bt.Button_one(bss, bcss, (self.screen_width / 3), (self.screen_height / 3), f"Screen type: {self.screen_mode}" , 2, self.screen),
            bt.Button_one(bss, bcss, (self.screen_width / 3), (self.screen_height / 3) * 1.4, f"Volume: {int(self.master_volume*100)}%" , 3, self.screen)
        ]

    def check_events(self):
        #Sprawdzanie wydarzeń.
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
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
                        if button.id == 0:
                            print("Przechodzę do poprzedniej strony.")
                            self.previous_screen()
                            return False

                        if button.id == 1:  # zmiana wielkości okna
                            if (self.screen_width == 800 and self.screen_height == 600):
                                self.screen_width = 1024
                                self.screen_height = 768

                            elif (self.screen_width == 1024 and self.screen_height == 768):
                                self.screen_width = 1280
                                self.screen_height = 720

                            elif (self.screen_width == 1280 and self.screen_height == 720):
                                self.screen_width = 1920
                                self.screen_height = 1080

                            elif (self.screen_width == 1920 and self.screen_height == 1080):
                                self.screen_width = 800
                                self.screen_height = 600


                            with open(self.scrn_par_path, 'r') as plik_screen_parameters:
                                screen_parameters = json.load(plik_screen_parameters)
                                # Modyfikacja odpowiedniego wpisu
                                for screen in screen_parameters['screen']:
                                    if screen['id'] == 0:
                                        screen['width'] = self.screen_width
                                        screen['height'] = self.screen_height

                            with open('../AOA/core/json/screen_parameters.json', 'w') as plik_screen_parameters:
                                json.dump(screen_parameters, plik_screen_parameters, indent=4)
                            cst.screen()

                        if button.id == 2:  # zmiana trybu pełnoekranowego
                            if self.screen_mode == "Window":
                                self.screen_mode = "Fullscreen"
                                self.screen_mode_b = 1
                                pygame.display.toggle_fullscreen()

                            elif self.screen_mode == "Fullscreen":
                                self.screen_mode = "Window"
                                self.screen_mode_b = 0
                                pygame.display.toggle_fullscreen()

                            with open(self.scrn_par_path, 'r') as plik_screen_parameters:
                                screen_parameters = json.load(plik_screen_parameters)
                                # Modyfikacja odpowiedniego wpisu
                                for screen in screen_parameters['screen']:
                                    if screen['id'] == 0:
                                        screen['mode'] = self.screen_mode_b
                            with open(self.scrn_par_path, 'w') as plik_screen_parameters:
                                json.dump(screen_parameters, plik_screen_parameters, indent=4)

                            cst.screen()

                        if button.id == 3:  # zmiana poziomu głośności
                            if self.master_volume < 1.0:
                                self.master_volume = round(self.master_volume + 0.1, 2)
                                if self.master_volume == 1.0:
                                    self.master_volume = 1
                            elif self.master_volume == 1.0:
                                self.master_volume = 0

                            # Odczyt danych z pliku JSON
                            with open(self.msc_snd_vol_path, 'r') as plik_volume:
                                volume = json.load(plik_volume)

                                # Modyfikacja odpowiedniego wpisu
                                for music in volume['music']:
                                    if music['name'] == 'master':
                                        music['volume'] = self.master_volume

                            # Zapis danych do pliku JSON
                            with open(self.msc_snd_vol_path, 'w') as plik_volume:
                                json.dump(volume, plik_volume, indent=4)

                            cst.music_and_sounds()
                            pygame.mixer.music.set_volume(cst.MASTER_MUSIC_VOLUME)  # ustawienie poziomu głośności

        return True

    def close(self):
        pygame.quit()
        sys.exit(0)

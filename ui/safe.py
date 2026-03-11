import pygame, os, sys, random,json, pygame_gui, string
from core import buttons as bt, CONST as cst
from ui import main as mn, game as gm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.surfaces import ButtonSurfaces as BS
from core.surfaces import StaticImageSurface as SIS
from core.CONST import ButtonCONST as BC
class Safe():
    def __init__(self, mainPY, textures, previousScreen):
        self.mainPY = mainPY
        self.screen = cst.HALF_SCREEN  # Ustawienie ekranu gry
        self.screen_width = cst.SCREEN_WIDTH/2  # Szerokość ekranu
        self.screen_height = cst.SCREEN_HEIGHT/2   # Wysokość ekranu

        self.textures = textures  # Ładowanie tekstur

        self.master_volume = cst.MASTER_MUSIC_VOLUME  # Ustawienie głośności

        self.MUSIC_END = pygame.USEREVENT + 1  # Event zakończenia muzyki
        pygame.mixer.music.set_endevent(self.MUSIC_END)  # Konfiguracja nasłuchiwania zakończenia utworu

        self.MaK_path = '../AOA/core/json/messages_and_keys.json'
        self.cover_pressed = 5
        self.read_MaK_file()
        self.draw_mess()

        self.previous_screen = previousScreen  # Poprzedni ekran
        self.background_name = 'blueAFN'
        self.background_image(self.background_name)  # Ustawienie
        self.main()  # Uruchomienie głównej pętli gry

    def main(self):
        # Główna pętla gry
        while True:
            self.read_MaK_file()
            self.fbuttons()  # Wywołanie funkcji static images
            self.background_image(self.background_name)  # Ustawienie tła
            bt.Button_one.bgChangeButton(self, self.buttons) # rysowanie static image
            self.check_events()  # Sprawdzanie wydarzeń
            pygame.display.update()  # Aktualizacja wyświetlacza

    def background_image(self,bg): #ustawianie tła strony
        background_image = self.textures[bg]
        background_image = pygame.transform.scale(background_image, BC.CC_CARD_SIZE)
        screen_X_position = self.screen_width*0.25
        screen_Y_position = self.screen_height*0.25
        self.screen.blit(background_image, (screen_X_position, screen_Y_position))

    def read_MaK_file(self): # czytanie z pliku messages_and_keys
        with open(self.MaK_path, 'r') as plik_mess_and_keys:
            mess_and_keys_parameters = json.load(plik_mess_and_keys)
            for message in mess_and_keys_parameters['messages']:
                if message ['id'] == 0:
                    self.true_message_OP1 = message['value']
                elif message ['id'] == 1:
                    self.true_message_OP2 = message['value']
            for state in mess_and_keys_parameters['variables_states']:
                if state['id'] == 1:
                    self.is_save_code_true = state['value']

    def draw_mess(self):
        alfabetUP = string.ascii_uppercase  # pobieranie alfabetu
        true_mess_place = random.randint(0, 4)
        #tworzenie ciagów wartości umieszczanych na obu stronach kopert
        self.code2 = [[] for _ in range(5)]
        self.code5 = [[] for _ in range(7)]

        if self.true_message_OP1 == self.true_message_OP2:
            for l in range(5):
                if l == true_mess_place:
                    for i in range(7):
                        if i < 2:
                            self.code2[l].append(self.true_message_OP1[i])
                        elif i > 1:
                            self.code5[l].append(self.true_message_OP1[i])
                        print(self.code2[l], self.code5[l])
                else:
                    for i in range(7):
                        letter = random.randint(0, 25)
                        if i < 2:
                            self.code2[l].append(alfabetUP[letter])
                        elif i > 1:
                            self.code5[l].append(alfabetUP[letter])
                    print(self.code2[l], self.code5[l])
        else:
            for l in range(5):
                for i in range(7):
                    letter = random.randint(0, 25)
                    if i < 2:
                        self.code2[l].append(alfabetUP[letter])
                        self.code5[l].append(alfabetUP[letter])
                    elif i > 1:
                        self.code5[l].append(alfabetUP[letter])
                print(self.code2[l], self.code5[l])
        #zmiana tablic na wyświetlane stringi
        self.code2_string = [''.join(sublist) for sublist in self.code2]
        self.code5_string = [''.join(sublist) for sublist in self.code5]

    def fbuttons(self): # buttony kopert
        cis = SIS.cover_image_surface
        cois = SIS.cookie_image_surface
        # zmieniamy obrazek koperty, jeśli użytkownik naciśnie na daną kopertę
        if self.cover_pressed == 5:
            self.buttons = [
                bt.Button_one(cis, cis, (self.screen_width / 6 * 3), (self.screen_height * 1.25), f"{self.code2_string[0]}", 0, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 4.5), (self.screen_height * 1.25), f"{self.code2_string[1]}", 1, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 6), (self.screen_height * 1.25), f"{self.code2_string[2]}", 2, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 7.5), (self.screen_height * 1.25), f"{self.code2_string[3]}", 3, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 9), (self.screen_height * 1.25), f"{self.code2_string[4]}", 4, self.screen)
            ]
        elif self.cover_pressed == 0:
            self.buttons = [
                bt.Button_one(cois, cois, (self.screen_width / 6 * 3), (self.screen_height * 1.25), f"{self.code5_string[0]}", 0, self.screen), #zmieniany
                bt.Button_one(cis, cis, (self.screen_width / 6 * 4.5), (self.screen_height * 1.25), f"{self.code2_string[1]}", 1, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 6), (self.screen_height * 1.25), f"{self.code2_string[2]}", 2, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 7.5), (self.screen_height * 1.25),f"{self.code2_string[3]}", 3, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 9), (self.screen_height * 1.25),f"{self.code2_string[4]}", 4, self.screen)
            ]
        elif self.cover_pressed == 1:
            self.buttons = [
                bt.Button_one(cis, cis, (self.screen_width / 6 * 3), (self.screen_height * 1.25),f"{self.code2_string[0]}", 0, self.screen),
                bt.Button_one(cois, cois, (self.screen_width / 6 * 4.5), (self.screen_height * 1.25), f"{self.code5_string[1]}", 1, self.screen), #zmieniany
                bt.Button_one(cis, cis, (self.screen_width / 6 * 6), (self.screen_height * 1.25), f"{self.code2_string[2]}", 2, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 7.5), (self.screen_height * 1.25), f"{self.code2_string[3]}", 3, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 9), (self.screen_height * 1.25), f"{self.code2_string[4]}", 4, self.screen)
            ]
        elif self.cover_pressed == 2:
            self.buttons = [
                bt.Button_one(cis, cis, (self.screen_width / 6 * 3), (self.screen_height * 1.25),f"{self.code2_string[0]}", 0, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 4.5), (self.screen_height * 1.25),f"{self.code2_string[1]}", 1, self.screen),
                bt.Button_one(cois, cois, (self.screen_width / 6 * 6), (self.screen_height * 1.25), f"{self.code5_string[2]}", 2, self.screen), #zmieniany
                bt.Button_one(cis, cis, (self.screen_width / 6 * 7.5), (self.screen_height * 1.25),f"{self.code2_string[3]}", 3, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 9), (self.screen_height * 1.25),f"{self.code2_string[4]}", 4, self.screen)
            ]
        elif self.cover_pressed == 3:
            self.buttons = [
                bt.Button_one(cis, cis, (self.screen_width / 6 * 3), (self.screen_height * 1.25), f"{self.code2_string[0]}", 0, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 4.5), (self.screen_height * 1.25), f"{self.code2_string[1]}", 1, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 6), (self.screen_height * 1.25), f"{self.code2_string[2]}", 2, self.screen),
                bt.Button_one(cois, cois, (self.screen_width / 6 * 7.5), (self.screen_height * 1.25), f"{self.code5_string[3]}", 3, self.screen), #zmieniany
                bt.Button_one(cis, cis, (self.screen_width / 6 * 9), (self.screen_height * 1.25), f"{self.code2_string[4]}", 4, self.screen)
            ]
        elif self.cover_pressed == 4:
            self.buttons = [
                bt.Button_one(cis, cis, (self.screen_width / 6 * 3), (self.screen_height * 1.25), f"{self.code2_string[0]}", 0, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 4.5), (self.screen_height * 1.25), f"{self.code2_string[1]}", 1, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 6), (self.screen_height * 1.25), f"{self.code2_string[2]}", 2, self.screen),
                bt.Button_one(cis, cis, (self.screen_width / 6 * 7.5), (self.screen_height * 1.25), f"{self.code2_string[3]}", 3, self.screen),
                bt.Button_one(cois, cois, (self.screen_width / 6 * 9), (self.screen_height * 1.25), f"{self.code5_string[4]}", 4, self.screen), #zmieniany
            ]
    def check_events(self):
        # Funkcja sprawdzająca wydarzenia
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Safe.close(self)  # Zakończenie gry
            elif event.type == self.MUSIC_END:
                mn.Main.next_track(self.mainPY)  # Przejście do kolejnego utworu ALLELUJA
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Przechodzę do poprzedniej strony.")
                    self.previous_screen()
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Sprawdzenie, czy kliknięcie jest poza ekranem
                if x < self.screen_width/4 or x > self.screen_width+(self.screen_width*0.75) or y < self.screen_height/4 or y > self.screen_height+(self.screen_height*0.75):
                    print("Kliknięcie poza ekranem!")
                    print("Przechodzę do poprzedniej strony.")
                    self.previous_screen()
                    return False
                else:
                    print("Kliknięcie wewnątrz ekranu.")
                    self.cover_pressed = 5
                for button in self.buttons:
                    if button.checkForInput(mouse_pos): #zmiana strony wyświetlanej koperty po naciśnięciu na nią
                        # koperty
                        if button.id == 0:
                            print(button.id)
                            self.cover_pressed = 0
                        if button.id == 1:
                            print(button.id)
                            self.cover_pressed = 1
                        if button.id == 2:
                            print(button.id)
                            self.cover_pressed = 2
                        if button.id == 3:
                            print(button.id)
                            self.cover_pressed = 3
                        if button.id == 4:
                            print(button.id)
                            self.cover_pressed = 4


    def close(self):
        # Funkcja kończąca grę
        pygame.quit()  # Wyjście z Pygame
        sys.exit(0)
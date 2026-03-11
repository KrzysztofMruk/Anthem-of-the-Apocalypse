import pygame, os, sys, random,json
from core import buttons as bt, CONST as cst
from ui import main as mn, game as gm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.surfaces import ButtonSurfaces as BS
from core.surfaces import StaticImageSurface as SIS
from core.CONST import ButtonCONST as BC

class Ewo():
    def __init__(self, mainPY, textures, previousScreen, operator):
        self.mainPY = mainPY
        self.operator = operator
        print(f"Operator set to: {self.operator}")  # Dodanie śledzenia wartości operator
        self.screen = cst.HALF_SCREEN  # Ustawienie ekranu gry
        self.screen_width = cst.SCREEN_WIDTH/2  # Szerokość ekranu
        self.screen_height = cst.SCREEN_HEIGHT  # Wysokość ekranu

        self.textures = textures  # Ładowanie tekstur

        self.master_volume = cst.MASTER_MUSIC_VOLUME  # Ustawienie głośności

        self.MUSIC_END = pygame.USEREVENT + 1  # Event zakończenia muzyki
        pygame.mixer.music.set_endevent(self.MUSIC_END)  # Konfiguracja nasłuchiwania zakończenia utworu

        self.MaK_path = '../AOA/core/json/messages_and_keys.json'
        self.x_keys_on_EWO = self.screen_width / 2

        self.fake_keys_generator()
        self.previous_screen = previousScreen  # Poprzedni ekran
        self.background_name = 'EWOcard1'
        self.background_image(self.background_name)  # Ustawienie
        self.main()  # Uruchomienie głównej pętli gry

    def main(self):
        # Główna pętla gry
        print(f"Operator set to: {self.operator}")  # Dodanie śledzenia wartości operator
        while True:
            self.fbuttons()  # Wywołanie funkcji przycisków
            self.background_image(self.background_name)  # Ustawienie tła

            bt.Button_one.bgChangeButton(self,self.arrow_buttons) #rysowanie strzałek

            self.current_date = cst.get_current_date()
            self.current_day = self.current_date.weekday()
            self.current_hour = self.current_date.hour

            self.check_events()  # Sprawdzanie wydarzeń
            if len(self.background_name) == 9:
                self.writing_keys(int('1' + self.background_name[8]))
            elif len(self.background_name) == 8:
                self.writing_keys(int(self.background_name[7]))
            pygame.display.update()  # Aktualizacja wyświetlacza

    def background_image(self,bg): #ustawianie tła strony
        background_image = self.textures[bg]
        background_image = pygame.transform.scale(background_image, BC.EWO_CARD_SIZE)
        if self.operator == "OP1":
            self.screen.blit(background_image,(0,0))
        elif self.operator == "OP2":
            self.screen.blit(background_image, (self.screen_width, 0))

    def fbuttons(self):
        # Funkcja odpowiedzialna za przyciski

        bals = BS.button_arrow_left_surface  # Powierzchnia przycisku strzałki w lewo
        balcs = BS.button_arrow_left_change_surface # Powierzchnia przycisku strzałki w lewo zmiana
        bars = BS.button_arrow_right_surface  # Powierzchnia przycisku strzałki w prawo
        barcs = BS.button_arrow_right_change_surface # Powierzchnia przycisku strzałki w prawo zmiana
        if self.operator == "OP1":
            self.arrow_l_x_pos = self.screen_width / 3
            self.arrow_R_x_pos = self.screen_width / 3 * 2
        elif self.operator == "OP2":
            self.arrow_l_x_pos = self.screen_width / 3 + self.screen_width
            self.arrow_R_x_pos = self.screen_width / 3 * 2 + self.screen_width

        # Przyciski w danych sytuacjach
        if self.background_name != 'EWOcard17' and self.background_name != 'EWOcard1': #na wszystkich stronach oprócz 1 i ostatniej
            self.arrow_buttons = [
                bt.Button_one(bals, balcs, (self.arrow_l_x_pos), (self.screen_height * 0.05), "", 0, self.screen),  # Utworzenie przycisku strzałki w lewo
                bt.Button_one(bars, barcs, (self.arrow_R_x_pos), (self.screen_height * 0.05), "", 1, self.screen),  # Utworzenie przycisku strzałki w prawo
            ]
        elif self.background_name == 'EWOcard1':    #na 1 stronie
            self.arrow_buttons = [
                bt.Button_one(bars, barcs, (self.arrow_R_x_pos), (self.screen_height * 0.05), "", 1, self.screen),  # Utworzenie przycisku strzałki w prawo
            ]
        elif self.background_name == 'EWOcard17':   #na ostatniej stronie
            self.arrow_buttons = [
                bt.Button_one(bals, balcs, (self.arrow_l_x_pos), (self.screen_height * 0.05), "", 0, self.screen),  # Utworzenie przycisku strzałki w lewo
            ]

    def writing_keys(self,numer_strony):
        self.read_MaK_file()
        if 8 <= numer_strony  <= 14: #wypisywanie kluczy na stronach ewo
            strona_dzien = numer_strony - 8
            print(numer_strony,"...",strona_dzien)
            if strona_dzien == self.current_day:
                if 4 <= self.current_hour < 12:
                    self.keysOP1[strona_dzien][0] = self.true_key_OP1
                    self.keysOP2[strona_dzien][0] = self.true_key_OP2
                elif 12 <= self.current_hour < 20:
                    self.keysOP1[strona_dzien][1] = self.true_key_OP1
                    self.keysOP2[strona_dzien][1] = self.true_key_OP2
                elif 20 <= self.current_hour or self.current_hour < 4:
                    self.keysOP1[strona_dzien][2] = self.true_key_OP1
                    self.keysOP2[strona_dzien][2] = self.true_key_OP2

            if self.operator == "OP1":

                key_half_length = len(self.keysOP1[strona_dzien][0]) // 2
                first_half_1 = ', '.join(str(digit) for digit in self.keysOP1[strona_dzien][0][:key_half_length])
                second_half_1 = ', '.join(str(digit) for digit in self.keysOP1[strona_dzien][0][key_half_length:])
                first_half_2 = ', '.join(str(digit) for digit in self.keysOP1[strona_dzien][1][:key_half_length])
                second_half_2 = ', '.join(str(digit) for digit in self.keysOP1[strona_dzien][1][key_half_length:])
                first_half_3 = ', '.join(str(digit) for digit in self.keysOP1[strona_dzien][2][:key_half_length])
                second_half_3 = ', '.join(str(digit) for digit in self.keysOP1[strona_dzien][2][key_half_length:])

                self.keys_on_EWO = [
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.3), f"Key for use from 4AM to 12PM",0, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.35), f"{first_half_1}", 1, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.39), f"{second_half_1}", 2, self.screen),# Wyświetl drugą połowę
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.44), f"Key for use from 12PM to 8PM",3, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.49), f"{first_half_2}", 4,self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.53), f"{second_half_2}", 5,self.screen),  # Wyświetl drugą połowę
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.58), f"Key for use from 8PM to 4AM",6, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.63), f"{first_half_3}", 7,self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.67), f"{second_half_3}", 8,self.screen),  # Wyświetl drugą połowę
                ]

            elif self.operator == "OP2":

                key_half_length = len(self.keysOP1[strona_dzien][0]) // 2
                first_half_1 = ', '.join(str(digit) for digit in self.keysOP2[strona_dzien][0][:key_half_length])
                second_half_1 = ', '.join(str(digit) for digit in self.keysOP2[strona_dzien][0][key_half_length:])
                first_half_2 = ', '.join(str(digit) for digit in self.keysOP2[strona_dzien][1][:key_half_length])
                second_half_2 = ', '.join(str(digit) for digit in self.keysOP2[strona_dzien][1][key_half_length:])
                first_half_3 = ', '.join(str(digit) for digit in self.keysOP2[strona_dzien][2][:key_half_length])
                second_half_3 = ', '.join(str(digit) for digit in self.keysOP2[strona_dzien][2][key_half_length:])

                self.keys_on_EWO = [
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.3), f"Key for use from 4AM to 12PM",0, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.35), f"{first_half_1}", 1, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.39), f"{second_half_1}", 2, self.screen),# Wyświetl drugą połowę
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.44), f"Key for use from 12PM to 8PM",3, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.49), f"{first_half_2}", 4,self.screen),
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.53), f"{second_half_2}", 5,self.screen),  # Wyświetl drugą połowę
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.58), f"Key for use from 8PM to 4AM",6, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.63), f"{first_half_3}", 7,self.screen),
                    bt.Static_writing(self.x_keys_on_EWO+self.screen_width, (self.screen_height * 0.67), f"{second_half_3}", 8,self.screen),  # Wyświetl drugą połowę
                ]

            bt.Static_writing.drawStaticWriting(self,self.keys_on_EWO)
        elif numer_strony == 15:    #wypisywanie safe codu każdego z operatorów w EWO
            if self.operator == "OP1":
                self.safe_code_on_EWO = [
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.3), f"{self.safe_code_OP1}",0, self.screen),
                ]
            elif self.operator == "OP2":
                self.safe_code_on_EWO = [
                    bt.Static_writing(self.x_keys_on_EWO + self.screen_width, (self.screen_height * 0.3),f"{self.safe_code_OP2}", 0, self.screen),
                ]
            bt.Static_writing.drawStaticWriting(self, self.safe_code_on_EWO)
        elif numer_strony == 17: #wypisywanie coded alphabetu w EWO
            coded_alphabet = self.coded_alphabet
            items = list(coded_alphabet.items())
            rozmiar_czesci = len(items) // 4
            # Dzielimy listę na cztery części
            czesc1 = dict(items[:rozmiar_czesci])
            czesc2 = dict(items[rozmiar_czesci:rozmiar_czesci * 2])
            czesc3 = dict(items[rozmiar_czesci * 2:rozmiar_czesci * 3])
            czesc4 = dict(items[rozmiar_czesci * 3:])

            #zamiana dict na stringi, by lepiej się to czytało na EWO
            czesc1 = ", ".join(f"{k}: {v}" for k, v in czesc1.items())
            czesc2 = ", ".join(f"{k}: {v}" for k, v in czesc2.items())
            czesc3 = ", ".join(f"{k}: {v}" for k, v in czesc3.items())
            czesc4 = ", ".join(f"{k}: {v}" for k, v in czesc4.items())

            # Wyświetlanie coded_alphabet w częściach
            if self.operator == "OP1":
                self.coded_alphabet_on_EWO = [
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.2), f"{czesc1}", 0, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.25), f"{czesc2}", 1, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.3), f"{czesc3}", 2, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO, (self.screen_height * 0.35), f"{czesc4}", 3, self.screen),
                ]
            elif self.operator == "OP2":
                self.coded_alphabet_on_EWO = [
                    bt.Static_writing(self.x_keys_on_EWO + self.screen_width, (self.screen_height * 0.2),f"{czesc1}", 0, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO + self.screen_width, (self.screen_height * 0.25), f"{czesc2}", 1, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO + self.screen_width, (self.screen_height * 0.3), f"{czesc3}", 2, self.screen),
                    bt.Static_writing(self.x_keys_on_EWO + self.screen_width, (self.screen_height * 0.35), f"{czesc4}", 3, self.screen),
                ]
            bt.Static_writing.drawStaticWriting(self, self.coded_alphabet_on_EWO)
                #print("Wartość jest poza zakresem.",numer_strony)


    def fake_keys_generator(self): #generowanie fałszywych kluczy
        for i in range(0,21):
            fake_keyOP1 = []
            fake_keyOP2 = []
            for l in range (0,34):
                fake_keyOP1.append(random.randint(0,26))
                fake_keyOP2.append(random.randint(0, 26))
            with open(self.MaK_path, 'r') as plik_mess_and_keys:
                mess_and_keys_parameters = json.load(plik_mess_and_keys)
                # Modyfikacja odpowiedniego wpisu
                for fake_key_in_file in mess_and_keys_parameters['fake_keysOP1']:
                    if fake_key_in_file['id'] == i:
                        fake_key_in_file['value'] = fake_keyOP1
                for fake_key_in_file in mess_and_keys_parameters['fake_keysOP2']:
                    if fake_key_in_file['id'] == i:
                        fake_key_in_file['value'] = fake_keyOP2

            with open('../AOA/core/json/messages_and_keys.json', 'w') as plik_mess_and_keys:
                json.dump(mess_and_keys_parameters, plik_mess_and_keys, indent=4)



    def read_MaK_file(self): # czytanie z pliku messages_and_keys
        with open(self.MaK_path, 'r') as plik_mess_and_keys:
            mess_and_keys_parameters = json.load(plik_mess_and_keys)
            for message in mess_and_keys_parameters['messages']:
                if message ['id'] == 0:
                    self.true_message_OP1 = message['value']
                elif message ['id'] == 1:
                    self.true_message_OP2 = message['value']
            for coded_message in mess_and_keys_parameters['coded_messages']:
                if coded_message ['id'] == 0:
                    self.coded_message_OP1 = coded_message['value']
                elif coded_message ['id'] == 1:
                    self.coded_message_OP2 = coded_message['value']
            for coded_alphabet in mess_and_keys_parameters['coded_alphabet']:
                if coded_alphabet ['id'] == 0:
                    self.coded_alphabet = coded_alphabet['value']
            for key in mess_and_keys_parameters['keys']:
                if key ['id'] == 0:
                    self.true_key_OP1 = key['value']
                elif key ['id'] == 1:
                    self.true_key_OP2 = key['value']
            for safe_code in mess_and_keys_parameters['safe_codes']:
                if safe_code ['id'] == 0:
                    self.safe_code_OP1 = safe_code['value']
                elif safe_code ['id'] == 1:
                    self.safe_code_OP2 = safe_code['value']

            self.keysOP1 = [[] for _ in range(7)]
            self.keysOP2 = [[] for _ in range(7)]
            # przypisywanie danych fake keysow do odpowiednich stron dni tygodnia
            for i in range(0, 21):
                for fake_keysOP1 in mess_and_keys_parameters['fake_keysOP1']:
                    if fake_keysOP1['id'] == i:
                        # Obliczamy indeks dla listy docelowej (0-6) na podstawie wartości i
                        target_index = i // 3
                        self.keysOP1[target_index].append(fake_keysOP1['value'])
                for fake_keysOP2 in mess_and_keys_parameters['fake_keysOP2']:
                    if fake_keysOP2['id'] == i:
                        # Obliczamy indeks dla listy docelowej (0-6) na podstawie wartości i
                        target_index = i // 3
                        self.keysOP2[target_index].append(fake_keysOP2['value'])

    def check_events(self):
        # Funkcja sprawdzająca wydarzenia
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ewo.close(self)  # Zakończenie gry
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
                if self.operator == "OP1":
                    if x < 0 or x > self.screen_width or y < 0 or y > self.screen_height:
                        print("Kliknięcie poza ekranem!")
                        print("Przechodzę do poprzedniej strony.")
                        self.previous_screen()
                        return False
                    else:
                        print("Kliknięcie wewnątrz ekranu.")
                elif self.operator == "OP2":
                    if x < 0 or x < self.screen_width or y < 0 or y > self.screen_height:
                        print("Kliknięcie poza ekranem!")
                        print("Przechodzę do poprzedniej strony.")
                        self.previous_screen()
                        return False
                    else:
                        print("Kliknięcie wewnątrz ekranu.")
                for button in self.arrow_buttons:
                    if button.checkForInput(mouse_pos):
                        #przechodzenie między stronami
                        if button.id == 0:  # lewa strzałka
                            if len(self.background_name) == 9 and self.background_name[8] != 0 and self.background_name != 'EWOcard10':
                                self.background_name = 'EWOcard1' + str(int(self.background_name[8]) - 1)
                                self.writing_keys(int('1'+self.background_name[8]))
                            elif len(self.background_name) == 8 and self.background_name[7] != 1:
                                self.background_name = 'EWOcard' + str(int(self.background_name[7]) - 1)
                                self.writing_keys(int(self.background_name[7]))
                            elif self.background_name == 'EWOcard10':
                                self.background_name = 'EWOcard9'
                                self.writing_keys(int(self.background_name[7]))
                            print(f"Przechodzę do {self.background_name}")
                        elif button.id == 1: # prawa strzałka
                            if len(self.background_name) == 9 and self.background_name[8] != 8:
                                self.background_name = 'EWOcard1' + str(int(self.background_name[8]) + 1)
                                self.writing_keys(int('1'+self.background_name[8]))
                            elif len(self.background_name) == 8  and self.background_name != 'EWOcard9':
                                self.background_name = 'EWOcard' + str(int(self.background_name[7]) + 1)
                                self.writing_keys(int(self.background_name[7]))
                            elif self.background_name == 'EWOcard9':
                                self.background_name = 'EWOcard10'
                                self.writing_keys(int(self.background_name[7]+'0'))
                            print(f"Przechodzę do {self.background_name}.")

    def close(self):
        # Funkcja kończąca grę
        pygame.quit()  # Wyjście z Pygame
        sys.exit(0)

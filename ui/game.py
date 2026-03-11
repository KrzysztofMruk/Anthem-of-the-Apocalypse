import pygame, os, sys,json
# Ustal katalog, w którym znajduje się plik .exe lub skrypt
if getattr(sys, 'frozen', False):  # Sprawdzenie, czy uruchamiasz plik .exe
    base_path = sys._MEIPASS  # Dla PyInstaller
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Dla skryptu

# Dodaj katalog `core` do ścieżki importów
core_path = os.path.join(base_path, '..', 'core')  # '..' przechodzi o jeden katalog wyżej
if core_path not in sys.path:
    sys.path.append(core_path)
from core import buttons as bt, CONST as cst, video_playing as vp
import esc_menu as esc
from ui import main as mn, EWO as ewo, code_confirmation as cc, safe_locks as sl, safe as s
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.surfaces import ButtonSurfaces as BS
from core.surfaces import StaticImageSurface as SIS

class Game():
    def __init__(self, mainPY, textures, previousScreen):
        self.mainPY = mainPY
        self.clock = pygame.time.Clock()

        self.load_sounds() # ładowanie dźwięku
        self.time_path = '../AOA/core/json/time.json'
        self.read_time_file()  # czytanie pliku z zmiennymi związanymi z czasem
        self.NUKE_ORDER_SOUND_END_EVENT = pygame.USEREVENT + 2  # Unikalne zdarzenie dla zakończenia dźwięku

        self.screen = cst.SCREEN  # Ustawienie ekranu gry
        self.screen_width = cst.SCREEN_WIDTH  # Szerokość ekranu
        self.screen_height = cst.SCREEN_HEIGHT  # Wysokość ekranu

        self.textures = textures  # Ładowanie tekstur

        self.master_volume = cst.MASTER_MUSIC_VOLUME  # Ustawienie głośności

        self.MUSIC_END = pygame.USEREVENT + 1  # Event zakończenia muzyki
        pygame.mixer.music.set_endevent(self.MUSIC_END)  # Konfiguracja nasłuchiwania zakończenia utworu

        self.previous_screen = previousScreen  # Poprzedni ekran

        self.MaK_path = '../AOA/core/json/messages_and_keys.json'
        self.win_conditions_path = "../AOA/core/json/win_conditions.json"

        self.background_name = 'war'
        self.background_image(self.background_name)  # Ustawienie tła

        #ustawianie statusu końca gry na brak końca
        self.isEnd = 0
        #ustawianie stanu przekręcenia kluczy atomowy na brak przekręcenia
        self.nuke_key_OP1_status = False
        self.nuke_key_OP2_status = False

        #ustawienia wstępnę dla komunikatów nuke
        self.nuke_order_sound_setting()
        self.main_game()  # Uruchomienie głównej pętli gry

    def main_game(self):
        # Główna pętla gry
        while True:
            self.read_MaK_file() #czytanie pliku z głównymi zmiennymi aktualnej gry
            self.read_time_file()

            self.fbuttons()  # Wywołanie funkcji przycisków
            self.static_images() # Wywołanie funkcji static images
            self.background_image(self.background_name)  # Ustawienie tła

            bt.Button_one.bgChangeButton(self, self.buttons_list)  # rysowanie przycisków
            bt.Static_image.drawStaticImage(self, self.static_images_list)  # rysowanie static image

            self.check_time_events()
            self.check_events()  # Sprawdzanie wydarzeń
            self.read_win_conditions_file()  # sprawdzanie czy się nie przegrało

            self.clock.tick(cst.FRAMERATE)
            pygame.display.update()  # Aktualizacja wyświetlacza

    def fbuttons(self):
        # Funkcja odpowiedzialna za przyciski


        bms = BS.button_menu_surface  # Powierzchnia przycisku menu
        bmcs = BS.button_menu_change_surface  # Powierzchnia przycisku zmiany menu

        bss = BS.button_safe_surface  # Powierzchnia przycisku sejfu
        bscs = BS.button_safe_change_surface # Powierzchnia przycisku sejfu naciśniętego

        ew1s = BS.button_EWO_1_surface # Powierzchnia przycisku EWO1
        ew1cs = BS.button_EWO_1_change_surface # Powierzchnia przycisku EWO1 naciśniętego

        ew2s = BS.button_EWO_2_surface # Powierzchnia przycisku EWO2
        ew2cs = BS.button_EWO_2_change_surface  # Powierzchnia przycisku EWO2 naciśniętego

        #powierzechnie dla valve buttona
        ccs = BS.button_cc_surface
        cccs = BS.button_cc_change_surface
        ccst = BS.button_cc_true_surface

        #ustawianie wyświetlanych obrazków kluczy atomowych w zależności od tego, czy je już przekręcono
        bnks = BS.button_nuke_key_surface
        if self.nuke_key_OP1_status == True:
            self.bnks1 = BS.button_nuke_key_change_surface
        else:
            self.bnks1 = BS.button_nuke_key_surface
        if self.nuke_key_OP2_status == True:
            self.bnks2 = BS.button_nuke_key_change_surface
        else:
            self.bnks2 = BS.button_nuke_key_surface

        # ustawienie wyświetlanie kluczy atomowych i innych butonów w zależności od potwierdzenia kodów w key_conifrmation
        if self.is_valve_code_true == True:
            self.buttons_list = [
                bt.Button_one(bss, bscs, (self.screen_width / 2), (self.screen_height * 0.2), "", 0, self.screen), # Utworzenie przycisku z użyciem wymiarów ekranu
                #EWO
                bt.Button_one(ew1s, ew1cs, (self.screen_width / 5), (self.screen_height * 0.4), "", 1, self.screen),
                bt.Button_one(ew2s, ew2cs, (self.screen_width / 5 * 4), (self.screen_height * 0.4), "", 2, self.screen),
                #valve
                bt.Button_one(ccst, ccst, (self.screen_width / 2), (self.screen_height * 0.4), "", 3, self.screen),
                #klucze
                bt.Button_one(self.bnks1, bnks, (self.screen_width / 5), (self.screen_height * 0.8), "", 4, self.screen),
                bt.Button_one(self.bnks2, bnks, (self.screen_width / 5 * 4), (self.screen_height * 0.8), "", 5, self.screen),
            ]

        else:
            self.buttons_list = [
                bt.Button_one(bss, bscs, (self.screen_width / 2), (self.screen_height * 0.2), "", 0, self.screen),  # Utworzenie przycisku z użyciem wymiarów ekranu
                # EWO
                bt.Button_one(ew1s, ew1cs, (self.screen_width / 5), (self.screen_height * 0.4), "", 1, self.screen),
                bt.Button_one(ew2s, ew2cs, (self.screen_width / 5 * 4), (self.screen_height * 0.4), "", 2, self.screen),
                # valve
                bt.Button_one(ccs, cccs, (self.screen_width / 2), (self.screen_height * 0.4), "", 3, self.screen),
            ]

    def static_images(self):
        ldlis = SIS.launch_disable_light_image_surface
        lelis = SIS.launch_enable_light_image_surface
        #ustawienie stanów lampek kontrolnych w zależności od potwierdzenia kodów w key_conifrmation
        if self.is_valve_code_true == True:
            self.static_images_list = [
                bt.Static_image(lelis, lelis, (self.screen_width / 5), (self.screen_height * 2 / 3), "", 0,self.screen),
                bt.Static_image(lelis, lelis, (self.screen_width / 5 * 4), (self.screen_height * 2 / 3), "", 1, self.screen)
            ]
        else:
            self.static_images_list = [
                bt.Static_image(ldlis,lelis, (self.screen_width / 5), (self.screen_height * 2 / 3), "", 0, self.screen),
                bt.Static_image(ldlis,lelis, (self.screen_width / 5 * 4), (self.screen_height * 2 / 3), "", 1, self.screen)
            ]

    def background_image(self,bg):
        # Funkcja ustawiająca tło
        background_image = self.textures[bg]  # Pobranie tekstury tła
        background_image = pygame.transform.scale(background_image, cst.SCREEN_SIZE)  # Skalowanie obrazu tła do rozmiaru ekranu
        self.screen.blit(background_image, (0, 0))  # Rysowanie obrazu tła na ekranie


    def nuke_order_sound_setting(self):
        # Użycie kanału dźwiękowego i ustawienie soundu dla alertu atomowego
        self.sound_keys_list = list(self.sounds.keys())
        #self.current_nuke_order_sound_index = 0
        if 0 <= self.current_nuke_order_sound_index < len(self.sound_keys_list):
            self.current_nuke_order_sound_key = self.sound_keys_list[self.current_nuke_order_sound_index]
        else:
            print("Index out of range!")
        #self.current_nuke_order_sound_key = self.sound_keys_list[self.current_nuke_order_sound_index]
        print(self.current_nuke_order_sound_key )
        self.nuke_order_sound_channel = pygame.mixer.Channel(1)  # Kanał 1
        self.NUKE_ORDER_SOUND_END_EVENT = pygame.USEREVENT + 2  # Unikalne zdarzenie dla zakończenia dźwięku
        self.nuke_order_sound_channel.set_endevent(self.NUKE_ORDER_SOUND_END_EVENT)
        # Lista nazw dźwięków do odtworzenia w kolejności
        self.nuke_order_sound_queue = ["op1Order", "op1Order", "op2Order", "op2Order"]  # Przykładowa kolejność odtwarzania

    def play_nuke_order(self):
        # Sprawdzenie, czy dźwięk jest w liście
        if self.current_nuke_order_sound_key in self.sounds:
            self.nuke_order_sound_channel.play(self.sounds[self.current_nuke_order_sound_key])
        else:
            print(f"Brak dźwięku o nazwie {self.current_nuke_order_sound_key}")
            print(self.sounds)

        # Zabezpieczenie, by dźwięk nie odtwarzał się wielokrotnie
        #self.attack_order_time = float('inf')

    def read_MaK_file(self): # czytanie z pliku messages_and_keys
        with open(self.MaK_path, 'r') as plik_mess_and_keys:
            mess_and_keys_parameters = json.load(plik_mess_and_keys)
            for message in mess_and_keys_parameters['messages']:
                if message ['id'] == 0:
                    self.true_message_OP1 = message['value']
                elif message ['id'] == 1:
                    self.true_message_OP2 = message['value']
            for state in mess_and_keys_parameters['variables_states']:
                if state['id'] == 0:
                    self.is_valve_code_true = state['value']
                if state["id"] == 1:
                    self.is_safe_code_true = state['value']
    def read_time_file(self):  # odczytanie do zmiennych z pliku mess_and_keys_parameters.json
        with open(self.time_path, 'r') as plik_time:
            time_parameters = json.load(plik_time)

            for order_time in time_parameters['attack_order_time']:
                if order_time['id'] == 0:  # odczytanie momentu rozpoczęcia komunikatu o ataku jądrowym
                    self.attack_order_time = order_time['value']
                if order_time['id'] == 1:   # czy wydano już rozkaz ataku
                    self.nuke_order_played = order_time['value']
                if order_time['id'] == 2:  # ile odtworzono do tej pory komunikatów z wiadomością
                    self.how_many_nuke_order_played = order_time['value']
                if order_time['id'] == 3:  # jaki jest index właśnie granego komunikatu
                    self.current_nuke_order_sound_index = order_time['value']
                if order_time['id'] == 4:  # jaki jest key właśnie granego komunikatu
                    self.current_nuke_order_sound_key = order_time['value']
    def read_win_conditions_file(self): # czytanie z pliku messages_and_keys
        with open(self.win_conditions_path, 'r') as plik_win_conditions:
            win_conditions = json.load(plik_win_conditions)
            for condition in win_conditions['number_of_nuke_keys_switched']:
                if condition ['id'] == 0:
                    number_of_nuke_keys_switched = condition['value']
                    if int(number_of_nuke_keys_switched) > 3:
                        pygame.mixer.music.stop()
                        print("Za dużo przekręceń kluczy")
                        vp.PlayVideo("video/AOA_lose_outro.mp4", 1.0)
                        self.isEnd = 1  # zmiana statusu końca gry na koniec
                        pygame.quit()
                        self.close()

            for condition in win_conditions['number_of_valve_code_entered']:
                if condition['id'] == 0:
                    number_of_valve_code_entered = condition['value']
                    if int(number_of_valve_code_entered) > 2:
                        pygame.mixer.music.stop()
                        print("Za dużo przekręceń próby z code confirmation/valve code")
                        vp.PlayVideo("video/AOA_lose_outro.mp4", 1.0)
                        self.isEnd = 1  # zmiana statusu końca gry na koniec
                        pygame.quit()
                        self.close()

    def load_sounds(self): #wpisywanie nazw plików dźwiękowych na listę, w celu ich późniejszego wykorzystania
        self.sounds = {}
        for sound in os.listdir("../AOA/sounds"):
            file = pygame.mixer.Sound("sounds/" + sound)
            self.sounds[sound.replace(".mp3", "")] = file

    def check_events(self):
        # Funkcja sprawdzająca wydarzenia
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.close(self)  # Zakończenie gry
            elif event.type == self.MUSIC_END:
                mn.Main.next_track(self.mainPY)  # Przejście do kolejnego utworu ALLELUJA
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:  # Przejście do menu pauzy
                    print(f"Przechodzę do esc_menu.")
                    self.start_esc_menu()

            # sprawdzanie czy użyto kombinacji klawiszy do przekręcenia kluczy atomowych
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p and pygame.K_m and  pygame.key.get_mods() & pygame.KMOD_LCTRL:  # Aktywacja klucza OP1
                    self.nuke_key_OP1_status = True
                    self.first_nuke_key_press_time = pygame.time.get_ticks()
                    print(self.first_nuke_key_press_time)
                    print(f"Przekręcono klucz operatora 1.")
                if event.key == pygame.K_KP_6 and pygame.key.get_mods() & pygame.KMOD_RCTRL:   # Aktywacja klucza OP2
                    self.nuke_key_OP2_status = True
                    self.second_nuke_key_press_time = pygame.time.get_ticks()
                    print(self.second_nuke_key_press_time)
                    print(f"Przekręcono klucz operatora 2.")

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons_list:
                    if button.checkForInput(mouse_pos):
                        if button.id == 0:  # Ustawienia
                            if self.is_safe_code_true == True:  # przejście do sejfu
                                print(f"Przechodzę do  sejfu")
                                self.start_safe()
                            elif  self.is_safe_code_true == False or self.is_safe_code_true == 3:  # przejście do blokady sejfu
                                print(f"Przechodzę do zamka sejfu")
                                self.start_safe_locks()
                        if button.id == 1:  # Przejście do EWO1
                            print(f"Przechodzę do EWO1.")
                            self.start_EWO1()
                        if button.id == 2:  # Przejście do EWO2
                            print(f"Przechodzę do EWO2.")
                            self.start_EWO2()
                        if button.id == 3:  # Przejście do code confirmation (czasem wspominany jako valve z powodu napisu na przycisku)
                            if self.is_valve_code_true == False or self.is_valve_code_true == 3: # sprawdzenie,czy kody nie zostały już wcześniej potwiedzone w key confirmation
                                print(f"Przechodzę do KC.")
                                self.start_key_confirmation()
                            else:  # jeśli zotały już wcześniej potwierdzone, komunikat
                                print("Kody już zaakceptowane")

            # Sprawdź, czy zakończył się odtwarzany dźwięk z sounds
            if pygame.time.get_ticks() >= (self.attack_order_time * 1000) and self.nuke_order_played and self.how_many_nuke_order_played < 3:
                if event.type == self.NUKE_ORDER_SOUND_END_EVENT:

                    # Przejście do kolejnego utworu w kolejce
                    self.how_many_nuke_order_played += 1
                    self.current_nuke_order_sound_index += 1
                    with open(self.time_path, 'r') as plik_time:
                        time_parameters = json.load(plik_time)
                        # Modyfikacja odpowiedniego wpisu
                        for order_time in time_parameters['attack_order_time']:
                            if order_time['id'] == 2:  # ile odtworzono do tej pory komunikatów z wiadomością
                                order_time['value'] = self.how_many_nuke_order_played
                            if order_time['id'] == 3:  # jaki jest index właśnie granego komunikatu
                                order_time['value'] = self.current_nuke_order_sound_index
                            if order_time['id'] == 4:  # jaki jest key właśnie granego komunikatu
                                order_time['value'] = self.current_nuke_order_sound_key

                    with open(self.time_path, 'w') as plik_time:
                        json.dump(time_parameters, plik_time, indent=4)

                    # zadabanie, by w wypadku przekroczenia długości kolejki odgrywano dźwięk z sounds od początku
                    if self.current_nuke_order_sound_index >= len(self.nuke_order_sound_queue):
                        self.current_nuke_order_sound_index = 0  # Zresetuj indeks na początek
                    self.current_nuke_order_sound_key = self.nuke_order_sound_queue[
                        self.current_nuke_order_sound_index]  # Zmieniamy klucz dźwięku z sounds
                    self.play_nuke_order()  # Odtwarzamy kolejny dźwięk z sounds

            #sprawdzenie, czy przekręcono oba klucze
            if self.nuke_key_OP1_status and self.nuke_key_OP2_status and self.isEnd == 0:
                if (0 < (self.second_nuke_key_press_time / 1000) - (self.first_nuke_key_press_time / 1000) <= 2) or (0 < (self.first_nuke_key_press_time / 1000) - (self.second_nuke_key_press_time / 1000) <= 2):
                    print("boom")  # sprawdzenie poprawności kodu
                    pygame.mixer.music.stop()
                    vp.PlayVideo("video/AOA_win_outro.mp4",1.0)
                    self.isEnd = 1  # zmiana statusu końca gry na koniec
                    pygame.quit()
                    self.close()
                else:
                    # zmiana obrazka klucza na ten nie przekręcony
                    self.bnks1 = BS.button_nuke_key_surface
                    self.bnks2 = BS.button_nuke_key_surface
                    # zmiana statusu kluczy na nieprzekreślone
                    self.nuke_key_OP1_status = False
                    self.nuke_key_OP2_status = False
                    with open(self.win_conditions_path, 'r') as plik_win_conditions:
                        win_conditions = json.load(plik_win_conditions)
                        # Modyfikacja odpowiedniego wpisu
                        for condition in win_conditions['number_of_nuke_keys_switched']:
                            if condition['id'] == 0:  # ile razy przekręcono klucze
                                condition['value'] = int(condition['value'])+1

                    with open(self.win_conditions_path, 'w') as plik_win_conditions:
                        json.dump(win_conditions, plik_win_conditions, indent=4)
                    self.isEnd = 0  # zmiana statusu końca gry na jego brak

    #sprawdzanie eventów związanych z czasem
    def check_time_events(self):
        if pygame.time.get_ticks() >= (self.attack_order_time * 1000) and not self.nuke_order_played:
            self.nuke_order_played = True
            with open(self.time_path, 'r') as plik_time:
                time_parameters = json.load(plik_time)
                # Modyfikacja odpowiedniego wpisu
                for order_time in time_parameters['attack_order_time']:
                    if order_time['id'] == 1:  # czy wydano już rozkaz ataku
                        order_time['value'] = self.nuke_order_played

            with open(self.time_path, 'w') as plik_time:
                json.dump(time_parameters, plik_time, indent=4)

            self.nuke_order_sound_setting()
            self.play_nuke_order()




    def show_main_game(self):
        # Funkcja odpowiedzialna za powrót do gry
        #self.screen.fill((255, 255, 255))  # Wypełnienie ekranu białym kolorem
        pygame.display.update()  # Aktualizacja wyświetlacza
        game = Game(self.mainPY,self.textures, self.previous_screen)  # Inicjalizacja obiektu Game ,self.screen
        Game(game.mainPY, game.textures, game.previous_screen)  # Tworzenie nowego obiektu Game , game.screen

    def start_esc_menu(self):
        # Funkcja odpowiedzialna za przejście do menu pauzy
        self.screen.fill((0, 0, 0))  # Wypełnienie ekranu czarnym kolorem
        pygame.display.update()  # Aktualizacja wyświetlacza
        esc.EscMenu(self.mainPY, self.textures, self.show_main_game)  # Uruchomienie menu pauzy

    def start_EWO1(self):
        # Funkcja odpowiedzialna za przejście do EWO1
        ewo.Ewo(self.mainPY, self.textures, self.show_main_game, "OP1")  # Uruchomienie EWO1

    def start_EWO2(self):
        # Funkcja odpowiedzialna za przejście do EWO1
        ewo.Ewo(self.mainPY, self.textures, self.show_main_game, "OP2")  # Uruchomienie EWO2

    def start_key_confirmation(self):
        # Funkcja odpowiedzialna za przejście do EWO1
        cc.KeyConfirmation(self.mainPY, self.textures, self.show_main_game)  # Uruchomienie key confirmation

    def start_safe_locks(self):
        # Funkcja odpowiedzialna za przejście do zamku sejfu
        sl.SafeCodeConfirmation(self.mainPY, self.textures, self.show_main_game)  # Uruchomienie key confirmation

    def start_safe(self):
        # Funkcja odpowiedzialna za przejście do sejfu
        s.Safe(self.mainPY, self.textures, self.show_main_game)  # Uruchomienie key confirmation

    def close(self):
        # Funkcja kończąca grę
        pygame.quit()  # Wyjście z Pygame
        sys.exit(0)
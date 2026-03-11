import pygame, os, sys, random,json, pygame_gui
from core import CONST as cst, video_playing as vp
from ui import main as mn, game as gm
from core.CONST import ButtonCONST as BC
class KeyConfirmation():
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
        self.win_conditions_path = "../AOA/core/json/win_conditions.json"

        self.previous_screen = previousScreen  # Poprzedni ekran
        self.background_name = 'key_confirmation_bg'
        self.background_image(self.background_name)  # Ustawienie
        self.main()  # Uruchomienie głównej pętli gry

    def main(self):
        self.manager = pygame_gui.UIManager((cst.SCREEN_WIDTH,cst.SCREEN_HEIGHT))

        # Obliczenia dla symetrycznego umiejscowienia pól tekstowych
        input_width, input_height = self.screen_width*0.25, self.screen_height*0.10
        input_y_position = self.screen_height # Ustawiamy wysokość, by oba pola były na tej samej linii

        # Tworzenie pól tekstowych
        self.input1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.screen_width * 0.30, input_y_position),(input_width, input_height)),manager=self.manager)
        self.input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.screen_width+(self.screen_width*0.45), input_y_position),(input_width, input_height)),manager=self.manager)
        clock = pygame.time.Clock()
        # Główna pętla gry
        while True:
            self.read_MaK_file()
            self.background_image(self.background_name)  # Ustawienie tła
            time_delta = clock.tick(60) / 1000.0  # Przelicznik czasu na sekundy
                # Aktualizacja GUI
            self.manager.update(time_delta)

            # Rysowanie elementów na ekranie
            self.check_events()  # Sprawdzanie wydarzeń
            self.read_win_conditions_file()  # sprawdzanie, czy nie przegrałem
            self.manager.draw_ui(self.screen)
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
            # Modyfikacja odpowiedniego wpisu
            for message in mess_and_keys_parameters['messages']:
                if message ['id'] == 0:
                    self.true_message_OP1 = message['value']
                elif message ['id'] == 1:
                    self.true_message_OP2 = message['value']
            for state in mess_and_keys_parameters['variables_states']:
                if state['id'] == 0:
                    self.is_valve_code_true = state['value']
    def read_win_conditions_file(self): # czytanie z pliku messages_and_keys
        with open(self.win_conditions_path, 'r') as plik_win_conditions:
            win_conditions = json.load(plik_win_conditions)
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

    def confirming(self,codeOP1, codeOP2): #potwierdzanie, że użytkownik wprowadził poprawny kod do valve
        self.read_MaK_file()
        print(self.true_message_OP1,self.true_message_OP2)
        true_valve_code_OP1 = ""
        true_valve_code_OP2 = ""
        for i in range(7,13):
            true_valve_code_OP1 = true_valve_code_OP1 + self.true_message_OP1[i]
            true_valve_code_OP2 = true_valve_code_OP2 + self.true_message_OP2[i]
        print(true_valve_code_OP1, true_valve_code_OP2)
        if true_valve_code_OP1 == codeOP1 and true_valve_code_OP2 == codeOP2:
            with open(self.MaK_path, 'r') as plik_mess_and_keys:
                mess_and_keys_parameters = json.load(plik_mess_and_keys)
                # Modyfikacja odpowiedniego wpisu
                for state in mess_and_keys_parameters['variables_states']:
                    if state ['id'] == 0:
                        state['value'] = True
            self.background_name = 'key_confirmation_bgT'
            with open('../AOA/core/json/messages_and_keys.json', 'w') as plik_mess_and_keys:
                json.dump(mess_and_keys_parameters, plik_mess_and_keys, indent=4)
            self.previous_screen()
        else:
            with open(self.MaK_path, 'r') as plik_mess_and_keys:
                mess_and_keys_parameters = json.load(plik_mess_and_keys)
                # Modyfikacja odpowiedniego wpisu
                for state in mess_and_keys_parameters['variables_states']:
                    if state ['id'] == 0:
                        state['value'] = False
            self.background_name = 'key_confirmation_bgF'
            with open('../AOA/core/json/messages_and_keys.json', 'w') as plik_mess_and_keys:
                json.dump(mess_and_keys_parameters, plik_mess_and_keys, indent=4)

            with open(self.win_conditions_path, 'r') as plik_win_conditions:
                win_conditions = json.load(plik_win_conditions)
                # Modyfikacja odpowiedniego wpisu
                for condition in win_conditions['number_of_valve_code_entered']:
                    if condition['id'] == 0:  # ile razy wpisano kod do valve
                        condition['value'] = int(condition['value']) + 1

            with open(self.win_conditions_path, 'w') as plik_win_conditions:
                json.dump(win_conditions, plik_win_conditions, indent=4)
    def check_events(self):
        # Funkcja sprawdzająca wydarzenia
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                KeyConfirmation.close(self)  # Zakończenie gry
            elif event.type == self.MUSIC_END:
                mn.Main.next_track(self.mainPY)  # Przejście do kolejnego utworu ALLELUJA
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Przechodzę do poprzedniej strony.")
                    self.previous_screen()
                    return False
                elif event.key == pygame.K_RETURN:  # Gdy użytkownik naciśnie Enter
                    OP1_valve_code = self.input1.get_text()  # Pobierz tekst z input1
                    OP2_valve_code = self.input2.get_text()  # Pobierz tekst z input2
                    self.confirming(OP1_valve_code, OP2_valve_code)

                    print("Wartość z input1:", OP1_valve_code)
                    print("Wartość z input2:", OP2_valve_code)
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
            self.manager.process_events(event)

    def close(self):
        # Funkcja kończąca grę
        pygame.quit()  # Wyjście z Pygame
        sys.exit(0)
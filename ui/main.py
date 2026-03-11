import pygame, os, sys, json, random
from core import buttons as bt, CONST as cst, text_to_speech as tts,video_playing as vp
import game as gm
import settings as sett
# Dodaj ścieżkę do katalogu nadrzędnego
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.surfaces import ButtonSurfaces as BS
from core.CONST import ButtonCONST as BC
class Main():
    def __init__(self):
        icon = pygame.image.load("icon2.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Anthem of the Apocalypse")

        self.sources()

        try:    #sprawdza, czy podano już numer piosenki do zagrania
            print(self.current_track_index )
        except AttributeError:
            self.current_track_index = 0  # Zmienna do śledzenia aktualnego utworu

        self.MUSIC_END = pygame.USEREVENT + 1  # Niestandardowe zdarzenie końca muzyki
        self.play_music(self.current_track_index)  # Rozpocznij odtwarzanie pierwszego utworu

        pygame.mixer.music.set_endevent(self.MUSIC_END)

        self.screen = cst.SCREEN
        self.clock = pygame.time.Clock()
        self.clock.tick(cst.FRAMERATE)
        self.dt = self.dt = self.clock.tick(cst.FRAMERATE) / 1000

        currentFile = __file__
        print(currentFile)

        self.check_events()


    def sources(self): #ładowanie zasobów
        self.load_textures()
        self.load_sounds()
        self.load_music()

    def load_textures(self): #wpisywanie nazw plików graficznych na listę, w celu ich późniejszego wykorzystania
        self.textures = {}
        for img in os.listdir("../AOA/img"):
            texture = pygame.image.load("img/" + img)
            self.textures[img.replace(".png", "")] = texture

    def load_sounds(self): #wpisywanie nazw plików dźwiękowych na listę, w celu ich późniejszego wykorzystania
        self.sounds = {}
        for sound in os.listdir("../AOA/sounds"):
            file = pygame.mixer.Sound("sounds/" + sound)
            self.sounds[sound.replace(".mp3", "")] = file

    def load_music(self):  # wpisywanie nazw plików dźwiękowych na listę, w celu ich późniejszego wykorzystania
        self.music_files = []  # lista plików muzycznych
        for music in os.listdir("../AOA/music"):
            if music.endswith(".wav") or music.endswith(".mp3"):  # sprawdzanie czy plik jest typu audio
                self.music_files.append("music/" + music)

    def play_music(self, track_index=0):  # Odtwarzanie muzyki z listy
        if 0 <= track_index < len(self.music_files):
            pygame.mixer.music.load(self.music_files[track_index])  # Ładowanie wybranego pliku muzycznego
            pygame.mixer.music.play()  # Odtwarzanie (w pętli -1 oznacza nieskończoną pętlę)
            pygame.mixer.music.set_volume(cst.MASTER_MUSIC_VOLUME)
        elif track_index == len(self.music_files):
            pygame.mixer.music.load(self.music_files[0])  # Ładowanie pierwszego pliku muzycznego
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(cst.MASTER_MUSIC_VOLUME)
        else:
            print("Niepoprawny indeks utworu.")

    def next_track(self):  # Przejście do kolejnego utworu
        self.current_track_index = (self.current_track_index + 1)  % len(self.music_files)
        self.play_music(self.current_track_index)

    def check_events(self): #sprawdzanie wydarzeń na stronie
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:  # Sprawdzanie, czy skończył się utwór
               self.next_track()  # Przejście do kolejnego utworu
        pass

class MainMenu():
    def __init__(self, textures, sounds, music_files):

        #ustawianie wartości ekranu
        self.screen = cst.SCREEN
        self.screen_width = cst.SCREEN_WIDTH
        self.screen_height = cst.SCREEN_HEIGHT

        # ładowanie zasobów
        self.textures = textures
        self.sounds = sounds
        self.music_files = music_files

        self.main_menu()

    def main_menu(self):
        while True :
            self.fbuttons()
            self.background_image('main_menu_background')

            #zmiany w przyciskach po najechenaiu na nie
            bt.Button_one.bgChangeButton(self,self.buttons)

            # ustawianie napisów na stronie tytułowej
            self.draw_title("Anthem of the Apocalypse", "red")
            self.dev_log_title("Development log", "red")
            self.dev_log("Work in progress", "red")

            pygame.display.update()
            self.check_events()


    def draw_title(self, text, text_col): #ustawianie tytułu strony
        font = pygame.font.SysFont("cambria", round(self.screen_height / 10))
        text = font.render(text, True, text_col)
        text_rect = text.get_rect(center=((self.screen_width / 2), (self.screen_height / 7)))
        self.screen.blit(text, text_rect)

    def fbuttons(self):
        # funkcja do wyświetlania przycisków
        # powierzchnie buttonów menu
        bms = BS.button_menu_surface
        bmcs = BS.button_menu_change_surface

        self.buttons = [
            bt.Button_one(bms,bmcs, (self.screen_width / 4), (self.screen_height / 3), "EASY", 0, self.screen),
            bt.Button_one(bms,bmcs, (self.screen_width / 4), (self.screen_height / 3)*1.4, "NORMAL", 1, self.screen),
            bt.Button_one(bms,bmcs, (self.screen_width / 4), (self.screen_height / 3)*1.8, "HARD", 2, self.screen),
            bt.Button_one(bms,bmcs, (self.screen_width / 4), (self.screen_height / 3)*2.2, "Settings", 3, self.screen),
            bt.Button_one(bms,bmcs, (self.screen_width / 4), (self.screen_height / 3)*2.6,"Exit", 4, self.screen)
        ]

    def background_image(self,bg): #ustawianie tła strony
        background_image = self.textures[bg]
        background_image = pygame.transform.scale(background_image, cst.SCREEN_SIZE)
        self.screen.blit(background_image,(0,0))

    def dev_log_title(self, text, text_col): #ustawianie tytułu dev loga
        font_title = pygame.font.SysFont("Cambria", round(self.screen_height / 18))
        text_title = font_title.render(text, True, text_col)
        text_title_rect = text_title.get_rect(center=((self.screen_width / 4)*3, (self.screen_height / 7)*2.1))
        self.screen.blit(text_title, text_title_rect)

    def dev_log(self, text, text_col): #ustawianie treści dev loga
        font = pygame.font.SysFont("Cambria", round(self.screen_height / 24))
        text = font.render(text, True, text_col)
        text_rect = text.get_rect(topright=((self.screen_width / 4)*3, (self.screen_height / 7)*2.6))
        self.screen.blit(text, text_rect)

    def check_events(self): #sprawdzanie wydarzeń na stronie
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == main.MUSIC_END:  # Sprawdzanie, czy skończył się utwór
               main.next_track()  # Przejście do kolejnego utworu
                #main.music_manager.handle_events()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.checkForInput(mouse_pos):
                        if (button.id == 0 or button.id == 1 or button.id == 2):  # uruchamianie jednego z trybów gry
                            print(f"Starting game with mode {bt.Button_one.game_mode}")
                            self.background_image('wait')
                            pygame.display.update()
                            #tts.text_to_speech()
                            tts.Main()
                            self.start_game()
                        elif button.id == 3: #Ustawienia
                            print(f"Przechodzę do ustawień.")
                            self.start_settings()
                        elif button.id == 4: #Wyjście
                            print(f"Opuszczam grę.")
                            self.close()


    def start_game(self): #funkcja odpowiadająca za przejście do pliku game.py
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        gm.Game(main, main.textures,self.show_main_menu)

    def start_settings(self): #funkcja odpowiadająca za przejście do pliku settings
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        sett.Settings(main, main.textures, self.show_main_menu)

    def show_main_menu(self): #funkcja odpowiedająca za możliwość powrotu do tej strony, jest przerzucana jako zmienna previousScreen
        self.screen.fill((255, 255, 255))
        pygame.display.update()
        MainMenu(main.textures, main.sounds, main.music_files)


    def close(self): #zakończenie programu
        pygame.quit()
        sys.exit(0)

def start_main(): #funkcja do uruchamiana Main() z zewnątrz jak i ze środka pliku
    global main
    main = Main()
    MainMenu(main.textures, main.sounds, main.music_files)

if __name__ == "__main__": #wykonuje się przy bezpośrednim uruchomieniu pliku

    pygame.init()
    pygame.mixer.init()

    # ścieżki odczytywanych plików
    MaK_path = '../AOA/core/json/messages_and_keys.json'
    time_path = '../AOA/core/json/time.json'

    vp.PlayVideo("video/AOA_intro.mp4", 2.0)
    # odczyt i modyfikacja z pliku mess_and_keys_parameters.json

    with open(MaK_path, 'r') as plik_mess_and_keys:
        mess_and_keys_parameters = json.load(plik_mess_and_keys)
        for state in mess_and_keys_parameters['variables_states']:
            if state['id'] == 0:  # is-valve_code-true
                state['value'] = 3
            if state['id'] == 1:  # is-safe_code-true
                state['value'] = 3
        # generowanie i wrzucanie do plików nowych safe kodów dla OP1 i OP2
        for safe_code in mess_and_keys_parameters['safe_codes']:
                if safe_code['id'] == 0:
                    safe_code['value'] = liczba = random.randint(1000, 9999)
                elif safe_code['id'] == 1:
                    safe_code['value'] = liczba = random.randint(1000, 9999)

    with open(MaK_path, 'w') as plik_mess_and_keys:
        json.dump(mess_and_keys_parameters, plik_mess_and_keys, indent=4)

    # odczyt i modyfikacja z pliku time.json

    with open(time_path, 'r') as plik_time:
        time_parameters = json.load(plik_time)
        for order_time in time_parameters['attack_order_time']:
                if order_time['id'] == 0:  # ustawianie momentu rozpoczęcia komunikatu o ataku jądrowym
                    order_time['value'] = random.randint(90, 240)
                    print(order_time['value'])
                if order_time['id'] == 1:  # czy wydano już rozkaz ataku
                    order_time['value'] = False
                if order_time['id'] == 2:  # ile odtworzono do tej pory komunikatów z wiadomością
                    order_time['value'] = 0
                if order_time['id'] == 3:  # jaki jest index właśnie granego komunikatu
                    order_time['value'] = 0
                if order_time['id'] == 4:  # jaki jest key właśnie granego komunikatu
                    order_time['value'] = 'op1Order'

    with open(time_path, 'w') as plik_time:
        json.dump(time_parameters, plik_time, indent=4)

    win_conditions_path = "core/json/win_conditions.json"
    with open(win_conditions_path, 'r') as plik_win_conditions:
        win_conditions = json.load(plik_win_conditions)
        # Modyfikacja odpowiedniego wpisu
        for condition in win_conditions['number_of_nuke_keys_switched']:
            if condition['id'] == 0:  # ile razy przekręcono klucze
                condition['value'] = 0
        for condition in win_conditions['number_of_valve_code_entered']:
            if condition['id'] == 0:  # ile razy wpisano kod do valve
                condition['value'] = 0
        for condition in win_conditions['number_of_safe_code_entered']:
            if condition['id'] == 0:  # ile razy wpisano kod do valve
                condition['value'] = 0

    with open(win_conditions_path, 'w') as plik_win_conditions:
        json.dump(win_conditions, plik_win_conditions, indent=4)


    start_main()





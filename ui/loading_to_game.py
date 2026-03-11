import pygame, sys
from core import CONST as cst
from ui import main as mn, game as gm

#NIE UŻYWANY
class Loading():
    def __init__(self, mainPY, textures, previousScreen):
        self.mainPY = mainPY

        self.screen = cst.SCREEN  # Ustawienie ekranu gry
        self.screen_width = cst.SCREEN_WIDTH  # Szerokość ekranu
        self.screen_height = cst.SCREEN_HEIGHT  # Wysokość ekranu

        self.textures = textures  # Ładowanie tekstur

        self.master_volume = cst.MASTER_MUSIC_VOLUME  # Ustawienie głośności


        self.MUSIC_END = pygame.USEREVENT + 1  # Event zakończenia muzyki
        pygame.mixer.music.set_endevent(self.MUSIC_END)  # Konfiguracja nasłuchiwania zakończenia utworu

        self.previous_screen = previousScreen  # Poprzedni ekran
        self.background_image()  # Ustawienie tła
        self.main_game()  # Uruchomienie głównej pętli gry

    def main_game(self):
        # Główna pętla gry
        while True:
            self.background_image()  # Ustawienie tła

            self.check_events()  # Sprawdzanie wydarzeń
            pygame.display.update()  # Aktualizacja wyświetlacza


    def background_image(self):
        # Funkcja ustawiająca tło
        background_image = self.textures['war']  # Pobranie tekstury tła
        background_image = pygame.transform.scale(background_image, cst.SCREEN_SIZE)  # Skalowanie obrazu tła do rozmiaru ekranu
        self.screen.blit(background_image, (0, 0))  # Rysowanie obrazu tła na ekranie


    def check_events(self):
        # Funkcja sprawdzająca wydarzenia
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Loading.close(self)  # Zakończenie gry
            elif event.type == self.MUSIC_END:
                mn.Main.next_track(self.mainPY)  # Przejście do kolejnego utworu ALLELUJA

    def start_game(self): #funkcja odpowiadająca za przejście do pliku game.py
        self.screen.fill((0, 0, 0))
        pygame.display.update()
        gm.Game(self.mainPY, self.textures, self.show_main_menu)

    def close(self):
        # Funkcja kończąca grę
        pygame.quit()  # Wyjście z Pygame
        sys.exit(0)


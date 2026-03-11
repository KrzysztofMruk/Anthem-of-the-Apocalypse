import pygame,os
from core import CONST as cst
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import speedx


class PlayVideo:
    def __init__(self,video_path,speed_factor):
        self.screen = cst.SCREEN  # Ustawienie ekranu gry
        self.screen_width = cst.SCREEN_WIDTH  # Szerokość ekranu
        self.screen_height = cst.SCREEN_HEIGHT  # Wysokość ekranu

        pygame.display.set_caption("Anthem of the Apocalypse")
        self.video_path = video_path
        self.speed_factor = speed_factor
        self.play_video()


    # Funkcja do odtwarzania wideo
    def play_video(self):
        # Ładowanie klipu wideo
        clip = VideoFileClip(self.video_path)

        # Zmieniamy prędkość wideo
        clip = speedx(clip, factor=self.speed_factor)  # Zmiana prędkości

        # Dopasowanie rozmiaru wideo do wymiarów ekranu
        clip = clip.resize(height=self.screen_height, width=self.screen_width)

        clip.preview(fps=60)

        cst.screen()
        self.screen = cst.SCREEN  # Ustawienie ekranu gry
        self.screen_width = cst.SCREEN_WIDTH  # Szerokość ekranu
        self.screen_height = cst.SCREEN_HEIGHT  # Wysokość ekranu





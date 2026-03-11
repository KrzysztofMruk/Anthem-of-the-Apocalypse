import pygame
from core import CONST as cst
from core.CONST import ButtonCONST as BC

pygame.init()
main_font = pygame.font.SysFont(BC.MENU_BUTTON_FONT,BC.MENU_BUTTON_FONT_SIZE)

class Button_one():
    game_mode = 0
    def __init__(self, image, change_image, x_pos, y_pos, text_input, id, screen): #tworzenie szablonu przycisku
        self.image = image
        self.main_image = image
        self.change_image = change_image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.id = id #id buttona
        self.screen = screen


    def update(self): # Rysowanie przycisku i tekstu na ekranie
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):  # Sprawdzanie, czy myszka jest w obszarze przycisku
        if self.rect.collidepoint(position):
            if self.text_input == "Poziom Łatwy":
                Button_one.game_mode = 1
            elif self.text_input == "Poziom Średni":
                Button_one.game_mode = 2
            elif self.text_input == "Poziom Trudny":
                Button_one.game_mode = 3
            return True
        return False

    def changeButton(self, position):  # Zmiana koloru tekstu przy najechaniu myszką
        if self.rect.collidepoint(position):
            self.text = main_font.render(self.text_input, True, "blue")
            self.image = self.change_image
            pass
        else:
            self.text = main_font.render(self.text_input, True, "white")
            self.image = self.main_image
            pass

    def bgChangeButton(self,buttons_menu):
        for button in buttons_menu:
            button.changeButton(pygame.mouse.get_pos())  # Zmiana wyglądu przycisku po najechaniu na niego
            button.update()

class Static_image(): # tworzenie szablonu statycznego obrazka
    def __init__(self, image, change_image, x_pos, y_pos, text_input, id, screen):
        self.image = image
        self.main_image = image
        self.change_image = change_image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.id = id  # id statycznego obrazka
        self.screen = screen

    def draw(self):  # Rysowanie przycisku i tekstu na ekranie
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def changeImage(self):  # Zmiana koloru tekstu przy najechaniu myszką
            self.temp_image = self.image
            self.image = self.change_image
            self.change_image = self.temp_image
    def drawStaticImage(self,images):
        for image in images:
            image.draw()

class Static_writing():
    def __init__(self, x_pos, y_pos, text_input, id, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "black")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.id = id  # id
        self.screen = screen

    def drawWriting(self):  # Rysowanie przycisku i tekstu na ekranie
        self.screen.blit(self.text, self.text_rect)

    def drawStaticWriting(self,writings):
        for text in writings:
            text.drawWriting()


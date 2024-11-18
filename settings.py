import pygame
import button
#todo
#settings tab, removing planets, custom mass, etc
#
pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (3, 132, 252)
RED = (240, 35, 12)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)
planetNames = ["Sun", "Earth", "Mars", "Mercury", "Venus"]
FONT = pygame.font.SysFont("SFMono Nerd Font", 16)

WIN = pygame.display.set_mode(( 300,500))
checklistImg = pygame.image.load('img/checklist.png').convert_alpha()
checklistImgAct = pygame.image.load('img/checklistAct.png').convert_alpha()
showSun = button.Button(30, 100, checklistImg, checklistImgAct, 1)
showEarth = button.Button(30, 130, checklistImg, checklistImgAct, 1)
showMars = button.Button(30, 160, checklistImg, checklistImgAct, 1)
showMercury = button.Button(30, 190, checklistImg, checklistImgAct, 1)
showVenus = button.Button(30, 220, checklistImg, checklistImgAct, 1)

class Settings:
    def __init__(self, list, font):
        self.newPlanets = list
        self.font = font
        self.newl =[True, True, True, True, True]

    def draw(self, win):
        pygame.draw.rect(win, DARK_GREY, (20, 90, 300, 500))
        win.blit(FONT.render('Sun', 1, WHITE),(55, 105))
        win.blit(FONT.render('Earth', 1, WHITE),(55, 135))
        win.blit(FONT.render('Mars', 1, WHITE),(55, 165))
        win.blit(FONT.render('Mercury', 1, WHITE),(55, 195))
        win.blit(FONT.render('Venus', 1, WHITE),(55, 225))

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
FONT_18px = pygame.font.SysFont("sfmonomedium,sfmonomediumnerdfontcomplete", 18)
FONT_13px = pygame.font.SysFont("sfmonomedium,sfmonomediumnerdfontcomplete", 13)
WIN = pygame.display.set_mode(( 300,500))

class Settings:
    def __init__(self, list, font):
        self.newPlanets = list
        self.font = font
        self.newl =[True, True, True, True, True]

    def draw(self, win):
        pygame.draw.rect(win, DARK_GREY, (20, 90, 300, 500))
        win.blit(FONT_18px.render('Toggle Planets', 1, WHITE),(30, 100))
        win.blit(FONT_13px.render('Sun', 1, WHITE),(55, 132))
        win.blit(FONT_13px.render('Earth', 1, WHITE),(55, 162))
        win.blit(FONT_13px.render('Mars', 1, WHITE),(55, 192))
        win.blit(FONT_13px.render('Mercury', 1, WHITE),(55, 222))
        win.blit(FONT_13px.render('Venus', 1, WHITE),(55, 252))
        win.blit(FONT_18px.render('Custom Planet Settings', 1, WHITE),(30, 280))
        win.blit(FONT_13px.render('Planet Mass:', 1, WHITE),(30, 317))

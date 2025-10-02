import pygame

class Images:
    def __init__(self):
        self.pauseImg = pygame.image.load('img/pause.png').convert_alpha()
        self.resumeImg = pygame.image.load('img/resume.png').convert_alpha()
        self.spedupInactive = pygame.image.load('img/spedupInac.png').convert_alpha()
        self.spedupActive = pygame.image.load('img/spedupAct.png').convert_alpha()
        self.newImg = pygame.image.load('img/create.png').convert_alpha()
        self.settingsImg = pygame.image.load('img/settings.png').convert_alpha()
        self.settingsActImg = pygame.image.load('img/settingsAct.png').convert_alpha()
        self.checklistImg = pygame.image.load('img/checklist.png').convert_alpha()
        self.checklistImgAct = pygame.image.load('img/checklistAct.png').convert_alpha()
        self.clearPlanets = pygame.image.load('img/clearplanets.png').convert_alpha()
        self.clearPlanetsAct = pygame.image.load('img/clearplanetsAct.png').convert_alpha()
    
    
    
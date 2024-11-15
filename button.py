import pygame
class Button():
    def __init__(self,x ,y, img, img2, scale):
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img,(int(width*scale), int(height*scale)))
        width2 = img2.get_width()
        height2 = img2.get_height()
        self.img2 = pygame.transform.scale(img2,(int(width*scale), int(height*scale)))
        self.rect= self.img.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, surface, state):
        action = state
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = not action
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        if action:
            surface.blit(self.img2, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.img, (self.rect.x, self.rect.y))
        return action
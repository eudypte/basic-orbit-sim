import pygame
import pygame_gui.ui_manager
import pygame_widgets
import button
import settings
import pygame_gui
from pygame_widgets.slider import Slider
import math 
pygame.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (3, 132, 252)
RED = (240, 35, 12)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)

FONT_16px = pygame.font.SysFont("sfmonomedium,sfmonomediumnerdfontcomplete", 16)
FONT_13px = pygame.font.SysFont("sfmonomedium,sfmonomediumnerdfontcomplete", 13)

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode(( WIDTH,HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
scaleSlider = Slider(WIN, WIDTH-420, 10, 400, 30, min = 100, max = 400,color=WHITE) #380width
newPlanetMassSlider = Slider(WIN, 35, 340, 180, 10, min = 1, max = 10,step = 0.1,color=WHITE) # * 10**24
newPlanetYVel = Slider(WIN, 35, 390, 180, 10, min = -50, max = 50,step = 0.5, initial = 25,color=WHITE) # * 100


pauseImg = pygame.image.load('img/pause.png').convert_alpha()
resumeImg = pygame.image.load('img/resume.png').convert_alpha()
spedupInactive = pygame.image.load('img/spedupInac.png').convert_alpha()
spedupActive = pygame.image.load('img/spedupAct.png').convert_alpha()
newImg = pygame.image.load('img/create.png').convert_alpha()
settingsImg = pygame.image.load('img/settings.png').convert_alpha()
settingsActImg = pygame.image.load('img/settingsAct.png').convert_alpha()
checklistImg = pygame.image.load('img/checklist.png').convert_alpha()
checklistImgAct = pygame.image.load('img/checklistAct.png').convert_alpha()
clearPlanets = pygame.image.load('img/clearplanets.png').convert_alpha()
clearPlanetsAct = pygame.image.load('img/clearplanetsAct.png').convert_alpha()

pauseButton = button.Button(80, 20, pauseImg, resumeImg, 1)
speedButton = button.Button(140, 20, spedupInactive, spedupActive, 1)
settingsButton = button.Button(20, 20, settingsImg, settingsActImg, 1)

showSun = button.Button(30, 130, checklistImg, checklistImgAct, 1)
showEarth = button.Button(30, 160, checklistImg, checklistImgAct, 1)
showMars = button.Button(30, 190, checklistImg, checklistImgAct, 1)
showMercury = button.Button(30, 220, checklistImg, checklistImgAct, 1)
showVenus = button.Button(30, 250, checklistImg, checklistImgAct, 1)

clearCustomPlanets = button.Button(30, 420, clearPlanets, clearPlanetsAct, 1)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1AU = 250 pixels
    TIMESTEP = 3600*24 # one day

    def __init__(self, x, y, radius, color, mass, active):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.active = active

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        radius = (self.radius / 250) * self.AU * self.SCALE

        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2 
                updated_points.append((x, y))
            if len(updated_points) > 100:
                updated_points = updated_points[-100:]
            if self.active:
                pygame.draw.lines(win, self.color, False, updated_points, 2)
        if self.active:
            pygame.draw.circle(win, self.color, (x,y), radius)
        if not self.sun:
            distance_text = FONT_16px.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            #win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
            if self.active:
                win.blit(distance_text, (((x - distance_text.get_width()/2)+15), ((y - distance_text.get_height()/2))-25))
                pygame.draw.lines(win, WHITE, False, [(x,y),(x+15,y-20)])

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        


def main():
    run = True
    pause = False
    spedup = False
    settingsmenu = False
    mouseFree = True
    debug = False
    clearPlanets = False
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30, True)
    sun.sun = True
    earth = Planet(-1 * Planet.AU,0,16,BLUE,5.9742 * 10**24, True)
    earth.y_vel = 29.893 * 1000
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, True)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, True)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, True)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]
    basePlanets = [sun, earth, mars, mercury, venus]
    planetsAct = [True, True, True, True, True]

    settingTest = settings.Settings(planets, FONT_16px)
    
    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        pos = pygame.mouse.get_pos()
        
        if debug:
            WIN.blit(FONT_16px.render(str(pos), 1, WHITE),(0, HEIGHT-20))       #For debug
            WIN.blit(FONT_16px.render(str(mouseFree), 1, WHITE),(0, HEIGHT-40))
        if ((pos[0]>20 and pos[0]<190) and (pos[1]>20 and pos[1]<70)) or (settingsmenu == True and ((pos[0]>20 and pos[0]<320) and (pos[1]>90 and pos[1]<590))) or (pos[0]>550 and pos[0]<WIDTH) and (pos[1]>0 and pos[1]<70):
            mouseFree = False
        else:
            mouseFree = True

        if pauseButton.draw(WIN, pause) == True:
            pause = True
        else:
            pause = False
        if speedButton.draw(WIN, spedup) == True:
            spedup = True
            for planet in planets:
                planet.TIMESTEP = 3600*48
        else:
            spedup = False
            for planet in planets:
                planet.TIMESTEP = 3600*24
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1 and scaleSlider.getValue() < 400:
                    scaleSlider.setValue(scaleSlider.getValue() + 15)
                elif event.y == -1 and scaleSlider.getValue() > 100:
                    scaleSlider.setValue(scaleSlider.getValue() - 15)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    spedup = not spedup
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    debug = not debug
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouseFree == True: 
                newP = Planet((pos[0]-(WIDTH/2))/scaleSlider.getValue() * Planet.AU, (pos[1]-(HEIGHT/2))/scaleSlider.getValue() * Planet.AU, 8, WHITE, newPlanetMassSlider.getValue() * 10**24, True)
                newP.y_vel = newPlanetYVel.getValue() * 1000
                planets.append(newP)

            #if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            #   WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


        for planet in planets:
            planet.SCALE = scaleSlider.getValue() / planet.AU
            if not pause:
                planet.update_pos(planets)
            planet.draw(WIN)
        
        if settingsButton.draw(WIN, settingsmenu) == True:
            settingsmenu = True
            settingTest.draw(WIN)
            if clearCustomPlanets.draw(WIN, clearPlanets) == True:
                while(len(planets)>5):
                    planets.pop()
                
            newPlanetMassSlider.show()
            newPlanetYVel.show()
            WIN.blit(FONT_13px.render(f"{round(newPlanetMassSlider.getValue().__float__(),1)} * 10^24", 1, WHITE),(130, 317))
            WIN.blit(FONT_13px.render(f"{round(newPlanetYVel.getValue().__float__(),1)} * 1000", 1, WHITE),(190, 367))
            WIN.blit(FONT_13px.render("Clear Custom Planets", 1, WHITE),(40, 430))

            if showSun.draw(WIN, planetsAct[0]) == True:
                planetsAct[0] = True
            else:
                planetsAct[0] = False

            if showEarth.draw(WIN, planetsAct[1]) == True:
                planetsAct[1] = True
            else:
                planetsAct[1] = False

            if showMars.draw(WIN, planetsAct[2]) == True:
                planetsAct[2] = True
            else:
                planetsAct[2] = False

            if showMercury.draw(WIN, planetsAct[3]) == True:
                planetsAct[3] = True
            else:
                planetsAct[3] = False

            if showVenus.draw(WIN, planetsAct[4]) == True:
                planetsAct[4] = True
            else:
                planetsAct[4] = False
        
            ct = 0
            for planet in basePlanets:
                planet.active = planetsAct[ct]
                ct += 1
            
        else:
            settingsmenu = False 
            newPlanetMassSlider.hide()   
            newPlanetYVel.hide()

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()

    pygame.quit

main()
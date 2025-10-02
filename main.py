import pygame
import pygame_widgets
import button
import settings
import pygame_gui
from pygame_widgets.slider import Slider
from planet import Planet
from config import *
from images import Images

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
# Sliders
# TODO: fix the blue bar behind sliders
scaleSlider = Slider(WIN, WIDTH-420, 10, 400, 30, min = 100, max = 400,color=WHITE) #380width
newPlanetMassSlider = Slider(WIN, 35, 340, 180, 10, min = 1, max = 10,step = 0.1,color=WHITE) # * 10**24
newPlanetYVel = Slider(WIN, 35, 390, 180, 10, min = -50, max = 50,step = 0.5, initial = 25,color=WHITE) # * 100

images = Images()

# Buttons Top Left
pauseButton = button.Button(80, 20, images.pauseImg, images.resumeImg, 1)
speedButton = button.Button(140, 20, images.spedupInactive, images.spedupActive, 1)
settingsButton = button.Button(20, 20, images.settingsImg, images.settingsActImg, 1)

# Menu Buttons
showSun = button.Button(30, 130, images.checklistImg, images.checklistImgAct, 1)
showEarth = button.Button(30, 160, images.checklistImg, images.checklistImgAct, 1)
showMars = button.Button(30, 190, images.checklistImg, images.checklistImgAct, 1)
showMercury = button.Button(30, 220, images.checklistImg, images.checklistImgAct, 1)
showVenus = button.Button(30, 250, images.checklistImg, images.checklistImgAct, 1)

clearCustomPlanets = button.Button(30, 420, images.clearPlanets, images.clearPlanetsAct, 1)

def main():
    run = True
    pause = False
    spedup = False
    settingsmenu = False
    mouseFree = True
    debug = False
    clearPlanets = False
    clock = pygame.time.Clock()

    # TODO: rewrite in a separate function
    sun = Planet(x=0, y=0, radius=30, color=YELLOW, mass=1.98892 * 10 ** 30, active=True)
    sun.sun = True
    earth = Planet(x=-1 * Planet.AU, y=0, radius=16, color=BLUE, mass=5.9742 * 10**24, active=True)
    earth.y_vel = 29.893 * 1000
    mars = Planet(x=-1.524 * Planet.AU, y=0, radius=12, color=RED, mass=6.39 * 10**23, active=True)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(x=0.387 * Planet.AU, y=0, radius=8, color=DARK_GREY, mass=3.30 * 10**23, active=True)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(x=0.723 * Planet.AU, y=0, radius=14, color=WHITE, mass=4.8685 * 10**24, active=True)
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
            # TODO: add a menu button for custom planets and make planets more customizable
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouseFree == True: 
                newP = Planet(x=(pos[0]-(WIDTH/2))/scaleSlider.getValue() * Planet.AU, y=(pos[1]-(HEIGHT/2))/scaleSlider.getValue() * Planet.AU, radius=8, color=WHITE, mass=newPlanetMassSlider.getValue() * 10**24, active=True)
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

            # TODO: rewrite this section with a helper function
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
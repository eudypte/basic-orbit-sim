import pygame
import math
from config import *

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

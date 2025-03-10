import math
import random
import pygame

SUN = (253, 184, 19)
MERCURY = (219, 206, 202)
VENUS = (139, 125, 130)
EARTH = (40, 122, 184)
MARS = (156, 46, 53)
JUPITER = (201, 144, 57)
SATURN = (101, 95, 69)
URANUS = (209, 231, 231)
NEPTUNE = (0, 125, 172)


class Planet:

    AU = 149.6e6 * 1000 
    G = 6.67428e-11 
    SCALE = 30 / AU 
    TIMESTEP = 3600 * 24 

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
        self.name = ""
        self.mass = 0
        self.orbit_time = 0
        self.actual_radius = 0
        self.gravity = 0
        self.mean_temp = 0
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.sun = False 


    def draw_planet(self):
        
        x = self.x * Planet.SCALE + 1280 / 2
        y = self.y * Planet.SCALE + 800 / 2
        return x, y
    

    def calculate_gravitational_force(self, planet_list):
        total_fx, total_fy = 0, 0

        for planet in planet_list:
            if self.name == planet.name:
                continue
            distance_x = planet.x - self.x
            distance_y = planet.y - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if planet.sun:
                self.distance_to_sun = distance
            gravitational_force = Planet.G * self.mass * planet.mass / distance ** 2

            angle = math.atan2(distance_y, distance_x) 
            force_x = math.cos(angle) * gravitational_force
            force_y = math.sin(angle) * gravitational_force
            total_fx += force_x
            total_fy += force_y
        
        self.x_vel += total_fx / self.mass * Planet.TIMESTEP
        self.y_vel += total_fy / self.mass * Planet.TIMESTEP

        self.x += self.x_vel * Planet.TIMESTEP
        self.y += self.y_vel * Planet.TIMESTEP


sun = Planet(0, 0, 8, SUN)
sun.sun = True
sun.mass = 1.98892e30
sun.name = "Sun"
sun.actual_radius = 696340
sun.gravity = 274.0
sun.mean_temp = 5499

mercury = Planet(0.387 * Planet.AU, 0, 2, MERCURY)
mercury.y_vel = -math.sqrt(Planet.G * sun.mass / (0.387 * Planet.AU))
mercury.mass = 0.33e24
mercury.name = "Mercury"
mercury.orbit_time = 88
mercury.actual_radius = 2440
mercury.gravity = 3.7
mercury.mean_temp = 167

venus = Planet(0.723 * Planet.AU, 0, 3, VENUS)
venus.y_vel = -math.sqrt(Planet.G * sun.mass / (0.723 * Planet.AU))
venus.mass = 4.8685e24
venus.name = "Venus"
venus.orbit_time = 225
venus.actual_radius = 6052
venus.gravity = 8.9
venus.mean_temp = 464

earth = Planet(-1 * Planet.AU, 0, 3, EARTH)
earth.y_vel = math.sqrt(Planet.G * sun.mass / (1 * Planet.AU))
earth.mass = 5.9742e24
earth.name = "Earth"
earth.orbit_time = 365
earth.actual_radius = 6371
earth.gravity = 9.8
earth.mean_temp = 15

mars = Planet(-1.524 * Planet.AU, 0, 3, MARS)
mars.y_vel = math.sqrt(Planet.G * sun.mass / (1.524 * Planet.AU))
mars.mass = 0.639e24
mars.name = "Mars"
mars.orbit_time = 687
mars.actual_radius = 3390
mars.gravity = 3.7
mars.mean_temp = -65

jupiter = Planet(5.203 * Planet.AU, 0, 5, JUPITER)
jupiter.y_vel = -math.sqrt(Planet.G * sun.mass / (5.203 * Planet.AU))
jupiter.mass = 1898.2e24
jupiter.name = "Jupiter"
jupiter.orbit_time = 4333
jupiter.actual_radius = 69911
jupiter.gravity = 23.1
jupiter.mean_temp = -110

saturn = Planet(-9.537 * Planet.AU, 0, 4, SATURN)
saturn.y_vel = math.sqrt(Planet.G * sun.mass / (9.537 * Planet.AU))
saturn.mass = 568.34e24
saturn.name = "Saturn"
saturn.orbit_time = 10759
saturn.actual_radius = 58232
saturn.gravity = 9.0
saturn.mean_temp = -140

uranus = Planet(-19.191 * Planet.AU, 0, 4, URANUS)
uranus.y_vel = math.sqrt(Planet.G * sun.mass / (19.191 * Planet.AU))
uranus.mass = 86.810e24
uranus.name = "Uranus"
uranus.orbit_time = 30687
uranus.actual_radius = 25362
uranus.gravity = 8.7
uranus.mean_temp = -195

neptune = Planet(30.069 * Planet.AU, 0, 4, NEPTUNE)
neptune.y_vel = -math.sqrt(Planet.G * sun.mass / (30.069 * Planet.AU))
neptune.mass = 102.413e24
neptune.name = "Neptune"
neptune.orbit_time = 60190
neptune.actual_radius = 24622
neptune.gravity = 11.0
neptune.mean_temp = -200

planet_list = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

class Star:
    def __init__(self, width,height):
        self.radius = random.randint(0,1)
        self.color = (255, 255, 255)
        self.pos_x = random.randint(0, width)
        self.pos_y = random.randint(0, height)
        self.decrease = True

    def show(self, screen):
        t = random.randint(0,100)

        if t == 1 or t == 0:
            if self.decrease and self.radius > 1:
                self.radius -= 1
                self.decrease = False
            else:
                self.radius += 1
                self.decrease = True
        
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)

star_list = [Star(1280,800) for _ in range(100)]
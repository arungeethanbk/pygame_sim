import pygame
import math
import random
from planets import planet_list
from planets import star_list

pygame.init()

WIDTH, HEIGHT = 1920,1080
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physix")
FONT = pygame.font.SysFont("Consolas", 18)
PAUSE_FONT = pygame.font.SysFont("Consolas", 24)
LEGEND_TEXTS = ["P Pause", "M Mute", "I Info off", "Q Quit", 
                "0 Sun", "1 Mercury", "2 Venus", "3 Earth", "4 Mars", "5 Jupiter", "6 Saturn", "7 Uranus", "8 Neptune"]

BG_MUSIC = pygame.mixer.Sound("stay.mp3")
BG_MUSIC.set_volume(0.9)
BG_MUSIC.play(loops=-1)

class Comet:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.radius = 1
        self.color = (0, 255, 0)  
        self.speed = 6  
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.initialize_position()
    
    def initialize_position(self):
        if self.direction == 'left':
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)
        elif self.direction == 'right':
            self.x = 0
            self.y = random.randint(0, HEIGHT)
        elif self.direction == 'up':
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT
        elif self.direction == 'down':
            self.x = random.randint(0, WIDTH)
            self.y = 0

    def move(self):
        if self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed

    def draw_comet(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def main():
    clock = pygame.time.Clock()
    running = True
    paused = False
    displayed_planet = None
    time_passed = 0
    pause_text = ""
    muted = False
    comet_interval = 3000  
    comet_timer = 0

    comet = None

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if paused:
                        paused = False
                    elif not paused:
                        paused = True
                        pause_text = PAUSE_FONT.render("PAUSED", 1, (255, 255, 255))
                        win.blit(pause_text, (WIDTH / 2 - pause_text.get_width() / 2, 20))
                        pygame.display.update()
                                    

                if pygame.K_0 <= event.key <= pygame.K_8:
                    planet_index = event.key - pygame.K_0  # 48
                    displayed_planet = planet_list[planet_index]


                if event.key == pygame.K_i:
                    if displayed_planet:
                        displayed_planet = None

                if event.key == pygame.K_q:
                    running = False

                if event.key == pygame.K_m:
                    if muted:
                        BG_MUSIC.set_volume(0.3)
                        muted = False
                    elif not muted:
                        BG_MUSIC.set_volume(0)
                        muted = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if displayed_planet:
                    displayed_planet = None
            
            comet_timer += dt
            if comet_timer >= comet_interval:
                comet = [Comet() for _ in range(3)]
                comet_timer = 0
        
        if not paused:
            time_passed += planet_list[0].TIMESTEP
            for planet in planet_list:
                planet.calculate_gravitational_force(planet_list)

            win.fill((0, 0, 0))

            if comet:
                for c in comet:
                    c.move()
                    c.draw_comet()
            
            for s in star_list:
                s.show(win)

            for planet in planet_list:
                x, y = planet.draw_planet()
                pygame.draw.circle(win, planet.color, (x, y), planet.radius)

        text_x = WIDTH - 105
        text_y = 20
        for legend_text in LEGEND_TEXTS:
            if displayed_planet:
                if displayed_planet.name.capitalize() in legend_text:
                    text = FONT.render(legend_text, 1, displayed_planet.color)
                else:
                    text = FONT.render(legend_text, 1, (255, 255, 255))
                win.blit(text, (text_x, text_y))
                text_y += 30
            else:
                text = FONT.render(legend_text, 1, (255, 255, 255))
                win.blit(text, (text_x, text_y))
                text_y += 30

        for planet in planet_list:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance = math.sqrt((planet.x * planet.SCALE + 1280 / 2 - mouse_x) ** 2 + (planet.y * planet.SCALE + 800 / 2 - mouse_y) ** 2)
            if distance <= planet.radius and not paused:
                idx = planet_list.index(planet)
                displayed_planet = planet_list[idx]

        if displayed_planet:
            if displayed_planet.name != "Sun":
                days_passed = time_passed / (3600 * 24)
                days_left = int(displayed_planet.orbit_time - days_passed)
                velocity = math.sqrt(displayed_planet.x_vel ** 2 + displayed_planet.y_vel ** 2) / 1000
                distance_to_sun = displayed_planet.distance_to_sun / 1000
                days_left_for_full_orbit = days_left % displayed_planet.orbit_time
                years_passed_since_start = days_passed / displayed_planet.orbit_time

                
                planet_info_text_1 = FONT.render(f"{displayed_planet.name}", 1, displayed_planet.color)
              
                lines = [
                    f"Mass: {displayed_planet.mass} kg",
                    f"Radius: {displayed_planet.actual_radius:,} km",
                    f"Gravity: {displayed_planet.gravity} m/s^2",
                    f"Mean Temperature: {displayed_planet.mean_temp} °C",
                    f"Velocity: {velocity:.1f} km/s",
                    f"Distance to Sun: {distance_to_sun:,.1f} km",
                    f"Days left for one full orbit: {days_left_for_full_orbit} days",
                    f"Time passed since start: {years_passed_since_start:.2f} {displayed_planet.name} years",
                    "Symbol: "
                ]

                
                rendered_lines = [FONT.render(line, 1, (255, 255, 255)) for line in lines]

                
                planet_info_text_2 = pygame.Surface((max(line.get_width() for line in rendered_lines), sum(line.get_height() for line in rendered_lines)))
                y_offset = 0
                for line in rendered_lines:
                    planet_info_text_2.blit(line, (0, y_offset))
                    y_offset += line.get_height()

                source_text = FONT.render("Source: NASA", 1, (255, 255, 255))
                win.blit(planet_info_text_1, (10, 20))
                win.blit(planet_info_text_2, (10, 40))

                
                try:
                    planet_image = pygame.transform.scale(pygame.image.load(f"assets/images/planets/{displayed_planet.name.lower()}.jpg"), (250, 250))
                except FileNotFoundError:
                    print(f"Planet image not found: assets/images/planets/{displayed_planet.name.lower()}.jpg")
                    planet_image = pygame.Surface((250, 250))
                    planet_image.fill((128, 128, 128))  
                win.blit(planet_image, (0, HEIGHT - 270))

                
                try:
                    symbol_image = pygame.image.load(f"assets/images/symbol/{displayed_planet.name.lower()}.jpg")
                except FileNotFoundError:
                    print(f"Symbol image not found: assets/images/symbol/{displayed_planet.name.lower()}.jpg")
                    symbol_image = pygame.Surface((50, 50))
                    symbol_image.fill((128, 128, 128))  
                win.blit(symbol_image, (85, planet_info_text_2.get_height() + 20))

            elif displayed_planet.name == "Sun":
                days_passed = int(time_passed / (3600 * 24))
                sun = displayed_planet
                sun_info_text_1 = FONT.render("Sun", 1, sun.color)
               
                sun_lines = [
                    f"Mass: {sun.mass} kg",
                    f"Radius: {sun.actual_radius:,} km",
                    f"Gravity (Surface): {sun.gravity} m/s^2",
                    f"Mean Temperature (Surface): {sun.mean_temp} °C",
                    f"Time passed since start: {days_passed} Sun days",
                    "Symbol: "
                ]

                sun_rendered_lines = [FONT.render(line, 1, (255, 255, 255)) for line in sun_lines]

               
                sun_info_text_2 = pygame.Surface((max(line.get_width() for line in sun_rendered_lines), sum(line.get_height() for line in sun_rendered_lines)))
                y_offset = 0

                for line in sun_rendered_lines:
                    sun_info_text_2.blit(line, (0, y_offset))
                    y_offset += line.get_height()

                source_text = FONT.render("Source: NASA", 1, (255, 255, 255))
                win.blit(sun_info_text_1, (10, 20))
                win.blit(sun_info_text_2, (10, 40))

                try:
                    sun_image = pygame.transform.scale(pygame.image.load("assets/images/planets/sun.jpg"), (250, 250))
                except FileNotFoundError:
                    print("Sun image not found: assets/images/planets/sun.jpg")
                    sun_image = pygame.Surface((250, 250))
                    sun_image.fill((255, 255, 0)) 
                win.blit(sun_image, (0, HEIGHT - 270))

                
                try:
                    sun_symbol = pygame.image.load("assets/images/symbol/sun.jpg")
                except FileNotFoundError:
                    print("Sun symbol not found: assets/images/symbol/sun.jpg")
                    sun_symbol = pygame.Surface((50, 50))
                    sun_symbol.fill((255, 255, 0))  
                win.blit(sun_symbol, (85, sun_info_text_2.get_height() + 20))

           
            x = int(displayed_planet.x * displayed_planet.SCALE + 1280 / 2)
            y = int(displayed_planet.y * displayed_planet.SCALE + 800 / 2)
            pygame.draw.circle(win, (255, 255, 255), (x, y), displayed_planet.radius + 5, width=1)

            current_x_distance = (displayed_planet.x - planet_list[0].x)
            current_y_distance = (displayed_planet.y - planet_list[0].y)
            center_x = int(planet_list[0].x * displayed_planet.SCALE + 1280 / 2)
            center_y = int(planet_list[0].y * displayed_planet.SCALE + 800 / 2)
            current_distance = math.sqrt(current_x_distance ** 2 + current_y_distance ** 2) * displayed_planet.SCALE
            pygame.draw.circle(win, displayed_planet.color, (center_x, center_y), current_distance, width=1)

            if displayed_planet.name == "Neptune":
                neptune = displayed_planet
                neptune_out_up = neptune.y * neptune.SCALE + 800 / 2 < 0
                neptune_out_down = neptune.y * neptune.SCALE + 800 / 2 > 800

                if neptune_out_up or neptune_out_down:
                    text = FONT.render("Neptune is out of screen now", 1, neptune.color)
                    win.blit(text, (10, planet_info_text_2.get_height() + 40))

                    if neptune_out_up:
                        line_start = (WIDTH / 2, 50)
                        line_end = (neptune.x * neptune.SCALE + 1280 / 2, neptune.y * neptune.SCALE + 800 / 2)
                        neptune_indicator = FONT.render("Neptune", 1, (255, 255, 255))
                        pygame.draw.line(win, (255, 255, 255), line_start, line_end) 
                        win.blit(neptune_indicator, (line_start[0] - neptune_indicator.get_width() / 2, line_start[1] + 20))

                    elif neptune_out_down:
                        line_start = (WIDTH / 2, HEIGHT - 50)
                        line_end = (neptune.x * neptune.SCALE + 1280 / 2, neptune.y * neptune.SCALE + 800 / 2)
                        neptune_indicator = FONT.render("Neptune", 1, (255, 255, 255))
                        pygame.draw.line(win, (255, 255, 255), line_start, line_end)
                        win.blit(neptune_indicator, (line_start[0] - neptune_indicator.get_width() / 2, line_start[1] - 20))

            elif displayed_planet.name == "Uranus":
                uranus = displayed_planet
                uranus_out_up = uranus.y * uranus.SCALE + 800 / 2 < 0
                uranus_out_down = uranus.y * uranus.SCALE + 800 / 2 > 800 

                if uranus_out_up or uranus_out_down:
                    text = FONT.render("Uranus is out of screen now", 1, uranus.color)
                    win.blit(text, (10, planet_info_text_2.get_height() + 40))

                    if uranus_out_up:
                        line_start = (WIDTH / 2, 50)
                        line_end = (uranus.x * uranus.SCALE + 1280 / 2, uranus.y * uranus.SCALE + 800 / 2)
                        uranus_indicator = FONT.render("Uranus", 1, (255, 255, 255))
                        pygame.draw.line(win, (255, 255, 255), line_start, line_end)
                        win.blit(uranus_indicator, (line_start[0] - neptune_indicator.get_width() / 2, line_start[1] + 20))

                    elif uranus_out_down:
                        line_start = (WIDTH / 2, HEIGHT - 50)
                        line_end = (uranus.x * uranus.SCALE + 1280 / 2, uranus.y * uranus.SCALE + 800 / 2)
                        uranus_indicator = FONT.render("Uranus", 1, (255, 255, 255))
                        pygame.draw.line(win, (255, 255, 255), line_start, line_end)
                        win.blit(uranus_indicator, (line_start[0] - uranus_indicator.get_width() / 2, line_start[1] - 20))

       
        if not paused:
            scale_info_text = FONT.render("Distances are to scale, sizes are not to scale.", 1, (255, 255, 255))
            win.blit(scale_info_text, (WIDTH - scale_info_text.get_width(), HEIGHT - scale_info_text.get_height()))
        
            pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    main()
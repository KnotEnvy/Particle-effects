import pygame
import random
import math
import sys
pygame.init()
pygame.font.init()
pygame.mixer.init()
FONT = pygame.font.SysFont("comicsans", 30)


class Button:
    def __init__(self, x, y, width, height, text, font, font_size, text_color, bg_color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                if self.rect.collidepoint(event.pos):
                    self.callback()

class Particle:
    def __init__(self, pos):
        # Don't create particles near the bottom of the screen where the buttons are located
        #if pos[1] > window_height - button_height - button_margin * 2:
        #    self.life = 0
        #    return

        self.pos = [pos[0], pos[1]]
        self.size = random.randint(1, 3)
        self.color = (random.randint(0, 210), random.randint(0, 75), random.randint(0, 100))
        self.life = 100

        # Set the initial velocity of the particle
        speed = random.uniform(1, 9)
        self.vel = [random.uniform(-speed, speed), random.uniform(-speed, speed)]

    def update(self):
        self.life -= 1
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update the size of the particle
        self.size = (self.size + .10) % 3 + 1

    def draw(self, surface):
        x = int(self.pos[0])
        y = int(self.pos[1])
        pygame.draw.circle(surface, self.color, (x, y), int(self.size))





# Set up the display window
window_width = 1280
window_height = (window_width * .66)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Particle Effects")

# Set up the clock
clock = pygame.time.Clock()



# Set up the buttons
button_font = "freesansbold.ttf"
button_font_size = 32
button_text_color = (255, 0, 255)
button_bg_color = (0, 0, 255)
button_width = 200
button_height = 50
button_margin = 50
buttons = [
    Button(button_margin,
           window_height - button_height - button_margin,
           button_width,
           button_height,
           "Increase Speed",
           button_font,
           button_font_size,
           button_text_color,
           button_bg_color,
           lambda: change_speed(0.1)),
    Button(button_margin * 2 + button_width,
           window_height - button_height - button_margin,
           button_width,
           button_height,
           "Decrease Speed",
           button_font,
           button_font_size,
           button_text_color,
           button_bg_color,
           lambda: change_speed(-0.1)),
    # Add more buttons here...
]


def change_speed(amount):
    global particle_speed
    particle_speed += amount

# Main game loop
particles = []
max_particles = 150000
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # Right mouse button
                # Change the color of all particles to a random color
                new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for particle in particles:
                    particle.color = new_color
        else:
            for button in buttons:
                button.handle_event(event)

    # Clear the screen
    screen.fill((100,100,100))

    # Create new particles
    if pygame.mouse.get_pressed()[0] and len(particles) < max_particles:
        for i in range(100):
            particles.append(Particle(pygame.mouse.get_pos()))

    # Update particles
    for particle in particles:
        particle.update()
        if particle.life <= 0 or particle.pos[0] < 0 or particle.pos[0] > window_width or particle.pos[1] < 0 or particle.pos[1] > window_height:
            particles.remove(particle)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Draw buttons
    for button in buttons:
        button.draw(screen)


    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

import pygame
import random
import math

class Particle:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.size = random.randint(1, 3)
        self.color = (random.randint(0, 210), random.randint(0, 75), random.randint(0, 100))
        self.life = 500

        # Set the initial velocity of the particle
        speed = random.uniform(2, 4)
        self.vel = [random.uniform(-speed, speed), random.uniform(-speed, speed)]

    def update(self):
        self.life -= 1
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update the velocity of the particle based on the current position of the mouse
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.pos[0]
        dy = mouse_pos[1] - self.pos[1]
        angle = math.atan2(dy, dx)
        speed = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
        self.vel = [-math.cos(angle) * speed, -math.sin(angle) * speed]

    def draw(self, surface):
        x1 = int(self.pos[0])
        y1 = int(self.pos[1])
        x2 = int(self.pos[0] + self.vel[0] * 10)
        y2 = int(self.pos[1] + self.vel[1] * 10)
        pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), self.size)


# Set up the display window
window_width = 1280
window_height = 1000
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Particle Effects")

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
particles = []
max_particles = 300000
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

    # Clear the screen
    screen.fill((0,0,0))

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

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

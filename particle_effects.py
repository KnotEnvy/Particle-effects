import pygame
import random

class Particle:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.vel = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.size = random.randint(5, 10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.life = 100

    def update(self):
        self.life -= 1
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)

# Set up the display window
window_width = 1280
window_height = 1000
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Particle Effects")

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
particles = []
max_particles = 10000
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear the screen
    screen.fill((0,0,0))

    # Create new particles
    if pygame.mouse.get_pressed()[0] and len(particles) < max_particles:
        for i in range(10):
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



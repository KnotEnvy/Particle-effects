import pygame
import random
import taichi as ti

ti.init(arch=ti.gpu)

@ti.func
def update_particle(pos, vel, mouse_pos):
    # Update the position of the particle
    pos[0] += vel[0]
    pos[1] += vel[1]
    # Update the velocity of the particle based on the current position of the mouse
    dx = mouse_pos[0] - pos[0]
    dy = mouse_pos[1] - pos[1]
    angle = ti.atan2(dy, dx)
    speed = ti.sqrt(vel[0]**2 + vel[1]**2)
    vel[0] = -ti.cos(angle) * speed
    vel[1] = -ti.sin(angle) * speed

@ti.kernel
def update_particle_kernel(pos: ti.template(), vel: ti.template(), mouse_pos_x: float, mouse_pos_y: float):
    update_particle(pos, vel, [mouse_pos_x, mouse_pos_y])

class Particle:
    def __init__(self, pos):
        self.pos = ti.Vector([pos[0], pos[1]])
        self.size = random.randint(1, 3)
        self.color = (random.randint(0, 210), random.randint(0, 75), random.randint(0, 100))
        self.life = 500
        # Set the initial velocity of the particle
        speed = random.uniform(2, 4)
        self.vel = ti.Vector([random.uniform(-speed, speed), random.uniform(-speed, speed)])

    def update(self):
        self.life -= 1
        mouse_pos = pygame.mouse.get_pos()
        update_particle_kernel(self.pos, self.vel, mouse_pos[0], mouse_pos[1])

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
max_particles = 3000
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
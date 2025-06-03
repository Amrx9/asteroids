import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        """Create a new asteroid at position (x, y) with given radius."""
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        """Draw the asteroid as a white circle outline."""
        pygame.draw.circle(screen, "white", self.position, self.radius, width=2)
    
    def update(self, dt):
        """Update asteroid position based on velocity."""
        self.position += (self.velocity * dt)
        
    def split(self):
        """Split asteroid into two smaller pieces, or destroy if too small."""
        # Remove this asteroid from all groups
        self.kill()

        # If asteroid is already minimum size, don't create smaller ones
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Create random angle for splitting
        split_angle = random.uniform(20, 50)
        
        # Calculate velocities for the two new asteroids
        velocity_1 = self.velocity.rotate(split_angle)
        velocity_2 = self.velocity.rotate(-split_angle)

        # Calculate new radius (smaller than original)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Create first smaller asteroid
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1.velocity = velocity_1 * 1.2  # Make it slightly faster
        
        # Create second smaller asteroid
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2.velocity = velocity_2 * 1.2  # Make it slightly faster
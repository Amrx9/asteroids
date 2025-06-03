import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    # Define screen edges where asteroids can spawn
    edges = [
        # Left edge (moving right)
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # Right edge (moving left)
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        # Top edge (moving down)
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        # Bottom edge (moving up)
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        """Create a new asteroid field manager."""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def create_asteroid(self, radius, position, velocity):
        """Create a new asteroid with given properties."""
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        return asteroid

    def get_random_spawn_properties(self):
        """Generate random properties for a new asteroid."""
        # Choose random edge to spawn from
        edge = random.choice(self.edges)
        
        # Generate random speed
        speed = random.randint(40, 100)
        
        # Calculate base velocity direction
        base_velocity = edge[0] * speed
        
        # Add random rotation to velocity
        velocity = base_velocity.rotate(random.randint(-30, 30))
        
        # Generate random position along chosen edge
        position = edge[1](random.uniform(0, 1))
        
        # Generate random asteroid size
        size_multiplier = random.randint(1, ASTEROID_KINDS)
        radius = ASTEROID_MIN_RADIUS * size_multiplier
        
        return radius, position, velocity

    def should_spawn_asteroid(self):
        """Check if it's time to spawn a new asteroid."""
        return self.spawn_timer > ASTEROID_SPAWN_RATE

    def update(self, dt):
        """Update the asteroid field, spawning new asteroids when needed."""
        # Update spawn timer
        self.spawn_timer += dt
        
        # Check if we should spawn a new asteroid
        if self.should_spawn_asteroid():
            # Reset timer
            self.spawn_timer = 0
            
            # Get random properties for new asteroid
            radius, position, velocity = self.get_random_spawn_properties()
            
            # Create the asteroid
            self.create_asteroid(radius, position, velocity)
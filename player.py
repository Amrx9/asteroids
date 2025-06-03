import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        """Create a new player at position (x, y)."""
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0

    def triangle(self):
        """Calculate the three points of the player's triangle shape."""
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        
        # Calculate triangle points
        point_a = self.position + forward * self.radius
        point_b = self.position - forward * self.radius - right
        point_c = self.position - forward * self.radius + right
        
        return [point_a, point_b, point_c]
    
    def draw(self, screen):
        """Draw the player as a white triangle."""
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        """Rotate the player based on turn speed and delta time."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        """Move the player forward based on current rotation."""
        forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward_direction * PLAYER_SPEED * dt

    def shoot(self):
        """Create a new shot if cooldown has expired."""
        if self.shoot_timer > 0:
            return  # Still cooling down
        
        # Reset shoot timer
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        
        # Create new shot at player position
        shot = Shot(self.position.x, self.position.y)
        
        # Set shot velocity based on player rotation
        shot_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = shot_direction * PLAYER_SHOOT_SPEED

    def handle_input(self, dt):
        """Handle keyboard input for player movement and actions."""
        keys = pygame.key.get_pressed()
        
        # Movement controls
        if keys[pygame.K_w]: 
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Rotation controls
        if keys[pygame.K_a]: 
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Shooting control
        if keys[pygame.K_SPACE]:
            self.shoot()

    def update(self, dt):
        """Update player state each frame."""
        # Handle player input
        self.handle_input(dt)
        
        # Update shoot cooldown timer
        self.shoot_timer -= dt
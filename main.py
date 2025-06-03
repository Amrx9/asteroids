import sys
import pygame
from player import Player
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def initialize_game():
    """Set up pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game")
    clock = pygame.time.Clock()
    return screen, clock

def create_sprite_groups():
    """Create and return all sprite groups needed for the game."""
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    return updatable, drawable, asteroids, shots

def setup_containers(updatable, drawable, asteroids, shots):
    """Set up sprite containers for each game object type."""
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)

def create_game_objects():
    """Create and return the initial game objects."""
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    return player, asteroid_field

def handle_events():
    """Handle pygame events. Returns True if game should continue."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def check_collisions(player, asteroids, shots):
    """Check for collisions between game objects."""
    # Check player-asteroid collisions
    for asteroid in asteroids:
        if asteroid.collision(player):
            print("Game Over!")
            print("Thanks for playing!")
            return False
    
    # Check shot-asteroid collisions
    for shot in shots:
        for asteroid in asteroids:
            if shot.collision(asteroid):
                shot.kill()
                asteroid.split()
                break  # Shot is destroyed, move to next shot
    
    return True

def update_display(screen, drawable):
    """Clear screen and draw all sprites."""
    screen.fill("black")
    
    for sprite in drawable:
        sprite.draw(screen)
    
    pygame.display.flip()

def main():
    """Main function to run the asteroid game."""
    # Initialize pygame and create game window
    screen, clock = initialize_game()
    
    # Create sprite groups
    updatable, drawable, asteroids, shots = create_sprite_groups()
    
    # Set up sprite containers
    setup_containers(updatable, drawable, asteroids, shots)
    
    # Create game objects
    player, asteroid_field = create_game_objects()
    
    # Main game loop
    dt = 0
    print("Asteroid Game Started!")
    print("Controls: WASD to move, SPACE to shoot")
    
    while True:
        # Handle events
        if not handle_events():
            break
        
        # Update all game objects
        updatable.update(dt)
        
        # Check collisions
        if not check_collisions(player, asteroids, shots):
            break
        
        # Update display
        update_display(screen, drawable)
        
        # Control frame rate
        dt = clock.tick(60) / 1000
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
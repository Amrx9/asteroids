import sys
import pygame
from player import *
from constants import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)

    player = Player(SCREEN_WIDTH/ 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    dt = 0

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                sys.exit()
        
            for bullet in shots:
                if bullet.collision(asteroid):
                    bullet.kill()
                    asteroid.split()

        screen.fill("black")

        for sprite in drawable:
            sprite.draw(screen)
        
        pygame.display.flip()
        dt = fps.tick(60) / 1000


if __name__ == "__main__":
    main()

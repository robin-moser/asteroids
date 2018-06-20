import pygame
from pygame.locals import *
from math import *
import random
import traceback

import spaceship
import asteroid

# Init screen
screen_size = [640, 480]

pygame.display.init()
pygame.font.init()

pygame.display.set_caption("Asteroids")
icon = pygame.Surface((1, 1))
icon.set_alpha(0)
pygame.display.set_icon(icon)
surface = pygame.display.set_mode(screen_size)

fonts = {
    16 : pygame.font.SysFont("Monosans",20,False),
    32 : pygame.font.SysFont("Monosans",32,False)
}

asteroid_count = 10

def start_game():

	global ship, asteroids
	ship = spaceship.Spaceship([screen_size[0]/2.0, screen_size[1]/2.0])

	asteroids = []
	add_asteroid(asteroid_count)


def add_asteroid(n=1):
	for i in range(n):
		asteroids.append(asteroid.Asteroid([
			random.randint(0, screen_size[0]),
			random.randint(0, screen_size[1])
		]))


def get_input(dt):

	keys_pressed = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT:
			return False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				return False

	if keys_pressed[K_LEFT]:
		ship.angle += 3.0

	if keys_pressed[K_RIGHT]:
		ship.angle -= 3.0

	if keys_pressed[K_UP]:
		ship.velocity[0] += dt * spaceship.Spaceship.speed * sin(radians(ship.angle))
		ship.velocity[1] += dt * spaceship.Spaceship.speed * cos(radians(ship.angle))

	if keys_pressed[K_DOWN]:
		ship.velocity[0] *= 0.99
		ship.velocity[1] *= 0.99

	if keys_pressed[K_SPACE]:
		ship.shoot()
	return True


def update(dt):

	ship.update(dt, screen_size)
	ship.collide_bullets(asteroids, dt)

	if len(asteroids) < asteroid_count:
		add_asteroid(1)

	for obj in asteroids:
		obj.update(dt, screen_size)
		
	return True


def draw():
	surface.fill((0, 0, 0))
	ship.draw(surface)

	for astro in asteroids:
		astro.draw(surface)

	surf_fps = fonts[16].render("FPS: "+str(round(clock.get_fps(),1)), True, (255,255,255))
	surface.blit(surf_fps,(screen_size[0]-surf_fps.get_width()-10,screen_size[1]-surf_fps.get_height()-10))

	surf_score = fonts[16].render("Score: "+str(ship.score), True, (255,255,255))
	surface.blit(surf_score,(screen_size[0]-surf_score.get_width()-10,10))


	pygame.display.flip()


def main():
	global clock

	target_fps = 60
	dt = 1.0/float(target_fps)

	start_game()
	clock = pygame.time.Clock()

	while True:
		if not get_input(dt):
			break
		if not update(dt):
			break
		draw()
		clock.tick(target_fps)
	pygame.quit()


if __name__ == "__main__":
	try:
		main()
	except:
		traceback.print_exc()
		pygame.quit()
		input()

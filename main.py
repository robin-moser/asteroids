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
screen = pygame.display.set_mode(screen_size)

surface = screen
surface = pygame.Surface(screen_size, 0, 32)

surface.fill((0, 0, 0, 255))

fonts = {
	16: pygame.font.SysFont("Monosans", 20, False),
	32: pygame.font.SysFont("Monosans", 32, False)
}


def start_game():
	global ship, asteroids, asteroid_count, remove_timeout
	ship = spaceship.Spaceship([screen_size[0] / 2.0, screen_size[1] / 2.0])

	asteroid_count = 10
	remove_timeout = 1
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
	global asteroid_count, ship, remove_timeout

	ship.update(dt, screen_size)
	ship.collide_bullets(asteroids, dt)
	ship.collide_asteroids(asteroids)
	ship.collide_ship(screen_size, asteroids)

	asteroid_count = round(ship.score / 2000 + 10)

	if len(asteroids) < asteroid_count and ship.lives:
		add_asteroid(1)

	for obj in asteroids:
		obj.update(dt, screen_size)

	if ship.lives == 0:
		if len(asteroids):
			if remove_timeout > 0:
				remove_timeout -= dt * 10
			else:
				asteroids.remove(asteroids[len(asteroids)-1])
				remove_timeout = 1
		# else:
		#	start_game()

	return True


def draw():
	surface.fill((0, 0, 0))
	ship.draw(surface)

	for astro in asteroids:
		astro.draw(surface)

	surf_fps = fonts[16].render("FPS: " + str(round(clock.get_fps(), 1)), True, (255, 255, 255))
	surface.blit(surf_fps, (screen_size[0] - surf_fps.get_width() - 10, screen_size[1] - 20))

	surf_score = fonts[16].render("Score: " + str(ship.score), True, (255, 255, 255))
	surface.blit(surf_score, (screen_size[0] - surf_score.get_width() - 10, 10))

	surf_life = fonts[16].render("Leben: " + str(ship.lives), True, (255, 255, 255))
	surface.blit(surf_life, (10, 10))

	surf_life = fonts[16].render("Alife: " + str(ship.alife), True, (255, 255, 255))
	surface.blit(surf_life, (10, 50))

	surf_timeout = fonts[16].render("Timeout: " + str(remove_timeout), True, (255, 255, 255))
	surface.blit(surf_timeout, (10, 30))

	surf_count = fonts[16].render("Anzahl: " + str(len(asteroids)), True, (255, 255, 255))
	surface.blit(surf_count, (screen_size[0] - surf_count.get_width() - 10, screen_size[1] - 40))
	screen.blit(surface, (0, 0))

	pygame.display.flip()


def main():
	global clock

	target_fps = 60
	dt = 1.0 / float(target_fps)

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

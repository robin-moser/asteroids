import pygame
from pygame.locals import *
from math import *
import random
import sys
import os
import traceback

import spaceship

# Init screen
screen_size = [640, 480]

pygame.display.init()
pygame.display.set_caption("Asteroids")
icon = pygame.Surface((1, 1))
icon.set_alpha(0)
pygame.display.set_icon(icon)
surface = pygame.display.set_mode(screen_size)


def start_game():

	global ship
	ship = spaceship.Spaceship([screen_size[0]/2.0, screen_size[1]/2.0])


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
	return True


def update(dt):

	ship.update(dt, screen_size)
	return True


def draw():
	surface.fill((0, 0, 0))
	ship.draw(surface)
	pygame.display.flip()


def main():
	global clock

	target_fps = 20
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

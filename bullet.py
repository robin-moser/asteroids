import pygame
from helpers import *

class Bullet(object):
	speed = 500.0

	def __init__(self, position, angle_rad):
		self.position = list(position)
		self.velocity = [
			Bullet.speed * cos(angle_rad),
			Bullet.speed * sin(angle_rad)
		]

		self.time = 0.0

	def update(self, dt):
		self.position[0] += self.velocity[0] * dt
		self.position[1] += self.velocity[1] * dt

		self.time += dt

	def draw(self, surface):
		x, y = rndint(self.position[0]), rndint(self.position[1])
		color = (255, 0, 0)
		pygame.draw.circle(surface, color, (x, y), 2)
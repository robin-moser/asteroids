import pygame

import random
from math import *


class Asteroid:
	speed = 10.0

	def __init__(self, position):

		self.health = 4
		self.radius = 20

		self.timeout = 0
		self.color = (255, 255, 255)
		self.idx = -1

		self.real_points = []
		self.position = list(position)

		self.angle = random.uniform(0.0, 360.0)
		self.scale = random.uniform(1.0, 1.5)
		self.velocity = [
			Asteroid.speed * random.uniform(-2.0, 2.0),
			Asteroid.speed * random.uniform(-2.0, 2.0)
		]

		self.rel_points = [
			[0, random.uniform(1.0, 1.5)],
			[45, random.uniform(1.0, 1.5)],
			[90, random.uniform(1.0, 1.5)],
			[135, random.uniform(1.0, 1.5)],
			[180, random.uniform(1.0, 1.5)],
			[225, random.uniform(1.0, 1.5)],
			[270, random.uniform(1.0, 1.5)],
			[315, random.uniform(1.0, 1.5)]
		]

		for i in range(len(self.rel_points)):
			self.rel_points[i] = (radians(self.rel_points[i][0]), self.scale * self.rel_points[i][1])

	def hit(self):
		self.health -= 1
		self.radius -= 3

	def collide_timeout(self, idx):
		if self.timeout == 0 and idx != self.idx:
			self.velocity[0] *= -1.0
			self.velocity[1] *= -1.0

			self.timeout = 60
			self.idx = idx

	def update(self, dt, screen_size):

		self.position[0] += self.velocity[0] * dt
		self.position[1] += self.velocity[1] * dt
		
		if self.position[0] < 0:
			self.position[0] = 0
			self.velocity[0] *= -1.0
		elif self.position[0] > screen_size[0]:
			self.position[0] = screen_size[0]
			self.velocity[0] *= -1.0
		if self.position[1] < 0:
			self.position[1] = 0
			self.velocity[1] *= -1.0
		elif self.position[1] > screen_size[1]:
			self.position[1] = screen_size[1]
			self.velocity[1] *= -1.0

		if self.timeout > 0:
			self.timeout -= 1

		self.real_points = []

		for point_angle, point_radius in self.rel_points:
			angle = radians(self.angle) + point_angle
			xp = point_radius * sin(angle) * self.radius
			yp = point_radius * cos(angle) * self.radius
			self.real_points.append((
				self.position[0] + xp,
				self.position[1] + yp
			))

	def draw(self, surface):
		pygame.draw.aalines(surface, self.color, True, self.real_points)

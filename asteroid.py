import pygame

import random
from math import *


class Asteroid:
	speed = 10.0

	def __init__(self, position):
		self.position = list(position)
		self.velocity = [
			Asteroid.speed * random.uniform(-2.0, 2.0),
			Asteroid.speed * random.uniform(-2.0, 2.0)
		]
		self.real_points = []

		self.rel_points = [[0, 20], [45, 20], [90, 20], [135, 20], [180, 20], [225, 20], [270, 20], [315, 20]]
		scale = random.uniform(1.0, 1.5)
		
		for i in range(len(self.rel_points)):
			self.rel_points[i] = (radians(self.rel_points[i][0]), scale * self.rel_points[i][1])

		self.angle = random.uniform(0.0, 360.0)

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

		self.real_points = []

		for point_angle, point_radius in self.rel_points:
			angle = radians(self.angle) + point_angle
			xp = point_radius * sin(angle)
			yp = point_radius * cos(angle)
			self.real_points.append((
				self.position[0] + xp,
				self.position[1] + yp
			))

	def draw(self, surface):

		color = (255, 255, 255)
		pygame.draw.aalines(surface, color, True, self.real_points)

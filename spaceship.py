import pygame
from math import *

import bullet


class Spaceship:

	speed = 300.0

	def __init__(self, position):

		self.score = 0

		self.position = list(position)
		self.velocity = [1.0, 0.0]
		self.angle = 180.0
		self.fire_timeout = 8
		self.real_points = []

		self.bullets = []
		self.fire = 0

		self.rel_points = [[0, 20], [-140, 20], [180, 7.5], [140, 20]]
		scale = 0.6
		for i in range(len(self.rel_points)):
			self.rel_points[i] = (radians(self.rel_points[i][0]), scale*self.rel_points[i][1])

	def shoot(self):
		if self.fire == 0:
			angle_rad = radians(-self.angle + 90)
			pos = [
				self.position[0] + 7.5 * cos(angle_rad),
				self.position[1] + 7.5 * sin(angle_rad)
			]
			self.bullets.append(bullet.Bullet(pos, angle_rad))
			self.fire = self.fire_timeout

	def collide_bullets(self, asteroids, dt):
		for bullet in self.bullets:
			for asteroid in asteroids:
				if (abs(round(asteroid.position[0]) - round(bullet.position[0]))) <= asteroid.scale * asteroid.radius and\
				   (abs(round(asteroid.position[1]) - round(bullet.position[1]))) <= asteroid.scale * asteroid.radius:
					asteroid.hit()
					self.score += 10

					if asteroid.health == 0:
						asteroids.remove(asteroid)
						self.score += 50
					if bullet in self.bullets:
						self.bullets.remove(bullet)

	@staticmethod
	def collide_asteroids(asteroids):
		for idx1, asteroid1 in enumerate(asteroids):
			for idx2, asteroid2 in enumerate(asteroids):

				if (idx1 != idx2) and\
					(abs(asteroid1.position[0] - asteroid2.position[0])) \
					<= asteroid1.scale * asteroid1.radius + asteroid2.scale * asteroid2.radius and \
					(abs(asteroid1.position[1] - asteroid2.position[1])) \
					<= asteroid1.scale * asteroid1.radius + asteroid2.scale * asteroid2.radius:

					asteroid1.collide_timeout(idx2)
					asteroid2.collide_timeout(idx1)
	def update(self, dt, screen_size):

		self.position[0] += self.velocity[0] * dt
		self.position[1] += self.velocity[1] * dt

		if self.position[0] < 0:
			self.position[0] = 0
			self.velocity[0] *= -0.5
		elif self.position[0] > screen_size[0]:
			self.position[0] = screen_size[0]
			self.velocity[0] *= -0.5
		if self.position[1] < 0:
			self.position[1] = 0
			self.velocity[1] *= -0.5
		elif self.position[1] > screen_size[1]:
			self.position[1] = screen_size[1]
			self.velocity[1] *= -0.5

		if self.fire > 0:
			self.fire -= 1
		self.real_points = []

		for point_angle, point_radius in self.rel_points:
			angle = radians(self.angle) + point_angle
			xp = point_radius * sin(angle)
			yp = point_radius * cos(angle)
			self.real_points.append((
				self.position[0] + xp,
				self.position[1] + yp
			))

		for b in self.bullets:
			b.update(dt)
			if b.time > 5.0:
				self.bullets.remove(b)
				continue

	def draw(self, surface):
		for b in self.bullets:
			b.draw(surface)

		color = (255, 255, 0)
		pygame.draw.aalines(surface, color, True, self.real_points)

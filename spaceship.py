import pygame
from math import *

import random
import bullet


class Spaceship:

	speed = 300.0

	def __init__(self, position):

		self.score = 0
		self.lives = 3
		self.alive = True
		self.dying = 0
		self.invincible = 3

		self.position = list(position)
		self.velocity = [1.0, 0.0]
		self.angle = 180.0
		
		self.fire_timeout = 6
		self.reload_timeout = 50
		self.reload_amount = 50

		self.real_points = []

		self.color = (255, 255, 0)
		self.bullets = []
		self.fire_to = 0
		self.fire_rl = self.reload_amount

		self.rel_points = [[0, 20], [-140, 20], [180, 7.5], [140, 20]]
		scale = 0.6
		for i in range(len(self.rel_points)):
			self.rel_points[i] = (radians(self.rel_points[i][0]), scale*self.rel_points[i][1])

	def shoot(self):
		if self.fire_to <= 0 and self.fire_rl > 0:

			accuracy = (abs(self.velocity[0]) + abs(self.velocity[1])) / 50
			angle_rad = radians(-self.angle + random.uniform(90-accuracy,90+accuracy))
			pos = [
				self.position[0] + 7.5 * cos(angle_rad),
				self.position[1] + 7.5 * sin(angle_rad)
			]
			self.bullets.append(bullet.Bullet(pos, angle_rad))
			self.fire_to = self.fire_timeout
			self.fire_rl -= 1

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

	def collide_ship(self, screen_size, asteroids):
		if self.dying <= 0 and not self.invincible > 0:
			for asteroid in asteroids:
				if (abs(round(asteroid.position[0]) - round(self.position[0]))) <= asteroid.scale * asteroid.radius and \
					(abs(round(asteroid.position[1]) - round(self.position[1]))) <= asteroid.scale * asteroid.radius:
					self.lives -= 1
					self.position = ([screen_size[0] / 2.0, screen_size[1] / 2.0])
					self.velocity = [0.0, 0.0]

					self.alive = False
					self.dying = 1

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

		if not self.alive and self.lives > 0:
			self.dying -= dt
			if self.dying <= 0:
				self.alive = True
				self.invincible = 2

		if self.invincible > 0:
			self.invincible -= dt

		if self.fire_to > 0:
			self.fire_to -= 1

		if self.fire_rl <= 0:
			self.fire_rl -= 1
			if self.fire_rl == -self.reload_timeout:
				self.fire_rl = self.reload_amount

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

		if self.alive:
			if not self.invincible  % 0.1 < 0.03:
				pygame.draw.aalines(surface, self.color, True, self.real_points)

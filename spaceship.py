import pygame
from math import *

class Spaceship:
	
	def __init__(self, position):

		self.position = list(position)
		self.velocity = [1.0,0.0]
		self.angle = 180.0

		self.rel_points = [[0, 20], [-140, 20], [180, 7.5], [140, 20]]
		scale = 0.6
		for i in range(len(self.rel_points)):
			self.rel_points[i] = (radians(self.rel_points[i][0]),scale*self.rel_points[i][1])
		
	def update(self, dt, screen_size):
		
		self.real_points = []
		for point_angle,point_radius in self.rel_points:
			angle = radians(self.angle) + point_angle
			xp = point_radius * sin(angle)
			yp = point_radius * cos(angle)
			self.real_points.append((
				self.position[0] + xp,
				self.position[1] + yp
			))

	def draw(self, surface):

		color = (255,255,255)
		pygame.draw.aalines(surface,color,True,self.real_points)
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
	32: pygame.font.SysFont("Monosans", 32, False),
	64: pygame.font.SysFont("Monosans", 64, False)
}


def start_game():
	global ship, asteroids, asteroid_count, remove_timeout, status, opacity
	ship = spaceship.Spaceship([screen_size[0] / 2.0, screen_size[1] / 2.0])

	asteroid_count = 10
	remove_timeout = 1
	opacity = 0

	status = 0
	updatestatus(0)
	asteroids = []
	add_asteroid(asteroid_count)

def load_highscore():
	global highscore
	try:
		f = open("highscore.txt","rb")
		highscore = int(f.read())
		f.close()
	except:
		highscore = 0

def write_highscore():
	f = open("highscore.txt","wb")
	f.write(str(highscore).encode())
	f.close()

def add_asteroid(n=1):
	for i in range(n):

		speed = 10 + ship.score / 1000
		ship_radius = 150

		pos1 = random.randint(0, screen_size[0])
		pos2 = random.randint(0, screen_size[1])

		while abs(pos1 - ship.position[0]) < ship_radius \
		and abs(pos2 - ship.position[1]) < ship_radius:

			pos1 = random.randint(0, screen_size[0])
			pos2 = random.randint(0, screen_size[1])

		asteroids.append(asteroid.Asteroid([
			pos1,
			pos2
		],speed))

def get_input(dt):
	keys_pressed = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == QUIT:
			return False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				return False
	if not status:
		if keys_pressed[K_LEFT] or keys_pressed[K_a]:
			ship.angle += 3.5

		if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
			ship.angle -= 3.5

		if keys_pressed[K_UP]  or keys_pressed[K_w]:
			ship.velocity[0] += dt * spaceship.Spaceship.speed * sin(radians(ship.angle))
			ship.velocity[1] += dt * spaceship.Spaceship.speed * cos(radians(ship.angle))

		if keys_pressed[K_DOWN] or keys_pressed[K_s]:
			ship.velocity[0] *= 0.99
			ship.velocity[1] *= 0.99

		if keys_pressed[K_SPACE]:
			ship.shoot()
	elif (status ==	 2):
		if keys_pressed[K_SPACE]:
				start_game()

	return True


def updatestatus(st):
	global status, opacity

	if (status != st):
		status = st
		opacity = 0


def update(dt):
	global asteroid_count, ship, remove_timeout, highscore

	ship.update(dt, screen_size)
	ship.collide_bullets(asteroids, dt)
	#ship.collide_asteroids(asteroids)
	ship.collide_ship(screen_size, asteroids)

	asteroid_realcount = round(asteroid_count + ship.score / 2000)

	if len(asteroids) < asteroid_realcount and ship.lives:
		add_asteroid(1)

	for obj in asteroids:
		obj.update(dt, screen_size)

	if ship.score > highscore:
		highscore = ship.score

	if ship.lives == 0:
		if not status:
			updatestatus(1)
		if len(asteroids):
			if remove_timeout > 0:
				remove_timeout -= dt * 10
			else:
				asteroids.remove(asteroids[len(asteroids)-1])
				remove_timeout = 1
		else:
			updatestatus(2)
	return True


def draw():
	global opacity, status, highscore
	surface.fill((0, 0, 0))
	
	for astro in asteroids:
		astro.draw(surface)

	ammo = str("")
	ammorefill = str("")

	for i in range(ship.fire_rl):
		ammo += "I"
		
	for i in range(-ship.fire_rl):
		ammorefill += "-"

	if not status:

		ship.draw(surface)

		surf_fps = fonts[16].render("FPS: " + str(round(clock.get_fps(), 1)), True, (255, 255, 255))
		surface.blit(surf_fps, (screen_size[0] - surf_fps.get_width() - 10, screen_size[1] - 20))

		surf_score = fonts[16].render("Score: " + str(ship.score), True, (255, 255, 255))
		surface.blit(surf_score, (screen_size[0] - surf_score.get_width() - 10, 10))

		surf_highscore = fonts[16].render("Highscore: " + str(highscore), True, (255, 255, 255))
		surface.blit(surf_highscore, (screen_size[0] - surf_highscore.get_width() - 10, 30))

		surf_life = fonts[16].render("Leben: " + str(ship.lives), True, (255, 255, 255))
		surface.blit(surf_life, (10, 10))

		surf_count = fonts[16].render("Anzahl: " + str(len(asteroids)), True, (255, 255, 255))
		surface.blit(surf_count, (screen_size[0] - surf_count.get_width() - 10, screen_size[1] - 40))
		
		surface.blit(fonts[16].render((str(ammo)), True, (255, 255, 255)), (100,10))
		surface.blit(fonts[16].render((str(ammorefill)), True, (255, 255, 255)), (100,10))

	else:

		if (opacity < 255):
			opacity += 5

		if (status == 1):
		
			surf_gameover = fonts[32].render("Gameover!", True, (opacity/1.5, opacity/1.5, opacity/1.5))
			surface.blit(surf_gameover, (screen_size[0]/2 - surf_gameover.get_width()/2, screen_size[1]/2 - surf_gameover.get_height()/2))

		else: 

			surf_score = fonts[32].render("Score: " + str(ship.score), True, (opacity/2, opacity/2, opacity))
			surface.blit(surf_score, (screen_size[0]/2 - surf_score.get_width()/2, 60))

			surf_highscore = fonts[32].render("Highscore: " + str(highscore), True, (opacity/2, opacity/2, opacity))
			surface.blit(surf_highscore, (screen_size[0]/2 - surf_highscore.get_width()/2, 90))

			surf_gameover = fonts[32].render("Press Space to restart", True, (opacity/1.5, opacity/1.5, opacity/1.5))
			surface.blit(surf_gameover, (screen_size[0]/2 - surf_gameover.get_width()/2, screen_size[1]/2 - surf_gameover.get_height()/2))

	screen.blit(surface, (0, 0))
	pygame.display.flip()

def main():
	global clock

	load_highscore()

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
	write_highscore()

if __name__ == "__main__":
	try:
		main()
	except:
		traceback.print_exc()
		pygame.quit()
		input()

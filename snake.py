import pygame
from vector import Vector
import numpy as np


class Snake:
    SNAKE_COLOR = pygame.Color(255,255,255)
    TAIL_COLOR = pygame.Color(128,128,128)
    FOOD_COLOR = pygame.Color(255,0,0)

    VELOCITY = 15
    KEY_DIRECTIONS = {
        pygame.K_UP:    Vector( 0,-1),
        pygame.K_DOWN:  Vector( 0, 1),
        pygame.K_RIGHT: Vector( 1, 0),
        pygame.K_LEFT:  Vector(-1, 0),
    }

    WIDTH = 64
    HEIGHT = 48
    SCALE = 10

    def __init__(self):
        pygame.init()
        self.render_surface = pygame.display.set_mode((self.WIDTH*self.SCALE, self.HEIGHT*self.SCALE), 0, 32)
        self.draw_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.draw_surface = self.draw_surface.convert()
        self.draw_surface.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 40)

        self.position = Vector(self.WIDTH//2, self.HEIGHT//2)
        self.velocity = Vector(1, 0)
        self.running = True
        # self.tail = []
        self.tail = [Vector(self.position.x+(-1*n*np.sign(self.position.x)), self.position.y) for n in range(3)]
        self.food = [Vector.random(self.WIDTH, self.HEIGHT)]

    def draw(self):
        pygame.draw.rect(self.draw_surface, self.SNAKE_COLOR, (*self.position, 1,1))
        for tail in self.tail:
            pygame.draw.rect(self.draw_surface, self.TAIL_COLOR, (*tail, 1, 1))
        for food in self.food:
            pygame.draw.rect(self.draw_surface, self.FOOD_COLOR, (*food, 1, 1))

        pygame.transform.scale(self.draw_surface, (self.WIDTH*self.SCALE, self.HEIGHT*self.SCALE), self.render_surface)

    def update(self):
        newpos = self.position + self.velocity
        if newpos != self.position:
            eaten = False
            for foodindex,foodpos in enumerate(self.food):
                if newpos == foodpos:
                    self.eat(foodindex)
                    eaten = True
            if not eaten:
                if self.tail:
                    self.tail.pop(-1)
                    self.tail.insert(0, self.position.copy())
            else:
                self.tail.insert(0, self.position.copy())
                # if len(self.tail) % 5 == 0:
                #     self.VELOCITY += 2
                # self.VELOCITY += 1
            self.position = newpos
            if self.position in self.tail:
                pygame.quit()
            if ([0,0] > self.position).any() or ([self.WIDTH, self.HEIGHT] <= self.position).any():
                pygame.quit()

    def eat(self, i):
        self.food.pop(i)
        self.food.append(Vector.random(self.WIDTH, self.HEIGHT))

    def run(self):
        while self.running:
            keypressed = False
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    break
                elif evnt.type == pygame.KEYDOWN and not keypressed:
                    if evnt.key in self.KEY_DIRECTIONS:
                        keypressed = True
                        newvel = self.KEY_DIRECTIONS[evnt.key]
                        if not np.equal(newvel, self.velocity).any():
                            self.velocity = newvel
            self.draw_surface.fill((0,0,0))
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.VELOCITY)


if __name__ == '__main__':
    snake = Snake()
    snake.run()

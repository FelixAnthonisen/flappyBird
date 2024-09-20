import pygame
from math import pi
import entities
from collisions import is_colliding
from random import randint
import time


bird_width = 40
bird_height = 28.5
pipe_width = 50
pipe_height = (1499 / 244) * pipe_width
gap = 130
pipe_vel = -1
pipes = []
has_started = False


def generate_pipe_pair(width, gap, pipes):
    h1 = randint(50, 300)
    pipes.append(entities.Entity(900, 0, pipe_vel, width, h1))
    pipes.append(entities.Entity(900, h1 + gap, pipe_vel, width, 504 - (h1 + gap)))


def restart(p):
    p.x_pos = 100
    p.y_pos = 300
    p.x_vel = 0
    p.y_vel = 0
    p.is_dead = False
    global has_started
    has_started = False
    pipes.clear()


generate_pipe_pair(pipe_width, gap, pipes)
p = entities.Player(100, 300, 0, bird_width, bird_height)

pygame.init()
screen = pygame.display.set_mode((900, 504))
done = False
background = pygame.image.load("Images/background.png")
# 12*17, 630*450
bird = pygame.image.load("Images/bird.png")
bird = pygame.transform.scale(bird, (bird_width, bird_height))
pipe_img = pygame.image.load("Images/pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, pipe_height))
pipeR_img = pygame.image.load("Images/pipeR.png")
pipeR_img = pygame.transform.scale(pipeR_img, (pipe_width, pipe_height))

while not done:
    if not has_started:
        for event in pygame.event.get():
            if event.type == 768:
                has_started = True
                p.jump()
                continue
        screen.blit(background, (0, 0))
        screen.blit(bird, (p.x_pos, p.y_pos))
        pygame.display.flip()
        continue
    if p.y_pos < 0:
        p.y_pos = 0
        p.y_vel = 0
    elif p.y_pos >= 504 - bird_height:
        p.y_pos = 504 - bird_height
        p.y_vel = 0
        p.is_dead = True
    else:
        p.fall()

    p.update_pos()
    for pipe in pipes:
        pipe.update_pos()
        if is_colliding(pipe, p):
            p.is_dead = True
            continue
    # remove pipes that go off screen
    if pipes[0].x_pos < 0:
        pipes.pop(0)
        pipes.pop(0)

    # generate new pipes
    if pipes[len(pipes) - 1].x_pos < 700:
        generate_pipe_pair(pipe_width, gap, pipes)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if (
            event.type == pygame.KEYDOWN
            and not p.is_dead
            and event.key == pygame.K_SPACE
        ):
            p.jump()

        if event.type == pygame.KEYDOWN and p.is_dead and event.key == pygame.K_r:
            restart(p)
            generate_pipe_pair(pipe_width, gap, pipes)
            continue

    screen.blit(background, (0, 0))
    # rotate bird
    if p.is_dead:
        screen.blit(pygame.transform.rotate(bird, -90), (p.x_pos, p.y_pos))
    else:
        if p.y_vel < 0:
            screen.blit(pygame.transform.rotate(bird, 20), (p.x_pos, p.y_pos))
        elif p.y_vel > 0:
            screen.blit(pygame.transform.rotate(bird, -20), (p.x_pos, p.y_pos))
        else:
            screen.blit(bird, (p.x_pos, p.y_pos))

    # bird hitbox
    # pygame.draw.circle(screen, (0, 0, 0), [p.centre[0], p.centre[1]], p.radius)
    # pipe hitbox
    for i, pipe in enumerate(pipes):
        if i % 2:
            screen.blit(pipe_img, (pipe.x_pos, pipe.y_pos))
        else:
            screen.blit(pipeR_img, (pipe.x_pos, pipe.height - pipe_height))
        # pygame.draw.rect(screen, (255, 0, 0), [pipe.x_pos, pipe.y_pos, pipe.width, pipe.height], 2)

    pygame.display.flip()
    time.sleep(0.004)

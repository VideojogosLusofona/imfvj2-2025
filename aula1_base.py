import pygame
import math
from pygame.math import Vector2
import numpy as np
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Window")
clock = pygame.time.Clock()
running = True
myPosition=pygame.Vector2(320,240)
myVelocity=pygame.Vector2(1,0)

mySpeed=10

image = pygame.image.load("head.png")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    screen.fill((0,0,0)) 
    
    target=Vector2( pygame.mouse.get_pos() )
    dir = target - myPosition 
    velocity = dir.normalize() * mySpeed
    travagem = 80

    if (dir.length()<travagem):
        velocity=velocity/dir.length()

    myPosition=myPosition+velocity
 
    pygame.draw.circle(screen,(255,0,0), target, 20 )
    pygame.draw.circle(screen,(255,0,0), target, 20 + travagem, 1 )
    pygame.draw.circle(screen,(0,255,0), myPosition, 20 )
    angulo = math.atan2( target.y - myPosition.y, target.x - myPosition.x)
    angulo_em_graus=math.degrees(angulo) 
    angulo_em_graus=round(angulo_em_graus) 
    rotimage = pygame.transform.rotate(image,-angulo_em_graus)

    rect = rotimage.get_rect(center=(myPosition.x, myPosition.y))
    screen.blit(rotimage,rect) #Roda
    pygame.display.flip()
    clock.tick(30)
pygame.quit()

import pygame
import math
import random
from pygame.math import Vector2
import numpy as np
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Window")
clock = pygame.time.Clock()
running = True
myPosition=pygame.Vector2(320,240)
mySpeed=2

#Generate a random initial direction
angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
myVelocity = Vector2(math.cos(angle), math.sin(angle)) * mySpeed  # Convert to velocity


image = pygame.image.load("head.png")
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        myVelocity+=Vector2(-1,0)
    if keys[pygame.K_RIGHT]:
        myVelocity+=Vector2(1,0)
    if keys[pygame.K_UP]:
        myVelocity+=Vector2(0,-1)
    if keys[pygame.K_DOWN]:
        myVelocity+=Vector2(0,1)
      
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    if(myPosition.x>WIDTH)or(myPosition.x<0):
        myVelocity.x*=-1
    if(myPosition.y>HEIGHT)or(myPosition.y<0):
        myVelocity.y*=-1

    screen.fill((0,0,0)) 
    
     # Calculate the forward vector based on the current velocity
    forward_vector = myVelocity.normalize()
    dir = forward_vector
    velocity = dir.normalize() * mySpeed
    travagem = 80

   # if (dir.length()<travagem):
   #     velocity=velocity/dir.length()

    myPosition=myPosition+velocity
 
   # pygame.draw.circle(screen,(255,0,0), target, 20 )
   # pygame.draw.circle(screen,(255,0,0), target, 20 + travagem, 1 )
   # pygame.draw.circle(screen,(0,255,0), myPosition, 20 )
    angulo = math.atan2( forward_vector.y - 0, forward_vector.x - 0)
    angulo_em_graus=math.degrees(angulo) 
    angulo_em_graus=round(angulo_em_graus) 
    rotimage = pygame.transform.rotate(image,-angulo_em_graus)

    rect = rotimage.get_rect(center=(myPosition.x, myPosition.y))
    screen.blit(rotimage,rect) #Roda
    pygame.display.flip()
    clock.tick(30)
pygame.quit()

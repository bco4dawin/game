from pygame import *
from sys import exit

width, height = 800, 400
init()
screen = display.set_mode((width, height))
display.set_caption("Test")
clock = time.Clock()
funt = font.Font('Pixeltype.ttf', 50)

back = Surface((800,400))
back.fill("Black")
bg = image.load('Assets/CXcV8Yh.png').convert_alpha()
ground = image.load('Assets/ground.png').convert_alpha()
txt = funt.render("Test Run", False, "Green")
enemy = image.load("Assets/enemy.png").convert_alpha()
enemy_posX = 800
enemy_posY = 250
brr = 1

while True:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            exit()

    screen.blit(back, (0,0))
    screen.blit(bg, (0, -460))
    screen.blit(ground, (0, 165))
    screen.blit(txt, (340, 100))
    enemy_posX -= 2
    if enemy_posY >= 200 and enemy_posY <= 250 and brr == 0:
        enemy_posY += 1
        if enemy_posY >= 250:
            brr = 1
    elif enemy_posY <= 250 and enemy_posY >= 200 and brr == 1:
        enemy_posY -= 1
        if enemy_posY <= 200:
            brr = 0


    
        
    if enemy_posX < -100: 
        enemy_posX = 800
    screen.blit(enemy, (enemy_posX, enemy_posY))

    display.update()
    clock.tick(60)
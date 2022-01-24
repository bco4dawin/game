import pygame, math
from sys import exit
import random

sWidth, sHeight = 1200, 600
clock = pygame.time.Clock()

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

pygame.init()

screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption("Dungeon Echos")

#font
font = pygame.font.Font("Pixeltype.ttf", 50)


#Player 
playerArr = []
for i in range(6):
    img = pygame.image.load(f'Assets/Adventurer/Individual Sprites/adventurer-run-0{i}.png')
    rect = img.get_rect()
    img = pygame.transform.scale(img, (rect.width * 3, rect.height * 3))
    playerArr.append(img)

idle = pygame.image.load(f'Assets/Adventurer/Individual Sprites/adventurer-idle-00.png')
rect = idle.get_rect()
idle = pygame.transform.scale(idle, (rect.width * 3, rect.height * 3))

sheet = pygame.image.load('Assets/wizard.png').convert_alpha()
cell = []

for i in range(10):
    w, h = 80, 80
    rect = pygame.Rect(i * w, 0, w, h)
    image = pygame.Surface(rect.size).convert()
    image.blit(sheet, (0,0), rect)
    alpha = image.get_at((0, 0))
    image.set_colorkey(alpha)
    cell.append(image)



bg = pygame.image.load('Assets/bg.png').convert()
rect = bg.get_rect()
bg = pygame.transform.scale(bg, (1200, 600))
x = 0

runningCount = 0
hor = 100
isJump = False
jumpCount = 15
pHeight = 2 * (sHeight /3) + 10
score = 0
run = 0
enemyPres = 0
enemyCount = 0
enemyX = [900, 980]
enemyH = 2 * (sHeight /3) + 20
enemyC = 0
n = random.randint(0, 2)

while True:

    global obstacles
    obstacles = []
    events()

    if run:
        rel_x = x % bg.get_rect().width
        screen.blit(bg, (rel_x  - bg.get_rect().width,0))
        if rel_x < sWidth:
            screen.blit(bg, (rel_x, 0))
        x -= 5
        
        #Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if hor > -20:
                hor -= 6
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if hor < 1050:
                hor += 6
        if not(isJump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                isJump = True
        else:
            if jumpCount >= -15:
                pHeight -=  jumpCount*2
                jumpCount -= 1
            else: 
                isJump = False
                jumpCount = 15
        
        
        screen.blit(playerArr[math.floor(runningCount)], (hor, pHeight))
        if math.floor(runningCount) == 5:
            runningCount = 0
        else:
            runningCount += 0.15


        scoreTXT = font.render(f'Score: {math.floor(score)}', True, (255,255,255))
        screen.blit(scoreTXT, (500, 10))
        score += 0.25
        

        if not(enemyPres):
            
            for i in range(n):
                screen.blit(cell[math.floor(enemyCount)], (enemyX[i], enemyH))
            enemyPres = 1
            n = random.randint(0, 2)

        else:

            for i in range(2):
                print(enemyH)
                screen.blit(cell[math.floor(enemyCount)], (enemyX[i], enemyH))
                if math.floor(enemyCount) >= 9:
                    enemyCount = 0
                else:
                    enemyCount += 0.15
                if enemyX[i] <= -80:
                    enemyPres = 0
                    enemyX = 1200
                else:
                    enemyX[i] -= 5

    else:

        screen.blit(bg, (0,0))
        screen.blit(idle, (hor, pHeight))
        cover = pygame.Surface((1200, 600))
        cover.set_alpha(150)
        cover.fill((0,0,0))
        screen.blit(cover, (0,0))

        startTXT = font.render("Press [Space] To Start", True, (255,255,255))
        screen.blit(startTXT, (400, 275))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run = 1


    pygame.display.update()
    clock.tick(120)
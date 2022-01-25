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
pygame.mixer.init()


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

for i in range(len(cell)):
    img = cell[i]
    rect = img.get_rect()
    img = pygame.transform.scale(img, (rect.width * 1.5, rect.height * 1.5))
    cell[i] = img



bg = pygame.image.load('Assets/bg.png').convert()
rect = bg.get_rect()
bg = pygame.transform.scale(bg, (1200, 600))
x = 0

runningCount = 0
hor = 100
dt = 0
playerWidth = (playerArr[0].get_rect().width) / 2
playerHeight = 3 * ((playerArr[0].get_rect().height) / 4) - 15
isJump = False
jumpCount = 12
pHeight = 2 * (sHeight /3) + 10
score = 0
run = 1
enemyPres = 1
enemyCount = 0
enemyX = [1000, 1080]
enemyH = 2 * (sHeight /3)
enemyC = 0
loss = False
n = random.randint(1, 2)

pygame.mixer.Channel(0).set_volume(0.1)
pygame.mixer.Channel(0).play(pygame.mixer.Sound('music.mp3'), -1)
while True:


    global obstacles
    obstacles = []
    events()

    if run == 0:
        rel_x = x % bg.get_rect().width
        screen.blit(bg, (rel_x  - bg.get_rect().width,0))
        if rel_x < sWidth:
            screen.blit(bg, (rel_x, 0))
        x -= 0.3 * dt
        
        #Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if hor > -20:
                hor -= 0.5 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if hor < 1050:
                hor += 0.5 * dt
        if not(isJump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                isJump = True
                pygame.mixer.Channel(1).set_volume(0.5)
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('jump.mp3'), 0)
        else:
            if jumpCount >= -12:
                pHeight -=  jumpCount*2
                jumpCount -= 1
            else: 
                isJump = False
                jumpCount = 12
        
        
        screen.blit(playerArr[math.floor(runningCount)], (hor, pHeight))
        if math.floor(runningCount) == 5:
            runningCount = 0
        else:
            runningCount += 0.15


        scoreTXT = font.render(f'Score: {math.floor(score)}', True, (255,255,255))
        screen.blit(scoreTXT, (500, 10))
        score += 0.25

        for i in range(n):
            if i == 0:
                if enemyCount >= 6:
                    newC = 0
                else: 
                    newC = enemyCount + 4
            else: 
                newC = enemyCount
            screen.blit(cell[math.floor(newC)], (enemyX[i], enemyH))
            
            if n == 2:
                if enemyX[1] <= -160:
                    enemyX[0] = 1200
                    enemyX[1] = 1280

                else:
                    enemyX[i] -= 12
            else:
                if enemyX[0] <= -80:
                    enemyX[0] = 1200
                    enemyX[1] = 1280

                else:
                    enemyX[i] -= 12

            if enemyCount >= 9.85:
                enemyCount = 0
            else:
                enemyCount += 0.1
            
        if n == 2:
            if (hor + playerWidth  >= enemyX[0] and hor <= enemyX[1]) and (pHeight + playerHeight >= enemyH + 10 and pHeight <= pHeight + 80):
                loss = True
                run = 1
        else:
            if (hor + playerWidth >= enemyX[0] and hor <= enemyX[0]) and (pHeight + playerHeight >= enemyH + 10 and pHeight <= pHeight + 80):
                loss = True
                run = 1
            
        if enemyX[0] == 1200 :
            n = random.randint(1, 2)

        f = open("scores.txt", "r")
        high = int(f.read())
        f.close()
        if score >= high:
            f = open("scores.txt", "w")
            f.write(str(math.floor(score)))
            f.close()
        else:
            pass
            

    elif loss == True:
        enemyPres = 1
        runningCount = 0
        hor = 100
        isJump = False
        jumpCount = 12
        pHeight = 2 * (sHeight /3) + 10
        enemyCount = 0
        enemyX = [900, 980]
        enemyH = 2 * (sHeight /3)
        enemyC = 0
        dt = 0
        screen.blit(bg, (0,0))
        screen.blit(idle, (hor, pHeight))
        cover = pygame.Surface((1200, 600))
        cover.set_alpha(150)
        cover.fill((0,0,0))
        screen.blit(cover, (0,0))

        startTXT = font.render("You Lost, Press [ENTER] To Restart", True, (255,0,0))
        screen.blit(startTXT, (325, 175))

        cScore = font.render(f"Current Score [{math.floor(score)}]", True, (255,255,255))
        screen.blit(cScore, (425, 225))


        f = open("scores.txt", "r")
        high = int(f.read())
        highScore = font.render(f"Highest Score [{high}]", True, (255,255,255))
        screen.blit(highScore, (425, 275))
        f.close()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            run = 0
            loss = False
            score = 0
    else:

        screen.blit(bg, (0,0))
        screen.blit(idle, (hor, pHeight))
        cover = pygame.Surface((1200, 600))
        cover.set_alpha(150)
        cover.fill((0,0,0))
        screen.blit(cover, (0,0))

        startTXT = font.render("Press [ENTER] To Start", True, (255,255,255))
        screen.blit(startTXT, (400, 275))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            run = 0


    pygame.display.update()
    dt = clock.tick(60)
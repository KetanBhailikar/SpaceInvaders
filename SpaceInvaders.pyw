import pygame
import math
import random
pygame.init()

screenHeight = 600
screenWidth = 800


class enemyBullets():
    def __init__(self, x, y):
        self.posx = x
        self.posy = y

    def travel(self, scr):
        pygame.draw.rect(scr, (255, 255, 255), pygame.Rect(int(self.posx-2.5), int(self.posy), 5, 8))
        self.posy += 0.9


class Bullet:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y

    def travel(self, scr):
        # draw the bullet and move it forward
        pygame.draw.rect(scr, (0, 255, 0), pygame.Rect(int(self.posx-1.5), int(self.posy), 3, 6))
        self.posy -= 0.6


class Player:
    def __init__(self):
        self.posy = screenHeight-60
        self.posx = screenWidth//2
        self.health = 3

    def moveLeft(self):
        self.posx -= 0.6

    def moveRight(self):
        self.posx += 0.6

    def drawPlayer(self, scr, image):
        # restrain the player from going out of the screen
        if self.posx >= screenWidth - 20:
            self.posx = screenWidth - 20
        if self.posx <= 20:
            self.posx = 20
        scr.blit(image, ((int(self.posx-20), int(self.posy-15))))


class Enemy:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        self.health = 100
        self.velocity = 0.05

    def drawEnemy(self, scr, image):
        # change the color depending on its health and also draw it
        scr.blit(image, ((int(self.posx-15), int(self.posy-15))))
        # pygame.draw.circle(scr, (color, color, color),
        #                    (self.posx, self.posy), 10)


# this function moves all the enemies and if they any one of them goes
# out of the screen, then changes the velocity of all the enemies
def moveEnemies(enemyList):
    for e in enemyList:
        e.posx += e.velocity
        if e.posx < 20 or e.posx > screenWidth - 20:
            for e in enemyList:
                e.velocity *= -1
                e.posy += 20


def startGame():
    score = 0
    showGameOverScreen = True
    # make the window appear
    win = pygame.display.set_mode((screenWidth, screenHeight))
    # set its caption to Space Invaders
    pygame.display.set_caption("Space Invaders")

    # load the monster image and make it small
    monster = pygame.image.load(r'Assets/monster.png').convert_alpha()
    monster = pygame.transform.scale(monster, (30, 30))

    # load the cannon image and make it small
    cannon = pygame.image.load(r'Assets/player.png').convert_alpha()
    cannon = pygame.transform.scale(cannon, (40, 30))

    # create the player
    pl = Player()

    ebullets = []   # array to hold all the enemybullet objects
    bullets = []    # array to hold all the bullet objects
    enemies = []    # array to hold all the enemy objects

    # create all the enemies
    for i in range(11):
        for j in range(5):
            enemies.append(Enemy(i*60+20, j*60+40))

    font = pygame.font.Font('freesansbold.ttf', 18)
    lives = font.render('Lives : '+str(pl.health), False, (255, 255, 255))

    # game loop
    loop = True
    while loop:
        # clear the window
        win.fill((0, 0, 0))

        # draw the player
        pl.drawPlayer(win, cannon)

        # show the lives left
        lives = font.render('Lives : '+str(pl.health), False, (255, 255, 255))
        win.blit(lives, (5, screenHeight-20))

        # show the score
        scoreText = font.render('Score : ' + str(score),False, (255, 255, 255))
        win.blit(scoreText, (5, screenHeight-45))
        # delete the enemy bullets if they go uou of screen
        for h in ebullets:
            if h.posy > screenHeight:
                ebullets.remove(h)
            h.travel(win)

        # remove the bullets if they go out of the screen
        # and also draw and move them
        for b in bullets:
            if b.posy < 0:
                bullets.remove(b)
            b.travel(win)

        # make a random enemy fire a bullet
        if len(enemies) != 0:
            ra = random.randint(0, len(enemies)-1)
        else:
            loop = False
        if len(ebullets) == 0:
            ebullets.append(enemyBullets(
                enemies[ra].posx, enemies[ra].posy))

        moveEnemies(enemies)
        # remove the enemies if their health is below zero and also draw them
        for e in enemies:
            if e.health <= 0:
                enemies.remove(e)
            e.drawEnemy(win, monster)

        # check for collisions for all the enemies and bullets
        for b in bullets:
            for e in enemies:
                if math.sqrt((e.posx - b.posx)**2 + (e.posy - b.posy)**2) <= 20:
                    bullets.remove(b)
                    e.health -= 100
                    score += 20

        # check for collisions forr all the enemy bullets and the player
        for j in ebullets:
            if math.sqrt((pl.posx - j.posx)**2 + (pl.posy - j.posy)**2) <= 20:
                ebullets.remove(j)
                pl.health -= 1
            if pl.health == 0:
                loop = False

        # check for collisions for all the enemies and the player
        for e in enemies:
            if math.sqrt((e.posx - pl.posx)**2 + (e.posy - pl.posy)**2) <= 40:
                loop = False

        # get the keys pressed
        keys = pygame.key.get_pressed()

        # if -> key is pressed, then move right
        if keys[pygame.K_RIGHT]:
            pl.moveRight()

        # if <- key is pressed, then move left
        if keys[pygame.K_LEFT]:
            pl.moveLeft()

        # if Tab is pressed, then restart the game
        if keys[pygame.K_TAB]:
            showGameOverScreen = False
            loop = False
            startGame()
        
        # looping through all the events
        for e in pygame.event.get():
            # if the X is pressed then exit
            if e.type == pygame.QUIT:
                loop = False
                showGameOverScreen = False

            # if a single key is down
            if e.type == pygame.KEYDOWN:
                # if SPACE is pressed then create a bullet object and
                # append it to the bullets list
                if e.key == pygame.K_SPACE:
                    if len(bullets) == 0:
                        bullets.append(Bullet(pl.posx, pl.posy))

        # update the display
        pygame.display.flip()
    if showGameOverScreen:
        gameOver(score, len(enemies))

# game over Screen


def gameOver(score, lent):
    # display the window
    win = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Space Invaders")

    # set the fonts and the font sizes
    font = pygame.font.Font('freesansbold.ttf', 42)
    fontsmall = pygame.font.Font('freesansbold.ttf', 18)

    # render the text (Win/Lose)
    if lent == 0:
        gameover = font.render('You Won!', False, (255, 255, 255))
    else:
        gameover = font.render('Game Over', False, (255, 255, 255))

    # render the text (Score and "Press Space to Restart")
    textrect = gameover.get_rect()
    textrect.center = (int(screenWidth/2), int(screenHeight/2-50))
    restart = fontsmall.render(
        'Press Space to Restart', False, (255, 255, 255))
    textrect2 = restart.get_rect()
    textrect2.center = (int(screenWidth/2), int(screenHeight/2 + 50))
    scoreText = fontsmall.render(
        'Score : ' + str(score), False, (255, 255, 255))
    textrect3 = scoreText.get_rect()
    textrect3.center = (int(screenWidth/2), int(screenHeight/2))

    # game loop
    loop = True
    while loop:
        # clear the screen
        win.fill((0, 0, 0))

        # show the You Won/Game Over text
        win.blit(gameover, textrect)

        # show the score
        win.blit(scoreText, textrect3)

        # show the restart text
        win.blit(restart, textrect2)

        for e in pygame.event.get():
            # close the window if "x" is pressed
            if e.type == pygame.QUIT:
                loop = False

            # restart the game if SPACE is pressed
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    loop = False
                    startGame()

        # update the display
        pygame.display.flip()


startGame()

from math import sqrt
import pygame as pg
import random

import os
import sys

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
ENEMY_WIDTH = 29
ENEMY_HEIGHT = 33
SPACE_BETWEEN_ROWS = 20
SPACE_BETWEEN_LINES = 20
ENEMIES_PER_LINE = 20
PLAYER_Y = 75
FORMATION_UPRIGHT_X = (SCREEN_WIDTH-(ENEMIES_PER_LINE*ENEMY_WIDTH)-(ENEMIES_PER_LINE-1)*SPACE_BETWEEN_ROWS)//2
FORMATION_UPRIGHT_Y = 500
WALLS_AMOUNT = 4
WALLS_WIDTH = 150


def resource_path(relative_path):
    """ Gestion ultra-fiable des chemins pour PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # On est dans l'EXE : PyInstaller décompresse dans ce dossier temporaire
        return os.path.join(sys._MEIPASS, relative_path)
    
    # On est en développement : on utilise le chemin réel du fichier .py
    # C'est ici que ça change : on part du dossier du SCRIPT, pas du dossier de CMD
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class Player(pg.sprite.Sprite):
    x = SCREEN_WIDTH//2
    y = PLAYER_Y
    shootCdStat = 20
    shootCd = 0

    def __init__(self):
        super().__init__()
        self.image = pg.image.load(resource_path("pereNoel.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):

        self.shootCd -= (self.shootCd > 0)

        pass

    def moveRight(self):
        if self.rect.x < SCREEN_WIDTH - self.rect.width - 4:
            self.rect.x += 4

    def moveLeft(self):
        if self.rect.x > 4:
            self.rect.x -= 4
    
    def shoot(self):
        if not self.shootCd:
            self.shootCd = self.shootCdStat
            return SnowBall(self.rect.x-4, PLAYER_Y,True)
        return None
        
class Wall(pg.sprite.Sprite):
    y = PLAYER_Y + 44 + 50

    def __init__(self, x):
        super().__init__()
        self.x = x

        # Load the image (your sprite graphic)
        self.image = pg.image.load(resource_path("giftWall.png").convert_alpha()

        # A rect is needed for position & collision
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    



class SnowBall(pg.sprite.Sprite):
    x = 100
    speed = 8
    
    def __init__(self, x, y, ally):
        super().__init__()
        self.x = x
        self.y = y
        self.ally = ally
        self.image = pg.image.load(resource_path("boule_de_neige.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.ally :
            self.rect.y +=self.speed
            if self.rect.y > SCREEN_HEIGHT :
                return False
            return True
        else :
            self.rect.y -=self.speed
            if self.rect.y < 0:
                return False
            return True


class Enemy(pg.sprite.Sprite):
    x = SCREEN_HEIGHT - ENEMY_HEIGHT
    y = SCREEN_WIDTH - ENEMY_WIDTH
    minShootDelay = 50
    shootIndex = 0
    inFormation = False

    def __init__(self, fPosition, maxShootDelay):
        super().__init__()
        self.images =  [
            pg.image.load(resource_path("lutin1.png").convert_alpha(),
            pg.image.load(resource_path("lutin2.png").convert_alpha()
        ]
        self.maxShootDelay = max(maxShootDelay, self.minShootDelay)
        self.shootDelay = random.randint(self.minShootDelay, self.maxShootDelay)
        self.fPosition = fPosition
        self.index = 0           # current animation frame
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.animation_speed = 0.1
        pass

    def isInFormation():
        pass
    
    def animate(self):
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[int(self.index)]

    def moveToFormation(self, speed):
        distX = self.fPosition[0] - self.rect.x
        distY = self.fPosition[1] - self.rect.y
        distTot = sqrt(distX*distX + distY*distY)
        if distTot < speed :
            self.rect.x = self.fPosition[0]
            self.rect.y = self.fPosition[1]
            self.inFormation = True
            return
        dirX = distX / distTot
        dirY = distY / distTot
        self.rect.x += dirX * speed
        self.rect.y += dirY * speed

    def update(self, down, speed, allRdy):
        self.animate()
        if [self.rect.x, self.rect.y] == self.fPosition:
            self.inFormation = True

        if not self.inFormation :
            self.moveToFormation(speed)

        if allRdy:
            if not down:
                self.rect.x += speed
            else :
                self.rect.y -= speed
            
            if self.shootIndex == self.shootDelay :
                self.shootIndex = 0
                self.shootDelay = random.randint(self.minShootDelay, self.maxShootDelay)
                return SnowBall(self.rect.x,self.rect.y, False)
            
            self.shootIndex += 1
            return False

        

class EnemySpawner():
    wave = 0

    waves = [
        [3, 5, 25, 100],
        [4, 30, 22, 70]
    ]


    uSpawnedThisWave = 0
    spawnIndex = waves[0][1]
    

    def __init__(self):
        self.uSpeed = self.waves[self.wave][0]
        self.uSpawnDelay = self.waves[self.wave][1]
        self.uShootSpeed = self.waves[self.wave][2]
        self.uNumber = self.waves[self.wave][3]
        self.spawnOrder = self.random_order(self.uNumber)

    def update(self):
        return self.spawnWave()
        pass

    def random_order(self,x):
        lst = list(range(x))
        random.shuffle(lst)
        return lst
    
    
    def getFormationCoordinates(self,pos):
        return (FORMATION_UPRIGHT_X + (pos%ENEMIES_PER_LINE) * (ENEMY_WIDTH + SPACE_BETWEEN_ROWS),
                FORMATION_UPRIGHT_Y + (pos//ENEMIES_PER_LINE) * (ENEMY_HEIGHT + SPACE_BETWEEN_LINES))

        

    def spawnWave(self):
        if self.uSpawnedThisWave < self.uNumber :
            if self.spawnIndex == self.uSpawnDelay :
                self.spawnIndex = 0
                self.uSpawnedThisWave += 1
                return Enemy(self.getFormationCoordinates(self.spawnOrder[self.uSpawnedThisWave-1]), 2000)
            self.spawnIndex += 1
        return False

class EnemyFormation():
    spawner = EnemySpawner()
    enemies = []
    allPlaced = False
    speed = 2

    pattern = [
        [False, speed, True],
        [False, -speed, True],
        [True, speed, True]
    ]
    patternIndex = 0
    movedUpBy = 0

    def __init__(self):
        pass
    
    def getMostLeftAndRightU(self):
        left = 0
        right = SCREEN_WIDTH
        for e in self.enemies:
            left = max(e.rect.x, left)
            right = min(e.rect.x, right)
        return (left, right)

    def incrementPattern(self):
        if self.patternIndex == 0 :
            if self.getMostLeftAndRightU()[0] >= SCREEN_WIDTH - ENEMY_WIDTH - SPACE_BETWEEN_ROWS:
                self.patternIndex = 1
        if self.patternIndex == 1 :
            if self.getMostLeftAndRightU()[1] <= SPACE_BETWEEN_ROWS:
                self.patternIndex = 2
        if self.patternIndex == 2 : 
            self.movedUpBy += self.speed
            if self.movedUpBy > ENEMY_HEIGHT:
                self.movedUpBy = 0
                self.patternIndex = 0

                


    def update(self, deadEnemies):
        newEnemy = self.spawner.update()
        ballShot = []
        if newEnemy:
            self.enemies.append(newEnemy)
        
        # deadEnemies is a dict: {Bullet: [Enemy1, Enemy2]}
        for hit_list in deadEnemies.values():
            for enemy in hit_list:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
        
        if not self.allPlaced:
            done = True
            for e in self.enemies:
                if not e.inFormation:
                    done = False
                e.update(False, 8, False)
            if done:
                self.allPlaced = True
        else :
            self.incrementPattern()
            for e in self.enemies:
                newSnowball = e.update(self.pattern[self.patternIndex][0], 
                         self.pattern[self.patternIndex][1], 
                         self.pattern[self.patternIndex][2])
                if newSnowball:
                    ballShot.append(newSnowball)
        
        return (newEnemy, ballShot)
    

        


class ChristmasInvader:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0

        self.playerSprites = pg.sprite.Group()
        self.enemiesSprites = pg.sprite.Group()
        self.snowballsAlliesSprites = pg.sprite.Group()
        self.snowballsEnemiesSprites = pg.sprite.Group()
        self.wallsSprites = pg.sprite.Group()

        self.player = Player()
        self.snowballsAllies = []
        self.snowballsEnemy = []
        self.playerSprites.add(self.player)
        self.enemies = []
        self.formation = EnemyFormation()
        self.deadEnemies = {}

        wallSpace = (SCREEN_WIDTH - WALLS_AMOUNT * WALLS_WIDTH)//(WALLS_AMOUNT+1)
        for i in range(WALLS_AMOUNT):
            self.wallsSprites.add(Wall(WALLS_WIDTH * i + wallSpace * (i+1)))


    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass
                if event.key == pg.K_LEFT:
                    pass
                if event.key == pg.K_RIGHT:
                    pass
                if event.key == pg.K_UP:
                    pass
                if event.key == pg.K_ESCAPE:    
                    self.running = False
                if event.key == pg.K_RETURN:
                    pass
                #pause
                if event.key == pg.K_p:
                    pg.time.wait(1000)
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT]:
            self.player.moveRight()
        if k[pg.K_LEFT]:
            self.player.moveLeft()
        if k[pg.K_SPACE]: 
            newSnowBall = self.player.shoot() 
            if newSnowBall :
                self.snowballsAllies.append(newSnowBall)
                self.snowballsAlliesSprites.add(self.snowballsAllies[-1])
                

    def update(self):
        self.player.update()
        
        for s in self.snowballsAllies:
            if not s.update() :
                self.snowballsAllies.remove(s)
                self.snowballsAlliesSprites.remove(s)
        
        for s in self.snowballsEnemy:
            if not s.update():
                self.snowballsEnemy.remove(s)
                self.snowballsEnemiesSprites.remove(s)

        newEnemy, newSnowBalls = self.formation.update(self.deadEnemies)

        for ns in newSnowBalls:
            self.snowballsEnemy.append(ns)
            self.snowballsEnemiesSprites.add(ns)

        if newEnemy:
            self.enemiesSprites.add(newEnemy)

        self.deadEnemies = pg.sprite.groupcollide(
            self.snowballsAlliesSprites,   # bullets
            self.enemiesSprites,  # enemies
            True,  # remove bullet
            True   # remove enemy
        )

        hitsOnWallA = pg.sprite.groupcollide(
            self.snowballsAlliesSprites,
            self.wallsSprites,
            True,
            False
        )

        hitsOnWallE = pg.sprite.groupcollide(
            self.snowballsEnemiesSprites,
            self.wallsSprites,
            True,
            False
        )

        hitsOnPlayer = pg.sprite.groupcollide(
            self.snowballsEnemiesSprites,
            self.playerSprites,
            True,
            True
        )
        
        if len(hitsOnPlayer):
            self.defeat()

    def defeat(self):
        font = pg.font.SysFont(None, 60)
        text = font.render("PERDU", True, (0, 0, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)     # Draw text centered
        pg.display.update()
        self.running = False    
        
    # def drawScore(self):
    #     font = pg.font.SysFont(None, 60)
    #     text = font.render("Score : " + self.score, True, (0, 0, 255))
    #     text_rect = text.get_reto=(0, 0))
    #     self.screen.blit(text, text_rect)     # Draw text centered


    def draw(self):
        self.screen.fill((255, 255, 255))
        self.playerSprites.draw(self.screen)
        self.snowballsAlliesSprites.draw(self.screen)
        self.snowballsEnemiesSprites.draw(self.screen)
        self.enemiesSprites.draw(self.screen)
        self.wallsSprites.draw(self.screen)


        pg.display.flip()




ChristmasInvader().run()
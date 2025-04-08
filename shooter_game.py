
from pygame import *
from random import randint
from time import time as timer
win_wid = 700
win_hei = 500
lost = 0
score = 0
rel_time =  False
num_fire = 0
window = display.set_mode((win_wid, win_hei))
display.set_caption('лабиринт')
background = transform.scale(image.load('galaxy.jpg'), (win_wid,win_hei))
class Gamesprite (sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))
class Player (Gamesprite):
    def Update(self):
        keys_pressed = key.get_pressed()
        if  keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_wid - 60:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top ,5,6,-10)
        bullets.add(bullet)
class Enemy (Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hei:
            self.rect.x = randint(80,win_wid - 80)
            self.rect.y = 0
            lost = lost + 1
hero = Player('rocket.png', 5,win_hei - 80,70,100,9)
class Asteroid (Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_hei:
            self.rect.x = randint(80,win_wid - 80)
            self.rect.y = 0
class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
             self.kill()
collide = [] 

fps = 60
game = True
finish = False
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1  = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)
enemys = sprite.Group()
bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(80, win_wid - 80), -40 , 80, 50, randint(1, 5))
    enemys.add(enemy)
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(80, win_wid - 80), -40 , 80, 50, randint(1, 7))
    asteroids.add(enemy)
while game:
    for i in  event.get():
        if i.type == QUIT:
            game = False 
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                fire_sound.play()
                hero.fire()
    if not finish:
        window.blit(background, (0,0))
        text_lost = font1.render('Пропущено:'+ str(lost),1,(255,255,255))
        window.blit(text_lost, (10,0))
        text_lose = font2.render(' you lose',1,(255,0,0))
        if score >= 10:
            text_win = font2.render(' you win',1,(0,0,255))
            window.blit(text_win,(250,230))
            finish = True
        text = font1.render('Счет:'+ str(score),1,(255,255,255))
        window.blit(text,(10,50))
        hero.Update()
        hero.reset()
        enemys.update()
        enemys.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroid.update()
        asteroids.draw(window)
        collides = sprite.groupcollide(enemys,bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy('ufo.png', randint(80,win_wid - 80),-40,80,50,randint(1,5))
            enemys.add(enemy)
        if sprite.spritecollide(hero,enemys, False) or lost >= 3 or sprite.spritecollide(hero,asteroids, False):
            finish = True
            window.blit(text_lose,(250,230))
        clock.tick(fps)
        display.update()
    time.delay(50)
import pygame, sys
from pygame.locals import *
import random, time
 
# Инициализация Pygame
pygame.init()

# Установка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Создание цветов
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Остальные переменные для использования в программе
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0  # Переменная для отслеживания собранных монет

# Установка шрифтов
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("road1.jpg")

# Создание белого экрана
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("konus.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin2.jpg")  # Загрузка изображения монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Создание спрайта игрока, врага и монеты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Добавление нового пользовательского события
INC_SPEED = pygame.USEREVENT + 1
COIN_EVENT = pygame.USEREVENT + 2  # Новое событие для добавления монет
pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(COIN_EVENT, 2000)  # Таймер для добавления монет каждые 2 секунды

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == COIN_EVENT:  # Проверка события добавления монеты
            coins.add(Coin())  # Добавление новой монеты

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Отображение количества собранных монет
    coins_count = font_small.render(str(COINS), True, BLACK)
    DISPLAYSURF.blit(coins_count, (SCREEN_WIDTH - 80, 10))

    # Движение и перерисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка на сбор монет
    if pygame.sprite.spritecollide(P1, coins, True):
        COINS += 1
        # coins.add(Coin())  # Убрано, так как монеты добавляются через событие COIN_EVENT

    # Проверка на столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)

import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.8
        self.on_ground = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, platforms):
        # 处理水平移动
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            
        # 跳跃
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            
        # 应用重力
        self.vel_y += self.gravity
        
        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y
        
        # 边界检查
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        # 更新碰撞矩形
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 平台碰撞检测
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # 下降时
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    
        # 地面碰撞检测
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True
            
    def draw(self, screen):
        # 绘制玩家（简单的红色矩形）
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # 绘制眼睛
        pygame.draw.circle(screen, WHITE, (int(self.x + 8), int(self.y + 10)), 3)
        pygame.draw.circle(screen, WHITE, (int(self.x + 22), int(self.y + 10)), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + 9), int(self.y + 10)), 1)
        pygame.draw.circle(screen, BLACK, (int(self.x + 23), int(self.y + 10)), 1)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Enemy:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = speed
        self.direction = 1
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, platforms):
        self.x += self.speed * self.direction
        
        # 边界反弹
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1
            
        # 平台边缘检测
        self.rect.x = self.x
        on_platform = False
        for platform in platforms:
            if (self.rect.bottom >= platform.rect.top and 
                self.rect.bottom <= platform.rect.top + 10 and
                self.rect.right > platform.rect.left and 
                self.rect.left < platform.rect.right):
                on_platform = True
                break
                
        # 地面检测
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            on_platform = True
            
        # 如果不在平台上，改变方向
        next_x = self.x + self.speed * self.direction
        next_rect = pygame.Rect(next_x, self.y, self.width, self.height)
        next_on_platform = False
        
        for platform in platforms:
            if (next_rect.bottom >= platform.rect.top and 
                next_rect.bottom <= platform.rect.top + 10 and
                next_rect.right > platform.rect.left and 
                next_rect.left < platform.rect.right):
                next_on_platform = True
                break
                
        if next_x >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            next_on_platform = True
            
        if on_platform and not next_on_platform:
            self.direction *= -1
            
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y + 8)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 17), int(self.y + 8)), 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("马里奥风格小游戏")
        self.clock = pygame.time.Clock()
        
        # 创建游戏对象
        self.player = Player(50, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
        
        # 创建平台
        self.platforms = [
            Platform(200, SCREEN_HEIGHT - 200, 150, 20),
            Platform(400, SCREEN_HEIGHT - 300, 150, 20),
            Platform(600, SCREEN_HEIGHT - 250, 150, 20),
            Platform(150, SCREEN_HEIGHT - 400, 100, 20),
            Platform(500, SCREEN_HEIGHT - 450, 120, 20),
        ]
        
        # 创建敌人
        self.enemies = [
            Enemy(300, SCREEN_HEIGHT - GROUND_HEIGHT - 25, 1),
            Enemy(500, SCREEN_HEIGHT - 320, 2),
            Enemy(650, SCREEN_HEIGHT - 270, 1.5),
        ]
        
        # 创建金币
        self.coins = [
            Coin(275, SCREEN_HEIGHT - 230),
            Coin(475, SCREEN_HEIGHT - 330),
            Coin(675, SCREEN_HEIGHT - 280),
            Coin(200, SCREEN_HEIGHT - 430),
            Coin(560, SCREEN_HEIGHT - 480),
        ]
        
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
    def handle_collisions(self):
        # 玩家与敌人碰撞
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                # 如果玩家从上方踩到敌人
                if (self.player.vel_y > 0 and 
                    self.player.rect.bottom - 10 < enemy.rect.top):
                    self.enemies.remove(enemy)
                    self.player.vel_y = -8  # 小跳跃效果
                    self.score += 100
                else:
                    # 重置游戏
                    self.reset_game()
                    
        # 玩家与金币碰撞
        for coin in self.coins:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.score += 50
                
    def reset_game(self):
        self.player = Player(50, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
        self.enemies = [
            Enemy(300, SCREEN_HEIGHT - GROUND_HEIGHT - 25, 1),
            Enemy(500, SCREEN_HEIGHT - 320, 2),
            Enemy(650, SCREEN_HEIGHT - 270, 1.5),
        ]
        for coin in self.coins:
            coin.collected = False
        self.score = 0
        
    def draw(self):
        # 绘制天空背景
        self.screen.fill(BLUE)
        
        # 绘制地面
        pygame.draw.rect(self.screen, GREEN, 
                        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # 绘制平台
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # 绘制金币
        for coin in self.coins:
            coin.draw(self.screen)
            
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # 绘制玩家
        self.player.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f"分数: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制操作说明
        help_text = pygame.font.Font(None, 24).render(
            "方向键/WASD移动, 空格/W/↑跳跃", True, BLACK)
        self.screen.blit(help_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # R键重置游戏
                        self.reset_game()
                        
            # 更新游戏对象
            self.player.update(self.platforms)
            for enemy in self.enemies:
                enemy.update(self.platforms)
                
            # 处理碰撞
            self.handle_collisions()
            
            # 绘制所有内容
            self.draw()
            
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
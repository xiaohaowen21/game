import pygame
import math
import random
import sys

# 初始化 pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.angle = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.last_shot = 0
        self.shoot_delay = 200  # 毫秒
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        # 移动
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # 边界检查
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
        # 更新矩形位置
        self.rect.x = self.x
        self.rect.y = self.y
        
        # 鼠标瞄准
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - (self.x + self.width // 2)
        dy = mouse_y - (self.y + self.height // 2)
        self.angle = math.atan2(dy, dx)
        
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            
            # 计算子弹起始位置
            start_x = self.x + self.width // 2 + math.cos(self.angle) * 20
            start_y = self.y + self.height // 2 + math.sin(self.angle) * 20
            
            return Bullet(start_x, start_y, self.angle, "player")
        return None
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
            
    def draw(self, screen):
        # 绘制玩家身体
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # 绘制枪管
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        end_x = center_x + math.cos(self.angle) * 25
        end_y = center_y + math.sin(self.angle) * 25
        pygame.draw.line(screen, BLACK, (center_x, center_y), (end_x, end_y), 3)
        
        # 绘制血条
        bar_width = 40
        bar_height = 6
        bar_x = self.x - 5
        bar_y = self.y - 15
        
        # 背景条
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # 血量条
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = random.uniform(1, 2)
        self.health = 50
        self.max_health = 50
        self.angle = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.last_shot = 0
        self.shoot_delay = random.randint(1000, 2000)
        self.ai_timer = 0
        self.target_x = x
        self.target_y = y
        
    def update(self, player):
        # AI 移动
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # 向玩家移动
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
            # 瞄准玩家
            self.angle = math.atan2(dy, dx)
            
        # 边界检查
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
        self.rect.x = self.x
        self.rect.y = self.y
        
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            self.shoot_delay = random.randint(1000, 2000)
            
            start_x = self.x + self.width // 2 + math.cos(self.angle) * 15
            start_y = self.y + self.height // 2 + math.sin(self.angle) * 15
            
            return Bullet(start_x, start_y, self.angle, "enemy")
        return None
        
    def take_damage(self, damage):
        self.health -= damage
        
    def draw(self, screen):
        # 绘制敌人身体
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # 绘制枪管
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        end_x = center_x + math.cos(self.angle) * 20
        end_y = center_y + math.sin(self.angle) * 20
        pygame.draw.line(screen, BLACK, (center_x, center_y), (end_x, end_y), 2)
        
        # 绘制血条
        bar_width = 30
        bar_height = 4
        bar_x = self.x - 2
        bar_y = self.y - 10
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Bullet:
    def __init__(self, x, y, angle, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.owner = owner
        self.radius = 3
        self.damage = 25
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
                
    def draw(self, screen):
        color = YELLOW if self.owner == "player" else ORANGE
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 1)

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # "health", "speed", "damage"
        self.radius = 15
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.collected = False
        self.spawn_time = pygame.time.get_ticks()
        
    def draw(self, screen):
        if not self.collected:
            if self.type == "health":
                color = GREEN
                symbol = "+"
            elif self.type == "speed":
                color = BLUE
                symbol = "S"
            else:  # damage
                color = RED
                symbol = "D"
                
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
            
            # 绘制符号
            font = pygame.font.Font(None, 24)
            text = font.render(symbol, True, WHITE)
            text_rect = text.get_rect(center=(self.x, self.y))
            screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D 枪战游戏")
        self.clock = pygame.time.Clock()
        
        # 游戏对象
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.bullets = []
        self.powerups = []
        
        # 游戏状态
        self.score = 0
        self.wave = 1
        self.enemies_killed = 0
        self.game_over = False
        self.paused = False
        
        # 字体
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # 敌人生成
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 3000  # 毫秒
        
        # 道具生成
        self.powerup_spawn_timer = 0
        self.powerup_spawn_delay = 15000
        
    def spawn_enemy(self):
        # 在屏幕边缘随机生成敌人
        side = random.randint(0, 3)
        if side == 0:  # 上边
            x = random.randint(0, SCREEN_WIDTH)
            y = 0
        elif side == 1:  # 右边
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # 下边
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
        else:  # 左边
            x = 0
            y = random.randint(0, SCREEN_HEIGHT)
            
        self.enemies.append(Enemy(x, y))
        
    def spawn_powerup(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        powerup_type = random.choice(["health", "speed", "damage"])
        self.powerups.append(PowerUp(x, y, powerup_type))
        
    def handle_collisions(self):
        # 子弹与敌人碰撞
        for bullet in self.bullets[:]:
            if bullet.owner == "player":
                for enemy in self.enemies[:]:
                    if math.sqrt((bullet.x - enemy.x - enemy.width//2)**2 + 
                               (bullet.y - enemy.y - enemy.height//2)**2) < 15:
                        enemy.take_damage(bullet.damage)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)
                            self.score += 100
                            self.enemies_killed += 1
                        break
                        
        # 敌人子弹与玩家碰撞
        for bullet in self.bullets[:]:
            if bullet.owner == "enemy":
                if math.sqrt((bullet.x - self.player.x - self.player.width//2)**2 + 
                           (bullet.y - self.player.y - self.player.height//2)**2) < 15:
                    self.player.take_damage(bullet.damage)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                        
        # 玩家与敌人碰撞
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(1)  # 持续伤害
                
        # 玩家与道具碰撞
        for powerup in self.powerups[:]:
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                if powerup.type == "health":
                    self.player.health = min(self.player.max_health, 
                                           self.player.health + 30)
                elif powerup.type == "speed":
                    self.player.speed = min(8, self.player.speed + 1)
                else:  # damage
                    self.player.shoot_delay = max(100, self.player.shoot_delay - 50)
                self.powerups.remove(powerup)
                
    def update(self):
        if self.game_over or self.paused:
            return
            
        # 更新玩家
        self.player.update()
        
        # 更新敌人
        for enemy in self.enemies:
            enemy.update(self.player)
            
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
        # 敌人射击
        for enemy in self.enemies:
            new_bullet = enemy.shoot()
            if new_bullet:
                self.bullets.append(new_bullet)
                
        # 生成敌人
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_spawn_timer > self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = current_time
            
        # 生成道具
        if current_time - self.powerup_spawn_timer > self.powerup_spawn_delay:
            self.spawn_powerup()
            self.powerup_spawn_timer = current_time
            
        # 处理碰撞
        self.handle_collisions()
        
        # 检查游戏结束
        if self.player.health <= 0:
            self.game_over = True
            
        # 波次系统
        if self.enemies_killed >= self.wave * 5:
            self.wave += 1
            self.enemy_spawn_delay = max(1000, self.enemy_spawn_delay - 200)
            
    def draw(self):
        # 清屏
        self.screen.fill(DARK_GREEN)
        
        # 绘制网格背景
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, (0, 50, 0), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, (0, 50, 0), (0, y), (SCREEN_WIDTH, y))
            
        # 绘制游戏对象
        self.player.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for powerup in self.powerups:
            powerup.draw(self.screen)
            
        # 绘制UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause()
            
        pygame.display.flip()
        
    def draw_ui(self):
        # 分数
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 波次
        wave_text = self.font.render(f"波次: {self.wave}", True, WHITE)
        self.screen.blit(wave_text, (10, 50))
        
        # 敌人数量
        enemies_text = self.font.render(f"敌人: {len(self.enemies)}", True, WHITE)
        self.screen.blit(enemies_text, (10, 90))
        
        # 玩家血量
        health_text = self.font.render(f"血量: {self.player.health}/{self.player.max_health}", 
                                     True, WHITE)
        self.screen.blit(health_text, (SCREEN_WIDTH - 200, 10))
        
        # 操作说明
        controls = [
            "WASD: 移动",
            "鼠标: 瞄准",
            "左键: 射击",
            "P: 暂停",
            "ESC: 退出"
        ]
        
        for i, control in enumerate(controls):
            text = pygame.font.Font(None, 20).render(control, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH - 150, 50 + i * 25))
            
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("游戏结束", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font.render(f"最终分数: {self.score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(final_score_text, score_rect)
        
        restart_text = self.font.render("按 R 重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("游戏暂停", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.bullets = []
        self.powerups = []
        self.score = 0
        self.wave = 1
        self.enemies_killed = 0
        self.game_over = False
        self.paused = False
        self.enemy_spawn_timer = 0
        self.powerup_spawn_timer = 0
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.game_over and not self.paused:  # 左键
                        new_bullet = self.player.shoot()
                        if new_bullet:
                            self.bullets.append(new_bullet)
                            
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
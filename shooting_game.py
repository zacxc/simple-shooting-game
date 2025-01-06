import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简单射击游戏")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 游戏时钟
clock = pygame.time.Clock()

# 飞船设置
player_width, player_height = 50, 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

# 子弹设置
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = -7

# 敌人设置
enemy_width, enemy_height = 50, 50
enemies = []
enemy_speed = 3
spawn_timer = 30  # 每30帧生成一个敌人

# 分数
score = 0
font = pygame.font.SysFont(None, 36)

# 游戏结束标志
game_over = False

# 主循环
def main():
    global player_x, bullets, enemies, score, game_over

    frame_count = 0
    while True:
        screen.fill(BLACK)

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 玩家输入
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed
            if keys[pygame.K_SPACE]:
                if frame_count % 10 == 0:  # 每10帧发射一次子弹
                    bullets.append([player_x + player_width // 2, player_y])

        # 更新子弹位置
        bullets = [[x, y + bullet_speed] for x, y in bullets if y > 0]

        # 更新敌人位置
        if frame_count % spawn_timer == 0 and not game_over:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemies.append([enemy_x, 0])
        enemies = [[x, y + enemy_speed] for x, y in enemies if y < HEIGHT]

        # 碰撞检测
        for bullet in bullets:
            for enemy in enemies:
                if (
                    enemy[0] < bullet[0] < enemy[0] + enemy_width
                    and enemy[1] < bullet[1] < enemy[1] + enemy_height
                ):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

        # 检测游戏结束
        for enemy in enemies:
            if enemy[1] + enemy_height >= player_y:
                game_over = True

        # 绘制玩家
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # 绘制子弹
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

        # 绘制敌人
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

        # 绘制分数
        score_text = font.render(f"分数: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 绘制游戏结束
        if game_over:
            game_over_text = font.render("游戏结束！按 R 重试", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            if keys[pygame.K_r]:
                # 重置游戏
                player_x = WIDTH // 2 - player_width // 2
                bullets = []
                enemies = []
                score = 0
                game_over = False

        # 更新屏幕
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1


if __name__ == "__main__":
    main()

from random import randint
from typing import Any

import pygame
from pygame.math import Vector2


class Color(pygame.Color):
    """颜色"""

    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    GRAY = pygame.Color(242, 242, 242)

    @staticmethod
    def random_color():
        """获得随机颜色"""
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return pygame.Color(r, g, b)


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, dx, dy, color, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        # 一定要有self.radius, 否则不能进行圆形检测
        self.radius = radius
        self.color = color
        self.velocity = Vector2(dx, dy)

        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(Color.BLACK)
        self.image.set_colorkey(Color.BLACK)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect()
        self.rect.x = x - radius
        self.rect.y = y - radius

        # 保存当前有碰撞的sprite, 避免重复计算
        self.collisions = []

    def center(self):
        return Vector2(*self.rect.center)

    def quality(self):
        """使用面积代表质量"""
        return self.radius ** 2

    def update(self, *args: Any, **kwargs: Any) -> None:
        # 碰撞清空
        self.collisions.clear()
        # 移动
        self.rect = self.rect.move(self.velocity.x, self.velocity.y)
        # 边缘检测
        if self.rect.x <= 0 and self.velocity.x <= 0:
            self.velocity.x *= -1
        if self.rect.x + self.radius * 2 >= screen.get_width() and self.velocity.x >= 0:
            self.velocity.x *= -1
        if self.rect.y <= 0 and self.velocity.y <= 0:
            self.velocity.y *= -1
        if self.rect.y + self.radius * 2 >= screen.get_height() and self.velocity.y >= 0:
            self.velocity.y *= -1


def collision(ball1: Ball, ball2: Ball) -> tuple[Vector2, Vector2]:
    """
    两球完全弹性碰撞反弹方向问题:
    https://blog.csdn.net/atgwwx/article/details/8486209
    光滑均匀小球间的碰撞:
    https://enjoyphysics.cn/Article807
    """
    # 计算球1质心指向球2质心的矢量，即法线矢量, 并且正则化
    normal_vector = (ball1.center() - ball2.center()).normalize()
    # 法线矢量逆时针旋转90度, 获得正交向量
    orthogonal_vector = normal_vector.rotate(-90)
    # 计算ball1的速度在normal_vector和orthogonal_vector上的投影
    ball1_normal_vector_speed = ball1.velocity.dot(normal_vector)
    ball1_orthogonal_vector_speed = ball1.velocity.dot(orthogonal_vector)
    # 计算ball2的速度在normal_vector和orthogonal_vector上的投影
    ball2_normal_vector_speed = ball2.velocity.dot(normal_vector)
    ball2_orthogonal_vector_speed = ball2.velocity.dot(orthogonal_vector)
    # 根据动量守恒和能量守恒, 计算ball1和ball2在normal_vector上的最终速率
    ball1_final_normal_vector_speed = \
        get_final_speed(ball2.quality(), ball2_normal_vector_speed, ball1.quality(), ball1_normal_vector_speed)
    ball2_final_normal_vector_speed = \
        get_final_speed(ball1.quality(), ball1_normal_vector_speed, ball2.quality(), ball2_normal_vector_speed)
    # 把ball1, ball2在正交向量上的速率, 恢复为速度
    ball1_final_orthogonal_vector_velocity = ball1_orthogonal_vector_speed * orthogonal_vector
    ball2_final_orthogonal_vector_velocity = ball2_orthogonal_vector_speed * orthogonal_vector
    # 把ball1, ball2在法线矢量上的最终速率, 恢复为速度
    ball1_final_normal_vector_velocity = ball1_final_normal_vector_speed * normal_vector
    ball2_final_normal_vector_velocity = ball2_final_normal_vector_speed * normal_vector
    # 将ball1, ball2的速度叠加
    return ball1_final_normal_vector_velocity + ball1_final_orthogonal_vector_velocity, \
           ball2_final_normal_vector_velocity + ball2_final_orthogonal_vector_velocity


def get_final_speed(m1: float, v1: float, m2: float, v2: float):
    """
    动量守恒 + 能量守恒 推导出来的最终速度公式:
    v2' = (2 * m1 * v1 + v2 * (m2 – m1)) / (m1 + m2)
    v1' = (2 * m2 * v2 + v1 * (m1 - m2)) / (m2 + m1)
    """
    return (2 * m1 * v1 + v2 * (m2 - m1)) / (m1 + m2)


def main():
    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()
    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()
    running = True
    # 开启一个事件循环处理发生的事件
    while running:
        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 处理鼠标事件的代码
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 获得点击鼠标的位置
                x, y = event.pos
                radius = randint(10, 100)
                dx, dy = randint(-10, 10), randint(-10, 10)
                color = Color.random_color()
                # 在点击鼠标的位置创建一个球(大小、速度和颜色随机)
                Ball(x, y, radius, dx, dy, color, all_sprites_list)

        all_sprites_list.update()
        sprites = [sprite for sprite in all_sprites_list.sprites() if isinstance(sprite, Ball)]

        for sprite1 in sprites:
            for sprite2 in sprites:
                if sprite1 == sprite2 or sprite1.collisions.__contains__(sprite2) \
                        or sprite2.collisions.__contains__(sprite1):
                    continue
                if pygame.sprite.collide_circle(sprite1, sprite2):
                    sprite1.velocity, sprite2.velocity = collision(sprite1, sprite2)
                    sprite1.collisions.append(sprite2)
                    sprite2.collisions.append(sprite1)

        screen.fill(Color.WHITE)

        all_sprites_list.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    # 初始化导入的pygame中的模块
    pygame.init()
    # 初始化用于显示的窗口并设置窗口尺寸
    screen = pygame.display.set_mode((800, 600))
    # 设置当前窗口的标题
    pygame.display.set_caption('collision with quality')

    main()

    pygame.quit()

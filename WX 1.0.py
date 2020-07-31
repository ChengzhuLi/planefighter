"""
以面向对象编程思路实现
通过类的继承重构代码
主要是通过Sprite精灵类的重写实现
主要重写__init__ 以及 update
"""
# todo """ ...."""为块注释


import pygame
from pygame import locals
# todo 这个模块包含了 Pygame 定义的各种常量。它的内容会被自动放入到 Pygame 模块的名字空间中
from sys import exit
from pygame.sprite import Sprite, Group
# todo pygame.sprite.Sprite - 可见游戏对象的简单基类，
# pygame本身就提供这个，可以作为父类,不提供update和rect
# todo pygame.sprite.Group - 用于保存和管理多个Sprite对象的容器类
import random


class BGSprite(Sprite):                             # 背景精灵
    def __init__(self, imagepath):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
    # 与之前的飞机大战不同在于该程序背景不是滚动的而是静态的因此不需要update方法，但是不提倡这种使用方法


class BulletSprite(Sprite):                             # 我方飞机子弹精灵

    def __init__(self, imagepath, rect, pos, speed):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed

    def move(self):
        self.rect.y -= self.speed
        # 下面控制的是我方战机的子弹长度，要保证子弹在出界前不会消失
        if self.rect.y < -100:
            self.kill()
            # pygame.sprite.Sprite.kill - 从所有组中删除Sprite，系统自带直接用就行

    def update(self):
        self.move()


class EnemySprite(Sprite):                          # 敌机及其子弹精灵
    def __init__(self, imagepath, rect, pos, speed, screen):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        # 在pygame中，所有在屏幕上显示的元素都可以视为一个surface
        # 用surface.subsurface()函数把shoot.png中我们想要的元素裁剪出来
        # 用subsurface剪切读入的图片，当然不剪也可以
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # self 定义的量里面都有x和y分量，所以下面换成yspeed也是OK的
        self.speed = speed
        # 这里面特指横向速度也是要有的，加速度为aspeed
        self.xspeed = speed
        # 设计定时
        self.timer = 0
        # 创建敌人子弹组
        self.bulletgroup = Group()
        # 用来画在屏幕上
        self.screen = screen

    def update(self):
        self.bulletgroup.update()
        self.bulletgroup.draw(self.screen)
        self.timer += 0.01
        if self.timer > 0.3:
            # print("敌机发射子弹")
            bullet = BulletSprite("images/bullet/enemy_bullet.png", [0, 0, 15, 20], [self.rect.x+15, self.rect.y+20], -5)
            # 添加到子弹组里面去
            self.bulletgroup.add(bullet)
            self.timer = 0
        self.rect.y += self.speed
        self.rect.x += self.xspeed
        # 下面满足子弹在屏幕横向来回射
        if self.rect.x > 400:
            self.xspeed *= -1
            self.rect.x += self.xspeed
        if self.rect.x < 0:
            self.xspeed *= -1
            self.rect.x += self.xspeed
        if self.rect.y > 800:
            self.kill()


class PlayerSprite(Sprite):                             # 玩家战机

    def __init__(self, imagepath, rect, pos, speed, screen):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed
        self.screen = screen
        # 建立玩家飞机子弹组，同上
        self.bulletgroup = Group()
        self.score = 0
        self.hp = 10
        self.timer = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[locals.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.x > 412:
                self.rect.x = 412
        if keys[locals.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = 0
        if keys[locals.K_UP]:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.rect.y = 0
        if keys[locals.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.y > 702:
                self.rect.y = 702

    def fire(self):
        # print("发射子弹")
        bullet = BulletSprite("images/bullet/TMD.png", [0, 0, 21, 59], [self.rect.x + 23, self.rect.y - 20], 6)
        bullet2 = BulletSprite("images/bullet/TMD.png", [0, 0, 21, 59], [self.rect.x + 60, self.rect.y - 20], 6)
        self.bulletgroup.add(bullet)
        self.bulletgroup.add(bullet2)

    def update(self):
        self.bulletgroup.update()
        self.bulletgroup.draw(self.screen)
        self.move()
        self.timer += 1
        if self.timer > 25:
            # print("战机发射子弹")
            bullet = BulletSprite("images/bullet/TMD.png", [0, 0, 21, 59], [self.rect.x + 23, self.rect.y - 20], 6)
            bullet2 = BulletSprite("images/bullet/TMD.png", [0, 0, 21, 59], [self.rect.x + 60, self.rect.y - 20], 6)
            self.bulletgroup.add(bullet)
            self.bulletgroup.add(bullet2)
            self.timer = 0


CREATE_ENEMY = locals.USEREVENT + 1


def main():
    pygame.init()
    pygame.display.set_caption("雷霆战机")
    screen = pygame.display.set_mode((512, 768))
    bggroup = Group()
    bgsprite = BGSprite("images/bg/bg.jpg")
    bggroup.add(bgsprite)
    playergroup = Group()
    playersprite = PlayerSprite("images/hero/hero.png", [0, 0, 100, 66], [bgsprite.rect.w/2 - 50, 600], 5, screen)
    playergroup.add(playersprite)
    enemygroup = Group()
    # 在事件队列上重复创建一个事件
    # set_timer(event id, milliseconds) -> None
    # 将事件类型设置为每隔给定的毫秒数显示在事件队列中。第一个事件将在经过一段时间后才会出现。
    # 可以在 游戏循环 的 事件监听 方法中捕获到该事件
    # 第 1 个参数 事件代号 需要基于常量 pygame.USEREVENT 来指定；
    # USEREVENT 是一个整数，再增加的事件可以使用 USEREVENT + 1 指定，依次类推…
    pygame.time.set_timer(CREATE_ENEMY, random.randint(500, 1000))
    font = pygame.font.Font(None, 32)

    while True:
        bggroup.update()
        bggroup.draw(screen)

        playergroup.update()
        playergroup.draw(screen)

        enemygroup.update()
        enemygroup.draw(screen)

        screen.blit(font.render("Score:"+str(playersprite.score), True, (255, 0, 0)), (20, 20))
        screen.blit(font.render("HP:" + str(playersprite.hp), True, (255, 0, 0)), (20, 60))

        pygame.display.update()
        # pygame.sprite.groupcollide - 查找在两个组之间发生碰撞的所有精灵。
        '''
        groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict
        这将在两组中找到所有精灵之间的碰撞。 通过比较每个Sprite的Sprite.rect属性或使用碰撞函数（如果它不是None）来确定碰撞。
        # group1中的每个Sprite都被添加到返回字典中。 每个项的值是group2中相交的Sprite列表。
        # 如果dokill参数为True，则将从各自的组中删除碰撞的Sprite。
        # 碰撞参数是一个回调函数，用于计算两个精灵是否发生碰撞。 
        它应该将两个精灵作为值并返回一个bool值，指示它们是否发生碰撞。 
        如果未传递碰撞，则所有精灵必须具有“rect”值，该值是精灵区域的矩形，将用于计算碰撞。
        '''
        check1 = pygame.sprite.groupcollide(playersprite.bulletgroup, enemygroup, True, True)# 碰撞检测 销毁子弹 销毁敌机
       # 这里面注意要用if语句判断一下再用
        if check1:
            playersprite.score += 1
        check2 = pygame.sprite.groupcollide(playergroup, enemygroup, False, True)
        # 这里面要敌机毁掉但是我方战机不会爆炸只会掉血
        if check2:
            playersprite.hp -= 1

        # print(enemygroup)
        for enemy in enemygroup:
            check3 = pygame.sprite.groupcollide(playergroup, enemy.bulletgroup, False, True)
            if check3:
                playersprite.hp -= 1
        if playersprite.hp <= 0:
            playersprite.kill()

        for event in pygame.event.get():
            if event.type == locals.KEYUP:
                if event.key == locals.K_SPACE:
                    playersprite.fire()
            if event.type == locals.QUIT:
                pygame.quit()
                exit()
            if event.type == CREATE_ENEMY:
                enemy = EnemySprite("images/enemy/enemy1.png", [0, 0, 102, 79],[random.randint(0, 410), -50], 2, screen)
                enemygroup.add(enemy)
        # playersprite.fire() #自动开火


if __name__ == '__main__':
    main()

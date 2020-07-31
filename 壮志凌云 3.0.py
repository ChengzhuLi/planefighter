# coding:UTF-8
import pygame
from pygame import locals
# todo 这个模块包含了 Pygame 定义的各种常量。它的内容会被自动放入到 Pygame 模块的名字空间中
from sys import exit
from pygame.sprite import Sprite, Group
# todo pygame.sprite.Sprite - 可见游戏对象的简单基类，
# pygame本身就提供这个，可以作为父类,不提供update和rect
# todo pygame.sprite.Group - 用于保存和管理多个Sprite对象的容器类
import random
import math
import time


class BGSprite(Sprite):                             # 背景精灵
    def __init__(self, imagepath):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        self.rect = self.image.get_rect()
        # 与之前的飞机大战不同在于该程序背景不是滚动的而是静态的因此不需要update方法，但是不提倡这种使用方法


class BulletHelp(Sprite):                               # 我方子弹补给品，其实对应wx1.0的就是我方子弹的代码部分
    def __init__(self, imagepath, rect, pos, speed, screen, movetype):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        # self.image = self.image.subsurface(rect)
        # 在pygame中，所有在屏幕上显示的元素都可以视为一个surface
        # 用surface.subsurface()函数把shoot.png中我们想要的元素裁剪出来
        # 用subsurface剪切读入的图片，当然不剪也可以
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed
        # 下面代可以保证速度随机但部分可控，与前面下程序对比这里面速度取值更多
        self.xspeed = random.randint(0, speed) * movetype
        self.screen = screen

    def update(self):
        # 此部分同先前子弹环节相同
        self.rect.y += self.speed
        self.rect.x += self.xspeed
        if self.rect.x > 400:
            self.xspeed *= -1
            self.rect.x += self.xspeed
        if self.rect.x < 0:
            self.xspeed *= -1
            self.rect.x += self.xspeed
        if self.rect.y > 800:
            self.kill()


class BulletSprite(Sprite):                             # 玩家子弹精灵租

    def __init__(self, imagepath, pos, speed, direction):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        # self.image = self.image.subsurface(rect)
        # 不加也行
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed
        self.dir = direction

    def move(self):
        # 目的实现子弹可以有轨迹的运行，直线加斜对角，用三角函数表示
        if self.dir == 0:
            self.rect.y -= self.speed
        elif self.dir > 0:
            # 右上走
            self.rect.y -= self.speed * math.sin(self.dir)
            self.rect.x -= self.speed * math.cos(self.dir+90)
        else:
            # 与上边相比就是相反数就是了 ，往左上走
            self.rect.y -= self.speed * math.sin(self.dir * -1)
            self.rect.x += self.speed * math.cos(self.dir * -1 + 90)
        if self.rect.y < -50:
            self.kill()
            # pygame.sprite.Sprite.kill - 从所有组中删除Sprite，系统自带直接用就行

    def update(self):
        self.move()


class EnemyBulletSprite(Sprite):                             # 敌机子弹精灵组，精灵在下面

    def __init__(self, imagepath, pos, speed, direction):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        # self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = speed
        self.dir = direction

    def move(self):
        # 只有纵向位移
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()

    def move2(self):
        # 左下
        self.rect.y -= self.speed
        self.rect.x -= self.speed/2
        if self.rect.y < -50:
            self.kill()

    def move3(self):
        # 右下
        self.rect.y -= self.speed
        self.rect.x += self.speed/2
        if self.rect.y < -50:
            self.kill()

    def update(self):       # 子弹发射方向
        if self.dir == 0:
            self.move()
        elif self.dir == -1:
            self.move2()
        elif self.dir == 1:
            self.move3()


class EnemySprite(Sprite):                          # 敌机及其子弹精灵
    def __init__(self, imagepath, pos, speed, screen, movetype, bullettype, hp):
        super().__init__()
        self.image = pygame.image.load(imagepath)
        # self.image = self.image.subsurface(rect)
        #         # 在pygame中，所有在屏幕上显示的元素都可以视为一个surface
        #         # 用surface.subsurface()函数把shoot.png中我们想要的元素裁剪出来
        #         # 用subsurface剪切读入的图片，当然不剪也可以
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # self 定义的量里面都有x和y分量，所以下面换成yspeed也是OK的
        self.speed = speed
        self.xspeed = random.randint(0, speed+1) * movetype
        # 这里面特指横向速度也是要有的，加速度为aspeed
        # 设计定时，第一个针对普通的，第二个针对boss
        self.timer = 0
        self.timer2 = 3
        # 创建敌人子弹组
        self.bulletgroup = Group()
        # 用来画在屏幕上
        self.screen = screen
        # 对于不同的子弹应该有不同类型
        self.bullettype = bullettype
        # boss有血量限制，要多打几下
        self.hp = hp

    def update(self):
        self.bulletgroup.update()
        self.bulletgroup.draw(self.screen)
        if self.bullettype == 0:    # 无boss
            self.timer += 0.01
            if self.timer > 1:
                # print("敌机发射子弹")，一次发三个
                bullet = EnemyBulletSprite("images/bullet/enemy_bullet1.png", [self.rect.x + 40, self.rect.y + 39.5],
                                           -2, 0)
                # 为什么选速度为负值，dir为特殊值参考敌机子弹精灵组
                bullet2 = EnemyBulletSprite("images/bullet/enemy_bullet1.png", [self.rect.x + 40, self.rect.y + 39.5],
                                            -2, -1)
                bullet3 = EnemyBulletSprite("images/bullet/enemy_bullet1.png", [self.rect.x + 40, self.rect.y + 39.5],
                                            -2, 1)
                # 添加到子弹组里面去
                self.bulletgroup.add(bullet)
                self.bulletgroup.add(bullet2)
                self.bulletgroup.add(bullet3)
                self.timer = 0
        else:       # 有boss
            self.timer += 0.01
            self.timer2 += 0.01
            if self.timer > 1:
                bullet = EnemyBulletSprite("images/bullet/enemy_bullet2.png", [self.rect.x + 40, self.rect.y + 39.5], -2, -1)
                bullet2 = EnemyBulletSprite("images/bullet/enemy_bullet2.png", [self.rect.x + 120, self.rect.y + 39.5], -2, 1)
                self.bulletgroup.add(bullet)
                self.bulletgroup.add(bullet2)
                self.timer = 0
            if self.timer2 > 4:
                # BOSS发射导弹
                bullet = EnemyBulletSprite("images/bullet/boss_bullet.png", [self.rect.x + 80, self.rect.y + 39.5], -2, 0)
                self.bulletgroup.add(bullet)
                self.timer2 = 0
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

    def bomb(self):
        # 显示敌机爆炸
        bombimages = ["images/boom/boom01.png",
                      "images/boom/boom02.png",
                      "images/boom/boom03.png",
                      "images/boom/boom04.png",
                      "images/boom/boom05.png",
                      "images/boom/boom06.png"]
        for i in bombimages:
            self.screen.blit(pygame.image.load(i), (self.rect.x, self.rect.y))
            # time.sleep(t)；参数 t – 这是要暂停执行的秒数
            # 此方法不返回任何值。
            # sleep() 方法暂停给定秒数后执行程序。
            # 该参数可以是一个浮点数来表示一个更精确的睡眠时间。
            time.sleep(0.01)
            pygame.display.update()
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
        self.hp = 10000
        self.timer = 0
        # self.canfire = False
        self.bullettype = 0
        self.bulletnum = 10

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
            if self.rect.y > 580:
                self.rect.y = 580

    def fire(self):
        self.timer += 1
        if self.timer > 50:
            self.timer = 0
            # 计时后三种射击方式
            if self.bullettype == 0:
                bullet = BulletSprite("images/bullet/bullet1.png",  [self.rect.x + 45, self.rect.y - 20], 6, 0)
                self.bulletgroup.add(bullet)
            elif self.bullettype == 1:
                bullet = BulletSprite("images/bullet/bullet1.png", [self.rect.x + 30, self.rect.y - 20], 6, 0)
                bullet2 = BulletSprite("images/bullet/bullet1.png", [self.rect.x + 60, self.rect.y - 20], 6, 0)
                self.bulletgroup.add(bullet)
                self.bulletgroup.add(bullet2)
            elif self.bullettype == 2:
                bullet = BulletSprite("images/bullet/bullet1.png", [self.rect.x + 30, self.rect.y - 20], 6, 0)
                bullet2 = BulletSprite("images/bullet/bullet1.png", [self.rect.x + 60, self.rect.y - 20], 6, 0)
                bullet3 = BulletSprite("images/bullet/bullet3r.png", [self.rect.x + 60, self.rect.y - 20], 6, 15)
                bullet4 = BulletSprite("images/bullet/bullet3l.png", [self.rect.x + 28, self.rect.y - 20], 6, -15.076)
                bullet5 = BulletSprite("images/bullet/bullet4r.png", [self.rect.x + 60, self.rect.y - 20], 6, 45.5)
                bullet6 = BulletSprite("images/bullet/bullet4l.png", [self.rect.x + 25, self.rect.y - 20], 6, -45.5)
                self.bulletgroup.add(bullet)
                self.bulletgroup.add(bullet2)
                self.bulletgroup.add(bullet3)
                self.bulletgroup.add(bullet4)
                self.bulletgroup.add(bullet5)
                self.bulletgroup.add(bullet6)
                self.bulletnum -= 1
                if self.bulletnum <= 0:     # 默认射击方式为1
                    self.bullettype = 1

    def update(self):
        self.bulletgroup.update()
        self.bulletgroup.draw(self.screen)
        # move是按键判断
        self.move()
        # 由于wx只有一种子弹所以不需子弹精灵组，
        # 所以没有fire而是把它放在主程序里面
        self.fire()


CREATE_ENEMY = locals.USEREVENT + 1
CREATE_BOSS = locals.USEREVENT + 2
CREATE_BULLET_HELP = locals.USEREVENT + 3


def main():
    pygame.init()
    pygame.display.set_caption('This is my first pygame-program')  # 设置窗口标题
    screen = pygame.display.set_mode((512, 768))
    #   pygame.display.set_icon()
    # 描述：更改显示窗口的系统图像
    # 语法：set_icon(Surface) -> None
    # 必须加pygame.image.load，
    # 否则会报错，出现TypeError: argument 1 must be pygame.Surface, not str
    pygame.display.set_icon(pygame.image.load("images/hero/hero.png"))
    bggroup = Group()
    bgsprite = BGSprite("images/bg/bg0.jpg")
    bggroup.add(bgsprite)
    #################################################
    playergroup = Group()
    playersprite = PlayerSprite("images/hero/hero_b_03.png", [0, 0, 122, 105], [bgsprite.rect.w/2 - 61, 580], 5, screen)
    playergroup.add(playersprite)
    ################################################
    enemygroup = Group()
    bullethelpgroup = Group()
    bossgroup = Group()
    # 在事件队列上重复创建一个事件
    # set_timer(event id, milliseconds) -> None
    # 将事件类型设置为每隔给定的毫秒数显示在事件队列中。第一个事件将在经过一段时间后才会出现。
    # 可以在 游戏循环 的 事件监听 方法中捕获到该事件
    # 第 1 个参数 事件代号 需要基于常量 pygame.USEREVENT 来指定；
    # USEREVENT 是一个整数，再增加的事件可以使用 USEREVENT + 1 指定，依次类推…
    pygame.time.set_timer(CREATE_ENEMY, random.randint(500, 1000))
    pygame.time.set_timer(CREATE_BOSS, random.randint(3000, 5000))
    pygame.time.set_timer(CREATE_BULLET_HELP, random.randint(3000, 5000))
    font = pygame.font.Font(None, 32)

    while True:
        bggroup.update()
        bggroup.draw(screen)

        playergroup.update()
        playergroup.draw(screen)

        enemygroup.update()
        enemygroup.draw(screen)

        bossgroup.update()
        bossgroup.draw(screen)

        bullethelpgroup.update()
        bullethelpgroup.draw(screen)

        screen.blit(font.render("Score:"+str(playersprite.score), True, (255, 0, 0)), (20, 20))
        screen.blit(font.render("HP:" + str(playersprite.hp), True, (255, 0, 0)), (20, 60))

        pygame.display.update()
        # pygame.sprite.groupcollide - 查找在两个组之间发生碰撞的所有精灵。
        '''
        # groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict
        这将在两组中找到所有精灵之间的碰撞。 通过比较每个Sprite的Sprite.rect属性或使用碰撞函数（如果它不是None）来确定碰撞。
        # group1中的每个Sprite都被添加到返回字典中。 每个项的值是group2中相交的Sprite列表。
        # 如果dokill参数为True，则将从各自的组中删除碰撞的Sprite。
        # 碰撞参数是一个回调函数，用于计算两个精灵是否发生碰撞。 
        它应该将两个精灵作为值并返回一个bool值，指示它们是否发生碰撞。 
        如果未传递碰撞，则所有精灵必须具有“rect”值，该值是精灵区域的矩形，将用于计算碰撞。
        '''
        check1 = pygame.sprite.groupcollide(playersprite.bulletgroup, enemygroup, True, False)#碰撞检测 销毁子弹 销毁敌机
        # 这里面注意要用if语句判断一下再用
        if check1:      # 说明击中但是减血而不是爆炸
            enemy.hp -= 1
            if enemy.hp <= 0:
                # values()得到的是一个字典形式的查询集(QuerySet),查询集是一个可迭代对象
                # 然后转化为列表
                # 代码中使用array[0][0] 来提取位置元素,本程序换成[0,0]也能运行
                # .bomb之所以这么做是为了显示连续的爆炸图像，

                list(check1.values())[0][0].bomb()
                playersprite.score += 100
        # ###########################################
        check11 = pygame.sprite.groupcollide(playersprite.bulletgroup, bossgroup, True, False)  # 碰撞检测 销毁子弹 销毁敌机
        if check11:
            boss.hp -= 1
            if boss.hp <= 0:
                list(check11.values())[0][0].bomb()
                playersprite.score += 500
        # ##########################################
        check2 = pygame.sprite.groupcollide(playergroup, enemygroup, False, True)
        # 这里面要敌机毁掉但是我方战机不会爆炸只会掉血
        if check2:
            list(check2.values())[0][0].bomb()
            playersprite.hp -= 1
        # ##########################################
        check22 = pygame.sprite.groupcollide(playergroup, bossgroup, False, True)
        if check22:
            list(check22.values())[0][0].bomb()
            playersprite.hp -= 1
        # ##########################################
        # print(enemygroup)
        for enemy in enemygroup:
            check3 = pygame.sprite.groupcollide(playergroup, enemy.bulletgroup, False, True)
            if check3:
                playersprite.hp -= 1
                # playersprite.bullettype = 0
        # ##########################################
        for boss in bossgroup:
            check33 = pygame.sprite.groupcollide(playergroup, boss.bulletgroup, False, True)
            if check33:
                playersprite.hp -= 1
                # playersprite.bullettype = 0
        if playersprite.hp <= 0:
            playersprite.kill()
        # ##########################################
        check4 = pygame.sprite.groupcollide(playergroup, bullethelpgroup, False, True)
        if check4:
            if playersprite.bullettype <= 1:
                playersprite.bullettype += 1
                playersprite.bulletnum = 10
            else:
                playersprite.bulletnum = 10
        playersprite.fire()
        for event in pygame.event.get():
            # if event.type == locals.KEYUP:
            #     if event.key == locals.K_SPACE:
            #         playersprite.fire()
            if event.type == locals.QUIT:
                pygame.quit()
                exit()
            if event.type == CREATE_ENEMY:
                enemy = EnemySprite("images/enemy/enemy2.png", [random.randint(0, 410), -50], 2, screen, random.randrange(-1, 1, 2), 0, 1)
                enemygroup.add(enemy)
            if event.type == CREATE_BOSS:
                boss = EnemySprite("images/enemy/boss.png", [random.randint(0, 410), -50], 1, screen, 0, 1, 15)
                bossgroup.add(boss)
            if event.type == CREATE_BULLET_HELP:
                bullethelp = BulletHelp("images/hero/supply.png", [0, 0, 40, 41], [random.randint(0, 410), -50], 2, screen, random.randrange(-1, 1, 2))
                bullethelpgroup.add(bullethelp)
            # playersprite.fire() #自动开火


if __name__ == '__main__':
    main()

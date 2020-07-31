import pygame
from pygame import locals
from sys import exit


def main():
    # 1  模块初始化
    pygame.init()
    # 2  获取绘制屏幕
    screen = pygame.display.set_mode((512, 768))
    # 8 设置窗口标题
    pygame.display.set_caption("雷霆战机")
    # 6 加载背景对象
    background = pygame.image.load("images/bg/bg.jpg")
    print(background.get_rect())
    # pygame.display.set_icon("images/hero/hero.png")
    # pygame.display.set_icon()  —  修改显示窗口的图标

    # 9 加载我方飞机
    player = pygame.image.load("images/hero/hero2.png")    # 使用单独的图片
    # allimage = pygame.image.load("images/hero/shoot.png")   # 加载共享大图
    # player = allimage.subsurface(0,99,102,106)    # 从共享大图中加载玩家飞机
    playerpos = [background.get_rect().w/2 - player.get_rect().w/2, 600]  # 居中公式
    # 第一个元素为宽，第二个元素为高
    # print("777"+playerpos)
    # 13 定义玩家分数 加载字体对象
    font = pygame.font.Font(None, 32)
    # 参数file：采用字体文件的路径，如果file参数设置为None则默认采用系统自带字体，如果自带字体文件无法打开就会报错；　　
    # 参数size：字体的大小
    score = 0

    # 3 游戏主循环
    while True:
        # 7  将背景对象绘制到屏幕中
        screen.blit(background, (0, 0))
        # 10 绘制我方飞机
        screen.blit(player, playerpos)
        # 14 渲染分数
        # font.render参数意义：.render（内容，是否抗锯齿，字体颜色，字体背景颜色）
        # 参考csdn 收藏的pygame的font模块
        screen.blit(font.render("Score:" + str(score), True, (255, 0, 0)), (20, 20))
        # 4 刷新屏幕
        pygame.display.update()
        # 5 事件监听
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                exit()
            # 12 监听到键盘事件
            # locals. K_键位为具体展示键
            elif event.type == locals.KEYDOWN:
                if event.key == locals.K_SPACE:
                    print("释放子弹")
                    score += 1
                elif event.key == locals.K_j:
                    print("释放技能1")
                elif event.key == locals.K_k:
                    print("释放技能2")
                elif event.key == locals.K_l:
                    print("释放技能3")

        # 11 接收用户输入
        key_events = pygame.key.get_pressed()
        # print(key_events)
        if key_events[locals.K_a] or key_events[locals.K_LEFT]:
            playerpos[0] -= 4
        elif key_events[locals.K_d] or key_events[locals.K_RIGHT]:
            playerpos[0] += 4
        elif key_events[locals.K_w] or key_events[locals.K_UP]:
            playerpos[1] -= 4
        elif key_events[locals.K_s] or key_events[locals.K_DOWN]:
            playerpos[1] += 4
        if playerpos[0] < 0:
            playerpos[0] = 0
        elif playerpos[0] > background.get_rect().w - player.get_rect().w:
            playerpos[0] = background.get_rect().w - player.get_rect().w
        elif playerpos[1] < 0:
            playerpos[1] = 0
        elif playerpos[1] > background.get_rect().h - player.get_rect().h:
            playerpos[1] = background.get_rect().h - player.get_rect().h


if __name__ == '__main__':
    main()

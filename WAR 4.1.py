import pygame
from pygame import locals
from sys import exit

offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
# 这个字典设计的牛逼，可以实现八个方向的运动
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 768


def main():
    # 1 模块初始化
    pygame.init()
    # 2 获取绘制屏幕
    screen = pygame.display.set_mode((512, 768))

    # 8 设置窗口标题
    pygame.display.set_caption("雷霆战机")
    # 6 加载背景对象
    background = pygame.image.load("images/bg/bg.jpg")
    print(background.get_rect())
    # pygame.display.set_icon("images/hero/hero.png") 修改显示窗口的图标
    # 9 加载我方飞机
    player = pygame.image.load("images/hero/hero.png")  # 使用单独的图片
    # allimage = pygame.image.load("images/hero/shoot.png")   #加载共享大图
    # player = allimage.subsurface(0,99,102,106)    #从共享大图中加载玩家飞机
    playerpos = [background.get_rect().w / 2 - player.get_rect().w / 2, 600]  # 居中公式
    # print("777"+playerpos)
    # 13 定义玩家分数 加载字体对象
    # Font(object, size) -> Font
    font = pygame.font.Font(None, 32)
    Score = 0
    # 3 游戏主循环
    while True:
        # 7 将背景对象绘制到屏幕中
        screen.blit(background, (0, 0))
        # 10 绘制我方飞机
        screen.blit(player, playerpos)

        #  11 渲染分数
        # render(text, antialias, color, background=None) -> Surface
        # 返回的 Surface 对象将保持表示文本所需要的尺寸（与 Font.size() 所返回的尺寸相同）
        screen.blit(font.render("Score:" + str(Score), True, (255, 0, 0)), (20, 20))
        # 4 刷新屏幕
        pygame.display.update()
        # 5 事件监听
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                exit()
            elif event.type == locals.KEYDOWN:
                if event.key == locals.K_SPACE:
                    print("发射子弹")
                    Score += 1
                elif event.key == locals.K_j:
                    print("释放技能1")

        # 11 接收用户输入
        key_events = pygame.key.get_pressed()
        # print(key_events)
        # 控制方向 == new add ==
        """"""
        #  如果按键满足字典内任何一个key，那么就将值改成需要的速度值，但是满足按下改变，抬起变回0
        """"""
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = 9       # 移动速度
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0


        hero_x = playerpos[0] + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT] # 克服按键冲突
        hero_y = playerpos[1] + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if hero_x < 0:
            playerpos[0] = 0
        elif hero_x > SCREEN_WIDTH - player.get_rect().w:
            playerpos[0] = SCREEN_WIDTH - player.get_rect().w
        else:
            playerpos[0] = hero_x

        if hero_y < 0:
            playerpos[1] = 0
        elif hero_y > SCREEN_HEIGHT - player.get_rect().h:
            playerpos[1] = SCREEN_HEIGHT - player.get_rect().h
        else:
            playerpos[1] = hero_y


if __name__ == '__main__':
    main()

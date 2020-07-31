import pygame
from pygame import locals
from sys import exit


def main():
    # 1 初始化pygame模块
    pygame.init()
    # 2 获取绘制窗口
    # set_mode中resoultion是指定宽和高，默认条件会和屏幕大小一致
    # flags指定屏幕附加选项，一般默认即可
    # depth表示颜色位数，默认自动匹配
    # TODO set_mode必须要有返回结果
    screen = pygame.display.set_mode((512, 768))
    # 8 设置窗口标题
    pygame.display.set_caption("雷霆战机")
    # 3 游戏使用主循环
    while True:
        # 4 刷新游戏屏幕
        # todo 4.update 更新屏幕显示
        # todo pygame.display.update()
        # TODO 格式固定，必须要用这个，否则看不到最新结果
        pygame.display.update()
        # 5 监听游戏事件
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    """
    定义项目入口函数
    """
    main()

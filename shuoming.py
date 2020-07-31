# TODO pygame入门
# 在游戏中，所有可见元素都是通过矩形区域来表示的，
# 本例中给出左上角为原点，横轴向右为x，纵轴向下为y，同时还要有（x，y，width，height）
# pygame 专门有一个特殊类 pygame.Rect用以描述矩形区域
# 注意pygame.Rect 中的R务必大写！,且第一个是宽度，第二个是高度
# 初始化 退出，导入三个环节不能少

# TODO 游戏窗口
# pygame专门提供一共模块pygame.display来创建窗口
# set_mode中resoultion是指定宽和高，默认条件会和屏幕大小一致
# flags指定屏幕附加选项，一般默认即可
# depth表示颜色位数，默认自动匹配
# set_mode必须要有返回结果

# TODO 创建图像
# 1.加载图像数据 ；load为装载路径，本地址直接用.表示
# 2.blit绘制图像,注意这个没有智能提示，blit（图像，位置），位置是一个元组
# 3.update 更新屏幕显示 ；格式固定，必须要用这个，否则看不到最新结果

# TODO 游戏循环
# 注意要创建一个时钟对象；pygame.time.Clock可以设置时钟（C必须大写）。。。。屏幕绘制速度-刷新帧率
# tick法会自动设置循环延时,一般等于屏幕刷新率（60或者144）
# 格式 self.clock.tick()

# TODO 更新位置
# 判断位置y是否小于等于0；if hero_rect.y + hero_rect.height <= 0:
# top :与窗口上边界的距离
# bottom :与窗口上边界的距离 + 图像本身的高度(height)
# 这里面用bottom参考图形设计意义即可

# TODO 注意事项
# 为了去除残影，需要每次循环重新绘制背景图像来抵消前一次的飞机图像
# 每一次调用update方法之前，需要把所有游戏图像全部绘制一遍
# 每次最先重新绘制背景图像

# TODO 监听
# 捕获事件，只有捕获游戏才有具体操作
# pygame.event.get函数可以获取用户当前动作，返回一个事件的列表
# event.type判断类型

# TODO 监听退出
# 判断事件类型是否为退出事件，pygame.QUIT是一个标志，表明要结束
# quit卸载全部模块
# 内置exit 直接退出全部程序

# TODO sprites
# 定义GameSprites继承自pygame.sprite.Sprite
# 后者第二部分是模块名，第三部分是类名，首字母大写
# 如果一个类的父类不是object，（）不写就默认是object，则在重写初始化方法中主动要先
# 调用super（）一下父类的__init__方法，否则无法享受父类已经写好的代码了
# 调用父类的初始化方法,speed默认为1
# 将指定的image_name创建，并加载对象中
# get_rect方法可以返回pygame.Rect（0,0，图像宽，图像高）的对象

# TODO 精灵演练
# todo 创建敌机的精灵组,用group类创建
# enemy_group = pygame.sprite.Group(enemy1, enemy2, enemy3, enemy4)

# todo 创建敌机的精灵
# enemy1 = GameSprite("./images/enemy1.png", 4)
# enemy2 = GameSprite("./images/enemy2.png", 3)
# enemy3 = GameSprite("./images/enemy3_n1.png", 1)
# enemy4 = GameSprite("./images/enemy3_n2.png", 2)

# todo 游戏循环,在循环中让精灵组调用update和draw（screen）
# update方法让精灵组所有精灵更新位置
# enemy_group.update()
# draw方法在屏幕上画出所有精灵
# enemy_group.draw(screen)

# todo 架构分析
"""最核心的重点"""
# 需要游戏初始化和游戏循环两大块
# TODO 初始化需要设置游戏的窗口，创建游戏时钟，同时创建精灵组和精灵
# 初始化方法中精灵组创建建议使用私有方法，从而减少改动效果
# TODO 循环主要是设置刷新帧率，监听事件，碰撞检测，更新精灵和精灵组，更新屏幕显示几部分

# TODO 定时器
# 使用pygame.time.set_timer()添加定时器，有两个关键参数
# 第一个是事件代号，基于整数常量pygame.USERVENT指定
# 第二个是milisecond，是事件触发的间隔毫秒值,单位是毫秒
# TODO 主要有三步：定义定时器常量、设置定时器事件、事件监听检测

# todo 键盘按键捕获
# 两种方式，第一种用pygame.KEYDOWN,如果是左边就是pygame.K_RIGHT,其他同理
# 第二种是利用键盘pygame.key.get_pressed()返回所有按键元组，如果按下就返回1
# 但是这种情况需要引入左右分析

#启动类
import pygame
from . import constants as C
from . import tools
#代表使用相对路径导入，即从当前项目中寻找需要导入的包或函数

pygame.init()
SCREEN=pygame.display.set_mode((C.SCREEN_WIDTH,C.SCREEN_HEIGHT))

GRAPHICS=tools.load_graphics("resources/graphics")


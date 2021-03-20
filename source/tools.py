#工具类
import pygame
from random import *
import sys
import os

class Game:

    def __init__(self,state_dict,start_state):
        self.screen=pygame.display.get_surface()
        self.clock=pygame.time.Clock()
        self.keys=pygame.key.get_pressed()
        self.state_dict=state_dict
        self.state=self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            next_state=self.state.next
            self.state.finished=False
            self.state=self.state_dict[next_state]
        self.state.update(self.screen,self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    self.keys=pygame.key.get_pressed()
                elif event.type==pygame.KEYUP:
                    self.keys=pygame.key.get_pressed()

            self.update()

            pygame.display.update()
            self.clock.tick(60)



def load_graphics(path,accept=('.png','.jpg','.gif')):
    """加载图片"""
    graphics={}
    for pic in os.listdir(path):                            #返回指定的文件夹包含的文件或文件夹的名字的列表。
        name,ext=os.path.splitext(pic)                      #分割路径，返回路径名和文件扩展名的元组
        if ext.lower() in accept:                            #转换字符串中所有大写字符为小写
            img=pygame.image.load(os.path.join(path,pic))       #把目录和文件名合成一个路径
            if img.get_alpha():
                img=img.convert_alpha()
            else:
                img=img.convert()
            graphics[name]=img
    return graphics


def get_image(sheet,x,y,width,height,colorkey,scale):
    """抠图"""
    image=pygame.Surface((width,height))
    image.blit(sheet,(0,0),(x,y,width,height))
    image.set_colorkey(colorkey)
    image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    return image
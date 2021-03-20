#游戏信息
import pygame
from .. import setup,tools
from .. import constants as C
from . import coin

pygame.font.init()

class Info:


    def __init__(self,state):
        self.state=state
        self.create_state_labels()
        self.create_info_labels()
        self.flash_coin=coin.FlashingCoin()

    def create_state_labels(self):
        self.state_labels = []
        if self.state=='main_menu':
            self.state_labels.append((self.create_labels("1  PLAYER GAME"),(272,360)))
            self.state_labels.append((self.create_labels("2  PLAYER GAME"),(272,405)))
            self.state_labels.append((self.create_labels("TOP -"),(290,465)))
            self.state_labels.append((self.create_labels("000000"),(400,465)))
        elif self.state=='load_screen':
            self.state_labels.append((self.create_labels("WORLD"), (280, 200)))
            self.state_labels.append((self.create_labels("1 - 1"), (430, 200)))
            self.state_labels.append((self.create_labels("X    3"), (380, 280)))
            self.player_image=tools.get_image(setup.GRAPHICS['mario_bros'],178,32,12,16,(0,0,0),C.PLAYER_MULTI)


    def create_info_labels(self):
        self.info_labels=[]
        self.info_labels.append((self.create_labels("WARIO"),(75,30)))
        self.info_labels.append((self.create_labels("WARLD"),(450,30)))
        self.info_labels.append((self.create_labels("TIME"),(625,30)))
        self.info_labels.append((self.create_labels("000000"),(75,55)))
        self.info_labels.append((self.create_labels("x 00"),(300,55)))
        self.info_labels.append((self.create_labels("1 - 1"),(480,55)))

    def create_labels(self,label,size=40,width_scale=1.25,height_scale=1):
        font=pygame.font.SysFont(C.FONT,size)
        label_images=font.render(label,1,(255,255,255))
        rect=label_images.get_rect()
        label_images=pygame.transform.scale(label_images,(int(rect.width * width_scale),
                                                          int(rect.height * height_scale)))
        return label_images

    def update(self):
        self.flash_coin.update()

    def draw(self,surface):
        for labels in self.state_labels:
            surface.blit(labels[0],labels[1])
        for labels in self.info_labels:
            surface.blit(labels[0],labels[1])
        surface.blit(self.flash_coin.image,self.flash_coin.rect)

        if self.state=='load_screen':
            surface.blit(self.player_image,(300,270))
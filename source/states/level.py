import pygame
from ..components import info,player,stuff
from .. import setup,tools
from .. import constants as C
import os
import json

class Level:

    def __init__(self):
        self.next=None
        self.finished=False
        self.info=info.Info('level')
        self.load_map_data()
        self.setup_background()
        self.setup_start_positions()
        self.setup_player()
        self.setup_ground_items()


    def load_map_data(self):
        file_name='level_1.json'
        file_path=os.path.join('source/data/maps',file_name)
        with open(file_path) as f:
            self.maps_data=json.load(f)

    def setup_background(self):
        self.image_name=self.maps_data['image_name']
        self.background = setup.GRAPHICS[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI),
                                                                   int(rect.height * C.BG_MULTI)))
        self.background_rect = self.background.get_rect()

        self.game_window=setup.SCREEN.get_rect()
        self.game_ground=pygame.Surface((self.background_rect.width,self.background_rect.height))

    def setup_start_positions(self):                #设置开始位置
        self.positions=[]
        for data in self.maps_data['maps']:
            self.positions.append((data['start_x'],data['end_x'],data['player_x'],data['player_y']))
        self.start_x,self.end_x,self.player_x,self.player_y=self.positions[0]

    def setup_player(self):
        self.player=player.Player('mario')
        self.player.rect.x=self.player_x+self.game_window.x                 #玩家相对窗口位置
        self.player.rect.bottom=self.player_y

    def setup_ground_items(self):
        self.ground_items_group=pygame.sprite.Group()
        for name in ['ground','pipe',step]:
            for item in self.maps_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'],item['y'],item['width'],item['height'],name))

    def update(self,surface,keys):
        self.player.update(keys)
        self.update_player_position()
        self.update_window_position()
        self.draw(surface)

    def update_player_position(self):
        self.player.rect.x+=self.player.x_vel
        if self.player.rect.x < self.start_x:          #限制玩家不能走出窗口
            self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.player.rect.y+=self.player.y_vel

    def update_window_position(self):                               #画面跟随角色移动
        third=self.game_window.x + self.game_window.width/3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < self.end_x:
            self.game_window.x+=self.player.x_vel
            self.start_x=self.game_window.x

    def draw(self,surface):
        self.game_ground.blit(self.background,self.game_window,self.game_window)
        self.game_ground.blit(self.player.image,self.player.rect)
        surface.blit(self.game_ground,(0,0),self.game_window)
        self.info.draw(surface)

import pygame
from .. import setup,tools
from .. import constants as C
import json
import os

class Player(pygame.sprite.Sprite):

    def __init__(self,name):
        pygame.sprite.Sprite.__init__(self)

        self.name=name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()


    #加载玩家json数据文件
    def load_data(self):
        file_name=self.name+'.json'
        file_path=os.path.join('source/data/player',file_name)
        with open(file_path) as f:
            self.player_data=json.load(f)

    #角色状态
    def setup_states(self):
        self.state='stand'
        self.face_right=True
        self.big=False
        self.dead=False
        self.can_jump=True

    #各方向速度
    def setup_velocities(self):
        speed=self.player_data['speed']
        self.x_vel=0
        self.y_vel=0

        self.max_walk_vel=speed["max_walk_speed"]          #速度
        self.max_run_vel=speed["max_run_speed"]
        self.max_y_vel=speed["max_y_velocity"]
        self.walk_accel=speed["walk_accel"]                 #加速度
        self.run_accel=speed["run_accel"]
        self.turn_accel=speed["turn_accel"]                 #转身
        self.jump_velocity=speed["jump_velocity"]          #重力
        self.anti_jump_velocity=speed["anti_jump_velocity"]
        self.gravity=C.GRAVITY

        self.max_x_vel=self.max_walk_vel
        self.x_accel=self.walk_accel


    #时长
    def setup_timers(self):
        self.walk_timer=0
        self.transition_timer=0

    #角色帧造型
    def load_images(self):
        sheet=setup.GRAPHICS['mario_bros']
        frame_rects=self.player_data['image_frames']

        self.right_small_normal_frames=[]
        self.right_big_normal_frames=[]
        self.right_big_fire_frames=[]
        self.left_small_normal_frames=[]
        self.left_big_normal_frames=[]
        self.left_big_fire_frames=[]

        self.small_normal_frames=[self.right_small_normal_frames,self.left_small_normal_frames]
        self.big_normal_frames=[self.right_big_normal_frames,self.left_big_normal_frames]
        self.big_fire_frames=[self.right_big_fire_frames,self.left_big_fire_frames]

        self.all_frames=[
            self.right_small_normal_frames,
            self.right_big_normal_frames,
            self.right_big_fire_frames,
            self.left_small_normal_frames,
            self.left_big_normal_frames,
            self.left_big_fire_frames
        ]

        self.right_frames=self.right_small_normal_frames
        self.left_frames=self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'],
                                                frame_rect['width'], frame_rect['height'], (0, 0, 0), C.PLAYER_MULTI)
                left_image = pygame.transform.flip(right_image, True, False)
                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_image)
                    self.left_small_normal_frames.append(left_image)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_image)
                    self.left_big_normal_frames.append(left_image)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_image)
                    self.left_big_fire_frames.append(left_image)

        self.frame_index = 0
        self.frames=self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self,keys):
        self.current_time=pygame.time.get_ticks()
        self.handle_states(keys)

    def handle_states(self,keys):
        if self.state== 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'basketball':
            self.basketball(keys)
        if self.face_right:
            self.image=self.right_frames[self.frame_index]
        else:
            self.image=self.left_frames[self.frame_index]

        self.can_jump_or_not(keys)

    def can_jump_or_not(self,keys):
        if not keys[pygame.K_KP2]:
            self.can_jump=True

    def stand(self,keys):
        self.frame_index=0
        self.x_vel=0
        self.y_vel=0

        if keys[pygame.K_RIGHT]:
            self.face_right=True
            self.state='walk'
        elif keys[pygame.K_LEFT]:
            self.face_right=False
            self.state='walk'
        elif keys[pygame.K_KP2] and self.can_jump:
            self.state='jump'
            self.y_vel=self.jump_velocity

    def walk(self,keys):
        if keys[pygame.K_KP1]:
            self.max_x_vel=self.max_run_vel
            self.x_accel=self.run_accel
        else:
            self.max_x_vel = self.max_walk_vel
            self.x_accel = self.walk_accel
        if keys[pygame.K_KP2] and self.can_jump:
            self.state = 'jump'
            self.y_vel = self.jump_velocity
        if self.current_time - self.walk_timer > self.calc_frame_duration():
            if self.frame_index < 3:
                self.frame_index+=1
            else:
                self.frame_index=1
            self.walk_timer=self.current_time
        if keys[pygame.K_RIGHT]:
            self.face_right=True
            if self.x_vel < 0:
                self.frame_index=5
                self.x_accel=self.turn_accel
            self.x_vel=self.calc_vel(self.x_vel,self.x_accel,self.max_x_vel,True)
        elif keys[pygame.K_LEFT]:
            self.face_right=False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel,self.x_accel,self.max_x_vel,False)
        else:
            if self.face_right:
                self.x_vel-=self.x_accel
                if self.x_vel < 0:
                    self.x_vel=0
                    self.state='stand'
            else:
                self.x_vel+=self.x_accel
                if self.x_vel > 0:
                    self.x_vel=0
                    self.state='stand'

    def jump(self,keys):
        self.frame_index=4
        self.y_vel+=self.anti_jump_velocity

        self.can_jump=False

        if self.y_vel > 0:
            self.state='fall'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)

        if not keys[pygame.K_KP2]:
            self.state='fall'

    def fall(self,keys):
        self.y_vel=self.calc_vel(self.y_vel,self.gravity,self.max_y_vel,True)

        # TODO   临时代码
        if self.rect.bottom >= C.GROUND_HEIGHT:
            self.rect.bottom = C.GROUND_HEIGHT
            self.y_vel=0
            self.state='walk'

        if keys[pygame.K_RIGHT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)


    def basketball(self,keys):
        pass

    def calc_vel(self,vel,accel,max_vel,is_positive):
        if is_positive:
            if vel <= max_vel:
                return min(vel + accel, max_vel)
            else:
                return max(vel - self.walk_accel, max_vel)  # 结束加速恢复原速
        else:
            if vel >= -max_vel:
                return max(vel - accel, -max_vel)
            else:
                return min(vel + self.walk_accel, max_vel)  # 结束加速恢复原速

    def calc_frame_duration(self):
        duration=-60/self.max_run_vel*abs(self.x_vel)+80
        return duration
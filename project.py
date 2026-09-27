# import section
import pygame as pg
from random import randint, uniform, choice

# CONSTANTS for setup
DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 800
DISPLAY_CAPTION = 'PONG - CHAOS EDITION'
MAX_FRAMERATE = 60

# basic pygame setup
pg.init()
display_surface = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption(DISPLAY_CAPTION)
clock = pg.Clock()

# CONSTANTS grouped in dictionaries
COLORS = {
    'bg_game':      '#AA4B39',  'bg_start':         '#AA4B39',   'bg_pause':     '#AA4B39', 'bg_end':     '#8E1B06',
    'title':        '#E4D6D3',  'subtitle':         '#C6887D', 
    'ui_text':      '#E4D6D3',  'ui_frame':         '#C6887D',
    'field':        '#E4D6D3',  'field_hit':        '#721200',
    'score_player': '#AA9739',  'score_opponent':   '#665C88',
    'player_lv1':   '#C6BA7D',  'player_lv2':       '#AA9739',   'player_lv3':   '#8E7706', 'player_lv4': '#725E00',
    'opponent_lv1': '#665C88',  'opponent_lv2':     '#403075',   'opponent_lv3': '#220F62',
    'impact':       '#E4D5D3',
    'ball_lv1':     '#2A7E43',  'ball_lv2':         '#046923',   'ball_lv3':     '#005419',
    'vball':        '#E4D6D3',
    'laser_red':    '#721000',
    'laser_blue':   '#14024E',
    'frozen':       '#95939D'
    }

SIZES = {
    'font_score':           50,
    'font_title':           100,        'font_subtitle':    50,
    'font_ui':              30,
    'paddles_vertical':     (32, 96),
    'paddles_horizontal':   (96, 32),
    'ball':                 (32, 32),
    'laser':                (16, 4),
}

SPEEDS = {
    'player_lv1':   400,    'player_lv2':   450,    'player_lv3':   500,
    'player_boost': 200,
    'opponent_lv1': 300,    'opponent_lv2': 400,    'opponent_lv3': 550,
    'ball_lv1':     400,    'ball_lv2':     425,    'ball_lv3':     450,
    'laser_red':    1000,
    'laser_blue':   2000,
    'frozen':       50,
}

ACCELERATION = {
    'player':       0.15,
    'opponent_lv1': 0.02,   'opponent_lv2': 0.03,   'opponent_lv3': 0.04,
}

DURATIONS = {
    'ball_1_move_delay': 700,
    'ball_2_move_delay': 1400,
    'impact_flash':      100,
    'frozen':            3000,
}

AUDIO = {
    # music
    'mus_full':                 'audio/mus_mowpea_pong_full.ogg',
    'mus_loop':                 'audio/mus_mowpea_pong_loop.ogg',

    # sound effects
    # commented out, as calling .play() on mixer.Sound objects during gameplay crashed pygame
    # leaving this section in project for future reference

    # 'sfx_ball1_explode':        pg.mixer.Sound('audio/sfx_env_ball1_explode.ogg'),
    # 'sfx_ball2_explode':        pg.mixer.Sound('audio/sfx_env_ball2_explode.ogg'),

    # 'sfx_balls_frozen':         pg.mixer.Sound('audio/sfx_env_balls_frozen.ogg'),
    # 'sfx_balls_unfrozen':       pg.mixer.Sound('audio/sfx_env_balls_unfrozen.ogg'),
    # 'sfx_balls_hit_paddle_01':  pg.mixer.Sound('audio/sfx_env_balls_hit_paddle_01.ogg'),
    # 'sfx_balls_hit_paddle_02':  pg.mixer.Sound('audio/sfx_env_balls_hit_paddle_02.ogg'),
    # 'sfx_balls_hit_paddle_03':  pg.mixer.Sound('audio/sfx_env_balls_hit_paddle_03.ogg'),
    # 'sfx_balls_hit_paddle_04':  pg.mixer.Sound('audio/sfx_env_balls_hit_paddle_04.ogg'),
    # 'sfx_balls_hit_paddle_05':  pg.mixer.Sound('audio/sfx_env_balls_hit_paddle_05.ogg'),
    # 'sfx_balls_hit_paddle_06':  pg.mixer.Sound('audio/sfx_env_balls_hit_paddle_06.ogg'),
    # 'sfx_balls_hit_walls_01':   pg.mixer.Sound('audio/sfx_env_balls_hit_walls_01.ogg'),
    # 'sfx_balls_hit_walls_02':   pg.mixer.Sound('audio/sfx_env_balls_hit_walls_02.ogg'),
    # 'sfx_balls_hit_walls_03':   pg.mixer.Sound('audio/sfx_env_balls_hit_walls_03.ogg'),

    # 'sfx_laser_bounce_01':      pg.mixer.Sound('audio/sfx_env_laser_bounce_01.ogg'),
    # 'sfx_laser_bounce_02':      pg.mixer.Sound('audio/sfx_env_laser_bounce_02.ogg'),

    # 'sfx_opponent_frozen':      pg.mixer.Sound('audio/sfx_opponent_frozen.ogg'),
    # 'sfx_opponent_unfrozen':    pg.mixer.Sound('audio/sfx_opponent_unfrozen.ogg'),
    # 'sfx_opponent_shoot_red':   pg.mixer.Sound('audio/sfx_opponent_shoot_red.ogg'),
    # 'sfx_opponent_shoot_blue':  pg.mixer.Sound('audio/sfx_opponent_shoot_blue.ogg'),

    # 'sfx_plr_boost':            pg.mixer.Sound('audio/sfx_plr_boost.ogg'),
    # 'sfx_plr_shoot_red':         pg.mixer.Sound('audio/sfx_plr_shoot_red.ogg'),
    # 'sfx_plr_shoot_blue':       pg.mixer.Sound('audio/sfx_plr_shoot_blue.ogg'),
    # 'sfx_plr_frozen':           pg.mixer.Sound('audio/sfx_plr_frozen.ogg'),
    # 'sfx_plr_unfrozen':         pg.mixer.Sound('audio/sfx_plr_unfrozen.ogg'),

    # 'sfx_ui_start_game':        pg.mixer.Sound('audio/sfx_ui_start_game.ogg'),
    # 'sfx_ui_pause_game':        pg.mixer.Sound('audio/sfx_ui_pause_game.ogg'),
    # 'sfx_ui_progress':          pg.mixer.Sound('audio/sfx_ui_progress.ogg'),
    # 'sfx_ui_score_opponent':    pg.mixer.Sound('audio/sfx_ui_score_opponent.ogg'),
    # 'sfx_ui_score_player':      pg.mixer.Sound('audio/sfx_ui_score_player.ogg'),
    # 'sfx_ui_lose_game':         pg.mixer.Sound('audio/sfx_ui_lose_game.ogg'),
    # 'sfx_ui_win_game':          pg.mixer.Sound('audio/sfx_ui_win_game.ogg'),
}

# states
running = True
start_game = True
in_game = False
end_game = False

# fonts with different sizes
font_score = pg.font.Font(filename = None, size = SIZES['font_score'])
font_title = pg.font.Font(filename = None, size = SIZES['font_title'])
font_subtitle = pg.font.Font(filename = None, size = SIZES['font_subtitle'])
font_ui = pg.font.Font(filename = None, size = SIZES['font_ui'])

# global variables
ball_1_can_spawn = True
ball_2_can_spawn = True
audio_volume = 0.5

# classes

# used some concepts from a pygame youtube tutorial by the channel 'Clear Code'
# copied or slightly changed code snippets from that tutorial will be marked with a comment 
# referring to 'CCPT' (Clear Code Pygame Tutorial)

# where functions serve same purpose across in different classes, there will be no comments

class Player(pg.sprite.Sprite):
    """A class for the player's paddle."""
    def __init__(self, groups):
        # CCPT: calling super() to pass arguments to parent class
        super().__init__(groups)

        # player level
        # used to unlock functions as the player progresses
        self.current_level = 1
        self.level = self.current_level
        
        # sprite of the player paddle
        self.image = pg.surface.Surface(SIZES['paddles_vertical'], flags = pg.SRCALPHA)
        # outer rectangle
        pg.draw.rect(
            surface = self.image, 
            color = COLORS[f'player_lv{self.level}'], 
            rect = pg.FRect(0, 0, SIZES['paddles_vertical'][0], SIZES['paddles_vertical'][1]),
            width = 4,
            border_radius = 4)
        # inner rectangle
        pg.draw.rect(
            surface = self.image,
            color = COLORS[f'player_lv{self.level}'],
            rect = pg.FRect(2, 2, SIZES['paddles_vertical'][0] - 5, SIZES['paddles_vertical'][1] - 5),
        )

        self.rect = self.image.get_frect(center = (30, DISPLAY_HEIGHT/2))
        # CCPT: use extra rectangle for collision detection between two moving objects (s. Ball and VBall classes)
        self.old_rect = self.rect.copy()

        # movement
        self.direction_y = 0
        self.speed = SPEEDS[f'player_lv{self.level}']
        self.acceleration = ACCELERATION['player']

        # abilities
        self.boost_duration = 3000
        self.boost_cooldown = 10000
        self.boost_available = True

        self.laser_red = None
        self.laser_red_unlocked = False
        self.laser_red_cooldown = 3000
        self.laser_red_available = True

        self.laser_blue = None
        self.laser_blue_unlocked = False
        self.laser_blue_cooldown = 4500
        self.laser_blue_available = True

        # frozen states
        self.can_freeze = True
        self.frozen = False

        # timers
        self.timer_boost_active = Timer(self.boost_duration, func = self.reset_speed)
        self.timer_boost_cooldown = Timer(self.boost_cooldown, func = self.boost_set_available)

        self.timer_laser_red_cooldown = Timer(self.laser_red_cooldown, func = self.laser_red_set_available)
        self.timer_laser_blue_cooldown = Timer(self.laser_blue_cooldown, func = self.laser_blue_set_available)

        self.default_color = True
        self.timer_color = Timer(duration = DURATIONS['impact_flash'], func = self.reset_color_change)

        self.timer_melt = Timer(duration = DURATIONS['frozen'], func = self.melt)

    def input(self):
        # inputs for movement

        # CCPT: basic concept of using keys to only change direction
        keys = pg.key.get_pressed()
        # amended CCPT code to add inertia to movement for an organic feel
        # lack of instant response also serves to make opponent more prone to mistakes (s. Opponent class)
        if keys[pg.K_w]:
            self.direction_y -= self.acceleration
            if self.direction_y < -1:
                self.direction_y = -1
        elif keys[pg.K_s]:
            self.direction_y += self.acceleration
            if self.direction_y > 1:
                self.direction_y = 1
        else:
            self.direction_y = 0

        # inputs for abilities

        # level 1: speed boost -> increases player speed for time specified in self.boost_duration
        action_key = pg.key.get_just_pressed()
        if self.level >= 1 and self.level != 4:
            if action_key[pg.K_SPACE] and self.boost_available:
                self.boost_speed()
                self.timer_boost_active.activate()
                self.timer_boost_cooldown.activate()
            elif action_key[pg.K_SPACE] and not self.boost_available:
                print('Boost is still in cooldown!')
        elif self.level >= 1 and self.level == 4:
            if action_key[pg.K_SPACE] and not self.boost_available:
                print('Boost is currently active!')

        # level 2: red laser ability -> shoot a laser that destroys balls for points and bounces off opponent
        if self.level >= 2 and self.level != 4:
            if action_key[pg.K_e] and self.laser_red_available:
                self.fire_laser_red()
                # here would be an opportune place to call play() on a pg.mixer.Sound object
                # however, it is within the active gameplay loop and causes pygame to crash/freeze
                # left here for reference
                # AUDIO['sfx_plr_shoot_red'].play()
            elif action_key[pg.K_e] and not self.laser_red_available:
                print('Red laser still in cooldown')

        # level 3: blue laser ability -> shoot a laser that slows down balls and opponent
        if self.level >= 3 and self.level != 4: # TEMPORARY: WIll be set back to self.level 2 in the end
            if action_key[pg.K_f] and self.laser_blue_available:
                self.fire_laser_blue()
            elif action_key[pg.K_f] and not self.laser_blue_available:
                print('Blue laser still in cooldown')

    def move(self, delta_time):
        # CCPT: formula taken from tutorial
        self.rect.y += self.direction_y * self.speed * delta_time
        # added boundaries for aesthetic and gameplay reasons
        if self.rect.top <= 10:
            self.rect.top = 10
        if self.rect.bottom >= DISPLAY_HEIGHT - 9:
            self.rect.bottom = DISPLAY_HEIGHT - 9

    def reset_color_change(self):
        # used to reset color after temporary color change from using speed boost ability
        self.default_color = True

    def change_color(self, color):
        # brief color flash "animation" to indicate collision; called by Ball object
        self.default_color = False
        # outer rectangle
        pg.draw.rect(
            surface = self.image, 
            color = color, 
            rect = pg.FRect(0, 0, SIZES['paddles_vertical'][0], SIZES['paddles_vertical'][1]),
            width = 4,
            border_radius = 4
            )
        # added subtle timer for color flash to be noticeable
        self.timer_color.activate()

    def change_stats(self):
        # changes player's attributes and unlocks new abilities with new level progress
        pg.draw.rect(
            surface = self.image,
            color = COLORS[f'player_lv{self.level}'],
            rect = pg.FRect(2, 2, SIZES['paddles_vertical'][0] - 5, SIZES['paddles_vertical'][1] - 5),
        )

        if self.level == 2 and self.laser_red_unlocked == False:
            self.laser_red_unlocked = True
            self.spawn_laser_red()

        if self.level == 3 and self.laser_blue_unlocked == False: # TEMPORARY: self.level will be set to 3
            self.laser_blue_unlocked = True
            self.spawn_laser_blue()

        if self.level < 4:
            self.speed = SPEEDS[f'player_lv{self.level}']

        # applies slow down effect from impact with blue laser from opponent
        if self.frozen:
            self.speed = SPEEDS['frozen']
            pg.draw.rect(
            surface = self.image,
            color = COLORS['frozen'],
            rect = pg.FRect(2, 2, SIZES['paddles_vertical'][0] - 5, SIZES['paddles_vertical'][1] - 5),
            )

    def boost_speed(self):
        # applies speed boost effect
        # player has been frozen by opponent, speed boost adds extra speed to slowed down speed
        self.level = 4
        self.boost_available = False
        self.speed += SPEEDS['player_boost']
        # after speed boost has been added, player is also freed from frozen effect
        self.melt()

    def reset_speed(self):
        # reset speed to speed value of current level after speed boost
        self.level = self.current_level
        self.speed = SPEEDS[f'player_lv{self.level}']
        print('Speed boost over!')

    def boost_set_available(self):
        self.boost_available = True

    def fire_laser_red(self):
        # shoots laser by calling shoot() on laser object
        # laser object is passed as argument to Player
        self.laser_red_available = False
        self.laser_red.shoot()
        self.timer_laser_red_cooldown.activate()

    def laser_red_set_available(self):
        # resets laser and spawns a new one
        self.laser_red_available = True
        self.spawn_laser_red()

    def spawn_laser_red(self):
        # instantiates a RedLaser object in front of player
        # it moves with player and serves as both in-game ammo-indicator and aiming device
        self.laser_red = RedLaser(
                groups = (all_sprites, laser_sprites), 
                paddles = collision_sprites, 
                balls = ball_sprites, 
                controller = self,
                pos = (self.rect.center + pg.Vector2(40,-15)),
                offset = pg.Vector2(40, -15),
                direction_x = 1,
                owner = 'player',
                )
    
    def fire_laser_blue(self):
        self.laser_blue_available = False
        self.laser_blue.shoot()
        print("Fire blue laser")
        self.timer_laser_blue_cooldown.activate()

    def laser_blue_set_available(self):
        self.laser_blue_available = True
        self.spawn_laser_blue()

    def spawn_laser_blue(self):
        self.laser_blue = BlueLaser(
            groups = all_sprites,
            paddles = collision_sprites,
            balls = ball_sprites,
            controller = self,
            pos = (self.rect.center + pg.Vector2(40, 15)),
            offset = pg.Vector2(40, 15),
            direction_x = 1,
        )

    def freeze(self):
        # changes variable to apply slow down effect in change_stats method
        self.frozen = True
        self.can_freeze = False
        self.timer_melt.activate()

    def melt(self):
        # resets slow down effect
        self.frozen = False
        self.can_freeze = True

    def level_up(self):
        self.current_level += 1
        self.level = self.current_level

    def update(self, delta_time):
        # calling all methods, tying some to level progression
        self.old_rect = self.rect.copy()
        self.timer_color.update()
        self.timer_melt.update()
        self.input()
        self.move(delta_time)
        if self.default_color:
            self.change_stats()
            self.change_color(COLORS[f'player_lv{self.level}'])
            if self.frozen:
                self.change_color(COLORS['frozen'])
        if self.level >= 1:
            self.timer_boost_active.update()
            self.timer_boost_cooldown.update()
        if self.level >= 2:
            self.timer_laser_red_cooldown.update()
        if self.level >= 3: # TEMPORARY: self.level will be set to 3 later
            self.timer_laser_blue_cooldown.update()
        
class Opponent(pg.sprite.Sprite):
    """A class for the opponent's paddle."""
    def __init__(self, groups, ball = None):
        super().__init__(groups)
        # other objects & values
        # takes instances of Ball as reference point for automatic movement
        self.ball = ball

        # opponent level
        self.current_level = 1
        self.level = self.current_level

        # sprite
        self.image = pg.surface.Surface(SIZES['paddles_vertical'], flags = pg.SRCALPHA)
        # outer rectangle
        pg.draw.rect(
            surface = self.image, 
            color = COLORS[f'opponent_lv{self.level}'], 
            rect = pg.FRect(0, 0, SIZES['paddles_vertical'][0], SIZES['paddles_vertical'][1]),
            width = 4,
            border_radius = 0)
        # inner rectangle
        pg.draw.rect(
            surface = self.image,
            color = COLORS[f'opponent_lv{self.level}'],
            rect = pg.FRect(2, 2, SIZES['paddles_vertical'][0] - 5, SIZES['paddles_vertical'][1] - 5),
        )
        self.rect = self.image.get_frect(center = (DISPLAY_WIDTH - 30, DISPLAY_HEIGHT/2))
        self.old_rect = self.rect.copy()

        # movement
        self.direction_y = 0
        self.speed = SPEEDS[f'opponent_lv{self.level}']
        self.acceleration = ACCELERATION[f'opponent_lv{self.level}']

        # abilities
        self.laser_red = None
        self.laser_red_unlocked = False
        self.laser_red_cooldown = 3000
        self.laser_red_available = True
        self.laser_red_decision = False

        self.laser_blue = None
        self.laser_blue_unlocked = False
        self.laser_blue_cooldown = 4000
        self.laser_blue_available = True
        self.laser_blue_decision = False

        # states
        self.can_freeze = True
        self.frozen = False
        
        # timers
        self.default_color = True
        self.timer_color = Timer(duration = DURATIONS['impact_flash'], func = self.reset_color_change)

        self.timer_laser_red_cooldown = Timer(duration = self.laser_red_cooldown, func = self.laser_red_set_available)
        self.timer_laser_blue_cooldown = Timer(duration = self.laser_blue_cooldown, func = self.laser_blue_set_available)

        self.timer_laser_red_shoot = RandomTimer(duration_min = 4000, duration_max = 6000, func = self.fire_laser_red, repeats = -1, autostart = True)
        self.timer_laser_blue_shoot = RandomTimer(duration_min = 4000, duration_max = 6000, func = self.fire_laser_blue, repeats = -1, autostart = True)

        self.timer_melt = Timer(duration = DURATIONS['frozen'], func = self.melt)

    def follow_ball_1(self):
        # CCPT: concept of opponent follwowing ball is taken from pong tutorial by Clear Code
        # CCPT Youtube Video on Pong (with timestamp): https://youtu.be/8OMghdHP-zs?si=QoNdA6LzbS2jYc29&t=22529
        # CCPT Code snippet on opponent movement: https://drive.google.com/file/d/1aTRrIBxsjeBiJJP2VhSrHddHOyx7rRLQ/view?usp=sharing

        # added inertia to opponent's movement and amended CCPT code snippet substantially
        # purpose 1: opponent feels less robotic and missing the balls feels more organic
        # purpose 2: opponent stutters when ball flies on a mostly horizontal line,
        # because this movement mechanic makes it go up and down to keep level with ball
        # having acceleration and inertia alleviates that unaesthetic side-effect
        if self.ball.rect.centery >= 0 and self.ball.rect.centery <= DISPLAY_HEIGHT:
            if self.ball.rect.centery < self.rect.centery:
                self.direction_y -= self.acceleration
                if self.direction_y < -1:
                    self.direction_y = -1
            if self.ball.rect.centery > self.rect.centery:
                self.direction_y += self.acceleration
                if self.direction_y > 1:
                    self.direction_y = 1
        else:
            if self.rect.centery < DISPLAY_HEIGHT / 2:
                self.direction_y += self.acceleration
                if self.direction_y > 1:
                    self.direction_y = 1
            if self.rect.centery > DISPLAY_HEIGHT / 2:
                self.direction_y -= self.acceleration
                if self.direction_y < -1:
                    self.direction_y = -1

    def collide_wall(self):
        # add some "padding" for paddle to stop at field line
        if self.rect.top <= 14:
            self.rect.top = 14
        if self.rect.bottom >= DISPLAY_HEIGHT - 12:
            self.rect.bottom = DISPLAY_HEIGHT - 12

    def move(self, delta_time):
        self.rect.y += self.direction_y * self.speed * delta_time

    def reset_color_change(self):
        self.default_color = True

    def change_color(self, color):
        self.default_color = False
        # outer rectangle
        pg.draw.rect(
            surface = self.image, 
            color = color, 
            rect = pg.FRect(0, 0, SIZES['paddles_vertical'][0], SIZES['paddles_vertical'][1]),
            width = 4,
            border_radius = 0
            )
        self.timer_color.activate()

    def change_stats(self):
        # inner rectangle
        pg.draw.rect(
            surface = self.image, 
            color = COLORS[f'opponent_lv{self.level}'],
            rect = pg.FRect(2, 2, SIZES['paddles_vertical'][0] - 5, SIZES['paddles_vertical'][1] - 5),
        )
        
        self.speed = SPEEDS[f'opponent_lv{self.level}']
        if self.frozen:
            self.speed = SPEEDS['frozen']
            # inner rectangle
            pg.draw.rect(
            surface = self.image, 
            color = COLORS['frozen'],
            rect = pg.FRect(2, 2, SIZES['paddles_vertical'][0] - 5, SIZES['paddles_vertical'][1] - 5),
            )

        self.acceleration = ACCELERATION[f'opponent_lv{self.level}']

    def change_abilities(self):
        if self.level == 2 and self.laser_red_unlocked == False:
            self.laser_red_unlocked = True
            self.spawn_laser_red()

        if self.level == 3 and self.laser_blue_unlocked == False:
            self.laser_blue_unlocked = True
            self.spawn_laser_blue()

    def fire_laser_red(self):
        # implemented a simple AI for opponent to shoot lasers at random after timed intervals
        self.laser_red_decision = False
        if self.laser_red_available:
            self.laser_red_decision = choice((True, False))
            if self.laser_red_decision:
                self.laser_red.shoot()
                print(f'{self.laser_red.owner} fires red laser')
            else:
                print('Opponent chooes not to fire red laser')
        self.laser_red_available = False
        self.timer_laser_red_cooldown.activate()

    def laser_red_set_available(self):
        self.laser_red_available = True
        if self.laser_red_decision:
            self.spawn_laser_red()

    def spawn_laser_red(self):
        self.laser_red = RedLaser(
                groups = all_sprites,
                paddles = collision_sprites,
                balls = ball_sprites,
                controller = self,
                pos = (self.rect.center + pg.Vector2(-40, -15)),
                offset = pg.Vector2(-40, -15),
                direction_x = -1,
                owner = 'opponent'
            )

    def fire_laser_blue(self):
        self.laser_blue_decision = False
        if self.laser_blue_available:
            self.laser_blue_decision = choice((True, False))
            if self.laser_blue_decision:
                self.laser_blue.shoot()
                print('Opponent fires blue laser')
            else:
                print('Opponent chose not fire blue laser')
        self.laser_blue_available = False
        self.timer_laser_blue_cooldown.activate()

    def laser_blue_set_available(self):
        self.laser_blue_available = True
        if self.laser_blue_decision:
            self.spawn_laser_blue()

    def spawn_laser_blue(self):
        self.laser_blue = BlueLaser(
            groups = all_sprites,
            paddles = collision_sprites,
            balls = ball_sprites,
            controller = self,
            pos = (self.rect.center + pg.Vector2(-40, 15)),
            offset = pg.Vector2(-40, 15),
            direction_x = -1
        )

    def freeze(self):
        self.frozen = True
        self.can_freeze = False
        self.timer_melt.activate()

    def melt(self):
        self.frozen = False
        self.can_freeze = True

    def level_up(self):
        self.current_level += 1
        self.level = self.current_level

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.timer_color.update()
        self.timer_melt.update()
        self.collide_wall()
        self.change_abilities()
        if self.ball:
            self.follow_ball_1()
        self.move(delta_time)
        if self.default_color:
            self.change_stats()
            self.change_color(COLORS[f'opponent_lv{self.level}'])
            if self.frozen:
                self.change_color(COLORS['frozen'])
        if self.level >= 2:
            self.timer_laser_red_cooldown.update()
            self.timer_laser_red_shoot.update()
        if self.level >= 3:
            self.timer_laser_blue_cooldown.update()
            self.timer_laser_blue_shoot.update()

class Ball(pg.sprite.Sprite):
    """
    A class for the first ball. Flies horizontally. Leaves display to left and right. 
    Bounces off top and bottom of display/walls.
    """
    def __init__(self, groups, paddles):
        super().__init__(groups)
        # other objects & value
        # takes both player's and opponent's paddles as reference for collisions and method calls
        self.paddles = paddles

        # level
        self.current_level = 1
        self.level = self.current_level

        # sprite
        self.image = pg.surface.Surface(SIZES['ball'], flags = pg.SRCALPHA)
        pg.draw.circle(
            surface = self.image, 
            color = COLORS[f'ball_lv{self.level}'], 
            center = (SIZES['ball'][0]/2, SIZES['ball'][1]/2),
            radius = SIZES['ball'][0]/2 - 1)
        self.rect = self.image.get_frect(center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
        self.old_rect = self.rect.copy()

        # movement
        self.active = False
        self.direction = pg.Vector2(choice((-1, 1)), uniform(0.6, 0.8) * choice((-1, 1)))
        self.speed = SPEEDS[f'ball_lv{self.level}']
        self.speed_boost = 2
        self.extra_speed = 0

        # states
        self.can_freeze = True
        self.frozen = False

        # timers
        self.timer_ball_movement = Timer(duration = DURATIONS['ball_1_move_delay'], func = self.set_active, repeats = 0, autostart = True)

        self.timer_melt = Timer(duration = DURATIONS['frozen'], func = self.melt)

    def set_active(self):
        self.active = True

    def bounce_off(self):
        # collisions with top and bottom walls
        # increases speed after each bounce
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y *= -1
            self.extra_speed += self.speed_boost
        if self.rect.bottom > DISPLAY_HEIGHT:
            self.rect.bottom = DISPLAY_HEIGHT
            self.direction.y *= -1
            self.extra_speed += self.speed_boost

        # collisions with player and opponent
        # CCPT: checks both current rectangle and rectangle one frame before
        # to allow for more precise collision detection between moving objects
        # it still has its flaw, but works most of the times
        # CCPT Youtube Video on Pong (with timestamp): https://youtu.be/8OMghdHP-zs?si=QoNdA6LzbS2jYc29&t=22529
        # CCPT Code snippet on using two rectangles: https://drive.google.com/file/d/19jfSFAF8C9ltHbcMg6lBIuvsECNoVjrH/view?usp=sharing
        for paddle in self.paddles:
            if isinstance(paddle, (Player, Opponent)):
                if self.rect.colliderect(paddle.rect):
                    self.extra_speed += self.speed_boost
                    if self.rect.left < paddle.rect.right and self.old_rect.left > paddle.old_rect.right:
                        self.direction.x *= -1
                        # trigger the color flash for the impact indication on the paddles
                        paddle.change_color(COLORS['impact'])
                    if self.rect.right > paddle.rect.left and self.old_rect.right < paddle.old_rect.left:
                        self.direction.x *= -1
                        paddle.change_color(COLORS['impact'])
            if isinstance(paddle, (HPlayer, HOpponent)):
                if self.rect.colliderect(paddle.rect):
                    if self.rect.top < paddle.rect.bottom and self.old_rect.top > paddle.old_rect.bottom:
                        self.direction.y *= -1
                        paddle.change_color(COLORS['impact'])
                    if self.rect.bottom > paddle.rect.top and self.old_rect.bottom < paddle.old_rect.top:
                        self.direction.y *= -1
                        paddle.change_color(COLORS['impact'])
        
        # CCPT: ensures consistent movement speed in diagonal direction
        if self.direction:
            self.direction = self.direction.normalize()

    def move(self, delta_time):
        self.rect.y += self.direction.y * self.speed * delta_time
        self.rect.x += self.direction.x * self.speed * delta_time
        self.bounce_off()

    def change_stats(self):
        # level progression similar to paddles
        pg.draw.circle(
            surface = self.image, 
            color = COLORS[f'ball_lv{self.level}'], 
            center = (SIZES['ball'][0]/2, SIZES['ball'][1]/2),
            radius = SIZES['ball'][0]/2 - 1
            )
        
        self.speed = SPEEDS[f'ball_lv{self.level}'] + self.extra_speed
        if self.frozen:
            self.speed = SPEEDS['frozen']
            pg.draw.circle(
            surface = self.image, 
            color = COLORS['frozen'], 
            center = (SIZES['ball'][0]/2, SIZES['ball'][1]/2),
            radius = SIZES['ball'][0]/2 - 1
            )

    def freeze(self):
        self.frozen = True
        self.can_freeze = False
        self.timer_melt.activate()

    def melt(self):
        self.frozen = False
        self.can_freeze = True

    def level_up(self):
        self.current_level += 1
        self.level = self.current_level

    def update(self, delta_time):
        self.timer_ball_movement.update()
        self.timer_melt.update()
        self.old_rect = self.rect.copy()
        self.change_stats()
        if self.active:
            self.move(delta_time)

class HPlayer(pg.sprite.Sprite):
    """
    A class for the second player-controllable paddle that spawns on the bottom of the screen
    after total score has reached a threshold. This paddle moves horizontally and has attributes
    of the first player paddle on level 3.
    """
    def __init__(self, groups):
        super().__init__(groups)
        self.active = False

        # sprite
        self.image = pg.surface.Surface(SIZES['paddles_horizontal'], flags = pg.SRCALPHA)
        # outer rectangle
        pg.draw.rect(
            surface = self.image,
            color = COLORS['player_lv3'],
            rect = pg.FRect(0, 0, SIZES['paddles_horizontal'][0], SIZES['paddles_horizontal'][1]),
            width = 4,
            border_radius = 4
        )
        # inner rectangle
        pg.draw.rect(
            surface = self.image,
            color = COLORS['player_lv3'],
            rect = pg.FRect(2, 2, SIZES['paddles_horizontal'][0] - 5, SIZES['paddles_horizontal'][1] - 5),
            width = 0,
            border_radius = 4,
            )
        self.rect = self.image.get_frect(center = (-50, DISPLAY_HEIGHT - 30))
        self.old_rect = self.rect.copy()

        # movement
        self.direction_x = 0
        self.speed = SPEEDS['player_lv3']
        self.acceleration = ACCELERATION['player']

        # timers
        self.default_color = True
        self.timer_color = Timer(duration = DURATIONS['impact_flash'], func = self.reset_color_change)

    def move_into_field(self):
        self.active = True
        self.rect.centerx = DISPLAY_WIDTH/2

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction_x -= self.acceleration
            if self.direction_x < -1:
                self.direction_x = -1
        elif keys[pg.K_RIGHT]:
            self.direction_x += self.acceleration
            if self.direction_x > 1:
                self.direction_x = 1
        else:
            self.direction_x = 0

    def move(self, delta_time):
        self.rect.x += self.direction_x * self.speed * delta_time
        if self.rect.left < 15 + SIZES['paddles_vertical'][0]:
            self.rect.left = 15 + SIZES['paddles_vertical'][0]
        if self.rect.right > DISPLAY_WIDTH - 15 - SIZES['paddles_vertical'][0]:
            self.rect.right = DISPLAY_WIDTH - 15 - SIZES['paddles_vertical'][0]

    def reset_color_change(self):
        self.default_color = True

    def change_color(self, color):
        self.default_color = False
        pg.draw.rect(
            surface = self.image,
            color = color,
            rect = pg.FRect(0, 0, SIZES['paddles_horizontal'][0], SIZES['paddles_horizontal'][1]),
            width = 4,
            border_radius = 4
        )
        self.timer_color.activate()
    
    def update(self, delta_time):
        if self.active:
            self.timer_color.update()
            self.input()
            self.move(delta_time)
            if self.default_color:
                self.change_color(COLORS['player_lv3'])

class HOpponent(pg.sprite.Sprite):
    """
    Like HPlayer just for the opponent. Spawns on top of display, moves horizontally, and follows
    the second ball which always moves towards either bottom or top of display.
    """
    def __init__(self, groups, ball = None):
        super().__init__(groups)
        self.active = False
        self.ball = ball

        # sprite
        self.image = pg.surface.Surface(SIZES['paddles_horizontal'], flags = pg.SRCALPHA)
        # outer rectangle
        pg.draw.rect(
            surface = self.image,
            color = COLORS['opponent_lv3'],
            rect = pg.FRect(0, 0, SIZES['paddles_horizontal'][0], SIZES['paddles_horizontal'][1]),
            width = 4
        )
        # inner rectangle
        pg.draw.rect(
            surface = self.image,
            color = COLORS['opponent_lv3'],
            rect = pg.FRect(2, 2, SIZES['paddles_horizontal'][0] - 5, SIZES['paddles_horizontal'][1] - 5)
        )
        self.rect = self.image.get_frect(center = (-50, 30))
        self.old_rect = self.rect.copy()

        # movement
        self.direction_x = 0
        self.speed = SPEEDS['opponent_lv3']
        self.acceleration = ACCELERATION['opponent_lv2']

        # timers
        self.default_color = True
        self.timer_color = Timer(duration = DURATIONS['impact_flash'], func = self.reset_color_change)

    def move_into_field(self):
        self.rect.centerx = DISPLAY_WIDTH/2
        self.active = True

    def follow_ball_2(self):
        # follows the second ball instead of the first, but can also collide with first ball
        # collision is handled in the respective Ball objects
        if self.ball.rect.centerx >= 0 and self.ball.rect.centerx <= DISPLAY_WIDTH:
            if self.ball.rect.centerx < self.rect.centerx:
                self.direction_x -= self.acceleration
                if self.direction_x < -1:
                    self.direction_x = -1
            if self.ball.rect.centerx > self.rect.centerx:
                self.direction_x += self.acceleration
                if self.direction_x > 1:
                    self.direction_x = 1
        else:
            if self.rect.centerx < DISPLAY_WIDTH / 2:
                self.direction_x += self.acceleration
                if self.direction_x > 1:
                    self.direction_x = 1
            if self.rect.centerx > DISPLAY_WIDTH / 2:
                self.direction_x -= self.acceleration
                if self. direction_x < -1:
                    self.direction_x = -1

    def move(self, delta_time):
        self.rect.x += self.direction_x * self.speed * delta_time
        if self.rect.left < 15 + SIZES['paddles_vertical'][0]:
            self.rect.left = 15 + SIZES['paddles_vertical'][0]
        if self.rect.right > DISPLAY_WIDTH - 15 - SIZES['paddles_vertical'][0]:
            self.rect.right = DISPLAY_WIDTH - 15 - SIZES['paddles_vertical'][0]
    
    def change_color(self, color):
        self.default_color = False
        pg.draw.rect(
            surface = self.image,
            color = color,
            rect = pg.FRect(0, 0, SIZES['paddles_horizontal'][0], SIZES['paddles_horizontal'][1]),
            width = 4
        )
        self.timer_color.activate()

    def reset_color_change(self):
        self.default_color = True

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        if self.active:
            self.timer_color.update()
            self.follow_ball_2()
            self.move(delta_time)
            if self.default_color:
                self.change_color(COLORS['opponent_lv3'])

class VBall(pg.sprite.Sprite):
    """Like first ball, but moves towards top and bottom of display, and bounces off left and right."""
    def __init__(self, groups, paddles):
        super().__init__(groups)
        # other objects & values
        self.paddles = paddles

        # sprite
        self.image = pg.surface.Surface((SIZES['ball']), flags = pg.SRCALPHA)
        pg.draw.circle(
            surface = self.image,
            color = COLORS['vball'],
            center = (SIZES['ball'][0]/2, SIZES['ball'][1]/2),
            radius = SIZES['ball'][0]/2,
            width = 4
        )
        self.rect = self.image.get_frect(center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))
        self.old_rect = self.rect.copy()

        # movement
        self.active = False
        self.direction = pg.Vector2(uniform(0.6, 0.8) * choice((-1, 1)), choice((-1, 1)))
        self.speed = SPEEDS['ball_lv1']
        self.speed_boost = 2
        self.extra_speed = 0

        # states
        self.can_freeze = True
        self.frozen = False

        # timers
        self.timer_active = False
        self.timer_ball_movement = Timer(duration = DURATIONS['ball_2_move_delay'], func = self.set_active, repeats = 0, autostart = True)

        self.timer_melt = Timer(duration = DURATIONS['frozen'], func = self.melt)

    def set_active(self):
        self.active = True

    def bounce_off(self):
        # walls
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction.x *= -1
            self.extra_speed += self.speed_boost
        if self.rect.right > DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH
            self.direction.x *= -1
            self.extra_speed += self.speed_boost

        # paddles
        for paddle in self.paddles:
            if isinstance(paddle, (HPlayer, HOpponent)):
                if self.rect.colliderect(paddle.rect):
                    if self.rect.top < paddle.rect.bottom and self.old_rect.top > paddle.old_rect.bottom:
                        self.direction.y *= -1
                        paddle.change_color(COLORS['impact'])
                    if self.rect.bottom > paddle.rect.top and self.old_rect.bottom < paddle.old_rect.top:
                        self.direction.y *= -1
                        paddle.change_color(COLORS['impact'])
            if isinstance(paddle, (Player, Opponent)):
                if self.rect.colliderect(paddle.rect):
                    if self.rect.left < paddle.rect.right and self.old_rect.left > paddle.old_rect.right:
                        self.direction.x *= -1
                        paddle.change_color(COLORS['impact'])
                    if self.rect.right > paddle.rect.left and self.old_rect.right < paddle.old_rect.left:
                        self.direction.x *= -1
                        paddle.change_color(COLORS['impact'])

        if self.direction:
            self.direction = self.direction.normalize()
        else:
            self.direction

    def move(self, delta_time):
        self.rect.y += self.direction.y * self.speed * delta_time
        self.rect.x += self.direction.x * self.speed * delta_time
        self.bounce_off()

    def change_stats(self):
        self.speed = SPEEDS['ball_lv3'] + self.extra_speed
        if self.frozen:
            self.speed = SPEEDS['frozen']
            pg.draw.circle(
            surface = self.image,
            color = COLORS['frozen'],
            center = (SIZES['ball'][0]/2, SIZES['ball'][1]/2),
            radius = SIZES['ball'][0]/2,
            width = 4
            )

    def freeze(self):
        self.frozen = True
        self.can_freeze = False
        self.timer_melt.activate()

    def melt(self):
        self.frozen = False 
        self.can_freeze = True

    def update(self, delta_time):
        self.timer_melt.update()
        self.change_stats()
        if self.timer_active:
            self.timer_ball_movement.update()
        if self.active:
            self.old_rect = self.rect.copy()
            self.move(delta_time)

class RedLaser(pg.sprite.Sprite):
    """
    A class for the red laser. Designed to spawn first and follow its respective controlling paddle.
    Has attributes to be controlled by player and opponent.
    """
    def __init__(self, groups, paddles, balls, controller, pos, offset, direction_x, owner):
        super().__init__(groups)
        # other objects and values
        # references to other objects to update laser position and to call different methods on those objects
        self.paddles = paddles
        self.balls = balls
        self.controller = controller
        self.owner = owner

        # sprite
        self.image = pg.surface.Surface(SIZES['laser'])
        self.image.fill(COLORS['laser_red'])
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

        # movement
        self.direction_x = direction_x
        self.speed = SPEEDS['laser_red']
        self.speed_boost = 25
        self.extra_speed = 0
        self.offset = offset

        # state
        self.shot = False

    def update_position(self):
        self.rect.center = self.controller.rect.center + self.offset

    def shoot(self):
        # called by player and opponent
        self.shot = True
    
    def fly(self, delta_time):
        self.rect.x += self.direction_x * self.speed * delta_time

    def bounce_off(self):
        # bounces off paddles and triggers color flash 'animations'
        # increases its speed after each bounce
        for paddle in self.paddles:
            if self.rect.colliderect(paddle.rect):
                if self.rect.right > paddle.rect.left and self.old_rect.right < paddle.old_rect.left:
                    self.direction_x *= -1
                    self.extra_speed += self.speed_boost
                    self.speed += self.extra_speed
                    paddle.change_color(COLORS['impact'])
                if self.rect.left < paddle.rect.right and self.old_rect.left > paddle.old_rect.right:
                    self.direction_x *= -1
                    self.extra_speed += self.speed_boost
                    self.speed += self.extra_speed
                    paddle.change_color(COLORS['impact'])
        
    def self_destroy(self):
        # removes sprite object from group upon leaving display boundaries
        if self.rect.left > DISPLAY_WIDTH or self.rect.right < 0:
            self.kill()

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        # this condition enables the spawn and shooting functionality
        if self.shot == False:
            self.update_position()
        else:
            self.fly(delta_time)
            self.bounce_off()
            self.self_destroy()
        
class BlueLaser(pg.sprite.Sprite):
    """
    A class for the blue laser. 
    """
    def __init__(self, groups, paddles, balls, controller, pos, offset, direction_x):
        super().__init__(groups)
        # other objets and values
        self.paddles = paddles
        self.balls = balls
        self.controller = controller

        # sprite
        self.image = pg.surface.Surface(SIZES['laser'])
        self.image.fill('blue')
        self.rect = self.image.get_frect(center = pos)
        self.old_rect = self.rect.copy()

        # movement
        self.direction_x = direction_x
        self.speed = SPEEDS['laser_blue']
        self.offset = offset

        # state
        self.shot = False

    def update_position(self):
        self.rect.center = self.controller.rect.center + self.offset

    def shoot(self):
        self.shot = True

    def fly(self, delta_time):
        self.rect.x += self.direction_x * self.speed * delta_time

    def freeze_paddles(self):
        # enables frozen state in paddles upon collision
        for paddle in self.paddles:
            if isinstance(paddle, Player) or isinstance(paddle, Opponent):
                if self.rect.colliderect(paddle.rect):
                    self.kill()
                    paddle.change_color(COLORS['frozen'])
                    paddle.freeze()

    def freeze_balls(self):
        # enables frozen state in balls upon collision
        for ball in self.balls:
            if self.rect.colliderect(ball.rect):
                self.kill()
                ball.freeze()

    def self_destroy(self):
        if self.rect.left > DISPLAY_WIDTH or self.rect.right < 0:
            self.kill()

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        if self.shot:
            self.fly(delta_time)
            self.self_destroy()
            self.freeze_paddles()
            self.freeze_balls()
        else:
            self.update_position()

class Explosion(pg.sprite.Sprite):
    """A class for the explosion animation of Ball objects."""
    def __init__(self, groups, pos):
        super().__init__(groups)
        # the position of collision between ball and laser
        self.pos = pos
        
        # individual explosion animation frames
        self.frame_1 = pg.surface.Surface((8, 8),    flags = pg.SRCALPHA)
        self.frame_2 = pg.surface.Surface((16, 16),  flags = pg.SRCALPHA)
        self.frame_3 = pg.surface.Surface((32, 32),  flags = pg.SRCALPHA)
        self.frame_4 = pg.surface.Surface((12, 12),  flags = pg.SRCALPHA)
        self.frame_5 = pg.surface.Surface((4, 4),    flags = pg.SRCALPHA)
        self.frame_b = pg.surface.Surface((32, 32))
        self.frame_b.fill(COLORS['bg_game'])

        # draw circles shapes onto self.frames
        self.draw_circles()

        self.anim_frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_b, self.frame_4, self.frame_b, self.frame_5]
        self.anim_index = 0
        self.anim_speed = 7

        # sprite
        self.image = self.anim_frames[self.anim_index]
        self.rect = self.image.get_frect(center = pos)

        self.exploded = True

    def draw_circles(self):
        # draw circles on individual explosion animation frames
        # this is separated into its own function so VExplosion 
        # that inherits from this Class can have its own custom function with custom colors
        pg.draw.circle(self.frame_1, 'white', (4, 4),    4,  0)
        pg.draw.circle(self.frame_2, 'white', (8, 8),    8,  0)
        pg.draw.circle(self.frame_3, 'white', (16, 16),  16, 0)
        pg.draw.circle(self.frame_4, 'white', (6, 6),    6,  0)
        pg.draw.circle(self.frame_5, 'white', (2, 2),    3,  1)

    def animate(self, delta_time):
        # CCPT: cycling through a list to animate is an idea from the CCPT
        # instead of importing image files, I opted for using pygame draw module
        self.anim_index += self.anim_speed * delta_time
        if self.anim_index >= len(self.anim_frames):
            self.anim_index = 0
            self.exploded = False
            self.kill()
        self.image = self.anim_frames[int(self.anim_index)]
        self.rect = self.image.get_frect(center = self.pos)

    def update(self, delta_time):
        if self.exploded:
            self.animate(delta_time)

class VExplosion(Explosion):
    """A class for the explosion animation of VBall objects. Inherits from Explosion class."""
    def __init__(self, groups, pos):
        super().__init__(groups, pos)

        self.draw_circles()

    def draw_circles(self):
        pg.draw.circle(self.frame_1, 'yellow', (4, 4),    4,  1)
        pg.draw.circle(self.frame_2, 'yellow', (8, 8),    8,  3)
        pg.draw.circle(self.frame_3, 'yellow', (16, 16),  16, )
        pg.draw.circle(self.frame_4, 'yellow', (6, 6),    6,  2)
        pg.draw.circle(self.frame_5, 'yellow', (2, 2),    3,  1) 

class Timer():
    """
    An all-purpose timer. It calls a function after a pre-defined duration.

    CCPT: In its core, this code was taken from the tutorial on how to make a 2D Platformer.

    Youtube Video (with timestamp): https://youtu.be/8OMghdHP-zs?si=VpvEKzZCpYpni_vk&t=26735
    Code excerpt from Clear Code: https://drive.google.com/file/d/1-mN2Ejui7N_hxBijIpb0DRMshLnu3JZq/view?usp=sharing

    I added additional functionality by implementing an option to make the timer loop indefinitely,
    which comes in handy for situations in which I didn't how often a timer should loop.
    """
    def __init__(self, duration:int = 0, func = None, repeats:int = 0, autostart:bool = False):
        """
        :param int duration: Duration in ms after which timer calls a function.
        :param int function: Function that is called by timer after end of duration.
        :param int repeats: Number of times the timer runs. 0 = no repeats, >0 = number of repears, -1 = infinite repeats.
        :param bool autostart: If True timer starts without activate() method 
        """
        self.duration = duration
        self.func = func
        self.repeats = repeats
        self.autostart = autostart

        self.start_time = 0

        if self.autostart:
            self.activate()

    def activate(self):
        # grabs the time at one specific point in time
        self.start_time = pg.time.get_ticks()

    def deactivate(self):
        # resets the timer
        self.start_time = 0
        if self.repeats > 0:
            self.repeats -= 1
            self.activate()
        elif self.repeats == -1:
            self.activate()

    def update(self):
        # needs to be called every frame so that pygame time is updated
        # a function, passed as an argument and stored in instance variable, is called
        if pg.time.get_ticks() - self.start_time > self.duration:
            if self.start_time > 0:
                self.func()
                self.deactivate()

class RandomTimer(Timer):
    """
    Inherits from Timer class. Works like Timer class, but duration is randomized 
    according to min/max value and after each timing cycle.
    """
    def __init__(self, duration_min:int, duration_max:int, func = None, repeats:int = 0, autostart:bool = False):
        super().__init__(duration = randint(duration_min, duration_max), func = func, repeats = repeats, autostart = autostart)
        self.duration_min = duration_min
        self.duration_max = duration_max

    def deactivate(self):
        self.start_time = 0
        self.duration = randint(self.duration_min, self.duration_max)
        if self.repeats > 0:
            self.repeats -= 1
            self.activate()
        elif self.repeats == -1:
            self.activate()

# sprite group objects
all_sprites = pg.sprite.Group()
collision_sprites = pg.sprite.Group()
ball_sprites = pg.sprite.Group()
laser_sprites = pg.sprite.Group()

# sprite objects
player_1 = Player(groups = (all_sprites, collision_sprites))
opponent_1 = Opponent(groups = (all_sprites, collision_sprites), ball = None)

player_2 = HPlayer(groups = (all_sprites, collision_sprites))
opponent_2 = HOpponent(groups = (all_sprites, collision_sprites), ball = None)

# functions
def ball_spawn():
    # instantiates a ball object from Ball
    # this function primarily serves the purpose satisfying CS50P specs
    # that required functions to be defined at same indentation level as main()
    ball_1 = Ball(groups = (all_sprites, ball_sprites), paddles = collision_sprites)
    opponent_1.ball = ball_1
    return ball_1

def vball_spawn():
    # same as ball_spawn for the second ball
    ball_2 = VBall(groups = (all_sprites, ball_sprites), paddles = collision_sprites)
    opponent_2.ball = ball_2
    return ball_2

def set_ball_1_spawn_state():
    # used to control ball spawn intervals
    global ball_1_can_spawn
    ball_1_can_spawn = True
    return True

def set_ball_2_spawn_state():
    global ball_2_can_spawn
    ball_2_can_spawn = True
    return True

def draw_field(ball_1, ball_2, total_score):
    """
    Draws demarcation lines on the edges of display. 
    
    If a ball flies through and counts as a point, the line will flash up briefly as a visual indication.
    If a ball bounces against the wall and doesn't count as a point, the line will not flash.

    After total_score reaches threshold, center line disappears and top/bottom lines appear, indicating that
    the game is now played in all directions simultaneously.
    """
    # local variables
    corner_offset = 10
    border_distance = 5
    line_width = 6

    line_left = pg.draw.line(display_surface, COLORS['field'], (border_distance, corner_offset),(border_distance, DISPLAY_HEIGHT-corner_offset), line_width)
    if line_left.colliderect(ball_1.rect):
        line_left = pg.draw.line(display_surface, COLORS['field_hit'], (border_distance, corner_offset), (border_distance, DISPLAY_HEIGHT-corner_offset), line_width)

    line_right = pg.draw.line(display_surface, COLORS['field'], (DISPLAY_WIDTH-border_distance, corner_offset), (DISPLAY_WIDTH-border_distance, DISPLAY_HEIGHT-corner_offset), line_width)
    if line_right.colliderect(ball_1.rect):
        line_right = pg.draw.line(display_surface, COLORS['field_hit'], (DISPLAY_WIDTH-border_distance, corner_offset), (DISPLAY_WIDTH-border_distance, DISPLAY_HEIGHT-corner_offset), line_width)

    # Add second playing field (total score: 9)
    if total_score > 9:
        line_top = pg.draw.line(display_surface, COLORS['field'], (corner_offset, border_distance), (DISPLAY_WIDTH-corner_offset, border_distance), line_width)
        if line_top.colliderect(ball_2.rect):
            line_top = pg.draw.line(display_surface, COLORS['field_hit'], (corner_offset, border_distance), (DISPLAY_WIDTH-corner_offset, border_distance), line_width)

        line_bottom = pg.draw.line(display_surface, COLORS['field'], (corner_offset, DISPLAY_HEIGHT-border_distance), (DISPLAY_WIDTH-corner_offset, DISPLAY_HEIGHT-border_distance), line_width)
        if line_bottom.colliderect(ball_2.rect):
            line_bottom = pg.draw.line(display_surface, COLORS['field_hit'], (corner_offset, DISPLAY_HEIGHT-border_distance), (DISPLAY_WIDTH-corner_offset, DISPLAY_HEIGHT-border_distance), line_width)
    
    # Center line for first playing field (until total score: 9)
    if total_score < 9:
        line_center = pg.draw.line(display_surface, COLORS['field'], (DISPLAY_WIDTH/2, corner_offset), (DISPLAY_WIDTH/2, DISPLAY_HEIGHT-corner_offset), line_width)    
    
    circle_center = pg.draw.aacircle(display_surface, COLORS['field'], (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2), DISPLAY_WIDTH/6, line_width)

def display_score(score_player, score_opponent):
    # local variables (created for better readability of this code section)
    center_distance = 75
    line_vdistance = 10
    line_length = 50

    # current player score
    score_player_surf = font_score.render(str(score_player), True, COLORS['score_player'])
    score_player_rect = score_player_surf.get_frect(midbottom = (DISPLAY_WIDTH/2 - center_distance, DISPLAY_HEIGHT/2))
    display_surface.blit(score_player_surf, score_player_rect)

    # fraction line separating current player score from maximum player score
    pg.draw.line(
        surface = display_surface,
        color = COLORS['score_player'], 
        start_pos = (DISPLAY_WIDTH/2 - center_distance - line_length/2, DISPLAY_HEIGHT/2), 
        end_pos = (DISPLAY_WIDTH/2 - line_length, DISPLAY_HEIGHT/2),
        width = 3
    )

    # maximum player score
    score_max_player_surf = font_score.render('30', True, COLORS['score_player'])
    score_max_player_rect = score_max_player_surf.get_frect(midtop = (DISPLAY_WIDTH/2 - center_distance, DISPLAY_HEIGHT/2 + line_vdistance))
    display_surface.blit(score_max_player_surf, score_max_player_rect)

    # current opponent score
    score_opponent_surf = font_score.render(str(score_opponent), True, COLORS['score_opponent'])
    score_opponent_rect = score_opponent_surf.get_frect(midbottom = (DISPLAY_WIDTH/2 + center_distance, DISPLAY_HEIGHT/2))
    display_surface.blit(score_opponent_surf, score_opponent_rect)

    # fraction line separating current opponent score form maximum opponent score
    pg.draw.line(
        surface = display_surface,
        color = COLORS['score_opponent'], 
        start_pos = (DISPLAY_WIDTH/2 + center_distance + line_length/2, DISPLAY_HEIGHT/2), 
        end_pos = (DISPLAY_WIDTH/2 + line_length, DISPLAY_HEIGHT/2),
        width = 3
    )
    
    # maximum opponent score
    score_max_opponent_surf = font_score.render('30', True, COLORS['score_opponent'])
    score_max_opponent_rect = score_max_opponent_surf.get_frect(midtop = (DISPLAY_WIDTH/2 + center_distance, DISPLAY_HEIGHT/2 + line_vdistance))
    display_surface.blit(score_max_opponent_surf, score_max_opponent_rect)

def display_screen_start():
    # displays all elements of start screen
    # separated function into several helper_functions to improve code readability
    distance_to_subtitle = 150
    draw_titles_start()
    draw_movement_controls(distance_to_subtitle)
    draw_abilities_controls(distance_to_subtitle)
    draw_ui_controls(distance_to_subtitle)
    draw_lines()

def draw_titles_start():
    # draws title
    title_surf = font_title.render('PONG', True, COLORS['title'])
    title_rect = title_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/5))
    display_surface.blit(title_surf, title_rect)

    # draws subtitle
    subtitle_surf = font_subtitle.render('CHAOS EDITION', True, COLORS['subtitle'])
    subtitle_rect = subtitle_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/4 + 50))
    display_surface.blit(subtitle_surf, subtitle_rect)

def draw_movement_controls(distance_to_subtitle):
    # draw header for 'movement' category
    ui_movement_surf = font_ui.render('MOVEMENT', True, COLORS['ui_text'])
    ui_movement_rect = ui_movement_surf.get_frect(center = (DISPLAY_WIDTH/6, DISPLAY_HEIGHT/3 + distance_to_subtitle))
    display_surface.blit(ui_movement_surf, ui_movement_rect)
    draw_ui_frame(ui_movement_rect.x, ui_movement_rect.y, ui_movement_rect.width, ui_movement_rect.height)

    # keys
    offset_mov = 50

    # w = up
    ui_w_surf = font_ui.render('w', True, COLORS['ui_text'])
    ui_w_rect = ui_w_surf.get_frect(center = (ui_movement_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_w_surf, ui_w_rect)

    ui_equal_w_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_w_rect = ui_equal_w_surf.get_frect(center = (ui_movement_rect.centerx - 15, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_equal_w_surf, ui_equal_w_rect)

    ui_up_surf = font_ui.render('up', True, COLORS['ui_text'])
    ui_up_rect = ui_up_surf.get_frect(midleft = (ui_movement_rect.centerx + 20, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_up_surf, ui_up_rect)

    # s = down
    ui_s_surf = font_ui.render('s', True, COLORS['ui_text'])
    ui_s_rect = ui_s_surf.get_frect(center = (ui_movement_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_s_surf, ui_s_rect)

    ui_equal_s_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_s_rect = ui_equal_s_surf.get_frect(center = (ui_movement_rect.centerx - 15, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_equal_s_surf, ui_equal_s_rect)

    ui_down_surf = font_ui.render('down', True, COLORS['ui_text'])
    ui_down_rect = ui_equal_s_surf.get_frect(midleft = (ui_movement_rect.centerx + 20, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_down_surf, ui_down_rect)

    # left arrow = left
    pg.draw.polygon(
        display_surface, 
        COLORS['ui_text'], 
        [(ui_movement_rect.centerx - 57, DISPLAY_HEIGHT/2 + 200 - 5),
        (ui_movement_rect.centerx - 57 + 10, DISPLAY_HEIGHT/2 + 200 - 10),
        (ui_movement_rect.centerx - 57 + 10, DISPLAY_HEIGHT/2 + 200)]
        )
    
    ui_equal_arrowleft_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_arrowleft_rect = ui_equal_arrowleft_surf.get_frect(center = (ui_movement_rect.centerx - 15, DISPLAY_HEIGHT/2 + 200 - 5))
    display_surface.blit(ui_equal_arrowleft_surf, ui_equal_arrowleft_rect)

    ui_left_surf = font_ui.render('left', True, COLORS['ui_text'])
    ui_left_rect = ui_equal_s_surf.get_frect(midleft = (ui_movement_rect.centerx + 20, DISPLAY_HEIGHT/2 + 200 - 5))
    display_surface.blit(ui_left_surf, ui_left_rect)
    
    # right arrow = right
    pg.draw.polygon(
        display_surface, 
        COLORS['ui_text'], 
        [(ui_movement_rect.centerx - 57, DISPLAY_HEIGHT/2 + 240),
        (ui_movement_rect.centerx - 57, DISPLAY_HEIGHT/2 + 240 + 10),
        (ui_movement_rect.centerx - 57 + 10, DISPLAY_HEIGHT/2 + 240 + 5)]
        )
    
    ui_equal_arrowright_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_arrowright_rect = ui_equal_arrowright_surf.get_frect(center = (ui_movement_rect.centerx - 15, DISPLAY_HEIGHT/2 + 240 + 5))
    display_surface.blit(ui_equal_arrowright_surf, ui_equal_arrowright_rect)

    ui_right_surf = font_ui.render('right', True, COLORS['ui_text'])
    ui_right_rect = ui_equal_s_surf.get_frect(midleft = (ui_movement_rect.centerx + 20, DISPLAY_HEIGHT/2 + 240 + 5))
    display_surface.blit(ui_right_surf, ui_right_rect)
    
def draw_abilities_controls(distance_to_subtitle):
    # draw header for 'abilities' category
    ui_abilities_surf = font_ui.render('ABILITIES', True, COLORS['ui_text'])
    ui_abilities_rect = ui_abilities_surf.get_frect(center = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + distance_to_subtitle))
    display_surface.blit(ui_abilities_surf, ui_abilities_rect)
    draw_ui_frame(ui_abilities_rect.x, ui_abilities_rect.y, ui_abilities_rect.width, ui_abilities_rect.height)

    # keys
    offset_mov = 50

    # e = red laser
    ui_e_surf = font_ui.render('e', True, COLORS['ui_text'])
    ui_e_rect = ui_e_surf.get_frect(center = (ui_abilities_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_e_surf, ui_e_rect)

    ui_equal_e_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_e_rect = ui_equal_e_surf.get_frect(center = (ui_abilities_rect.centerx - 15, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_equal_e_surf, ui_equal_e_rect)

    ui_red_surf = font_ui.render('red laser', True, COLORS['ui_text'])
    ui_red_rect = ui_red_surf.get_frect(midleft = (ui_abilities_rect.centerx + 20, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_red_surf, ui_red_rect)

    # f = blue laser
    ui_f_surf = font_ui.render('f', True, COLORS['ui_text'])
    ui_f_rect = ui_f_surf.get_frect(center = (ui_abilities_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_f_surf, ui_f_rect)

    ui_equal_f_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_f_rect = ui_equal_f_surf.get_frect(center = (ui_abilities_rect.centerx - 15, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_equal_f_surf, ui_equal_f_rect)

    ui_blue_laser_surf = font_ui.render('blue laser', True, COLORS['ui_text'])
    ui_blue_laser_rect = ui_equal_f_surf.get_frect(midleft = (ui_abilities_rect.centerx + 20, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_blue_laser_surf, ui_blue_laser_rect)

    # space = boost
    ui_space_surf = font_ui.render('space', True, COLORS['ui_text'])
    ui_space_rect = ui_space_surf.get_frect(midright = (ui_abilities_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 200 - 5))
    display_surface.blit(ui_space_surf, ui_space_rect)

    ui_equal_space_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_space_rect = ui_equal_space_surf.get_frect(center = (ui_abilities_rect.centerx - 15, DISPLAY_HEIGHT/2 + 200 - 5))
    display_surface.blit(ui_equal_space_surf, ui_equal_space_rect)

    ui_left_surf = font_ui.render('boost', True, COLORS['ui_text'])
    ui_left_rect = ui_equal_space_surf.get_frect(midleft = (ui_abilities_rect.centerx + 20, DISPLAY_HEIGHT/2 + 200 - 5))
    display_surface.blit(ui_left_surf, ui_left_rect)

def draw_ui_controls(distance_to_subtitle):
    # draw header for 'UI' category
    ui_ui_surf = font_ui.render('UI', True, COLORS['ui_text'])
    ui_ui_rect = ui_ui_surf.get_frect(center = (DISPLAY_WIDTH - DISPLAY_WIDTH/6, DISPLAY_HEIGHT/3 + distance_to_subtitle))
    display_surface.blit(ui_ui_surf, ui_ui_rect)
    draw_ui_frame(ui_ui_rect.x, ui_ui_rect.y, ui_ui_rect.width, ui_ui_rect.height) 

    # keys
    offset_mov = 40

    # esc = pause
    ui_escape_surf = font_ui.render('esc', True, COLORS['ui_text'])
    ui_escape_rect = ui_escape_surf.get_frect(midright = (ui_ui_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_escape_surf, ui_escape_rect)

    ui_equal_escape_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_escape_rect = ui_equal_escape_surf.get_frect(center = (ui_ui_rect.centerx - 15, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_equal_escape_surf, ui_equal_escape_rect)

    ui_pause_surf = font_ui.render('pause', True, COLORS['ui_text'])
    ui_pause_rect = ui_pause_surf.get_frect(midleft = (ui_ui_rect.centerx + 20, DISPLAY_HEIGHT/2 + 100))
    display_surface.blit(ui_pause_surf, ui_pause_rect)

    # return = start / resume
    ui_enter_surf = font_ui.render('enter', True, COLORS['ui_text'])
    ui_enter_rect = ui_enter_surf.get_frect(midright = (ui_ui_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_enter_surf, ui_enter_rect)

    ui_equal_enter_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_enter_rect = ui_equal_enter_surf.get_frect(center = (ui_ui_rect.centerx - 15, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_equal_enter_surf, ui_equal_enter_rect)

    ui_start_surf = font_ui.render('start /', True, COLORS['laser_red'])
    ui_start_rect = ui_start_surf.get_frect(midleft = (ui_ui_rect.centerx + 20, DISPLAY_HEIGHT/2 + 150))
    display_surface.blit(ui_start_surf, ui_start_rect)

    ui_resume_surf = font_ui.render('resume', True, COLORS['ui_text'])
    ui_resume_rect = ui_resume_surf.get_frect(midleft = (ui_ui_rect.centerx + 20, DISPLAY_HEIGHT/2 + 180))
    display_surface.blit(ui_resume_surf, ui_resume_rect)

    # 1 = volume down
    ui_one_surf = font_ui.render('1', True, COLORS['ui_text'])
    ui_one_rect = ui_one_surf.get_frect(midright = (ui_ui_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 240))
    display_surface.blit(ui_one_surf, ui_one_rect)

    ui_equal_one_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_one_rect = ui_equal_one_surf.get_frect(center = (ui_ui_rect.centerx - 15, DISPLAY_HEIGHT/2 + 240))
    display_surface.blit(ui_equal_one_surf, ui_equal_one_rect)

    ui_volumedown_surf = font_ui.render('vol. down', True, COLORS['ui_text'])
    ui_volumedown_rect = ui_volumedown_surf.get_frect(midleft = (ui_ui_rect.centerx + 20, DISPLAY_HEIGHT/2 + 240))
    display_surface.blit(ui_volumedown_surf, ui_volumedown_rect)

    # 2 = volume up
    ui_two_surf = font_ui.render('2', True, COLORS['ui_text'])
    ui_two_rect = ui_two_surf.get_frect(midright = (ui_ui_rect.centerx - offset_mov, DISPLAY_HEIGHT/2 + 290))
    display_surface.blit(ui_two_surf, ui_two_rect)

    ui_equal_two_surf = font_ui.render('=', True, COLORS['ui_text'])
    ui_equal_two_rect = ui_equal_two_surf.get_frect(center = (ui_ui_rect.centerx - 15, DISPLAY_HEIGHT/2 + 290))
    display_surface.blit(ui_equal_two_surf, ui_equal_two_rect)

    ui_volumeup_surf = font_ui.render('vol. up', True, COLORS['ui_text'])
    ui_volumeup_rect = ui_volumeup_surf.get_frect(midleft = (ui_ui_rect.centerx + 20, DISPLAY_HEIGHT/2 + 290))
    display_surface.blit(ui_volumeup_surf, ui_volumeup_rect)
    
def draw_lines():
    # draws 2 lines separating the categories in start screen
    pg.draw.line(
        surface = display_surface, 
        color = COLORS['ui_frame'], 
        start_pos = (DISPLAY_WIDTH/3, DISPLAY_HEIGHT/2 + 90), 
        end_pos = (DISPLAY_WIDTH/3, DISPLAY_HEIGHT - 100), 
        width = 3
        )
    pg.draw.line(
        surface = display_surface, 
        color = COLORS['ui_frame'], 
        start_pos = (DISPLAY_WIDTH - DISPLAY_WIDTH/3, DISPLAY_HEIGHT/2 + 90), 
        end_pos = (DISPLAY_WIDTH - DISPLAY_WIDTH/3, DISPLAY_HEIGHT - 100), 
        width = 3
        )

def draw_ui_frame(x, y, width, height):
    """A helper function to draw frames around text surfaces."""
    # condition added to include draw_ui_frame in test_project.py
    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(width, (int, float)) and isinstance(height, (int, float)):
        pg.draw.rect(
            surface = display_surface,
            color = COLORS['ui_frame'],
            rect = (x - 5, y - 5, width + 10, height + 5),
            width = 3,
            border_radius = 3
            )
    else:
        raise ValueError('x must be int or float')
    
def display_screen_pause():
    # overlays a pause screen over the gameplay screen
    title_surf = font_title.render('PAUSE', True, COLORS['title'])
    title_rect = title_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + 50))
    display_surface.blit(title_surf, title_rect)

    subtitle_surf = font_subtitle.render('Press ENTER to resume', True, COLORS['subtitle'])
    subtitle_rect = subtitle_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + 150))
    display_surface.blit(subtitle_surf, subtitle_rect)
 
def display_screen_end(score_player, score_opponent):
    # overlays an ending screen over the gameplay screen
    title_win_surf = font_title.render('You Won', True, COLORS['title'])
    title_win_rect = title_win_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + 50))
    
    subtitle_win_surf = font_subtitle.render('Congrats!', True, COLORS['subtitle'])
    subtitle_win_rect = subtitle_win_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + 150))

    title_lose_surf = font_title.render('You Lost', True, COLORS['title'])
    title_lose_rect = title_lose_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + 50))

    subtitle_lose_surf = font_subtitle.render('Good game though!', True, COLORS['subtitle'])
    subtitle_lose_rect = subtitle_lose_surf.get_frect(midtop = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT/3 + 150))

    # different on-screen message depending on final scores
    # final scores passed as arguments from within main()
    if score_player >= 30:
        display_surface.blit(title_win_surf, title_win_rect)
        display_surface.blit(subtitle_win_surf, subtitle_win_rect)
    elif score_opponent >= 30:
        display_surface.blit(title_lose_surf, title_lose_rect)
        display_surface.blit(subtitle_lose_surf, subtitle_lose_rect)

def music_player():
    """
    A function that starts music and loops a specific segment of that music.

    Technically, a music file (mus_full) is played. The last segment of mus_full is loopable
    and is split into a separate music file called mus_loop. This one is queued to play after
    mus_full has played in full once; thus creating the impression of a seamless loop.

    I wrote and edited the music myself.
    """
    pg.mixer.music.load(AUDIO['mus_full'])
    pg.mixer.music.set_volume(audio_volume)
    pg.mixer.music.play()
    pg.mixer.music.queue(AUDIO['mus_loop'], namehint='', loops = -1)

def main():
    # start and loop music
    music_player()

    # references to global variables
    global running
    global start_game
    global in_game
    global end_game
    global audio_volume

    global ball_1_can_spawn
    global ball_2_can_spawn

    # local variables
    score_player = 0
    score_opponent = 0
    total_score = 0

    # timers for delayed ball (re)spawns
    timer_ball_1_spawn = Timer(duration = 1250, func = set_ball_1_spawn_state)
    timer_ball_2_spawn = Timer(duration = 1500, func = set_ball_2_spawn_state)

    # create first ball instances
    if ball_1_can_spawn:
        ball_1 = ball_spawn()
        ball_1_can_spawn = False
    
    # second ball is spawned, but remains inactive until second pong game starts
    # however, being visible in the beginning, it creates illusion of being part of the playing field
    if ball_2_can_spawn:
        ball_2 = vball_spawn()
        ball_2_can_spawn = False

    # gameplay loop
    while running:
        # delta time
        delta_time = clock.tick(MAX_FRAMERATE) / 1000
        
        # pygame events
        for event in pg.event.get():
            # quit game via mouse-click on 'x' of the pygame window
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                # quit game via pressing 'ESC'
                if event.key == pg.K_ESCAPE:
                    running = False
                # start/resume game via pressing 'Enter'
                if event.key == pg.K_RETURN:
                    if in_game == False:
                        in_game = True
                    else:
                        in_game = False
                    # switches state so that every 'Enter' press after the first leads to pause screen
                    if start_game:
                        start_game = False
                # raises music volume
                if event.key == pg.K_1:
                    if audio_volume > 0 and audio_volume <= 1.0:
                        audio_volume -= 0.1
                        pg.mixer.music.set_volume(audio_volume)
                        if audio_volume < 0:
                            audio_volume = 0
                        if audio_volume > 1:
                            audio_volume = 1
                # lowers music volume
                if event.key == pg.K_2:
                    if audio_volume >= 0 and audio_volume < 1.0:
                        audio_volume += 0.1
                        pg.mixer.music.set_volume(audio_volume)
                        if audio_volume > 1:
                            audio_volume = 1
                        if audio_volume < 0:
                            audio_volume = 0

                # debug keys
                # switches to end screen from pause screen 
                # ending message won't be displayed if max_score has not been reached
                if event.key == pg.K_BACKSPACE:
                    if end_game:
                        end_game = False
                    else:
                        end_game = True
                # adds five points to player
                if event.key == pg.K_RSHIFT:
                    score_player += 5

        if in_game:
            # game logic updates
            all_sprites.update(delta_time)
            total_score = score_player + score_opponent

            # balls score logic
            if ball_1.rect.right <= 0:
                ball_1.kill()
                ball_1.rect.midbottom = pg.Vector2(DISPLAY_WIDTH / 2, - 50) # move killed ball out of field
                score_opponent += 1
                timer_ball_1_spawn.activate()
            if ball_1.rect.left >= DISPLAY_WIDTH:
                ball_1.kill()
                ball_1.rect.midbottom = pg.Vector2(DISPLAY_WIDTH / 2, - 50) # move killed ball out of field
                score_player += 1
                timer_ball_1_spawn.activate()

            if ball_2.rect.bottom <= 0:
                ball_2.kill()
                ball_2.rect.midleft = pg.Vector2(DISPLAY_WIDTH + 50, DISPLAY_HEIGHT / 2) # move killed ball out of field
                score_player += 1
                timer_ball_2_spawn.activate()
            if ball_2.rect.top >= DISPLAY_HEIGHT:
                ball_2.kill()
                ball_2.rect.midleft = pg.Vector2(DISPLAY_WIDTH + 50, DISPLAY_HEIGHT / 2) # move killed ball out of field
                score_opponent += 1
                timer_ball_2_spawn.activate()

            # red laser and balls score logic
            # hitting a ball with the red laser results in ball explosion and +1 point
            for laser in laser_sprites:
                if laser.shot:
                    if laser.rect.colliderect(ball_1.rect):
                        Explosion(all_sprites, ball_1.rect.center)
                        laser.kill()
                        ball_1.kill()
                        ball_1.rect.midbottom = pg.Vector2(DISPLAY_WIDTH / 2, - 50) # move killed ball out of field
                        timer_ball_1_spawn.activate()
                        if laser.owner == 'player':
                            score_player += 1
                        if laser.owner == 'opponent':
                            score_opponent += 1
                    if laser.rect.colliderect(ball_2.rect):
                        VExplosion(all_sprites, ball_2.rect.center)
                        laser.kill()
                        ball_2.kill()
                        ball_2.rect.midleft = pg.Vector2(DISPLAY_WIDTH + 50, DISPLAY_HEIGHT / 2)
                        timer_ball_2_spawn.activate()
                        if laser.owner == 'player':
                            score_player += 1
                        if laser.owner == 'opponent':
                            score_opponent += 1
                    
            # score progression system
            if total_score >= 3:
                if player_1.current_level == 1:
                    player_1.level_up()
                if opponent_1.current_level == 1:
                    opponent_1.level_up()
                if ball_1.current_level == 1:
                    ball_1.level_up()
            if total_score >= 6:
                if player_1.current_level == 2:
                    player_1.level_up()
                if opponent_1.current_level == 2:
                    opponent_1.level_up()
                if ball_1.current_level == 2:
                    ball_1.level_up()
            # add second game of Pong (score: 9)
            if total_score > 9 and ball_2.timer_active == False:
                ball_2.timer_active = True
            if total_score == 9 and player_2.rect.centerx == -50:
                player_2.move_into_field()
                opponent_2.move_into_field()

            # end of game
            if score_player >= 30 or score_opponent >= 30:
                in_game = False
                end_game = True
    
            # timer updates
            timer_ball_1_spawn.update()
            timer_ball_2_spawn.update()

            # ball (re)spawns
            if not ball_1 in all_sprites and ball_1_can_spawn:
                ball_1 = ball_spawn()
                ball_1_can_spawn = False
            if not ball_2 in all_sprites and ball_2_can_spawn:
                ball_2 = vball_spawn()
                ball_2_can_spawn = False

            # sprite and surface updates
            display_surface.fill(COLORS['bg_game'])
            display_score(score_player, score_opponent)
            draw_field(ball_1, ball_2, total_score)
            all_sprites.draw(display_surface)

            # audio
            pg.mixer.music.unpause()

        elif not in_game and start_game:
            # print('You are in the Start Screen')
            display_surface.fill(COLORS['bg_start'])
            display_screen_start()

        elif not in_game and not start_game and not end_game:
            # print('You are in the Pause Screen')
            display_surface.fill(COLORS['bg_pause'])
            display_screen_pause()
            pg.mixer.music.pause()

        elif not in_game and not start_game and end_game:
            # print('You are in the End Screen')
            display_surface.fill(COLORS['bg_end'])
            display_screen_end(score_player, score_opponent)
            pg.mixer.music.fadeout(5000)

        pg.display.update()

    pg.quit()

# run the code
if __name__ == '__main__':
    main()
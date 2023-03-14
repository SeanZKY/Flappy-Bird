import threading

import pygame
import time
import threading
import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
BIRD_ANIMATION_COUNT = 20
PASSIVE_ANIMATION = "passive_bird.png"
FALLING_ANIMATION = "falling_bird.png"
FLYING_ANIMATION = "flying_bird.png"
GAME_NAME = "Flappy_bird"
BIRD_X_START = 0
BIRD_Y_START = 100
WHITE = (255,255,255)
BACKGROUND = "background.png"
GAME_MUSIC = "game_music.mp3"
BIRD_WIDTH = 200
X_PIPE_START = 1000
PIPE_DISTANCE = 1000
UP_PIPE = "up_pipe.png"
DOWN_PIPE = "down_pipe.png"
MAX_PIPE_Y = 850
MIN_PIPE_Y = 300
BIRDS_SPEED = 20
BACKGROUND_YPOS = 0
MAX_AREA_SIZE = -450
BACKGROUND_SPEED = 30
MINIMUM_PIPE_DISTANCE = 1400
MAXIMUM_PIPE_DISTANCE = 1450
BIRD_JUMP_HEIGHT = 200
MINIMUMU_PIPE_RECYCLE = -100
SCORE_FILE = "score.txt"
EMPTY_STRING = ""
HIGH_SCORE = "HighScore: "
CURRENT_SCORE = "CurrentScore: "
SPACE = " "
PIPE_X_DISTANCE = 500
INCREAMENT = 1
LOWEST_SCORE = 0
SCORE_X = 100
SCORE_Y = 0
WRITE_FILE = "w"
READ_FILE = "r"
SCORE_SIZE = 30
FONT = 'Comic Sans MS'
MIN_INDEX = 0
MAX_INDEX = 3
AREA_START_X = 0
PIPE_WIDTH = 60
Y_POS_BALANCE = 62
Y_POS_BALANCE_UP = 300
BLACK = (0,0,0)
FRAMES_DIVIDE = 4






def main():
    game = Game()
    game.start_game()





class Game:
    def __init__(self):
        self.inside = False
        self.exit = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.player0 = player()
        self.area = background()
        self.pipe1 = pipe()
        self.pipe2 = pipe()
        self.pipe3 = pipe()
        self.clock = pygame.time.Clock()
        self.scores = score()


    def start_game(self):
        self.pipe2.xpos = self.pipe1.xpos + PIPE_X_DISTANCE
        self.pipe3.xpos = self.pipe2.xpos + PIPE_X_DISTANCE
        self.play_music()
        pygame.display.set_caption(GAME_NAME)
        self.area.draw(self.screen)
        pygame.display.flip()
        animation_thread = threading.Thread(target=self.animation)
        animation_thread.start()
        self.player_input()

    def animation(self):
        animation_list = [self.player0.falling_animation,self.player0.passive_animation,self.player0.flying_animation]
        index = MIN_INDEX
        while self.player0.alive and not self.exit:
            self.player0.movment()
            self.area.draw(self.screen)
            self.player0.draw_bird(animation_list[index],self.screen)
            self.pipe1.draw_pipe(self.screen)
            self.pipe2.draw_pipe(self.screen)
            self.pipe3.draw_pipe(self.screen)
            self.scores.display_score(self.screen)
            pygame.display.flip()
            self.check_limits()
            self.clock.tick(BIRD_ANIMATION_COUNT)
            index += INCREAMENT
            self.move_objects()
            if index == MAX_INDEX:
                index = MIN_INDEX
        pygame.mixer.music.stop()


    def check_limits(self):
        if self.pipe1.xpos <= MINIMUMU_PIPE_RECYCLE:
            self.pipe1 = pipe()
        if self.pipe2.xpos <= MINIMUMU_PIPE_RECYCLE:
            self.pipe2 = pipe()
        if self.pipe3.xpos <= MINIMUMU_PIPE_RECYCLE:
            self.pipe3 = pipe()
            self.pipe2.xpos = self.pipe1.xpos + PIPE_X_DISTANCE
            self.pipe3.xpos = self.pipe2.xpos + PIPE_X_DISTANCE
        if self.area.xpos <= MAX_AREA_SIZE:
            self.area.xpos = AREA_START_X
        self.check_pipe_limits(self.pipe1)
        self.check_pipe_limits(self.pipe2)
        self.check_pipe_limits(self.pipe3)

    def check_pipe_limits(self,pipe):

        if self.player0.xpos <= pipe.xpos + PIPE_WIDTH and self.player0.xpos >= pipe.xpos - PIPE_WIDTH:
            self.inside = True
            if self.player0.ypos >= pipe.ypos-Y_POS_BALANCE or self.player0.ypos <= pipe.ypos-Y_POS_BALANCE_UP:
                self.player0.alive = False
                self.scores.save_score()
        elif self.inside and self.player0.xpos > pipe.xpos + PIPE_WIDTH:
            self.scores.add_score()
            self.inside = False



    def move_objects(self):
        self.area.xpos -= BACKGROUND_SPEED
        self.pipe1.xpos -= BACKGROUND_SPEED
        self.pipe2.xpos -= BACKGROUND_SPEED
        self.pipe3.xpos -= BACKGROUND_SPEED



    def player_input(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    self.player0.alive = False
                    self.scores.save_score()
                    break
                elif event.type == pygame.KEYDOWN and self.player0.alive:
                    if event.key == pygame.K_SPACE:
                        for num in range(FRAMES_DIVIDE):
                            self.player0.ypos -= BIRD_JUMP_HEIGHT/FRAMES_DIVIDE
                            self.area.draw(self.screen)
                            self.pipe1.draw_pipe(self.screen)
                            self.pipe2.draw_pipe(self.screen)
                            self.pipe3.draw_pipe(self.screen)
                            self.player0.draw_bird(self.player0.flying_animation,self.screen)
                            self.scores.display_score(self.screen)
                            pygame.display.flip()


    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.play()






class background():
    def __init__(self):
        self.background_image = pygame.image.load(BACKGROUND)
        self.xpos = AREA_START_X


    def draw(self,screen):
        screen.blit(self.background_image, (self.xpos, BACKGROUND_YPOS))



class pipe():
    import random
    def __init__(self):
        self.xpos = self.random_x_pos()
        self.ypos = self.random_y_pos()
        self.down_pipe_png = pygame.image.load(DOWN_PIPE)
        self.up_pipe_png = pygame.image.load(UP_PIPE)
        self.down_pipe_png.set_colorkey(WHITE)
        self.up_pipe_png.set_colorkey(WHITE)

    def draw_pipe(self,screen):
        screen.blit(self.up_pipe_png, (self.xpos, self.ypos))
        screen.blit(self.down_pipe_png, (self.xpos, self.ypos-PIPE_DISTANCE))

    def random_x_pos(self):
        return  random.randint(MINIMUM_PIPE_DISTANCE, MAXIMUM_PIPE_DISTANCE)
    def random_y_pos(self):
        return random.randint(MIN_PIPE_Y, MAX_PIPE_Y)


class player():

    def __init__(self):
        self.alive = True
        self.xpos = BIRD_X_START
        self.ypos = BIRD_Y_START
        self.passive_animation = pygame.image.load(PASSIVE_ANIMATION)
        self.passive_animation.set_colorkey(WHITE)
        self.falling_animation = pygame.image.load(FALLING_ANIMATION)
        self.falling_animation.set_colorkey(WHITE)
        self.flying_animation = pygame.image.load(FLYING_ANIMATION)
        self.flying_animation.set_colorkey(WHITE)

    def movment(self):
        self.ypos += BIRDS_SPEED


    def draw_bird(self,animation,screen):
        screen.blit(animation, (self.xpos, self.ypos))

class score():
    def __init__(self):
        self.xpos = SCORE_X
        self.ypos = SCORE_Y
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT, SCORE_SIZE)
        self.max = self.highest_score()
        self.current = LOWEST_SCORE

    def highest_score(self):
        with open(SCORE_FILE,READ_FILE) as file:
            file = file.read()
            if file != EMPTY_STRING:
                return int(file)
            else:
                return LOWEST_SCORE

    def add_score(self):
        self.current += INCREAMENT
        if self.current > self.max:
            self.max = self.current

    def display_score(self,screen):
        textsurface = self.font.render(HIGH_SCORE + str(self.max) + SPACE + SPACE + CURRENT_SCORE + str(self.current), False, BLACK)
        screen.blit(textsurface, (self.xpos, self.ypos))

    def save_score(self):
        with open(SCORE_FILE,WRITE_FILE) as file:
            file.write(str(self.max))









if __name__ == '__main__':
    main()
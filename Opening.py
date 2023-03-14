import threading
import FlappyBird
import pygame
import FlappyOnline

WIDTH = 1400
HEIGHT = 1000
FONT = 'Comic Sans MS'
FONT_SIZE = 30
SINGLE_PLAY = "Single Player"
MULTI_PLAY = "Multi Player"
SINGLE_PLAY_X = 400
SINGLE_PLAY_Y = 100
MULTI_PLAY_Y = 150
MULTI_PLAY_X = 400
FPS = 30
IMAGE_POS = (0,0)
FRAMES_NUM = 27
IMAGES_NAME = "giphy-"
IMAGE_TYPE = ".png"
TEXT_START_X = 0
TEXT_START_Y = 0
BLACK = (0,0,0)
FIRST_INDEX = 0
SECOND_INDEX = 1
LEFT_CLICK = 1
TEXT_WIDTH = 170
TEXT_HEIGHT = 50
OPENING_MUSIC = "background_music.mp3"



def main():
    start = loading_screen()
    start.start_screen()

class loading_screen:
    def __init__(self):
        self.start = False
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.single_play = text_box()
        self.multiplay = text_box()
        self.single_play.xpos = SINGLE_PLAY_X
        self.multiplay.xpos = MULTI_PLAY_X
        self.single_play.ypos = SINGLE_PLAY_Y
        self.multiplay.ypos = MULTI_PLAY_Y
        self.offline = False
        self.online = False

    def start_screen(self):
        self.play_music()
        animation_thread = threading.Thread(target=self.animation)
        animation_thread.start()
        self.check_start()

    def check_start(self):
        quit = False
        while not self.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                    if self.single_play.compare_position(pygame.mouse.get_pos()[FIRST_INDEX],pygame.mouse.get_pos()[SECOND_INDEX]):
                        self.start = True
                        self.offline = True
                        break
                    elif self.multiplay.compare_position(pygame.mouse.get_pos()[FIRST_INDEX],pygame.mouse.get_pos()[SECOND_INDEX]):
                        self.start = True
                        self.online = True
        if self.offline:
            FlappyBird.main()
        elif self.online:
            pygame.quit()
            FlappyOnline.main()






    def animation(self):
        while not self.start:
            for num in range(FRAMES_NUM):
                if self.start:
                    break
                image = pygame.image.load(IMAGES_NAME + str(num) + IMAGE_TYPE)
                self.screen.blit(image,IMAGE_POS)
                self.single_play.display_box(SINGLE_PLAY, self.screen)
                self.multiplay.display_box(MULTI_PLAY, self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(OPENING_MUSIC)
        pygame.mixer.music.play()





class text_box():
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT, FONT_SIZE)
        self.xpos = TEXT_START_X
        self.ypos = TEXT_START_Y

    def display_box(self,sentence,screen):
        textsurface = self.font.render(sentence , False, BLACK)
        screen.blit(textsurface, (self.xpos, self.ypos))

    def compare_position(self,xpos,ypos):
        if self.xpos <= xpos and self.xpos+ TEXT_WIDTH >= xpos and self.ypos+TEXT_HEIGHT >= ypos and self.ypos <= ypos:
            return  True
        return False


if __name__ == '__main__':
    main()







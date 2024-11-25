import pygame as pg
from paths import *
from constants import *
import string

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

quote = 'Quality is not an act, it is a habit.'

class Text(pg.sprite.Sprite):

    containers = None

    def __init__(self, text, font, fontsize, color):
        super().__init__(self.containers)
        self.text = text
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()

class Quote(Text):

    containers = None

    def __init__(self, text, font, fontsize, color):
        super().__init__(text, font, fontsize, color)
        # User input used to color text.
        self.user = Text('', ASSET_DIR / 'fonts' /'pixel.ttf', 20, 'green')
        self.rect.center = SCREEN_RECT.center
        self.user.rect = self.rect
        self.wrongs = 0
        self.wronged = False

    def update(self):
        self.image = self.font.render(self.text, 1, self.color)
        
        if (not self.text.startswith(self.user.text) and
            not self.wronged):
            self.wronged = not self.wronged
            self.color = 'red'
            self.wrongs += 1
            print(f'Wrongs: {self.wrongs}')
            
        elif self.text.startswith(self.user.text):
            if self.wronged:
                self.wronged = not self.wronged
            self.color = 'black'
            self.user.image = self.font.render(self.user.text, 1, self.user.color)

    def type_out(self, events):
        for event in events:
            if event.type == pg.TEXTINPUT:
                if (event.text in string.ascii_letters
                    + string.digits
                    + string.punctuation
                    +  ' ' and
                    not self.wronged):
                    self.user.text = self.user.text + event.text
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.user.text = self.user.text[:-1]
        
all_sprites = pg.sprite.Group()
foo = pg.sprite.Group()

Text.containers = all_sprites
Quote.containers = all_sprites

text = Quote('Quality is not an act, it is a habit.', ASSET_DIR / 'fonts' / 'pixel.ttf', 13, 'black')



while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
    text.type_out(events)
    
    screen.fill('white')

    all_sprites.draw(screen)
    all_sprites.update()


    pg.display.flip()
    clock.tick(60)
pg.quit()
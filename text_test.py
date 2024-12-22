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

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(self.containers)
        self.text = text
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.bgcolor = bgcolor
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        self.rect = self.image.get_rect()

class Quote(Text):

    containers = None

    def __init__(self, text, font, fontsize, color, bgcolor=None):
        super().__init__(text, font, fontsize, color, bgcolor)
        # User input used to color text.
        self.user = Text('', ASSET_DIR / 'fonts' /'pixel.ttf', 20, 'green')
        self.rect.center = SCREEN_RECT.center
        self.rect = self.rect.move(0, -SCREEN_RECT.height // 3)
        self.user.rect = self.rect
        self.wrongs = 0
        self.wronged = False

    def update(self):
        self.image = self.font.render(self.text, 1, self.color, self.bgcolor)
        
        if self.user.text == self.text:
            self.user.kill()
            self.kill()
        if (not self.text.startswith(self.user.text) and
            not self.wronged):
            self.wronged = not self.wronged
            self.color = 'red'
            self.wrongs += 1
            
        elif self.text.startswith(self.user.text):
            if self.wronged:
                self.wronged = not self.wronged
            self.color = 'black'
            self.user.image = self.font.render(self.user.text, 1, self.user.color)

    # Needs pg.event.get() as events
    def type_out(self, events):
        for event in events:
            if event.type == pg.TEXTINPUT:
                if (event.text in string.ascii_letters
                    + string.digits
                    + string.punctuation
                    +  ' ' and
                    not self.wronged):
                    self.user.text = self.user.text + event.text
            elif (event.type == pg.KEYDOWN and
                  event.key == pg.K_BACKSPACE):
                    self.user.text = self.user.text[:-1]

class Bar(pg.sprite.Sprite):

    containers = None

    def __init__(self):
        super().__init__(self.containers)
        self.size = (50,20)
        self.image = pg.image.load('assets/images/shell.png')
        self.rect = self.image.get_rect()

class Foo(pg.sprite.Sprite):

    containers = None

    def __init__(self):
        super().__init__(self.containers)
        self.size = (100,200)
        self.image = pg.image.load('assets/images/pantry.png')
        self.rect = self.image.get_rect()
        self.thing = Bar()


all_sprites = pg.sprite.Group()
bar = pg.sprite.Group()

Text.containers = all_sprites
Quote.containers = all_sprites

Bar.containers = bar
Foo.containers = all_sprites



foo = Foo()

screen.fill('white')
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        foo.thing.rect.move_ip(0, -2)
    elif keys[pg.K_s]:
        foo.thing.rect.move_ip(0, 2)

    all_sprites.draw(screen)
    bar.draw(foo.image)
    all_sprites.update()
    bar.update()

    pg.display.flip()
    clock.tick(60)
pg.quit()
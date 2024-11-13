import pygame as pg
from paths import *
import string

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

quote = 'Quality is not an act, it is a habit'.lower()

class Text(pg.sprite.Sprite):
    def __init__(self, text, font, fontsize, color):
        super().__init__()
        self.text = text
        self.font = pg.font.Font(font, fontsize)
        self.color = color
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()

class Word(Text):
    def __init__(self, text, font, fontsize, color):
        super().__init__(text, font, fontsize, color)
        self.user = Text('', ASSET_DIR / 'fonts' /'pixel.ttf', 20, 'green')

    def update(self):
        self.rect = screen.get_rect().center
        self.user.rect = self.rect
        self.image = self.font.render(self.text, 1, self.color)
        
        
        if not self.text.startswith(self.user.text):
            self.color = 'red'
        else:
            self.color = 'black'
            self.user.image = self.font.render(self.user.text, 1, self.user.color)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if (event.unicode in string.ascii_lowercase) or (event.unicode in string.punctuation):
                self.user.text = self.user.text + event.unicode
            if event.key == pg.K_BACKSPACE:
                self.user.text = self.user.text[:-1]
          
class Quote(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        

text = Word('foo', ASSET_DIR / 'fonts' /'pixel.ttf', 20, 'black')

text_group = pg.sprite.Group(text, text.user)
print(text_group.sprites())

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        text.handle_event(event)
    
    screen.fill('white')

    text_group.draw(screen)
    text_group.update()

    if len(text_group.sprites()) > 0:
        if text_group.sprites()[0].text == text_group.sprites()[1].text:
            text_group.empty()

    pg.display.flip()
    clock.tick(60)
pg.quit()




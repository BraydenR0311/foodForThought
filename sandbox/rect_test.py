import pygame as pg

pg.init()

screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True

class Menu(pg.sprite.Sprite):

    containers = None

    def __init__(self):
        super().__init__(self.containers)
        self.image = pg.Surface((20,20))
        self.rect = pg.image.load
        
menugroup = pg.sprite.Group()

Menu.containers = menugroup

menu = Menu()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill('white')

    menugroup.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()
import pygame as pg
from paths import *
from constants import *

from src.gamestate import Gamestate
from src.services import load_image

from src.sprites import (
    Appliance,
    Floor,
    Player,
    Button,
    Popup,
    read_tilemap,
    # TEST
    Foo
)

# TODO: remove tests and dont use load_image function.

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
global_state = Gamestate.PLAYING # TODO: change to MAIN_MENU

background, _ = load_image(IMAGE_DIR / 'background.png')

# Create groups.
all_sprites = pg.sprite.Group()
appliances = pg.sprite.Group()
buttons = pg.sprite.Group()
kitchen = pg.sprite.Group()
popups = pg.sprite.Group()

# Assign sprite classes to certain groups.
Player.containers = all_sprites
Floor.containers = kitchen, all_sprites
Appliance.containers = appliances, kitchen, all_sprites
Button.containers = buttons
Popup.containers = popups, all_sprites
# TEST
Foo.containers = popups, all_sprites

# Initialize objects.
kitchen_rect = read_tilemap('map1')
player = Player()
play = Button('play')

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT or event.type == pg.K_q:
            running = False

    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()

    # Game starts in the main menu.
    if global_state == Gamestate.MAIN_MENU:
        mouse_pos = pg.mouse.get_pos()
        mouse = pg.mouse.get_pressed()
        click = mouse[0]

        # Apply background.
        SCREEN.blit(background)
        # Draw only those in the 'buttons' group.
        buttons.draw(SCREEN)

        # Button logic.
        # Not encapsulated, same as player movement logic.
        for button in buttons.sprites():
            # Mouse hovering over button.
            armed = button.rect.collidepoint(mouse_pos)
            # Nothing done to button.
            if not armed and not click:
                button.change_image('play')
                button.clicked = False
            # Mouse is hovering.
            if armed:
                button.change_image('play_armed')
            # Hovering and left click held.
            if armed and click:
                button.change_image('play_clicked')
                button.clicked = True  
            # Activate button.
            if armed and not click and button.clicked:
                button.clicked = False
                global_state = Gamestate.PLAYING



    elif global_state == Gamestate.PLAYING:

        # Draw objects
        SCREEN.blit(background)
        all_sprites.draw(SCREEN)
        all_sprites.update()

        # Move sprite, checking for collisions
        keys = pg.key.get_pressed()
        up = keys[pg.K_w]
        down = keys[pg.K_s]
        left = keys[pg.K_a]
        right = keys[pg.K_d]

        if up:
            player.dy = -player.speed
            player.animate(player.walk_up)
            player.rect.move_ip(0, player.dy)
        if down:
            player.dy = player.speed
            player.animate(player.walk_down)
            player.rect.move_ip(0, player.dy)
        hitlist = pg.sprite.spritecollide(player, appliances, False)
        for sprite in hitlist:
            if player.dy > 0:
                player.rect.bottom = sprite.rect.top
            elif player.dy < 0:
                player.rect.top = sprite.rect.bottom
        if left:
            player.dx = -player.speed
            player.animate(player.walk_left)
            player.rect.move_ip(player.dx, 0)
        if right:
            player.dx = player.speed
            player.animate(player.walk_right)
            player.rect.move_ip(player.dx, 0)
        hitlist = pg.sprite.spritecollide(player, appliances, False)
        for sprite in hitlist:
            if player.dx > 0:
                player.rect.right = sprite.rect.left 
            elif player.dx < 0:
                player.rect.left = sprite.rect.right

        # Keep chef in the kitchen.
        player.rect.clamp_ip(kitchen_rect)

        # Player next to pantry
        # TODO: must have a popup object assigned to an appliance
        # for appliance in appliances:
        #     if appliance.zone.colliderect(player):
        
        for appliance in appliances.sprites():
            print(appliance.popup.rect)
    pg.display.flip()
    clock.tick(60)

pg.quit()


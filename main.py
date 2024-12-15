# TODO: change syntax for button and interactions to foo.is_pressed(pg.K_foo)
# TODO: clock from 9-5, increment by 30 every 10 secs. Day ends at 5.
# TODO: money from tickets according to dish quality.

import pygame as pg
import random
from paths import *
from constants import *

from src.gamestate import Gamestate, global_state

from src.sprites import (
    Appliance,
    Floor,
    Player,
    Button,
    Popup,
    Food,
    Quote,
    Text,
    Ticket,
    Generic,
    Timer,
    read_tilemap,
)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

background = pg.image.load(IMAGE_DIR / 'background.png').convert()

# Create groups.
all_sprites = pg.sprite.Group()
players = pg.sprite.Group()
appliances = pg.sprite.Group()
buttons = pg.sprite.Group()
kitchen = pg.sprite.Group()
popups = pg.sprite.Group()
quotes = pg.sprite.Group()
cook_group = pg.sprite.GroupSingle()
texts = pg.sprite.Group()
foods = pg.sprite.Group()
tickets = pg.sprite.Group()
generics = pg.sprite.Group()
cook_timer = pg.sprite.Group()
# TEST
foos = pg.sprite.Group()

# Assign sprite classes to certain groups.
Player.containers = players, all_sprites
Floor.containers = kitchen, all_sprites
Appliance.containers = appliances, kitchen, all_sprites
Button.containers = buttons, all_sprites
Popup.containers = popups, all_sprites
Quote.containers = quotes, all_sprites
Text.containers = texts, all_sprites
Food.containers = foods, all_sprites
Ticket.containers = tickets, all_sprites
Generic.containers = generics, all_sprites
Timer.containers = cook_timer, all_sprites

# Initialize objects.
kitchen_rect = read_tilemap(ASSET_DIR / 'map.txt')
player = Player()
play = Button('play')


running = True
while running:
    

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    secs = pg.time.get_ticks() // 1000

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

        kitchen.draw(screen)
        players.draw(screen)
        popups.draw(screen)
        tickets.draw(screen)
        foods.draw(screen)
        generics.draw(screen)

        # Update all objects.
        all_sprites.update()

        # Direction controls and collision with appliances.
        keys = pg.key.get_pressed()

        # Directional Keybindings
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


         # Generate tickets
        # TODO: generate tickets dynamically
        if not tickets:
            foo = Ticket('burger')

        # Manage interaction between player and appliances.
        interaction = keys[pg.K_e]

        # Only interact with the closest appliance.
        closest = min(appliances.sprites(),
                      key=lambda x: player.center_vec.distance_to(x.center_vec))
        
        for appliance in appliances:
            if appliance is not closest:
                appliance.popup.kill()

        if closest.zone.colliderect(player):
            closest.popup.add(Popup.containers)
        else:
            closest.popup.kill()

        if interaction:
            for ticket in tickets:
                for ingredient in ticket.ingredients:
                    ingr_app = ingredient.APPLIANCE_DICT[ingredient.kind]
                    if (ingr_app == closest.kind):
                        cooked_ticket = ticket
                        cooked = ingredient
                        quote = ticket.quotes[0]
                        quote.add(cook_group)
                        global_state = Gamestate.TYPING

        pause = keys[pg.K_ESCAPE]        

    elif global_state == Gamestate.TYPING:
        SCREEN.blit(background)
        kitchen.draw(screen)
        players.draw(screen)
        tickets.draw(screen)
        foods.draw(screen)
        cook_group.draw(screen)
        texts.draw(screen)
        generics.draw(screen)
        cook_timer.draw(screen)
        # Put this before pg.display.flip()
        all_sprites.update()

        quote.type_out(events)
        if not cook_timer:
            timer = Timer(len(quote.text.split()),
                  ASSET_DIR / 'fonts' / 'pixel.ttf',
                  80,
                  'black') 
        print(int(timer.text))
        if int(timer.text) == 0 or quote.wrongs >= 3:
            quote.user.kill()
            cooked.check.image = pg.image.load(IMAGE_DIR / 'x.png').convert_alpha()
            cooked_ticket.ingredients.remove(cooked)
            cooked_ticket.cooked.append(cooked)
            cooked_ticket.quotes.remove(quote)
            cooked.check.add(Generic.containers)
            timer.kill()
            global_state = Gamestate.PLAYING





        if not cook_group:
            quote.user.kill()
            cooked_ticket.ingredients.remove(cooked)
            cooked_ticket.cooked.append(cooked)
            cooked_ticket.quotes.remove(quote)
            cooked.check.add(Generic.containers)
            timer.kill()
            global_state = Gamestate.PLAYING

    pg.display.flip()
    clock.tick(FPS)
    
pg.quit()
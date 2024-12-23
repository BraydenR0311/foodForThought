# TODO: change syntax for button and interactions to foo.is_pressed(pg.K_foo)
# TODO: clock from 9-5, increment by 30 every 10 secs. Day ends at 5.
# TODO: Update ticket locations as tickets are completed
# TODO: money from tickets according to dish quality.

import pygame as pg
import random
from paths import *
from src.config import Config
from utils.utils import read_tilemap, quoteread
from utils.gamemanager import GameManager, State

#TODO: Replace Status and Popup to Generic
from src.components.button import Button
from src.components.food import Food
from src.components.generic import Generic
from src.components.player import Player
from src.components.shiftclock import ShiftClock
from src.components.status import Status, Popup
from src.components.text import Text, Quote
from src.components.ticket import Ticket, TicketManager
from src.components.tiles import Floor, Appliance
from src.components.timer import Timer

pg.init()

# Initialize game manager object.
game_manager = GameManager()
game_manager.load_screen() 
screen = pg.display.set_mode((Config.WIDTH, Config.HEIGHT))
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
statuses = pg.sprite.Group()
cook_timer = pg.sprite.Group()
generics = pg.sprite.Group()
shiftclock_group = pg.sprite.GroupSingle()

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
Status.containers = statuses, all_sprites
Timer.containers = cook_timer, all_sprites
Generic.containers = generics, all_sprites
ShiftClock.containers = shiftclock_group, all_sprites

# Initialize objects.
kitchen_rect = read_tilemap(ASSET_DIR / 'map.txt', Floor, Appliance)
player = Player()
play = Button('play')
quit_game = Button('quit')
shiftclock = ShiftClock(
    '9:00', ASSET_DIR / 'fonts' / 'pixel.ttf', 20, 'black'
)
ticketmanager = TicketManager(15, 8, game_manager.get_quotes())

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()

    # Game starts in the main menu.
    if game_manager.state == State.MAIN_MENU:
        mouse_pos = pg.mouse.get_pos()
        mouse = pg.mouse.get_pressed()
        click = mouse[0]

        # Apply background.
        game_manager.draw_background(background)
        # Draw only those in the 'buttons' group.
        game_manager.draw(buttons)

        # Button logic.
        # Not encapsulated, same as player movement logic.
        for button in buttons.sprites():
            # Mouse hovering over button.
            armed = button.rect.collidepoint(mouse_pos)
            # Nothing done to button.
            if not armed and not click:
                button.armed = False
                button.unarm()
                button.clicked = False
            # Mouse is hovering.
            if armed and not button.armed:
                button.armed = True
                button.arm()
            # Hovering and left click held.
            if armed and click and not button.clicked:
                button.click()
                button.clicked = True  
            # Activate button.
            if armed and not click and button.clicked:
                button.clicked = False
                if button.kind == 'play':
                    shiftclock.start_time()
                    game_manager.set_state(State.PLAYING)
                elif button.kind == 'quit':
                    running = False

    elif game_manager.state == State.PLAYING:

        # After a certain amount of time, generate a ticket.
        ticketmanager.update(tickets, shiftclock)
        
        # Draw objects.
        game_manager.draw_background(background)

        game_manager.draw(
            kitchen,
            players,
            popups,
            tickets,
            foods,
            statuses,
            generics,
            shiftclock_group
        )

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
            # First elligible ingredient wanted.
            for ticket in reversed(tickets.sprites()): # Reversing gives oldest first.
                print(ticket.dish.kind)
                for ingredient in reversed(ticket.ingredients):
                    ingr_appliance = ingredient.APPLIANCE_DICT[ingredient.kind]
                    # Find ingredient for the interacted appliance.
                    if ingr_appliance == closest.kind:
                        cooked_ticket = ticket
                        cooked = ingredient
                        quote = ticket.quotes[0]
                        quote.add(cook_group)
                        game_manager.set_state(State.TYPING)

        pause = keys[pg.K_ESCAPE]        

    elif game_manager.state == State.TYPING:
        # Continue spawning tickets even while typing
        ticketmanager.update(tickets, shiftclock)

        game_manager.draw_background(background)

        game_manager.draw(
            kitchen,
            players,
            tickets,
            foods,
            cook_group,
            texts,
            statuses,
            cook_timer,
            shiftclock,
            generics
        )
        # Put this before pg.display.flip()

        quote.handle_ipnut(events)
        if not cook_timer:
            timer = Timer(len(quote.text.split()) + 3,
                  ASSET_DIR / 'fonts' / 'pixel.ttf',
                  80, 'black')

        # Add Wrongs if mess up.
        if (quote.wrongs > len(timer.wrongs) and
            quote.wrongs < 3):
            timer.add_wrong()

        current_wrongs = quote.wrongs

        if int(timer.text) == 0 or quote.wrongs >= 3:
            quote.user.kill()
            cooked.status.image = pg.image.load(IMAGE_DIR / 'x.png').convert_alpha()
            cooked_ticket.ingredients.remove(cooked)
            cooked_ticket.cooked.append(cooked)
            cooked_ticket.quotes.remove(quote)
            cooked.status.add(Status.containers)
            timer.kill()
            for status in timer.wrongs:
                status.kill()

            game_manager.set_state(State.PLAYING)





        if not cook_group:
            quote.user.kill()
            cooked_ticket.ingredients.remove(cooked)
            cooked_ticket.cooked.append(cooked)
            cooked_ticket.quotes.remove(quote)
            cooked.status.add(Status.containers)
            timer.kill()
            for status in timer.wrongs:
                status.kill()
            game_manager.set_state(State.PLAYING)

    pg.display.flip()
    game_manager.clock.tick(Config.FPS)
    
pg.quit()
# TODO: change syntax for button and interactions to foo.is_pressed(pg.K_foo)
# TODO: clock from 9-5, increment by 30 every 10 secs. Day ends at 5.
# TODO: Update ticket locations as tickets are completed
# TODO: money from tickets according to dish quality.

# This program as a whole is my honest attempt at OOP.
# Some caveats:
#   - the only instance properties that 'should be' allowed directly accessed
#   by other classes are images and rects. I couldn't be bothered to make
#   methods to allow this, and it seems in the spirit of pygame to allow
#   direct access to these.

import pygame as pg
import random
from paths import *
from src.config import Config
from src.utils.utils import get_screen_rect, read_tilemap, set_sprite_images
from src.utils.gamemanager import GameManager, State
from src.utils.audiomanager import AudioManager
from src.utils.tablemanager import TableManager

#TODO: Replace Status and Popup to Generic
from src.components.button import Button
from src.components.food import Food
from src.components.generic import Generic
from src.components.player import Player
from src.components.shiftclock import ShiftClock
from src.components.popup import Popup
from src.components.text import Text, QuoteSection
from src.components.ticket import Ticket
from src.components.tile import Tile, Floor, Appliance, Table
from src.components.timer import Timer

from src.shared_data import *

pg.init()
# Initialize game manager object.
game_manager = GameManager()
game_manager.load_screen() 
background = pg.image.load(IMAGE_DIR / 'background.png').convert()

# Create groups.
all_sprites = pg.sprite.Group()
players = pg.sprite.Group()
appliances = pg.sprite.Group()
buttons = pg.sprite.Group()
kitchen = pg.sprite.Group()
popups = pg.sprite.Group()
quotes = pg.sprite.Group()
being_cooked_group = pg.sprite.GroupSingle()
texts = pg.sprite.Group()
foods = pg.sprite.Group()
tickets = pg.sprite.Group()
statuses = pg.sprite.Group()
cook_timer = pg.sprite.Group()
generics = pg.sprite.Group()
shiftclock_group = pg.sprite.GroupSingle()
tables = pg.sprite.Group()

# Assign sprite classes to certain groups.
Appliance.containers = appliances, kitchen, all_sprites
Button.containers = buttons, all_sprites
Floor.containers = kitchen, all_sprites
Food.containers = foods, all_sprites
Generic.containers = generics, all_sprites
Player.containers = players, all_sprites
Popup.containers = popups, all_sprites
QuoteSection.containers = quotes, all_sprites
ShiftClock.containers = shiftclock_group, all_sprites
Text.containers = texts, all_sprites
Ticket.containers = tickets, all_sprites
Timer.containers = cook_timer, all_sprites
Table.containers = appliances, tables, kitchen, all_sprites

# Set images for each class.
for cls in (
    Food,
    Player,
    Tile,
    Popup,
    Button,
    Ticket
):
    set_sprite_images(cls)

# Player needs animations initialized.
Player.set_additional_images()

# Initialize objects.
audiomanager = AudioManager()
screen_center = get_screen_rect().center

running = True
while running:
    # Debugging.
    # print(game_manager.clock)

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()

    # Loop through songs.
    audiomanager.play_music()

    # Apply background.
    game_manager.draw_background(background)

    # Things that need to happen during both phases.
    if game_manager.state == State.PLAYING or game_manager.state == State.TYPING:
        pass

    # Game starts in the main menu.
    if game_manager.state == State.MAIN_MENU:

        if not buttons:
            Button('play', (screen_center[0], screen_center[1] - 150))
            Button('quit', (screen_center[0], screen_center[1] + 150))


        mouse_pos = pg.mouse.get_pos()
        mouse = pg.mouse.get_pressed()
        click = mouse[0]

        # Draw only those in the 'buttons' group.
        game_manager.draw(buttons)

        for button in buttons:
            if button.kind == 'play' and button.activated:
                game_manager.set_state(State.INITIALIZING_ROUND)
                for button in buttons:
                    button.kill()
            if button.kind == 'quit' and button.activated:
                running = False

        # Pass mouse position and click data every frame to buttons.
        buttons.update(mouse_pos, click)


    if game_manager.state == State.INITIALIZING_ROUND:
        # Initialize round objects.
        kitchen_rect = read_tilemap(
            ASSET_DIR / 'map.txt',
            Player,
            Floor,
            Appliance,
            Table
        )
        tablemanager = TableManager(tables)
        # TODO: Old shiftclock still exists. kill it.
        # Create new shiftclock.
        shiftclock = ShiftClock('9:00', 20, 'black')
        pressing_e = False
        game_manager.set_state(State.PLAYING)

    

    if game_manager.state == State.PLAYING:
        # Begin keeping track of time. Pauses when game is paused, and resets when
        # new round begins.
        shiftclock.start()
    
        game_manager.draw(
            kitchen,
            players,
            tickets,
            foods,
            statuses,
            generics,
            texts,
            shiftclock_group,
            popups
        )


        player = players.sprites()[0]

        # TODO: create player method 'move(direction)'
        # Direction controls and collision with appliances.
        keys = pg.key.get_pressed()
 
        # Directional Keybindings
        up = keys[pg.K_w]
        down = keys[pg.K_s]
        left = keys[pg.K_a]
        right = keys[pg.K_d]

        if up:
            player.dy = -player.speed
            player.animate(player.animations['walk_up'])
            player.rect.move_ip(0, player.dy)
        if down:
            player.dy = player.speed
            player.animate(player.animations['walk_down'])
            player.rect.move_ip(0, player.dy)
        hitlist = pg.sprite.spritecollide(player, appliances, False)
        for sprite in hitlist:
            if player.dy > 0:
                player.rect.bottom = sprite.rect.top
            elif player.dy < 0:
                player.rect.top = sprite.rect.bottom
        if left:
            player.dx = -player.speed
            player.animate(player.animations['walk_left'])
            player.rect.move_ip(player.dx, 0)
        if right:
            player.dx = player.speed
            player.animate(player.animations['walk_right'])
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
        closest = min(
            appliances,
            key=lambda appliance: player.get_distance_from(appliance)
        )

        # Player is giving taking order or giving a dish to the table.
        if (
            # Within range of table.
            player.rect.colliderect(closest.get_hitbox()) and
            # Interaction key is pressed.
            keys[pg.K_e]
        ):
            # Closest appliance is a table and is ready to order.
            if closest in tables and closest.order:
                player.take_order(closest)
            # Closest appliance is a kitchen appliance.
            elif closest not in tables:
                if player.ticket:
                    quote = player.ticket.quote_sections[0]
                    for ingr in player.ticket.ingredients:
                        if closest.kind == ingr.APPLIANCE_DICT[ingr.kind]:
                            ingredient_to_cook = ingr
                            game_manager.set_state(State.TYPING)

        pause = keys[pg.K_ESCAPE]  

        # Update all objects.
        all_sprites.update(
            elapsed=shiftclock.get_elapsed(), # Keep track of time.
            player_rect=player.rect, # Player location and hitbox
            keys=keys, # Which keys are being pressed
            closest = closest
            )

        tablemanager.update(shiftclock.get_elapsed())
        
        # One loop in State.PLAYING has passed. User can interact now.
        if not keys[pg.K_e]:
            pressing_e = False

    if game_manager.state == State.TYPING:
        # Continue spawning tickets even while typing
        shiftclock.update()
        cook_timer.update()
        quotes.update()

        game_manager.draw_background(background)
        game_manager.draw(
            kitchen,
            players,
            tickets,
            foods,
            being_cooked_group,
            statuses,
            cook_timer,
            shiftclock_group,
            texts,
            generics
        )

        # Logic for typing.
        quote.handle_input(events)

        # Prevent user from holding E and reentering typing phase.
        if keys[pg.K_e]:
            pressing_e = True
        else:
            pressing_e = False

        if not cook_timer:
            # TODO: Adjust based on difficulty setting.
            # Set the timer duration according to quote length.
            timer = Timer(
                len(quote.text.split()) + 3,
                80,
                'black'
            )
            print(timer.text)

        # Add wrongs if mess up.
        if (quote.misses > len(timer.wrongs) and
            quote.misses < 3):
            timer.add_wrong()

        # If time runs out or user messes up 3 times.
        if int(timer.text) == 0 or quote.misses >= 3:
            quote.finish_incorrectly()
            ingredient_to_cook.status.make_wrong()
            ingredient_to_cook.status.add(Status.containers)
            ticket_to_cook.cooked.append(ingredient_to_cook)
            ticket_to_cook.quotes.remove(quote)
            # Kill sprites for typing sequence.
            timer.kill()
            for status in timer.wrongs:
                status.kill()

            game_manager.set_state(State.PLAYING)
        
        if quote.is_final_correct:
            ingredient_to_cook.status.add(Status.containers)
            ticket_to_cook.cooked.append(ingredient_to_cook)
            ticket_to_cook.quotes.remove(quote)
            # Kill sprites for typing sequence.
            timer.kill()
            for status in timer.wrongs:
                status.kill()
            game_manager.set_state(State.PLAYING)

    pg.display.flip()
    game_manager.clock.tick(Config.FPS)
    
pg.quit()

# TODO: change syntax for button and interactions to foo.is_pressed(pg.K_foo)
# TODO: clock from 9-5, increment by 30 every 10 secs. Day ends at 5.
# TODO: Update ticket locations as tickets are completed
# TODO: money from tickets according to dish quality.
# TODO: Set up scene/level system for setting up and tearing down objects.

# This program as a whole is a demonstration of my OOP skills.
# It comes complete with:
# Abstract base classes that define scenes
# Scene/state management
# Components of the game represented as objects, some of which inherit from one
# another
# Some caveats:
#   - the only instance properties that 'should be' allowed directly accessed
#   by other classes are images and rects. I couldn't be bothered to make
#   methods to allow this, and it seems in the spirit of pygame to allow
#   direct access to these.

import pygame as pg


# TODO: Replace Status and Popup to Generic
from .components.button import Button
from .components.food import Food
from .components.player import Player
from .components.popup import Popup
from .components.ticket import Ticket
from .components.status import Status
from .components.generic import Generic
from .components.timer import Timer
from .components.shiftclock import ShiftClock
from .components.text import Text
from .components.tile import Tile, InteractTile, Appliance, Floor, Table
from .gamestates.statekey import StateKey
from .managers.audiomanager import AudioManager
from .managers.gamestatemanager import GameStateManager
from .gamestates.mainmenu import MainMenu
from .gamestates.level import Level
from .gamestates.cook import Cook
from .groups import *

from .managers.visualmanager import VisualManager

pg.init()

# Assign sprite classes to certain groups.
InteractTile.containers = interact_tiles, kitchen, all_sprites
Appliance.containers = appliances, interact_tiles, kitchen, all_sprites
Table.containers = tables, interact_tiles, kitchen, all_sprites
Button.containers = buttons, all_sprites
Floor.containers = kitchen, all_sprites
Food.containers = foods, all_sprites
Generic.containers = generics, all_sprites
Status.containers = statuses, all_sprites
Player.containers = player_group, all_sprites
Popup.containers = popups, all_sprites
ShiftClock.containers = texts, all_sprites
Text.containers = texts, all_sprites
Ticket.containers = tickets, all_sprites
Timer.containers = texts, all_sprites

# Setup resource managers.
visualmanager = VisualManager()

visualmanager.load_screen()
# Set images for each class.
for sprite_class in (Food, Player, Tile, Popup, Button, Ticket, Status):
    visualmanager.set_sprite_images(sprite_class)

audiomanager = AudioManager()

# Setup gamestate elements.
gamestatemanager = GameStateManager()

# Instantiate gamestates with their keys.
gamestates = [
    MainMenu(
        StateKey.MAIN_MENU,
    ),
    Level(StateKey.LEVEL),
    Cook(StateKey.COOK),
]

# Make sure gamestatemanager and gamestates are aware of each other.
for gamestate in gamestates:
    gamestatemanager.register_gamestate(gamestate, audiomanager, visualmanager)

# Start at main menu.
gamestatemanager.goto(StateKey.MAIN_MENU)

while gamestatemanager.is_running():
    # Debugging.
    # print(gamemanager.clock)
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            gamestatemanager.quit()

    # Make sure current state has a copy of the current events.
    gamestatemanager.send_data({"events": events})
    gamestatemanager.run()

pg.quit()

# # Game starts in the main menu.
# if gamestatemanager.state == State.MAIN_MENU:
#
#     if not buttons:
#         Button("play", (screen_center[0], screen_center[1] - 150))
#         Button("quit", (screen_center[0], screen_center[1] + 150))
#
#     # Draw only those in the 'buttons' group.
#     gamemanager.draw(buttons)
#
#     for button in buttons:
#         if button.kind == "play" and button.activated:
#             gamemanager.set_state(State.INITIALIZING_ROUND)
#             for button in buttons:
#                 button.kill()
#         if button.kind == "quit" and button.activated:
#             running = False
#
#     # Pass mouse position and click data every frame to buttons.
#     buttons.update(mouse_pos, click)
#
# if gamemanager.state == State.INITIALIZING_ROUND:
#     # Initialize round objects.
#     kitchen_rect = read_tilemap(
#         ASSET_DIR / "map.txt", Player, Floor, Appliance, Table
#     )
#     tablemanager = TableManager(tables)
#     # TODO: Old shiftclock still exists. kill it.
#     # Create new shiftclock.
#     shiftclock = ShiftClock()
#     pressing_e = False
#     gamemanager.set_state(State.PLAYING)
#
# if gamemanager.state == State.PLAYING:
#     # Begin keeping track of time. Pauses when game is paused, and resets when
#     # new round begins.
#     shiftclock.start()
#
#     gamemanager.draw(
#         kitchen,
#         players,
#         tickets,
#         foods,
#         statuses,
#         generics,
#         texts,
#         shiftclock_group,
#         popups,
#     )
#
#     # Update all objects.
#     all_sprites.update(
#         elapsed=shiftclock.get_elapsed(),  # Keep track of time.
#         player_rect=player.rect,  # Player location and hitbox
#         keys=keys,  # Which keys are being pressed
#         closest=closest,
#     )
#
#     tablemanager.update(shiftclock.get_elapsed())
#
#     player = players.sprites()[0]
#
#     # TODO: create player method 'move(direction)'
#     # Direction controls and collision with appliances.
#     keys = pg.key.get_pressed()
#
#     # Directional Keybindings
#     up = keys[pg.K_w]
#     down = keys[pg.K_s]
#     left = keys[pg.K_a]
#     right = keys[pg.K_d]
#
#     if up:
#         player.dy = -player.speed
#         player.animate(player.animations["walk_up"])
#         player.rect.move_ip(0, player.dy)
#     if down:
#         player.dy = player.speed
#         player.animate(player.animations["walk_down"])
#         player.rect.move_ip(0, player.dy)
#     hitlist = pg.sprite.spritecollide(player, appliances, False)
#     for sprite in hitlist:
#         if player.dy > 0:
#             player.rect.bottom = sprite.rect.top
#         elif player.dy < 0:
#             player.rect.top = sprite.rect.bottom
#     if left:
#         player.dx = -player.speed
#         player.animate(player.animations["walk_left"])
#         player.rect.move_ip(player.dx, 0)
#     if right:
#         player.dx = player.speed
#         player.animate(player.animations["walk_right"])
#         player.rect.move_ip(player.dx, 0)
#     hitlist = pg.sprite.spritecollide(player, appliances, False)
#     for sprite in hitlist:
#         if player.dx > 0:
#             player.rect.right = sprite.rect.left
#         elif player.dx < 0:
#             player.rect.left = sprite.rect.right
#
#     # Keep chef in the kitchen
#     player.rect.clamp_ip(kitchen_rect)
#
#     # Only interact with the closest appliance.
#     closest = min(
#         appliances,
#         key=lambda appliance: player.get_distance_from(appliance),
#     )
#
#     # Player is giving taking order or giving a dish to the table.
#     if (
#         # Within range of table.
#         player.rect.colliderect(closest.get_hitbox())
#         and
#         # Interaction key is pressed.
#         keys[pg.K_e]
#     ):
#         # Closest appliance is a table and is ready to order.
#         if closest in tables and closest.order:
#             player.take_order(closest)
#         # Closest appliance is a kitchen appliance.
#         elif closest not in tables:
#             # Player has already taken an order.
#             if player.ticket:
#                 # Get quote sections in order.
#                 quote = player.ticket.quote_sections[0]
#                 for ingr in player.ticket.ingredients:
#                     if closest.kind == ingr.APPLIANCE_DICT[ingr.kind]:
#                         ingredient_to_cook = ingr
#                         gamemanager.set_state(State.TYPING)
#
#     pause = keys[pg.K_ESCAPE]
#
#     # One loop in State.PLAYING has passed. User can interact now.
#     if not keys[pg.K_e]:
#         pressing_e = False
#
# if gamemanager.state == State.TYPING:
#     # Continue spawning tickets even while typing
#     shiftclock.update()
#     cook_timer.update()
#     quotes.update()
#
#     gamemanager.draw_background(background)
#     gamemanager.draw(
#         kitchen,
#         players,
#         tickets,
#         foods,
#         being_cooked_group,
#         statuses,
#         cook_timer,
#         shiftclock_group,
#         texts,
#         generics,
#     )
#
#     # Logic for typing.
#     quote.handle_input(events)
#
#     # Prevent user from holding E and reentering typing phase.
#     if keys[pg.K_e]:
#         pressing_e = True
#     else:
#         pressing_e = False
#
#     if not cook_timer:
#         # TODO: Adjust based on difficulty setting.
#         # Set the timer duration according to quote length.
#         timer = Timer(len(quote.text.split()) + 3, 80, "black")
#         print(timer.text)
#
#     # Add wrongs if mess up.
#     if quote.misses > len(timer.wrongs) and quote.misses < 3:
#         timer.add_wrong()
#
#     # If time runs out or user messes up 3 times.
#     if int(timer.text) == 0 or quote.misses >= 3:
#         quote.finish_incorrectly()
#         ingredient_to_cook.status.make_wrong()
#         ingredient_to_cook.status.add(Status.containers)
#         ticket_to_cook.cooked.append(ingredient_to_cook)
#         ticket_to_cook.quotes.remove(quote)
#         # Kill sprites for typing sequence.
#         timer.kill()
#         for status in timer.wrongs:
#             status.kill()
#
#         gamemanager.set_state(State.PLAYING)
#
#     if quote.is_final_correct:
#         ingredient_to_cook.status.add(Status.containers)
#         ticket_to_cook.cooked.append(ingredient_to_cook)
#         ticket_to_cook.quotes.remove(quote)
#         # Kill sprites for typing sequence.
#         timer.kill()
#         for status in timer.wrongs:
#             status.kill()
#         gamemanager.set_state(State.PLAYING)

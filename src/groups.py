import pygame as pg

from src.components.button import Button
from src.components.food import Food
from src.components.generic import Generic
from src.components.player import Player
from src.components.popup import Popup
from src.components.shiftclock import ShiftClock
from src.components.text import QuoteSection, Text
from src.components.ticket import Ticket
from src.components.tile import Appliance, Floor, Table, Tile

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

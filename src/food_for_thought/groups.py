import pygame as pg

from .components.button import Button
from .components.food import Food
from .components.generic import Generic
from .components.player import Player
from .components.popup import Popup
from .components.shiftclock import ShiftClock
from .components.text import QuoteSection, Text
from .components.ticket import Ticket
from .components.tile import Appliance, Floor, Table
from .components.timer import Timer

pg.sprite.Group()
# Create groups.
all_sprites = pg.sprite.Group()
player_group = pg.sprite.GroupSingle()
appliances = pg.sprite.Group()
buttons = pg.sprite.Group()
kitchen = pg.sprite.Group()
popups = pg.sprite.Group()
quotes = pg.sprite.Group()
texts = pg.sprite.Group()
foods = pg.sprite.Group()
tickets = pg.sprite.Group()
statuses = pg.sprite.Group()
generics = pg.sprite.Group()
tables = pg.sprite.Group()

# Assign sprite classes to certain groups.
Appliance.containers = appliances, kitchen, all_sprites
Button.containers = buttons, all_sprites
Floor.containers = kitchen, all_sprites
Food.containers = foods, all_sprites
Generic.containers = generics, all_sprites
Player.containers = player_group, all_sprites
Popup.containers = popups, all_sprites
QuoteSection.containers = quotes, all_sprites
ShiftClock.containers = texts, all_sprites
Text.containers = texts, all_sprites
Ticket.containers = tickets, all_sprites
Timer.containers = texts, all_sprites
Table.containers = appliances, tables, kitchen, all_sprites

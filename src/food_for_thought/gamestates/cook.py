from typing import override


from .. import groups

from .gamestate import GameState
from ..gamestates.statekey import StateKey

from ..components.typeui import TypeUI
from ..components.ticket import Ticket, TicketIngredient
from ..components.levelclock import LevelClock
from ..managers.gamestatemanager import GameStateManager
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager
from ..managers.tablemanager import TableManager
import logging

logger = logging.getLogger(__name__)

gamestate_manager = GameStateManager()
visual_manager = VisualManager()
audio_manager = AudioManager()


class Cook(GameState):
    def __init__(self) -> None:
        super().__init__(StateKey.COOK)

    @override
    def _setup(self):
        self.level_clock: LevelClock = self.data["level_clock"]
        self.ticket: Ticket = self.data["ticket"]
        self.cook_ingredient: TicketIngredient = self.data["cook_ingredient"]
        self.table_manager: TableManager = self.data["table_manager"]
        self.quote_chunk = self.ticket.pop()
        if not self.quote_chunk:
            logger.error("No quote. This shouldn't be happening. returning to level")
            gamestate_manager.goto(StateKey.LEVEL)
            return
        self.typeui = TypeUI(
            self.quote_chunk, self.level_clock.get_elapsed(), fontsize=15
        )

    @override
    def run(self):
        events = self.data["events"]
        self.typeui.handle_input(events)

        if self.typeui.is_written():
            self.ticket.mark_correct(self.cook_ingredient.metadata.name)
            gamestate_manager.goto(StateKey.LEVEL, teardown=True)
            return

        if self.typeui.num_misses() >= 3 or self.typeui.times_up():
            self.ticket.mark_wrong(self.cook_ingredient.metadata.name)
            gamestate_manager.goto(StateKey.LEVEL, teardown=True)
            return

        # FIX: Add pressing e functionality
        # if pg.key.get_pressed()[pg.K_e]:
        #     pressing_e = True
        # else:
        #     pressing_e = False

        self._update()
        self._draw()

    @override
    def _update(self):
        self.typeui.update(self.level_clock.get_elapsed())
        self.level_clock.update()
        groups.tables.update(self.level_clock.get_elapsed())
        groups.popups.update(self.level_clock.get_elapsed())
        groups.texts.update(self.level_clock.get_elapsed(), self.data["dt"])

        self.table_manager.update(self.level_clock.get_elapsed())

    @override
    def _draw(self):
        visual_manager.draw_background()
        visual_manager.draw(
            groups.kitchen,
            groups.player_group,
            groups.tickets,
            groups.foods,
            groups.statuses,
            groups.popups,
            groups.texts,
            groups.generics,
        )

    @override
    def _teardown(self):
        self.typeui.kill()

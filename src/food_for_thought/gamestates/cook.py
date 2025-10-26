from typing import override


from .. import groups

from .gamestate import GameState
from ..gamestates.statekey import StateKey

from ..components.typeui import TypeUI
from ..managers.gamestatemanager import GameStateManager
from ..managers.visualmanager import VisualManager
from ..managers.audiomanager import AudioManager

gamestate_manager = GameStateManager()
visual_manager = VisualManager()
audio_manager = AudioManager()


class Cook(GameState):
    def __init__(self) -> None:
        super().__init__(StateKey.COOK)

    @override
    def _setup(self):
        self.level_clock = self.data["level_clock"]
        self.quote = self.data["quote"]
        self.ticket = self.data["ticket"]
        self.ingredient = self.data["to_cook"]
        self.typeui = TypeUI(
            self.quote.get_content(), self.level_clock.get_elapsed(), fontsize=15
        )

    @override
    def run(self):
        events = self.data["events"]
        done = False
        self.typeui.handle_input(events)

        if self.typeui.is_written():
            self.ingredient.finish_cooked()
            gamestate_manager.goto(StateKey.LEVEL, teardown=True)
        elif self.typeui.get_misses() >= 3 or self.typeui.times_up():
            print(self.typeui.get_misses())
            print(self.typeui.times_up())
            self.ingredient.finish_ruined()
            gamestate_manager.goto(StateKey.LEVEL, teardown=True)

        # FIX: Add pressing e functionality
        # if pg.key.get_pressed()[pg.K_e]:
        #     pressing_e = True
        # else:
        #     pressing_e = False

        self._update()
        self._draw()

        if done:
            gamestate_manager.goto(StateKey.LEVEL, teardown=True)

    @override
    def _update(self):
        self.typeui.update(self.level_clock.get_elapsed())
        self.level_clock.update()
        groups.tables.update(self.level_clock.get_elapsed())

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

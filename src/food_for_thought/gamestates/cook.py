from typing import override


from .. import groups

from .gamestate import GameState
from ..gamestates.statekey import StateKey

from ..components.typeui import TypeUI


class Cook(GameState):
    def __init__(self, statekey) -> None:
        super().__init__(statekey)

    @override
    def _setup(self):
        self.shiftclock = self.data["shiftclock"]
        self.quote = self.data["quote"]
        self.ticket = self.data["ticket"]
        self.ingredient = self.data["to_cook"]
        self.typeui = TypeUI(
            self.quote.get_content(), self.shiftclock.get_elapsed(), fontsize=15
        )

    @override
    def _teardown(self):
        self.typeui.kill()

    @override
    def run(self):
        events = self.data["events"]
        done = False
        self.typeui.handle_input(events)

        if self.typeui.is_written():
            self.ingredient.finish_cooked()
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)
        elif self.typeui.get_misses() >= 3 or self.typeui.times_up():
            print(self.typeui.get_misses())
            print(self.typeui.times_up())
            self.ingredient.finish_ruined()
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)

        # FIX: Add pressing e functionality
        # if pg.key.get_pressed()[pg.K_e]:
        #     pressing_e = True
        # else:
        #     pressing_e = False

        self._update()
        self._draw()

        if done:
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)

    @override
    def _update(self):
        self.typeui.update(self.shiftclock.get_elapsed())
        self.shiftclock.update()
        groups.tables.update(self.shiftclock.get_elapsed())

    @override
    def _draw(self):
        self._visualmanager.draw_background()
        self._visualmanager.draw(
            groups.kitchen,
            groups.player_group,
            groups.tickets,
            groups.foods,
            groups.statuses,
            groups.popups,
            groups.texts,
            groups.generics,
        )

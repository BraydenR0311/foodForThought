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
        self.events = self.data["events"]
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
        done = False
        self.typeui.handle_input(self.events)

        if self.typeui.is_written():
            self.ingredient.finish_cooked()
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)
        elif self.typeui.get_misses() >= 3 or self.timer.is_done():
            self.ingredient.finish_ruined()
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)

        # FIX: Add pressing e functionality
        # if pg.key.get_pressed()[pg.K_e]:
        #     pressing_e = True
        # else:
        #     pressing_e = False

        # User mistyped, but less than 3 times.
        if (
            self.quote.num_misses() > len(self.timer.wrongs)
            and self.quote.num_misses < 3
        ):
            # Add x mark below timer.
            self.timer.add_wrong()

        # If time runs out or user messes up 3 times.
        if int(self.timer.text) == 0 or self.quote.num_misses() >= 3:
            # Ingredient finished incorrectly.
            self.ingredient.make_wrong()
            done = True
        else:
            self.ingredient.make_correct()
            self.ticket.increment_score()
            done = True

        self._update()
        self._draw()

        if done:
            self._gsmanager.goto(StateKey.LEVEL, teardown=True)

    @override
    def _update(self):
        self.timer.update()
        self.shiftclock.update()
        groups.quotes.update()
        groups.tables.update()

    @override
    def _draw(self):
        self._visualmanager.draw_background()
        self._visualmanager.draw(
            groups.tickets,
            groups.foods,
            groups.statuses,
            groups.texts,
            groups.generics,
        )

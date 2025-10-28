import random
from ..components.table import Table
from .. import groups


class TableManager:
    # Minimum default time before table can decide order (in ms).
    LOWER = 3000
    # Max default time before table can decide order.
    UPPER = 10000

    def __init__(self, spritegroup: pg.sprite.Group):
        self.spritegroup = spritegroup
        self.table = None
        self.elapsed = None
        # Acts as a table's random time before they decide to order. Needs to
        # be chosen one at a time so it can be adjusted based on the number of
        # tables currently ordering.
        self.decide_time = 0
        # Mark a specific point point in time where the last 'decide_time'
        # was chosen.
        self.last_decide_time = 0

    def update(self, elapsed):
        self.elapsed = elapsed
        # Decide time has not been chosen yet.
        if not self.decide_time and self.tables_ready_order():
            self.set_decide_time(
                # Scale according to number of tables currently waiting.
                self.LOWER * (self.num_waiting() + 1),
                self.UPPER * (self.num_waiting() + 1),
            )

        # Amount of time passed since last order was placed.
        if self.elapsed - self.last_decide_time > self.decide_time:
            table = self.get_random_table()
            table._decide_order()
            self.decide_time = 0

    def tables_ready_order(self) -> list[Table]:
        """Get list of all sprites who have decided their order and are
        waiting to receive one from the chef.
        """
        return [sprite for sprite in self.spritegroup.sprites() if not sprite.order]

    def num_waiting(self) -> int:
        """Return number of tables ready to order."""
        return len(self.spritegroup) - len(self.tables_ready_order())

    def get_random_table(self) -> Table:
        """Choose random table from sprites."""
        return random.choice(self.tables_ready_order())

    def set_decide_time(self, lower: int, upper: int) -> None:
        """Choose random decide time based on a range in milliseconds."""
        self.decide_time = random.randint(lower, upper)
        self.last_decide_time = self.elapsed

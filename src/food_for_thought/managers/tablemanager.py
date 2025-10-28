import random
from ..components.table import Table
from .. import groups


class TableManager:
    _instance = None
    _initialized = False

    INCREASE_SECS = 4

    INITIAL_MIN_DECIDING_SECS = 1
    INITIAL_MAX_DECIDING_SECS = 5

    # Will leave at this time.
    SECS_BEFORE_LEAVE = 60

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if TableManager._initialized:
            return
        self._next_order_time = 0.0

    def update(self, level_elapsed):
        # Only on first loop.
        if not self._next_order_time:
            self._schedule_next_order_time(level_elapsed)

        # Time to order.
        if level_elapsed >= self._next_order_time:
            self._table_order()
            self._schedule_next_order_time(level_elapsed)

    def _table_order(self):
        """Pick an available table and order."""
        table = self._get_random_available_table()
        table.decide_order()

    def _get_random_available_table(self):
        """Randomly choose an available table."""
        return random.choice(self._get_tables_not_waiting())

    def _schedule_next_order_time(self, level_elapsed) -> None:
        """Update the next order time."""
        min_deciding_secs = (
            TableManager.INITIAL_MIN_DECIDING_SECS
            + TableManager.INCREASE_SECS * self._get_num_waiting()
        )
        max_deciding_secs = (
            TableManager.INITIAL_MAX_DECIDING_SECS
            + TableManager.INCREASE_SECS * self._get_num_waiting()
        )
        self._next_order_time = level_elapsed + random.uniform(
            min_deciding_secs, max_deciding_secs
        )

    def _get_tables_not_waiting(self) -> list[Table]:
        """Get tables who are not waiting."""
        return [table for table in groups.tables.sprites() if not table.is_waiting()]

    def _get_num_waiting(self) -> int:
        """Return number of tables waiting for food."""
        return len([table for table in groups.tables.sprites() if table.is_waiting()])

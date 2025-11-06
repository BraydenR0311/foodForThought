import random
from ..components.table import Table
from .. import groups
import logging

logger = logging.getLogger(__name__)


class TableManager:
    _instance = None
    _initialized = False

    INCREASE_TIME = 4000

    INITIAL_MIN_DECIDING_TIME = 1000
    INITIAL_MAX_DECIDING_TIME = 5000

    # Will leave at this time.
    TIME_BEFORE_LEAVE = 60000

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
        if table:
            table.decide_order()

    def _get_random_available_table(self):
        """Randomly choose an available table."""
        available_tables = [
            table for table in groups.tables.sprites() if table.can_order()
        ]
        if not available_tables:
            return
        return random.choice(available_tables)

    def _schedule_next_order_time(self, level_elapsed) -> None:
        """Update the next order time."""
        min_deciding_time = (
            TableManager.INITIAL_MIN_DECIDING_TIME
            + TableManager.INCREASE_TIME * self._get_num_waiting()
        )
        max_deciding_time = (
            TableManager.INITIAL_MAX_DECIDING_TIME
            + TableManager.INCREASE_TIME * self._get_num_waiting()
        )
        self._next_order_time = level_elapsed + random.uniform(
            min_deciding_time, max_deciding_time
        )
        logger.debug(
            "Next order time: %.2f. Min: %.2f. Max: %.2f",
            self._next_order_time,
            min_deciding_time,
            max_deciding_time,
        )

    def _get_num_waiting(self) -> int:
        """Return number of tables waiting for food."""
        return len(
            [table for table in groups.tables.sprites() if not table.can_order()]
        )

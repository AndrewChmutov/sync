import logging
from typing import Any

from socketio import AsyncNamespace

from sync.communication.frontend.model import (
    Settings,
    Statistics,
)
from sync.communication.node.discovery import Discovery
from sync.runtime.runner import AsyncRunner


class Node(AsyncNamespace):
    def __init__(
        self,
        runner: AsyncRunner,
        settings: Settings,
        statistics: Statistics,
        logger: logging.Logger,
        namespace: Any = "/node",
    ) -> None:
        super().__init__(namespace)
        self.runner = runner
        self.logger = logger
        self.settings = settings
        self.statistics = statistics
        self.discovery = Discovery(self.runner, self.logger)

from typing import Any
from socketio import AsyncNamespace
import logging

from communication.frontend.model import Settings, Statistics
import utils

class Nodes(AsyncNamespace):
    def __init__(
        self,
        settings: Settings,
        statistics: Statistics,
        logger: logging.Logger,
        namespace: Any = "/ui"
    ):
        super().__init__(namespace)
        self.logger = logger
        self.settings = settings
        self.statistics = statistics

    def on_connect(self, sid: str, environ: dict[str, Any]):
        self.logger.info(f"UI Connection: {sid}")

    def on_set_password(self, _key: str, password: str):
        self.settings.password = password

    async def on_check_dir(self, _key: str, dir: str):
        self.settings.dir = dir
        is_correct = utils.correct_dir(dir)
        self.logger.info(f"Received {"not " if is_correct else ""}correct dir: {dir}")
        await self.emit("correct_dir", is_correct)

    def on_disconnect(self, sid: str):
        self.logger.warning(f"UI Disconnect: {sid}")


from dataclasses import asdict
from typing import Any
from socketio import AsyncNamespace
import logging

from communication.frontend.model import Settings, Statistics
import main
import utils

class UI(AsyncNamespace):
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
        self.logger.info(f"[UI] WebSocket connected: {sid}")

    def on_set_password(self, _key: str, password: str):
        self.settings.password = password

    async def on_check_dir(self, _key: str, dir: str):
        self.settings.dir = dir
        is_correct = utils.correct_dir(dir)
        self.logger.info(
            f'[UI] WebSocket request correct_dir for "{dir}". '
            f"Respond with: {is_correct}"
        )
        await self.emit("correct_dir", is_correct)

    async def on_get_stats(self, _key: str):
        response = asdict(self.statistics)
        self.logger.info(
            "[UI] Websocket request get_stats. "
            f"Respond with: {response}"
        )
        await self.emit("set_stats", response)

    def on_disconnect(self, sid: str):
        self.logger.warning(f"[UI] WebSocket disconnected: {sid}")

import logging
from pathlib import Path
from typing import Any

from socketio import AsyncNamespace

from sync.communication.frontend.model import Settings, Statistics


class UI(AsyncNamespace):
    def __init__(
        self,
        settings: Settings,
        statistics: Statistics,
        logger: logging.Logger,
        namespace: Any = "/ui",
    ) -> None:
        super().__init__(namespace)
        self.logger = logger
        self.settings = settings
        self.statistics = statistics

    def on_connect(self, sid: str, environ: dict[str, Any]) -> None:
        self.logger.info(f"[UI] WebSocket connected: {sid}")

    def on_set_password(self, _key: str, password: str) -> None:
        self.settings.password = password

    async def on_check_dir(self, _key: str, dir: str) -> None:
        self.settings.dir = dir
        is_correct = self._is_correct_dir(dir)
        self.logger.info(
            f'[UI] WebSocket request correct_dir for "{dir}". '
            f"Respond with: {is_correct}"
        )
        await self.emit("correct_dir", is_correct)

    async def on_get_stats(self, _key: str) -> None:
        response = self.statistics.model_dump()
        self.logger.info(
            "[UI] Websocket request get_stats. " f"Respond with: {response}"
        )
        await self.emit("set_stats", response)

    def on_disconnect(self, sid: str) -> None:
        self.logger.warning(f"[UI] WebSocket disconnected: {sid}")

    @staticmethod
    def _is_correct_dir(dir: str) -> bool:
        return dir.strip() != "" and Path(dir).expanduser().is_dir()

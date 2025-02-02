import logging
from pathlib import Path
from typing import Any

from socketio import AsyncNamespace

from sync.communication.frontend.model import (
    CurrentDevice,
    LocalState,
    Settings,
    Statistics,
)
from sync.runtime import job
from sync.runtime.runner import AsyncRunner


class UI(AsyncNamespace):
    def __init__(
        self,
        runner: AsyncRunner,
        settings: Settings,
        statistics: Statistics,
        logger: logging.Logger,
        namespace: Any = "/ui",
    ) -> None:
        super().__init__(namespace)
        self.runner = runner
        self.logger = logger
        self.settings = settings
        self.statistics = statistics
        self.current_device: CurrentDevice | None = None
        self.agent: str | None = None

    async def on_connect(self, sid: str, environ: dict[str, Any]) -> None:
        self.logger.info(f"[UI] WebSocket connected: {sid}")
        self.agent = environ["HTTP_USER_AGENT"]

        async def set_current_device() -> None:
            device = self.current_device or CurrentDevice.empty()
            await self.emit("set_current_device", device.model_dump())

        self.runner.run_periodic(set_current_device, 1)
        await self.emit("set_stats", self.statistics.model_dump())

    def on_set_password(self, _key: str, password: str) -> None:
        self.settings.password = password

    async def on_check_dir(self, _key: str, dir: str) -> None:
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

    async def on_scan(self, _key: str, path: str | Path) -> None:
        path = Path(path).expanduser()
        self.statistics.refreshes += 1
        if not path.is_dir():
            local_state = LocalState.empty()
        else:
            self.current_device = CurrentDevice(
                path=f"{path} (Loading)",
                local_state=None,
                agent=self.agent or "agent",
            )
            local_state = await self.runner.run_worker(job.LocalState, path)  # noqa: E501
        self.current_device = CurrentDevice(
            path=str(path),
            local_state=local_state,
            agent=self.agent or "agent",
        )

        await self.emit("set_stats", self.statistics.model_dump())

    def on_disconnect(self, sid: str) -> None:
        self.logger.warning(f"[UI] WebSocket disconnected: {sid}")

    @staticmethod
    def _is_correct_dir(dir: str) -> bool:
        return dir.strip() != "" and Path(dir).expanduser().is_dir()

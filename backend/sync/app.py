import functools
import logging
from collections.abc import Callable
from os import PathLike
from typing import cast

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp, AsyncServer

from sync.communication import globals
from sync.communication.frontend.socket import UI

StrOrPath = str | PathLike[str]


class App:
    def __init__(
        self,
        ssl_certfile: StrOrPath | None = None,
        ssl_keyfile: StrOrPath | None = None,
        ssl_keyfile_password: str | None = None,
        log_level: str | int = logging.DEBUG,
    ) -> None:
        # FastAPI
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Security
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.ssl_keyfile_password = ssl_keyfile_password

        # Logging
        self.logger = logging.getLogger("uvicorn.asgi")
        self.logger.setLevel(log_level)

        # Uvicorn
        socket_server = AsyncServer(
            async_mode="asgi", cors_allowed_origins="*"
        )
        socket_server.register_namespace(
            UI(globals.settings, globals.stats, self.logger)
        )
        self._app = ASGIApp(socket_server, app)

    def run(self) -> Callable[[str], None]:
        return cast(
            Callable[[str], None],
            functools.partial(
                uvicorn.run,
                log_level=self.logger.level,
                use_colors=True,
                ssl_certfile=self.ssl_certfile,
                ssl_keyfile=self.ssl_keyfile,
                ssl_keyfile_password=self.ssl_keyfile_password,
            ),
        )

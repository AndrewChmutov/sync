from pathlib import Path
from dataclasses import dataclass
from ssl import SSLContext
import ssl
from typing import Any
import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import AsyncServer, AsyncNamespace, ASGIApp

from communication.frontend.model import Settings, Statistics
from communication.frontend.socket import UI
from communication.node.socket import Nodes
from communication import globals


logger = logging.getLogger("uvicorn.asgi")





socket_server = AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_server.register_namespace(UI(globals.settings, globals.stats, logger))
# socket_server.register_namespace(Nodes(globals.settings, globals.stats, logger))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ssl_context = SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("../cert/cert.pem", keyfile="../cert/key.pem")
#
# @app.post("/api/set-password")
# async def set_password(request: Request):
#     data = await request.json()
#     SETTINGS.password = data.get("password")
#
# @app.post("/api/set-dir")
# async def set_dir(request: Request) -> Response:
#     data = await request.json()
#     dir = data.get("dir", "")
#     SETTINGS.dir = dir
#
#     return JSONResponse({
#         "correct": 
#     })

logger.info("kek")
top_app = ASGIApp(socket_server, app)

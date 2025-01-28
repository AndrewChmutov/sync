import time

from communication.frontend.model import Settings, Statistics

start_time = time.time()
settings = Settings()
stats = Statistics()
checksums: dict[str, str] = {}

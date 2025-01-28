from communication.frontend.model import Settings, Statistics
import time


start_time = time.time()
settings = Settings()
stats = Statistics()
checksums: dict[str, str] = {}

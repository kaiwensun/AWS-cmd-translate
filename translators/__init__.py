import importlib
from config import settings

for engine_name in settings.ENGINES:
    importlib.import_module("." + engine_name, "translators")

__all__ = settings.ENGINES

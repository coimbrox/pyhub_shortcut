# pyhub_shortcut/__init__.py

from .cli import main as cli_main
from .config import actions
from .config_manager import ConfigManager
from .core import ShortcutManager
from .core_improved import ShortcutManager as ImprovedShortcutManager
from .ui import show_menu

__version__ = "0.1.0"

__all__ = [
    "ShortcutManager",
    "ImprovedShortcutManager",
    "ConfigManager",
    "show_menu",
    "actions",
    "cli_main",
]

# pyhub_shortcut/__init__.py

from .cli import main as cli_main
from .config import actions
from .config_manager import ConfigManager
from .core import ShortcutManager
from .core_improved import ShortcutManager as ImprovedShortcutManager
from .ui import show_menu

try:
    from .droplist_manager import DropListAction, DropListManager
except ImportError:
    # Importação opcional caso as dependências não estejam disponíveis
    DropListManager = None
    DropListAction = None

__version__ = "0.1.1"
__author__ = "Gabriel Coimbra"
__email__ = "coimbrawebs@gmail.com"
__description__ = "Biblioteca Python para criar menus DropList interativos com atalhos de teclado + scroll do mouse"

__all__ = [
    "ShortcutManager",
    "ImprovedShortcutManager",
    "ConfigManager",
    "DropListManager",
    "DropListAction",
    "show_menu",
    "actions",
    "cli_main",
    "__version__",
]

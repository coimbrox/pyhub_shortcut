# pyhub_shortcut/core_improved.py

import logging
import subprocess
import threading
from typing import Any, Callable, Dict, List

import keyboard

from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class ShortcutManager:
    """Gerenciador de atalhos globais melhorado"""

    def __init__(self, config_manager: ConfigManager = None):
        self.config_manager = config_manager or ConfigManager()
        self.active = False
        self.registered_hotkeys = []
        self._setup_logging()

    def _setup_logging(self):
        """Configura logging básico"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def start(self):
        """Inicia o gerenciador de atalhos"""
        if self.active:
            logger.warning("ShortcutManager já está ativo")
            return

        self.active = True
        self._register_hotkeys()
        logger.info("ShortcutManager iniciado com sucesso")

    def _register_hotkeys(self):
        """Registra todos os atalhos configurados"""
        for i, action in enumerate(self.config_manager.actions):
            try:
                hotkey = action.get("hotkey", f"ctrl+{i+1}")
                keyboard.add_hotkey(hotkey, lambda idx=i: self._execute_action(idx))
                self.registered_hotkeys.append(hotkey)
                logger.info(f"Atalho registrado: {hotkey} -> {action['label']}")
            except Exception as e:
                logger.error(f"Erro ao registrar atalho {hotkey}: {e}")

    def _execute_action(self, index: int):
        """Executa uma ação pelo índice"""
        try:
            if 0 <= index < len(self.config_manager.actions):
                action = self.config_manager.actions[index]
                command = action["command"]

                logger.info(f"Executando: {action['label']} -> {command}")

                # Executa o comando
                subprocess.Popen(command, shell=True)

        except Exception as e:
            logger.error(f"Erro ao executar ação {index}: {e}")

    def stop(self):
        """Para o gerenciador de atalhos"""
        if not self.active:
            return

        self.active = False
        keyboard.unhook_all_hotkeys()
        self.registered_hotkeys.clear()
        logger.info("ShortcutManager parado")

    def reload_config(self):
        """Recarrega configurações"""
        if self.active:
            self.stop()
            self.config_manager = ConfigManager()
            self.start()
        else:
            self.config_manager = ConfigManager()

    def list_actions(self) -> List[Dict[str, Any]]:
        """Lista todas as ações configuradas"""
        return self.config_manager.actions.copy()

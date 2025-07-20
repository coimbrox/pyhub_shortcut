# pyhub_shortcut/config_manager.py

import json
import os
from pathlib import Path
from typing import Any, Dict, List


class ConfigManager:
    """Gerencia configurações de atalhos de forma flexível"""

    def __init__(self, config_file: str = None):
        self.config_file = config_file or self._get_default_config_path()
        self.actions = self._load_config()

    def _get_default_config_path(self) -> str:
        """Retorna o caminho padrão para o arquivo de configuração"""
        home = Path.home()
        config_dir = home / ".pyhub_shortcut"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.json")

    def _load_config(self) -> List[Dict[str, Any]]:
        """Carrega configurações do arquivo JSON"""
        if not os.path.exists(self.config_file):
            return self._get_default_actions()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("actions", self._get_default_actions())
        except (json.JSONDecodeError, FileNotFoundError):
            return self._get_default_actions()

    def _get_default_actions(self) -> List[Dict[str, Any]]:
        """Retorna ações padrão"""
        return [
            {
                "label": "Abrir Google",
                "command": "start https://www.google.com",
                "hotkey": "ctrl+1",
            },
            {"label": "Abrir Notepad", "command": "notepad", "hotkey": "ctrl+2"},
            {"label": "Abrir VS Code", "command": "code .", "hotkey": "ctrl+3"},
        ]

    def save_config(self):
        """Salva configurações no arquivo"""
        config_data = {"actions": self.actions}
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    def add_action(self, label: str, command: str, hotkey: str):
        """Adiciona uma nova ação"""
        self.actions.append({"label": label, "command": command, "hotkey": hotkey})
        self.save_config()

    def remove_action(self, index: int):
        """Remove uma ação pelo índice"""
        if 0 <= index < len(self.actions):
            self.actions.pop(index)
            self.save_config()

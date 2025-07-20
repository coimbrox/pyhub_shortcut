# pyhub_shortcut/droplist_manager.py

import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import keyboard
import mouse

from .ui import DropListMenu


@dataclass
class DropListAction:
    """Representa uma ação no menu droplist"""

    label: str
    command: str
    icon: Optional[str] = None
    category: Optional[str] = None
    hotkey: Optional[str] = None


class DropListManager:
    """
    Gerenciador principal para menus DropList
    Combina atalhos de teclado + scroll do mouse para mostrar menus contextuais
    """

    def __init__(self):
        self.active = False
        self.menu_visible = False
        self.current_menu = None
        self.actions: Dict[str, List[DropListAction]] = {}
        self.trigger_combinations = {}
        self.scroll_buffer = []
        self.last_scroll_time = 0
        self.scroll_threshold = 0.1  # segundos entre scrolls

    def register_droplist(
        self, trigger_key: str, actions: List[DropListAction], menu_id: str = "default"
    ):
        """
        Registra um novo DropList

        Args:
            trigger_key: Tecla que ativa o menu (ex: 'ctrl')
            actions: Lista de ações do menu
            menu_id: ID único para o menu
        """
        self.actions[menu_id] = actions
        self.trigger_combinations[trigger_key] = menu_id

    def start(self):
        """Inicia o gerenciador de DropLists"""
        if self.active:
            return

        self.active = True
        self._setup_listeners()

    def _setup_listeners(self):
        """Configura listeners de teclado e mouse"""
        # Thread para monitorar combinações de teclas
        threading.Thread(target=self._monitor_key_combinations, daemon=True).start()

        # Listener de eventos do mouse (inclui scroll)
        mouse.hook(self._mouse_event_handler)

    def _monitor_key_combinations(self):
        """Monitora combinações de teclas para ativar menus"""
        while self.active:
            for trigger_key, menu_id in self.trigger_combinations.items():
                if keyboard.is_pressed(trigger_key):
                    # Espera por scroll enquanto a tecla estiver pressionada
                    self._wait_for_scroll_while_pressed(trigger_key, menu_id)
            time.sleep(0.01)

    def _wait_for_scroll_while_pressed(self, trigger_key: str, menu_id: str):
        """Espera por scroll enquanto a tecla trigger estiver pressionada"""
        start_time = time.time()

        while keyboard.is_pressed(trigger_key) and self.active:
            # Se houve scroll recente, mostra o menu
            if (time.time() - self.last_scroll_time) < 0.5:
                self._show_droplist(menu_id)
                break

            # Timeout após 2 segundos
            if time.time() - start_time > 2.0:
                break

            time.sleep(0.01)

    def _mouse_event_handler(self, event):
        """Handler para eventos do mouse, filtra apenas scroll"""
        if hasattr(event, "event_type") and event.event_type == "wheel":
            current_time = time.time()
            dy = getattr(event, "delta", 0)

            # Registra o scroll
            self.last_scroll_time = current_time
            self.scroll_buffer.append((current_time, dy))

            # Limpa buffer antigo
            self.scroll_buffer = [
                (t, scroll) for t, scroll in self.scroll_buffer if current_time - t < 1.0
            ]

    def _show_droplist(self, menu_id: str):
        """Mostra o menu DropList especificado"""
        if self.menu_visible or menu_id not in self.actions:
            return

        actions = self.actions[menu_id]
        if not actions:
            return

        self.menu_visible = True

        # Obtém posição do cursor
        cursor_pos = mouse.get_position()

        # Cria e mostra o menu
        self.current_menu = DropListMenu(
            actions=actions,
            position=cursor_pos,
            on_select=self._on_menu_select,
            on_close=self._on_menu_close,
        )

        self.current_menu.show()

    def _on_menu_select(self, action: DropListAction):
        """Handler para quando uma ação é selecionada"""
        import subprocess

        try:
            # Executa o comando da ação
            subprocess.Popen(action.command, shell=True)
            print(f"✅ Executando: {action.label} -> {action.command}")
        except Exception as e:
            print(f"❌ Erro ao executar {action.label}: {e}")

        self._close_menu()

    def _on_menu_close(self):
        """Handler para quando o menu é fechado"""
        self._close_menu()

    def _close_menu(self):
        """Fecha o menu atual"""
        self.menu_visible = False
        if self.current_menu:
            self.current_menu.close()
            self.current_menu = None

    def stop(self):
        """Para o gerenciador"""
        self.active = False
        self._close_menu()
        mouse.unhook_all()
        keyboard.unhook_all()


# Exemplo de uso
def create_default_droplist():
    """Cria um DropList padrão com ações comuns"""
    manager = DropListManager()

    # DropList para desenvolvimento
    dev_actions = [
        DropListAction("🌐 Abrir GitHub", "start https://github.com", "🌐"),
        DropListAction("💻 VS Code", "code .", "💻"),
        DropListAction("📁 Explorer", "explorer .", "📁"),
        DropListAction("🔧 Terminal", "powershell", "🔧"),
    ]

    # DropList para produtividade
    productivity_actions = [
        DropListAction("📧 Gmail", "start https://gmail.com", "📧"),
        DropListAction("📅 Calendar", "start https://calendar.google.com", "📅"),
        DropListAction("📝 Notion", "start https://notion.so", "📝"),
        DropListAction("🎵 Spotify", "start https://spotify.com", "🎵"),
    ]

    # Registra os menus
    manager.register_droplist("ctrl", dev_actions, "development")
    manager.register_droplist("alt", productivity_actions, "productivity")

    return manager

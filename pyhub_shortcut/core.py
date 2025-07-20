# pyhub_shortcut/core.py

import keyboard
import threading

class ShortcutManager:
    def __init__(self, action_callback):
        self.action_callback = action_callback
        self.active = False

    def start(self):
        self.active = True
        threading.Thread(target=self._listen_shortcuts, daemon=True).start()

    def _listen_shortcuts(self):
        keyboard.add_hotkey('ctrl+1', lambda: self.action_callback(0))
        keyboard.add_hotkey('ctrl+2', lambda: self.action_callback(1))
        keyboard.add_hotkey('ctrl+3', lambda: self.action_callback(2))
        # Você pode adicionar Ctrl + Scroll futuramente com mouse lib

    def stop(self):
        self.active = False
        keyboard.unhook_all_hotkeys()

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyhub_shortcut import actions, core, ui


def handle_action(index):
    action = actions[index]
    ui.show_menu([action])


if __name__ == "__main__":
    manager = core.ShortcutManager(handle_action)
    manager.start()

    print("Atalhos ativos! Pressione Ctrl+1, Ctrl+2, etc...")
    input("Pressione Enter para sair...")
    input("Pressione Enter para encerrar.\n")
    manager.stop()

# pyhub_shortcut/cli.py

import argparse
import sys
import time

from .config_manager import ConfigManager
from .core_improved import ShortcutManager


def main():
    """Interface de linha de comando principal"""
    parser = argparse.ArgumentParser(
        description="PyHub Shortcut - Gerenciador de atalhos globais"
    )
    parser.add_argument(
        "--config", "-c", help="Caminho para arquivo de configuração personalizado"
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="Lista todas as ações configuradas"
    )
    parser.add_argument(
        "--add",
        "-a",
        nargs=3,
        metavar=("LABEL", "COMMAND", "HOTKEY"),
        help="Adiciona nova ação: --add 'Label' 'comando' 'ctrl+4'",
    )
    parser.add_argument(
        "--remove", "-r", type=int, metavar="INDEX", help="Remove ação pelo índice"
    )
    parser.add_argument(
        "--daemon",
        "-d",
        action="store_true",
        help="Executa em modo daemon (sem interface)",
    )

    args = parser.parse_args()

    # Inicializa gerenciador de configuração
    config_manager = ConfigManager(args.config)

    # Lista ações
    if args.list:
        list_actions(config_manager)
        return

    # Adiciona ação
    if args.add:
        label, command, hotkey = args.add
        config_manager.add_action(label, command, hotkey)
        print(f"✅ Ação adicionada: {label} ({hotkey})")
        return

    # Remove ação
    if args.remove is not None:
        if 0 <= args.remove < len(config_manager.actions):
            action = config_manager.actions[args.remove]
            config_manager.remove_action(args.remove)
            print(f"🗑️ Ação removida: {action['label']}")
        else:
            print("❌ Índice inválido")
        return

    # Inicia gerenciador
    if args.daemon:
        run_daemon(config_manager)
    else:
        run_interactive(config_manager)


def list_actions(config_manager: ConfigManager):
    """Lista todas as ações configuradas"""
    print("\n📋 Ações Configuradas:")
    print("-" * 50)
    for i, action in enumerate(config_manager.actions):
        hotkey = action.get("hotkey", f"ctrl+{i+1}")
        print(f"{i:2d}. {action['label']} ({hotkey})")
        print(f"    Comando: {action['command']}")
    print()


def run_daemon(config_manager: ConfigManager):
    """Executa em modo daemon"""
    manager = ShortcutManager(config_manager)
    manager.start()

    print("🚀 PyHub Shortcut iniciado em modo daemon")
    print("Pressione Ctrl+C para parar")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Parando...")
        manager.stop()


def run_interactive(config_manager: ConfigManager):
    """Executa em modo interativo"""
    manager = ShortcutManager(config_manager)
    manager.start()

    print("🎮 PyHub Shortcut - Modo Interativo")
    print("=" * 40)
    list_actions(config_manager)
    print("Comandos disponíveis:")
    print("  'list' - Lista ações")
    print("  'reload' - Recarrega configuração")
    print("  'quit' - Sair")
    print()

    try:
        while True:
            command = input("pyhub> ").strip().lower()

            if command == "quit":
                break
            elif command == "list":
                list_actions(config_manager)
            elif command == "reload":
                manager.reload_config()
                print("🔄 Configuração recarregada")
                list_actions(manager.config_manager)
            elif command == "":
                continue
            else:
                print("❌ Comando não reconhecido")

    except KeyboardInterrupt:
        pass
    finally:
        print("\n🛑 Parando...")
        manager.stop()


if __name__ == "__main__":
    main()

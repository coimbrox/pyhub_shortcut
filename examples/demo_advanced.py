"""
Exemplo avançado do pyhub_shortcut
Demonstra o uso das funcionalidades melhoradas
"""

import os
import sys

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyhub_shortcut import ConfigManager, ImprovedShortcutManager


def exemplo_basico():
    """Exemplo básico usando configuração padrão"""
    print("🚀 Exemplo Básico - PyHub Shortcut")
    print("=" * 40)

    # Usa configuração padrão
    manager = ImprovedShortcutManager()
    manager.start()

    # Lista ações configuradas
    print("\n📋 Ações configuradas:")
    for i, action in enumerate(manager.list_actions()):
        hotkey = action.get("hotkey", f"ctrl+{i+1}")
        print(f"  {hotkey} -> {action['label']}")

    print("\n✨ Atalhos ativos! Teste os atalhos configurados.")
    print("Pressione Enter para parar...")

    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        manager.stop()
        print("🛑 Manager parado.")


def exemplo_configuracao_personalizada():
    """Exemplo com configuração personalizada"""
    print("🎨 Exemplo com Configuração Personalizada")
    print("=" * 45)

    # Cria configuração personalizada
    config = ConfigManager()

    # Adiciona algumas ações personalizadas
    config.add_action("Abrir YouTube", "start https://youtube.com", "ctrl+shift+y")
    config.add_action("Abrir Terminal", "powershell", "ctrl+shift+t")
    config.add_action("Calculadora", "calc", "ctrl+shift+c")

    # Inicia manager com configuração personalizada
    manager = ImprovedShortcutManager(config)
    manager.start()

    print("\n📋 Ações personalizadas:")
    for i, action in enumerate(manager.list_actions()):
        hotkey = action.get("hotkey", f"ctrl+{i+1}")
        print(f"  {hotkey} -> {action['label']}")

    print("\n✨ Atalhos personalizados ativos!")
    print("Pressione Enter para parar...")

    try:
        input()
    except KeyboardInterrupt:
        pass
    finally:
        manager.stop()
        print("🛑 Manager parado.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Exemplos do PyHub Shortcut")
    parser.add_argument(
        "--advanced",
        "-a",
        action="store_true",
        help="Executa exemplo avançado com configuração personalizada",
    )

    args = parser.parse_args()

    if args.advanced:
        exemplo_configuracao_personalizada()
    else:
        exemplo_basico()

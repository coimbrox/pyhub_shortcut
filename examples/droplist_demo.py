"""
Exemplo completo do PyHub DropList
Demonstra como criar menus interativos com atalhos + scroll
"""

import os
import sys
import time

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from PyQt5.QtWidgets import QApplication

    from pyhub_shortcut.droplist_manager import DropListAction, DropListManager
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Instale as dependências: pip install pyqt5 mouse")
    sys.exit(1)


def create_development_droplist():
    """Cria DropList para desenvolvimento"""
    return [
        DropListAction("🌐 GitHub", "start https://github.com", "🌐"),
        DropListAction("💻 VS Code", "code .", "💻"),
        DropListAction("📁 Explorer", "explorer .", "📁"),
        DropListAction("🔧 Terminal", "powershell", "🔧"),
        DropListAction("🐍 Python REPL", "python", "🐍"),
        DropListAction("📊 Task Manager", "taskmgr", "📊"),
    ]


def create_productivity_droplist():
    """Cria DropList para produtividade"""
    return [
        DropListAction("📧 Gmail", "start https://gmail.com", "📧"),
        DropListAction("📅 Calendar", "start https://calendar.google.com", "📅"),
        DropListAction("📝 Notion", "start https://notion.so", "📝"),
        DropListAction("🎵 Spotify", "start https://spotify.com", "🎵"),
        DropListAction("💬 WhatsApp", "start https://web.whatsapp.com", "💬"),
        DropListAction("🎮 Discord", "start https://discord.com", "🎮"),
    ]


def create_utilities_droplist():
    """Cria DropList para utilitários"""
    return [
        DropListAction("🧮 Calculadora", "calc", "🧮"),
        DropListAction("📋 Clipboard", "clipbrd", "📋"),
        DropListAction("🔍 Everything", "everything", "🔍"),
        DropListAction("📷 Screenshot", "snippingtool", "📷"),
        DropListAction("🎨 Paint", "mspaint", "🎨"),
        DropListAction("📝 Notepad", "notepad", "📝"),
    ]


def main():
    """Função principal do exemplo"""
    print("🎯 PyHub DropList - Exemplo Completo")
    print("=" * 50)

    # Inicializa PyQt
    app = QApplication(sys.argv)

    # Cria o gerenciador
    manager = DropListManager()

    # Registra os DropLists
    manager.register_droplist("ctrl", create_development_droplist(), "development")
    manager.register_droplist("alt", create_productivity_droplist(), "productivity")
    manager.register_droplist("shift", create_utilities_droplist(), "utilities")

    # Inicia o gerenciador
    manager.start()

    print("🚀 DropLists ativos!")
    print()
    print("📋 Como usar:")
    print("  🔹 Ctrl + Scroll  → Menu de Desenvolvimento")
    print("  🔹 Alt + Scroll   → Menu de Produtividade")
    print("  🔹 Shift + Scroll → Menu de Utilitários")
    print()
    print("💡 Dicas:")
    print("  • Mantenha a tecla pressionada e role o scroll")
    print("  • Use ↕️ scroll ou setas para navegar")
    print("  • Enter ou click para executar")
    print("  • Esc para fechar o menu")
    print()
    print("Pressione Ctrl+C para parar...")

    try:
        # Loop principal
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n🛑 Parando DropList Manager...")
        manager.stop()
        app.quit()
        print("✅ Finalizado!")


if __name__ == "__main__":
    main()

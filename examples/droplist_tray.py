"""
PyHub DropList com System Tray
Executa na bandeja do sistema com controles completos
"""

import os
import sys
import time
from pathlib import Path

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from PyQt5.QtCore import QTimer, pyqtSignal
    from PyQt5.QtGui import QIcon, QPixmap
    from PyQt5.QtWidgets import (
        QAction,
        QApplication,
        QMenu,
        QMessageBox,
        QSystemTrayIcon,
    )

    from pyhub_shortcut.droplist_manager import DropListAction, DropListManager
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Instale as dependências: pip install pyqt5 mouse keyboard")
    sys.exit(1)


class DropListTrayApp:
    """Aplicação do DropList com System Tray"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.manager = DropListManager()
        self.setup_tray()
        self.setup_droplists()

    def setup_tray(self):
        """Configura o ícone da bandeja"""
        # Verifica se o sistema suporta system tray
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                None, "System Tray", "System tray não está disponível neste sistema."
            )
            sys.exit(1)

        # Cria o ícone da bandeja
        self.tray_icon = QSystemTrayIcon(self.app)

        # Define o ícone (usa ícone padrão se não encontrar o customizado)
        icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
        if icon_path.exists():
            self.tray_icon.setIcon(QIcon(str(icon_path)))
        else:
            # Usa ícone padrão do sistema
            self.tray_icon.setIcon(
                self.app.style().standardIcon(self.app.style().SP_ComputerIcon)
            )

        # Cria o menu de contexto
        self.create_context_menu()

        # Define tooltip
        self.tray_icon.setToolTip(
            "PyHub DropList - Menus com Ctrl/Alt/Shift + Clique do Meio"
        )

        # Conecta eventos
        self.tray_icon.activated.connect(self.on_tray_activated)

        # Mostra o ícone
        self.tray_icon.show()

        # Mensagem de inicialização
        self.tray_icon.showMessage(
            "PyHub DropList Ativo! 🎯",
            "Use Ctrl/Alt/Shift + Clique do Meio para acessar menus",
            QSystemTrayIcon.Information,
            3000,
        )

    def create_context_menu(self):
        """Cria menu de contexto da bandeja"""
        menu = QMenu()

        # Ações principais
        status_action = QAction("✅ DropList Ativo", menu)
        status_action.setEnabled(False)
        menu.addAction(status_action)

        menu.addSeparator()

        # Informações de uso
        help_action = QAction("ℹ️ Como usar", menu)
        help_action.triggered.connect(self.show_help)
        menu.addAction(help_action)

        # Teste de DropLists
        test_action = QAction("🧪 Testar DropList", menu)
        test_action.triggered.connect(self.test_droplist)
        menu.addAction(test_action)

        menu.addSeparator()

        # Configurações
        config_action = QAction("⚙️ Configurações", menu)
        config_action.triggered.connect(self.show_config)
        menu.addAction(config_action)

        menu.addSeparator()

        # Sair
        quit_action = QAction("🚪 Sair", menu)
        quit_action.triggered.connect(self.quit_application)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)

    def setup_droplists(self):
        """Configura os DropLists padrão"""
        # DropList de Desenvolvimento
        dev_actions = [
            DropListAction("🌐 GitHub", "start https://github.com", "🌐"),
            DropListAction("💻 VS Code", "code .", "💻"),
            DropListAction("📁 Explorer", "explorer .", "📁"),
            DropListAction("🔧 Terminal", "powershell", "🔧"),
            DropListAction("🐍 Python REPL", "python", "🐍"),
            DropListAction("📊 Task Manager", "taskmgr", "📊"),
        ]

        # DropList de Produtividade
        productivity_actions = [
            DropListAction("📧 Gmail", "start https://gmail.com", "📧"),
            DropListAction("📅 Calendar", "start https://calendar.google.com", "📅"),
            DropListAction("📝 Notion", "start https://notion.so", "📝"),
            DropListAction("🎵 Spotify", "start https://spotify.com", "🎵"),
            DropListAction("💬 WhatsApp", "start https://web.whatsapp.com", "💬"),
            DropListAction("🎮 Discord", "start https://discord.com", "🎮"),
        ]

        # DropList de Utilitários
        utilities_actions = [
            DropListAction("🧮 Calculadora", "calc", "🧮"),
            DropListAction("📋 Clipboard", "clipbrd", "📋"),
            DropListAction("📷 Screenshot", "snippingtool", "📷"),
            DropListAction("🎨 Paint", "mspaint", "🎨"),
            DropListAction("📝 Notepad", "notepad", "📝"),
            DropListAction("🔍 Pesquisar", "start ms-search:", "🔍"),
        ]

        # Registra os DropLists
        self.manager.register_droplist("ctrl", dev_actions, "development")
        self.manager.register_droplist("alt", productivity_actions, "productivity")
        self.manager.register_droplist("shift", utilities_actions, "utilities")

        # Inicia o gerenciador
        self.manager.start()

    def on_tray_activated(self, reason):
        """Handler para cliques no ícone da bandeja"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_help()

    def show_help(self):
        """Mostra ajuda de uso"""
        help_text = """
🎯 PyHub DropList - Como Usar

📋 Controles Disponíveis:
• Ctrl + Clique do Meio  → Menu de Desenvolvimento
• Alt + Clique do Meio   → Menu de Produtividade  
• Shift + Clique do Meio → Menu de Utilitários

💡 Como Usar:
1. Pressione e MANTENHA a tecla (Ctrl/Alt/Shift)
2. Clique no botão do meio do mouse (scroll wheel)
3. Menu aparece na posição do cursor
4. Use scroll ou setas ↕️ para navegar
5. Enter ou click para executar
6. Esc para fechar

🎯 O DropList roda em background na bandeja.
Clique direito no ícone para mais opções!
        """

        QMessageBox.information(None, "PyHub DropList - Ajuda", help_text)

    def test_droplist(self):
        """Testa se os DropLists estão funcionando"""
        if self.manager.active:
            self.tray_icon.showMessage(
                "✅ DropList Funcionando!",
                "Use Ctrl/Alt/Shift + Clique do Meio para testar",
                QSystemTrayIcon.Information,
                2000,
            )
        else:
            self.tray_icon.showMessage(
                "❌ DropList Inativo",
                "Erro no gerenciador de DropLists",
                QSystemTrayIcon.Critical,
                2000,
            )

    def show_config(self):
        """Mostra configurações (placeholder)"""
        QMessageBox.information(
            None,
            "Configurações",
            "Configurações avançadas serão implementadas em breve!\n\n"
            "Por enquanto, edite o código para personalizar os menus.",
        )

    def quit_application(self):
        """Sai da aplicação"""
        self.manager.stop()
        self.tray_icon.hide()
        self.app.quit()

    def run(self):
        """Executa a aplicação"""
        # Configura timer para manter a aplicação viva
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)  # Apenas mantém vivo
        self.timer.start(1000)  # A cada segundo

        # Executa o loop principal
        return self.app.exec_()


def main():
    """Função principal"""
    try:
        app = DropListTrayApp()
        return app.run()
    except KeyboardInterrupt:
        print("\n🛑 Aplicação interrompida pelo usuário")
        return 0
    except Exception as e:
        print(f"❌ Erro na aplicação: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

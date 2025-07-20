# pyhub_shortcut/ui.py

import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ActionMenu(QWidget):
    def __init__(self, actions):
        super().__init__()
        self.setWindowTitle("PyHub Shortcut")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        for action in actions:
            btn = QPushButton(action["label"])
            btn.clicked.connect(lambda _, a=action: self.run_action(a))
            layout.addWidget(btn)

        self.setLayout(layout)

    def run_action(self, action):
        import subprocess

        subprocess.Popen(action["command"], shell=True)
        self.close()


class DropListMenu(QWidget):
    """
    Menu DropList moderno e responsivo
    Aparece na posição do cursor e permite navegação rápida
    """

    action_selected = pyqtSignal(object)
    menu_closed = pyqtSignal()

    def __init__(self, actions, position=(0, 0), on_select=None, on_close=None):
        super().__init__()
        self.actions = actions
        self.on_select = on_select
        self.on_close = on_close
        self.selected_index = 0

        self._setup_ui()
        self._setup_style()
        self._position_menu(position)

        # Auto-hide timer
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.close)
        self.hide_timer.setSingleShot(True)

    def _setup_ui(self):
        """Configura a interface do menu"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)

        # Título do menu
        title = QLabel("🎯 DropList Menu")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(title)

        # Lista de ações
        self.action_list = QListWidget()
        self.action_list.setMaximumHeight(200)

        for i, action in enumerate(self.actions):
            item = QListWidgetItem()

            # Widget customizado para cada item
            item_widget = self._create_action_item(action, i)
            item.setSizeHint(item_widget.sizeHint())

            self.action_list.addItem(item)
            self.action_list.setItemWidget(item, item_widget)

        # Seleciona o primeiro item
        if self.actions:
            self.action_list.setCurrentRow(0)

        layout.addWidget(self.action_list)

        # Dica de uso
        hint = QLabel(
            "↕️ Scroll para navegar • Enter/Click para executar • Esc para fechar"
        )
        hint.setAlignment(Qt.AlignCenter)
        hint.setFont(QFont("Segoe UI", 8))
        hint.setStyleSheet("color: #666; padding: 4px;")
        layout.addWidget(hint)

        self.setLayout(layout)

        # Conecta eventos
        self.action_list.itemDoubleClicked.connect(self._on_item_activated)

    def _create_action_item(self, action, index):
        """Cria widget customizado para item de ação"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)

        # Ícone/emoji
        icon_label = QLabel(action.icon or "⚡")
        icon_label.setFont(QFont("Segoe UI", 12))
        icon_label.setFixedWidth(24)
        layout.addWidget(icon_label)

        # Label da ação
        label = QLabel(action.label)
        label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(label)

        # Atalho (se houver)
        if hasattr(action, "hotkey") and action.hotkey:
            hotkey_label = QLabel(action.hotkey)
            hotkey_label.setFont(QFont("Segoe UI", 8))
            hotkey_label.setStyleSheet("color: #888; font-weight: bold;")
            layout.addWidget(hotkey_label)

        layout.addStretch()
        widget.setLayout(layout)

        return widget

    def _setup_style(self):
        """Aplica estilo moderno ao menu"""
        self.setStyleSheet(
            """
            DropListMenu {
                background-color: #2b2b2b;
                border: 2px solid #404040;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                border-radius: 4px;
                margin: 1px;
                padding: 2px;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """
        )

    def _position_menu(self, position):
        """Posiciona o menu próximo ao cursor"""
        x, y = position

        # Ajusta posição para não sair da tela
        screen = QApplication.primaryScreen().geometry()
        menu_size = self.sizeHint()

        if x + menu_size.width() > screen.width():
            x = screen.width() - menu_size.width() - 10
        if y + menu_size.height() > screen.height():
            y = screen.height() - menu_size.height() - 10

        self.move(max(10, x), max(10, y))

    def _on_item_activated(self, item):
        """Handler para quando um item é ativado"""
        row = self.action_list.row(item)
        if 0 <= row < len(self.actions):
            action = self.actions[row]
            if self.on_select:
                self.on_select(action)
            self.action_selected.emit(action)

    def keyPressEvent(self, event):
        """Handler para eventos de teclado"""
        key = event.key()

        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            current_row = self.action_list.currentRow()
            if 0 <= current_row < len(self.actions):
                action = self.actions[current_row]
                if self.on_select:
                    self.on_select(action)
                self.action_selected.emit(action)
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        """Handler para scroll do mouse"""
        delta = event.angleDelta().y()
        current_row = self.action_list.currentRow()

        if delta > 0:  # Scroll up
            new_row = max(0, current_row - 1)
        else:  # Scroll down
            new_row = min(len(self.actions) - 1, current_row + 1)

        self.action_list.setCurrentRow(new_row)

        # Reset hide timer
        self.hide_timer.start(3000)  # 3 segundos

    def show(self):
        """Mostra o menu e inicia timer de auto-hide"""
        super().show()
        self.activateWindow()
        self.raise_()
        self.setFocus()

        # Auto-hide após 5 segundos de inatividade
        self.hide_timer.start(5000)

    def closeEvent(self, event):
        """Handler para fechamento do menu"""
        if self.on_close:
            self.on_close()
        self.menu_closed.emit()
        super().closeEvent(event)


def show_menu(actions):
    app = QApplication(sys.argv)
    menu = ActionMenu(actions)
    menu.show()
    sys.exit(app.exec_())


def show_droplist(actions, position=(0, 0)):
    """Função utilitária para mostrar um DropList rapidamente"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    menu = DropListMenu(actions, position)
    menu.show()

    return menu

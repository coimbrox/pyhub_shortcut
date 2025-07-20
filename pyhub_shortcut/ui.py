# pyhub_shortcut/ui.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
import sys

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

def show_menu(actions):
    app = QApplication(sys.argv)
    menu = ActionMenu(actions)
    menu.show()
    sys.exit(app.exec_())

# build_exe.py
"""
Script para criar executável do PyHub DropList
"""

import os
import sys

import PyInstaller.__main__


def build_executable():
    """Constrói o executável usando PyInstaller"""

    # Configurações do PyInstaller
    args = [
        "examples/droplist_tray.py",  # Script principal com system tray
        "--onefile",  # Um único arquivo executável
        "--windowed",  # Sem console (para GUI)
        "--name=PyHubDropList",  # Nome do executável
        "--icon=assets/icon.ico",  # Ícone (se existir)
        "--add-data=pyhub_shortcut;pyhub_shortcut",  # Inclui o módulo
        "--add-data=assets;assets",  # Inclui assets (ícones)
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=keyboard",
        "--hidden-import=mouse",
        "--clean",  # Limpa cache antes de buildar
        "--noconfirm",  # Não pede confirmação
    ]

    # Remove o ícone se não existir
    if not os.path.exists("assets/icon.ico"):
        args = [arg for arg in args if not arg.startswith("--icon")]

    print("🔨 Construindo executável...")
    PyInstaller.__main__.run(args)
    print("✅ Executável criado em dist/PyHubDropList.exe")


if __name__ == "__main__":
    build_executable()

# build_simple.py
"""
Script de build simplificado para Windows
Sem emojis para evitar problemas de encoding
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"[INFO] {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"[OK] {description} concluido!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha em {description}:")
        if e.stdout:
            print(f"Saida: {e.stdout}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False


def clean_build():
    """Limpa arquivos de build anteriores"""
    print("[INFO] Limpando arquivos de build...")

    # Remove diretórios de build
    dirs_to_remove = ["build", "dist"]
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            if os.name == "nt":  # Windows
                subprocess.run(
                    f'rmdir /s /q "{dir_name}"', shell=True, capture_output=True
                )
            else:
                subprocess.run(f'rm -rf "{dir_name}"', shell=True, capture_output=True)

    # Remove arquivos .egg-info
    for item in Path(".").glob("*.egg-info"):
        if item.is_dir():
            if os.name == "nt":
                subprocess.run(f'rmdir /s /q "{item}"', shell=True, capture_output=True)
            else:
                subprocess.run(f'rm -rf "{item}"', shell=True, capture_output=True)


def build_wheel():
    """Constrói wheel para distribuição"""
    commands = [
        (
            "python -m pip install --upgrade build twine",
            "Instalando ferramentas de build",
        ),
        ("python -m build", "Construindo wheel e source distribution"),
    ]

    for command, description in commands:
        if not run_command(command, description):
            return False
    return True


def check_distribution():
    """Verifica a distribuição criada"""
    # Lista arquivos na pasta dist
    dist_path = Path("dist")
    if not dist_path.exists():
        print("[ERRO] Pasta dist nao encontrada")
        return False

    # Encontra arquivos .whl e .tar.gz
    files = list(dist_path.glob("*.whl")) + list(dist_path.glob("*.tar.gz"))
    if not files:
        print("[ERRO] Nenhum arquivo de distribuicao encontrado")
        return False

    # Verifica cada arquivo
    for file in files:
        if not run_command(
            f'python -m twine check "{file}"', f"Verificando {file.name}"
        ):
            return False

    return True


def build_executable():
    """Constrói executável usando PyInstaller"""
    # Primeiro verifica se PyInstaller está instalado
    if not run_command("python -m pip install pyinstaller", "Instalando PyInstaller"):
        return False

    # Comando PyInstaller
    cmd = [
        "python",
        "-m",
        "PyInstaller",
        "examples/droplist_demo.py",
        "--onefile",
        "--name=PyHubDropList",
        "--add-data=pyhub_shortcut;pyhub_shortcut",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=keyboard",
        "--hidden-import=mouse",
        "--clean",
        "--noconfirm",
    ]

    command_str = " ".join(cmd)
    return run_command(command_str, "Construindo executavel")


def main():
    """Função principal de build"""
    print("PyHub DropList - Build Script Simplificado")
    print("=" * 50)

    # Verifica se estamos no diretório correto
    if not os.path.exists("setup.py"):
        print("[ERRO] Execute este script no diretorio raiz do projeto")
        sys.exit(1)

    # Menu de opções
    print("\nEscolha uma opcao:")
    print("1. Build para PyPI (wheel + source)")
    print("2. Build executavel (PyInstaller)")
    print("3. Build completo (ambos)")
    print("4. Apenas limpar cache")

    choice = input("\nEscolha (1-4): ").strip()

    # Limpa sempre antes de começar
    clean_build()

    success = False

    if choice == "1":
        success = build_wheel() and check_distribution()
    elif choice == "2":
        success = build_executable()
    elif choice == "3":
        success = build_wheel() and check_distribution() and build_executable()
    elif choice == "4":
        print("[OK] Cache limpo!")
        return
    else:
        print("[ERRO] Opcao invalida")
        return

    if success:
        print("\n[SUCCESS] Build concluido com sucesso!")
        print("\nArquivos gerados:")

        # Lista arquivos na pasta dist
        dist_path = Path("dist")
        if dist_path.exists():
            for file in dist_path.iterdir():
                if file.is_file():
                    size = file.stat().st_size / 1024 / 1024  # MB
                    print(f"  {file.name} ({size:.1f} MB)")

        print("\nProximos passos:")
        if choice in ["1", "3"]:
            print("  Para testar: pip install dist/*.whl")
            print("  Para publicar: python -m twine upload dist/*")
        if choice in ["2", "3"]:
            print("  Executavel em: dist/PyHubDropList.exe")
    else:
        print("\n[FAILED] Build falhou! Verifique os erros acima.")


if __name__ == "__main__":
    main()

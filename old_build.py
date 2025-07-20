# build.py
"""
Script de build para distribuição do PyHub DropList
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"Executando: {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"OK: {description} concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERRO em {description}:")
        print(f"Saída: {e.stdout}")
        print(f"Erro: {e.stderr}")
        return False


def clean_build():
    """Limpa arquivos de build anteriores"""
    print("Limpando arquivos de build...")

    # Remove diretórios de build
    dirs_to_remove = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_remove:
        if os.name == "nt":  # Windows
            subprocess.run(f"rmdir /s /q {pattern} 2>nul", shell=True)
        else:  # Linux/Mac
            subprocess.run(f"rm -rf {pattern}", shell=True)


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


def build_executable():
    """Constrói executável usando PyInstaller"""
    commands = [
        ("python -m pip install pyinstaller", "Instalando PyInstaller"),
        ("python build_exe.py", "Construindo executável"),
    ]

    for command, description in commands:
        if not run_command(command, description):
            return False
    return True


def check_distribution():
    """Verifica a distribuição criada"""
    if not run_command("python -m twine check dist/*", "Verificando distribuição"):
        return False
    return True


def main():
    """Função principal de build"""
    print("PyHub DropList - Build Script")
    print("=" * 40)

    # Verifica se estamos no diretório correto
    if not os.path.exists("setup.py"):
        print("ERRO: execute este script no diretório raiz do projeto")
        sys.exit(1)

    # Menu de opções
    print("\nEscolha uma opção:")
    print("1. Build para PyPI (wheel + source)")
    print("2. Build executável (PyInstaller)")
    print("3. Build completo (ambos)")
    print("4. Apenas limpar cache")

    choice = input("\nEscolha (1-4): ").strip()

    # Limpa sempre antes de começar
    clean_build()

    if choice == "1":
        success = build_wheel() and check_distribution()
    elif choice == "2":
        success = build_executable()
    elif choice == "3":
        success = build_wheel() and check_distribution() and build_executable()
    elif choice == "4":
        print("Cache limpo!")
        return
    else:
        print("Opção inválida")
        return

    if success:
        print("\nBuild concluído com sucesso!")
        print("\nArquivos gerados:")

        # Lista arquivos na pasta dist
        dist_path = Path("dist")
        if dist_path.exists():
            for file in dist_path.iterdir():
                size = file.stat().st_size / 1024 / 1024  # MB
                print(f"  {file.name} ({size:.1f} MB)")

        print("\nPróximos passos:")
        if choice in ["1", "3"]:
            print("  Para testar: pip install dist/*.whl")
            print("  Para publicar: python -m twine upload dist/*")
        if choice in ["2", "3"]:
            print("  Executável em: dist/PyHubDropList.exe")
    else:
        print("\nBuild falhou! Verifique os erros acima.")


if __name__ == "__main__":
    main()

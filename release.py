# release.py
"""
Script completo de release para PyHub DropList
Gera executavel e prepara para publicacao no PyPI
"""

import os
import subprocess
import sys
from pathlib import Path


def print_step(step, description):
    print(f"\n[{step}] {description}")
    print("-" * 50)


def run_command(command, description, critical=True):
    """Executa comando e retorna True/False"""
    print(f"Executando: {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"OK: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERRO: {description}")
        if e.stdout:
            print(f"Saida: {e.stdout}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        if critical:
            print("Processo interrompido devido a erro critico.")
            sys.exit(1)
        return False


def clean_build():
    """Limpa builds anteriores"""
    print("Limpando arquivos anteriores...")
    dirs_to_clean = ["dist", "build", "*.egg-info"]

    for pattern in dirs_to_clean:
        if "*" in pattern:
            # Para patterns com wildcard
            for item in Path(".").glob(pattern):
                if item.is_dir():
                    subprocess.run(
                        f'Remove-Item -Recurse -Force "{item}" -ErrorAction SilentlyContinue',
                        shell=True,
                    )
        else:
            # Para diretórios específicos
            if Path(pattern).exists():
                subprocess.run(
                    f'Remove-Item -Recurse -Force "{pattern}" -ErrorAction SilentlyContinue',
                    shell=True,
                )


def main():
    print("PyHub DropList - Script de Release Completo")
    print("=" * 60)

    # Verifica pré-requisitos
    if not Path("setup.py").exists():
        print("ERRO: Execute este script no diretorio raiz do projeto")
        sys.exit(1)

    print_step("1", "Preparação")
    clean_build()

    print_step("2", "Instalando dependências de build")
    run_command(
        "python -m pip install --upgrade build twine pyinstaller",
        "Instalando ferramentas",
    )

    print_step("3", "Construindo pacotes para PyPI")
    run_command(
        "python setup.py sdist bdist_wheel", "Criando wheel e source distribution"
    )

    print_step("4", "Verificando qualidade dos pacotes")
    run_command("python -m twine check dist/*", "Verificando pacotes", critical=False)

    print_step("5", "Construindo executável")
    # Comando PyInstaller
    pyinstaller_cmd = [
        "python",
        "-m",
        "PyInstaller",
        "examples/droplist_demo.py",
        "--onefile",
        "--windowed",
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

    command_str = " ".join(pyinstaller_cmd)
    run_command(command_str, "Criando executavel", critical=False)

    print_step("6", "Testando instalação local")
    # Testa a instalação do wheel
    wheel_files = list(Path("dist").glob("*.whl"))
    if wheel_files:
        wheel_file = wheel_files[0]
        run_command(
            f'python -m pip install "{wheel_file}" --force-reinstall --quiet',
            "Testando instalacao",
            critical=False,
        )
        run_command(
            "python -c \"import pyhub_shortcut; print(f'Versao: {pyhub_shortcut.__version__}')\"",
            "Verificando import",
            critical=False,
        )

    print_step("7", "Resumo dos arquivos gerados")

    # Lista arquivos da dist
    dist_path = Path("dist")
    if dist_path.exists():
        print("\nArquivos para PyPI:")
        total_size = 0
        for file in dist_path.glob("*.whl"):
            size = file.stat().st_size / 1024  # KB
            total_size += size
            print(f"  wheel: {file.name} ({size:.1f} KB)")

        for file in dist_path.glob("*.tar.gz"):
            size = file.stat().st_size / 1024  # KB
            total_size += size
            print(f"  source: {file.name} ({size:.1f} KB)")

        # Verifica executável
        exe_file = dist_path / "PyHubDropList.exe"
        if exe_file.exists():
            exe_size = exe_file.stat().st_size / 1024 / 1024  # MB
            print(f"\nExecutavel:")
            print(f"  PyHubDropList.exe ({exe_size:.1f} MB)")
        else:
            print("\nExecutavel: NAO CRIADO (verifique erros acima)")

        print(f"\nTamanho total dos pacotes: {total_size:.1f} KB")

    print_step("8", "Próximos passos")
    print("Para publicar no PyPI:")
    print("  1. Teste primeiro no TestPyPI:")
    print("     python -m twine upload --repository testpypi dist/*")
    print("  2. Depois publique no PyPI oficial:")
    print("     python -m twine upload dist/*")
    print("")
    print("Para distribuir executavel:")
    print("  1. Teste o executavel: dist/PyHubDropList.exe")
    print("  2. Crie release no GitHub com o executavel anexado")
    print("")
    print("Configuracao necessaria:")
    print("  1. Crie conta no PyPI: https://pypi.org/account/register/")
    print("  2. Configure arquivo .pypirc com tokens de API")
    print(
        "  3. Ou use: python -m twine upload --username __token__ --password <seu-token>"
    )


if __name__ == "__main__":
    main()

# publish_helper.py
"""
Script auxiliar para publicacao no PyPI
Evita o problema do executavel no upload
"""

import subprocess
import sys
from pathlib import Path


def print_banner():
    print("=" * 60)
    print("PyHub DropList - Publicacao no PyPI")
    print("=" * 60)


def check_files():
    """Verifica se os arquivos necessarios existem"""
    dist_path = Path("dist")
    if not dist_path.exists():
        print("ERRO: Pasta dist nao encontrada. Execute o build primeiro.")
        return False

    wheel_files = list(dist_path.glob("*.whl"))
    tar_files = list(dist_path.glob("*.tar.gz"))

    if not wheel_files or not tar_files:
        print("ERRO: Arquivos de distribuicao nao encontrados.")
        print("Execute: python setup.py sdist bdist_wheel")
        return False

    print("Arquivos encontrados:")
    for file in wheel_files + tar_files:
        size = file.stat().st_size / 1024  # KB
        print(f"  {file.name} ({size:.1f} KB)")

    return True


def upload_to_testpypi():
    """Faz upload para TestPyPI"""
    print("\nFazendo upload para TestPyPI...")
    print("Sera solicitado seu token de API do TestPyPI")
    print("Obtenha em: https://test.pypi.org/manage/account/token/")

    cmd = "python -m twine upload --repository testpypi dist/*.whl dist/*.tar.gz"
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print("\nSUCESSO! Upload para TestPyPI concluido!")
        print("Verifique em: https://test.pypi.org/project/pyhub-droplist/")
        return True
    else:
        print("\nERRO no upload para TestPyPI!")
        return False


def upload_to_pypi():
    """Faz upload para PyPI oficial"""
    print("\nFazendo upload para PyPI OFICIAL...")
    print("ATENCAO: Isso publicara o pacote oficialmente!")
    print("Sera solicitado seu token de API do PyPI")
    print("Obtenha em: https://pypi.org/manage/account/token/")

    confirm = input("\nTem certeza? Digite 'SIM' para continuar: ")
    if confirm != "SIM":
        print("Upload cancelado.")
        return False

    cmd = "python -m twine upload dist/*.whl dist/*.tar.gz"
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print("\nSUCESSO! Upload para PyPI concluido!")
        print("Verifique em: https://pypi.org/project/pyhub-droplist/")
        print("Usuarios podem instalar com: pip install pyhub-droplist")
        return True
    else:
        print("\nERRO no upload para PyPI!")
        return False


def test_installation():
    """Testa a instalacao do TestPyPI"""
    print("\nTestando instalacao do TestPyPI...")
    cmd = "pip install --index-url https://test.pypi.org/simple/ pyhub-droplist --force-reinstall"
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print("Instalacao bem-sucedida!")
        # Testa import
        test_cmd = "python -c \"import pyhub_shortcut; print(f'Versao: {pyhub_shortcut.__version__}')\""
        subprocess.run(test_cmd, shell=True)
    else:
        print("Erro na instalacao!")


def main():
    print_banner()

    if not check_files():
        sys.exit(1)

    print("\nEscolha uma opcao:")
    print("1. Upload para TestPyPI (recomendado primeiro)")
    print("2. Upload para PyPI oficial")
    print("3. Testar instalacao do TestPyPI")
    print("4. Sair")

    choice = input("\nOpcao (1-4): ").strip()

    if choice == "1":
        if upload_to_testpypi():
            print("\nProximo passo: Teste a instalacao (opcao 3)")

    elif choice == "2":
        upload_to_pypi()

    elif choice == "3":
        test_installation()

    elif choice == "4":
        print("Saindo...")

    else:
        print("Opcao invalida!")


if __name__ == "__main__":
    main()

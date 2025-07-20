# publish.py
"""
Script para publicar o PyHub DropList no PyPI
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Executa comando e retorna sucesso/falha"""
    print(f"🔨 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} concluído!")
        if result.stdout:
            print(f"📋 Saída: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}:")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False


def check_prerequisites():
    """Verifica se tudo está pronto para publicação"""
    print("🔍 Verificando pré-requisitos...")

    # Verifica arquivos obrigatórios
    required_files = ["setup.py", "README.md", "LICENSE", "pyproject.toml"]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print(f"❌ Arquivos obrigatórios não encontrados: {missing_files}")
        return False

    # Verifica se tem conta no PyPI
    pypirc_path = Path.home() / ".pypirc"
    if not pypirc_path.exists():
        print("⚠️ Arquivo .pypirc não encontrado")
        print("💡 Você precisará configurar suas credenciais do PyPI")

        response = input("Continuar mesmo assim? (y/n): ").lower()
        if response != "y":
            return False

    print("✅ Pré-requisitos verificados!")
    return True


def build_package():
    """Constrói o pacote"""
    commands = [
        ("python -m pip install --upgrade build twine", "Instalando ferramentas"),
        ("python -m build --clean", "Construindo pacote"),
        ("python -m twine check dist/*", "Verificando pacote"),
    ]

    for command, description in commands:
        if not run_command(command, description):
            return False
    return True


def publish_to_testpypi():
    """Publica no TestPyPI primeiro"""
    print("\n🧪 Publicando no TestPyPI...")
    command = "python -m twine upload --repository testpypi dist/*"
    return run_command(command, "Upload para TestPyPI")


def publish_to_pypi():
    """Publica no PyPI oficial"""
    print("\n🚀 Publicando no PyPI...")
    command = "python -m twine upload dist/*"
    return run_command(command, "Upload para PyPI")


def test_installation():
    """Testa a instalação do pacote"""
    print("\n🧪 Testando instalação...")
    commands = [
        (
            "pip install --index-url https://test.pypi.org/simple/ pyhub-droplist",
            "Testando instalação do TestPyPI",
        ),
    ]

    for command, description in commands:
        run_command(command, description)  # Não falha se der erro


def main():
    """Função principal"""
    print("🚀 PyHub DropList - Publicação no PyPI")
    print("=" * 50)

    if not check_prerequisites():
        sys.exit(1)

    print("\nEscolha uma opção:")
    print("1. 🧪 Publicar no TestPyPI (recomendado primeiro)")
    print("2. 🚀 Publicar no PyPI oficial")
    print("3. 🔄 Build + TestPyPI + PyPI (completo)")
    print("4. 📦 Apenas build (sem publicar)")

    choice = input("\nEscolha (1-4): ").strip()

    # Sempre faz build primeiro
    print("\n" + "=" * 30)
    if not build_package():
        print("💥 Falha no build!")
        sys.exit(1)

    if choice == "1":
        success = publish_to_testpypi()
        if success:
            print("\n✅ Publicado no TestPyPI!")
            print("🔗 Verifique em: https://test.pypi.org/project/pyhub-droplist/")
            test_installation()

    elif choice == "2":
        response = input("\n⚠️ Tem certeza? Isso publicará no PyPI oficial (y/n): ")
        if response.lower() == "y":
            success = publish_to_pypi()
            if success:
                print("\n🎉 Publicado no PyPI!")
                print("🔗 Verifique em: https://pypi.org/project/pyhub-droplist/")

    elif choice == "3":
        # TestPyPI primeiro
        if publish_to_testpypi():
            print("\n✅ TestPyPI ok!")
            response = input("Continuar para PyPI oficial? (y/n): ")
            if response.lower() == "y":
                if publish_to_pypi():
                    print("\n🎉 Publicação completa!")

    elif choice == "4":
        print("\n📦 Build concluído! Arquivos em dist/")

    else:
        print("❌ Opção inválida")

    # Mostra arquivos gerados
    print("\n📁 Arquivos gerados:")
    dist_path = Path("dist")
    if dist_path.exists():
        for file in dist_path.iterdir():
            size = file.stat().st_size / 1024  # KB
            print(f"  📄 {file.name} ({size:.1f} KB)")


if __name__ == "__main__":
    main()

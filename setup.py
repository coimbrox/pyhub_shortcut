import os

from setuptools import find_packages, setup


# Lê o README para descrição longa
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    return "PyHub DropList - Menus interativos com atalhos de teclado + scroll"


setup(
    name="pyhub-droplist-coimbrox",
    version="0.1.1",
    author="Gabriel Coimbra",
    author_email="seu-email@exemplo.com",  # Adicione seu email
    description="Biblioteca Python para criar menus DropList interativos com atalhos de teclado + scroll do mouse",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/coimbrox/pyhub-shortcut",
    packages=find_packages(),
    install_requires=[
        "keyboard",
        "mouse",
        "pyqt5",  # Ou "pyqt6", dependendo da versão que estiver usando
    ],
    entry_points={
        "console_scripts": [
            "pyhub-shortcut=pyhub_shortcut.cli:main",
            "pyhub-droplist=pyhub_shortcut.droplist_manager:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    keywords="shortcuts hotkeys automation productivity",
)

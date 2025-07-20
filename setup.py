from setuptools import find_packages, setup

setup(
    name="pyhub-shortcut",
    version="0.1.0",
    author="Gabriel Coimbra",
    description="Biblioteca Python para criar atalhos globais com menus interativos e execução de ações",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/coimbrox/pyhub-shortcut",  # Atualiza com seu GitHub real
    packages=find_packages(),
    install_requires=[
        "keyboard",
        "pyqt5",  # Ou "pyqt6", dependendo da versão que estiver usando
    ],
    entry_points={
        "console_scripts": [
            "pyhub-shortcut=pyhub_shortcut.cli:main",
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

# 🚀 Guia de Distribuição - PyHub DropList

Este guia mostra como criar executáveis e publicar no PyPI.

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Conta no PyPI** (criar em https://pypi.org/account/register/)
3. **Git** configurado
4. **Dependências** instaladas

```bash
pip install -r requirements.txt
```

## 🏗️ Processo de Build

### Opção 1: Build Automático
```bash
python build.py
```
Escolha uma das opções:
1. 📦 Build para PyPI (wheel + source)
2. 🖥️ Build executável (PyInstaller) 
3. 🔄 Build completo (ambos)
4. 🧹 Apenas limpar cache

### Opção 2: Build Manual

#### Para PyPI:
```bash
# Instala ferramentas
pip install build twine

# Limpa builds anteriores
rm -rf build dist *.egg-info

# Constrói pacote
python -m build

# Verifica pacote
python -m twine check dist/*
```

#### Para Executável:
```bash
# Instala PyInstaller
pip install pyinstaller

# Constrói executável
python build_exe.py
```

## 📤 Publicação no PyPI

### Configuração Inicial

1. **Crie arquivo .pypirc** (Windows: `%USERPROFILE%\.pypirc`):
```ini
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # Seu token do PyPI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # Seu token do TestPyPI
```

2. **Obtenha tokens de API**:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

### Publicação Automática
```bash
python publish.py
```

### Publicação Manual

#### 1. Teste no TestPyPI primeiro:
```bash
python -m twine upload --repository testpypi dist/*
```

#### 2. Teste a instalação:
```bash
pip install --index-url https://test.pypi.org/simple/ pyhub-droplist
```

#### 3. Publique no PyPI oficial:
```bash
python -m twine upload dist/*
```

## 🎯 Executável Standalone

O executável será criado em `dist/PyHubDropList.exe` e pode ser distribuído independentemente.

### Características:
- ✅ Não precisa Python instalado
- ✅ Todas dependências incluídas
- ✅ Arquivo único (--onefile)
- ⚠️ Arquivo grande (~50-100MB)
- ⚠️ Inicialização mais lenta

## 🔄 Fluxo Completo de Release

1. **Desenvolvimento**:
   ```bash
   git add .
   git commit -m "feat: nova funcionalidade"
   git push origin main
   ```

2. **Testes**:
   ```bash
   python examples/droplist_demo.py
   ```

3. **Build**:
   ```bash
   python build.py  # Escolha opção 3 (completo)
   ```

4. **Teste local**:
   ```bash
   pip install dist/*.whl
   pyhub-droplist --help
   ```

5. **Publicação**:
   ```bash
   python publish.py  # Escolha opção 1 (TestPyPI primeiro)
   ```

6. **Verificação**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ pyhub-droplist
   ```

7. **Release oficial**:
   ```bash
   python publish.py  # Escolha opção 2 (PyPI)
   ```

8. **Tag do Git**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

## 📊 Verificações Finais

- [ ] ✅ Todos os testes passam
- [ ] ✅ README.md atualizado
- [ ] ✅ Versão incrementada em setup.py
- [ ] ✅ CHANGELOG.md criado
- [ ] ✅ Build funciona sem erros
- [ ] ✅ Executável roda corretamente
- [ ] ✅ Instalação do PyPI funciona
- [ ] ✅ Documentação completa

## 🐛 Troubleshooting

### Problema: "Module not found"
```bash
pip install --upgrade setuptools wheel build
```

### Problema: "Authentication failed"
- Verifique tokens do PyPI
- Use tokens, não senhas
- Confira arquivo .pypirc

### Problema: "Package already exists"
- Incremente versão em setup.py
- Use sufixos como 0.1.0a1, 0.1.0b1

### Problema: "Executável não roda"
- Teste em máquina limpa (sem Python)
- Verifique antivírus
- Use --debug para logs

## 📞 Suporte

- 🐛 Issues: https://github.com/coimbrox/pyhub-shortcut/issues
- 📧 Email: seu-email@exemplo.com
- 💬 Discussões: GitHub Discussions

# 🧩 PyHub Shortcut

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Biblioteca Python moderna para criar **atalhos globais** com **menus interativos** e **execução automatizada de ações**. Perfeito para aumentar sua produtividade e automatizar tarefas repetitivas!

## ✨ Features

- 🎯 **Atalhos globais personalizáveis** (ex: `Ctrl+1`, `Ctrl+Shift+Y`)
- ⚙️ **Configuração flexível** via JSON
- 🖥️ **Interface CLI completa** para gerenciamento
- 🔄 **Recarregamento dinâmico** de configurações
- 📝 **Logging integrado** para debugging
- 🛡️ **Tratamento robusto de erros**
- 🎮 **Modo interativo e daemon**

## 🚀 Instalação Rápida

```bash
# Clona o repositório
git clone https://github.com/coimbrox/pyhub-shortcut.git
cd pyhub-shortcut

# Instala em modo desenvolvimento
pip install -e .
```

## 📖 Uso Básico

### Via Linha de Comando

```bash
# Lista ações configuradas
pyhub-shortcut --list

# Adiciona nova ação
pyhub-shortcut --add "Abrir YouTube" "start https://youtube.com" "ctrl+shift+y"

# Executa em modo daemon
pyhub-shortcut --daemon

# Modo interativo
pyhub-shortcut
```

### Via Python

```python
from pyhub_shortcut import ImprovedShortcutManager, ConfigManager

# Configuração básica
manager = ImprovedShortcutManager()
manager.start()

# Com configuração personalizada
config = ConfigManager()
config.add_action("Terminal", "powershell", "ctrl+shift+t")

manager = ImprovedShortcutManager(config)
manager.start()

# Não esqueça de parar
manager.stop()
```

## 🎛️ Configuração

As configurações são salvas em `~/.pyhub_shortcut/config.json`:

```json
{
  "actions": [
    {
      "label": "Abrir Google",
      "command": "start https://www.google.com",
      "hotkey": "ctrl+1"
    },
    {
      "label": "VS Code",
      "command": "code .",
      "hotkey": "ctrl+2"
    }
  ]
}
```

## 📁 Estrutura do Projeto

```
pyhub_shortcut/
├── __init__.py          # API principal
├── config.py            # Configurações básicas (legacy)
├── config_manager.py    # Gerenciador moderno de configurações
├── core.py              # Core básico (legacy)
├── core_improved.py     # Core melhorado com logging
├── ui.py                # Interface PyQt
└── cli.py               # Interface de linha de comando
```

## 🔧 Exemplos Avançados

```bash
# Exemplo básico
python examples/demo.py

# Exemplo avançado com configuração personalizada
python examples/demo_advanced.py --advanced
```

## 🛠️ Dependências

- `keyboard` - Para captura de atalhos globais
- `PyQt5` - Para interface gráfica (opcional)

## 📋 To-Do / Roadmap

- [ ] Suporte a atalhos com scroll do mouse
- [ ] Interface gráfica para gerenciamento
- [ ] Suporte a scripts Python como ações
- [ ] Profiles de configuração
- [ ] Integração com bandejas do sistema
- [ ] Suporte multiplataforma (Linux/macOS)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 👨‍💻 Autor

**Gabriel Coimbra**
- GitHub: [@coimbrox](https://github.com/coimbrox)

---

⭐ **Gostou do projeto? Deixe uma estrela!**

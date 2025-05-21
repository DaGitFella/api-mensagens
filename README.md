# 📡 API de Mensagens

Este repositório contém a API de mensagens, desenvolvida com Python e gerenciada com [Poetry](https://python-poetry.org/), focando em um ambiente isolado e organizado para dependências.

## 🚀 Requisitos

- Python (a versão será gerenciada pelo Poetry)
- [Poetry](https://python-poetry.org/)
- `pipx` (recomendado para instalações locais)
- [Task](https://taskfile.dev/) para gerenciamento de comandos

## 🛠️ Instalação

### ✅ 1. Instalando o Poetry

- **Se estiver no Codespaces**, instale diretamente com:

```bash
pip install poetry
```

- **Se estiver rodando localmente**, **não instale o poetry diretamente com `pip` fora de um ambiente isolado**. Em vez disso, use o `pipx`:

```bash
pip install pipx
pipx install poetry
```

> ⚠️ **Importante:** Não instale o `poetry` globalmente com `pip` fora de um ambiente virtual. Isso pode causar conflitos com dependências de outros pacotes Python no sistema.

---

### ✅ 2. Configurando o Ambiente

Com o `poetry` já instalado:

```bash
poetry python install 3.13          # Baixa e instala o Python 3.13 (caso necessário)
poetry self add poetry-plugin-shell # Adiciona o plugin do shell para o poetry
poetry shell                        # Entra no shell do poetry
poetry install                      # Instala todas as dependências do projeto
```

---

## ▶️ Rodando a API

Entre na pasta do projeto:

```bash
task run
```

---

## 📌 Observações

- Sempre utilize ambientes virtuais isolados ao trabalhar com o `poetry`.
- O uso do `pipx` garante que o `poetry` não conflite com outros pacotes Python no sistema global.

---

## 📄 Licença

Este projeto está licenciado sob os termos da GPL3.

---

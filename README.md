'''

# 📡 API de Mensagens

Este repositório contém a API de mensagens, desenvolvida com Python e gerenciada com [Poetry](https://python-poetry.org/), focando em um ambiente isolado e organizado para dependências.

## 🚀 Requisitos

* Python (a versão será gerenciada pelo Poetry)
* [Poetry](https://python-poetry.org/)
* `pipx` (recomendado para instalações locais)
* [Task](https://taskfile.dev/) para gerenciamento de comandos

'''
## 🛠️ Instalação

### ✅ 1. Instalando o `pipx`

O `pipx` permite instalar ferramentas Python globais de forma isolada. Veja como instalá-lo de acordo com o seu sistema operacional:

#### 🔵 Windows (recomendado: via [Scoop](https://scoop.sh))

1. Instale o [Scoop](https://scoop.sh/) (caso ainda não tenha):

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

2. Adicione o repositório `main` e instale o `pipx`:

```powershell
scoop install python
scoop install pipx
pipx ensurepath
```

> Após executar `pipx ensurepath`, **reinicie o terminal** para que o caminho seja reconhecido.

---

#### 🟢 Distros baseadas em Arch (Arch, Manjaro, EndeavourOS...)

```bash
sudo pacman -S pipx
pipx ensurepath
```

---

#### 🔴 Distros baseadas em Debian (Debian, Ubuntu, Linux Mint...)

```bash
sudo apt update
sudo apt install pipx python3-venv
pipx ensurepath
```

> ⚠️ Caso o `pipx` não esteja disponível diretamente no seu repositório:
>
> ```bash
> python3 -m pip install --user pipx
> python3 -m pipx ensurepath
> ```

---

### ✅ 2. Instalando o Poetry

Com o `pipx` instalado corretamente, instale o `poetry`:

```bash
pipx install poetry
```

> ⚠️ **Importante:** Não instale o `poetry` com `pip` diretamente fora de um ambiente isolado. Isso pode causar conflitos com dependências de outros pacotes Python no sistema.

---

### ✅ 3. Configurando o Ambiente

Com o `poetry` já instalado:

```bash
poetry python install 3.13          # Baixa e instala o Python 3.13 (caso necessário)
poetry self add poetry-plugin-shell # Adiciona o plugin do shell para o poetry
poetry shell                        # Entra no shell do poetry
poetry install                      # Instala todas as dependências do projeto
```

---

## ▶️ Rodando a API

Antes de iniciar a aplicação, é necessário aplicar as migrações do banco de dados com o Alembic:

```bash
alembic upgrade head
```

Em seguida, rode a aplicação com:

```bash
task run
```

---

## 📌 Observações

* Sempre utilize ambientes virtuais isolados ao trabalhar com o `poetry`.
* O uso do `pipx` garante que o `poetry` não conflite com outros pacotes Python no sistema global.
* Certifique-se de que o banco de dados esteja acessível e configurado corretamente no arquivo `.env` antes de rodar `alembic upgrade head`.

---

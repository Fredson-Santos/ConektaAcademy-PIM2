# 🎓 ConektaAcademy

**Sistema de Gerenciamento Acadêmico Inteligente**

Sistema completo de gestão acadêmica com interface web moderna (Streamlit) e modo terminal (CLI), desenvolvido para gerenciamento de alunos, professores, disciplinas, turmas e cursos.

[Ver Diagramas UML](diagramas/) · [Documentação Completa](Documentação/MDs/) · [Reportar Erro](https://github.com) · [Solicitar Features](https://github.com)

---

## 📑 Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
   - [Objetivos do Projeto](#objetivos-do-projeto)
   - [Funcionalidades](#funcionalidades)
   - [Tecnologias Utilizadas](#tecnologias-utilizadas)
2. [Começando](#começando)
   - [Pré-requisitos](#pré-requisitos)
   - [Instalação](#instalação)
3. [Tutorial do Sistema](#tutorial-do-sistema)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Documentação](#documentação)
6. [Licença](#licença)
7. [Contato](#contato)

---

## 📖 Sobre o Projeto

O **ConektaAcademy** é um sistema de gerenciamento acadêmico completo desenvolvido para facilitar a administração de instituições de ensino. O sistema oferece interfaces intuitivas para três perfis de usuário distintos: **Alunos**, **Professores** e **Secretaria**, cada um com funcionalidades específicas e personalizadas.

Com foco em modernização e eficiência, o projeto integra funcionalidades de gestão acadêmica, geração de relatórios, sistema de chat de ajuda com IA, e suporte multiplataforma (Web e Terminal).

### Objetivos do Projeto

**Objetivo Geral:** Desenvolver um sistema completo de gerenciamento acadêmico que centralize todas as operações educacionais, desde o cadastro de usuários até a geração de relatórios e boletins.

**Objetivos Específicos:**

- ✅ Gerenciamento completo de usuários (alunos, professores, secretaria)
- ✅ Controle de turmas, disciplinas e cursos
- ✅ Sistema de notas e avaliações (NP1, NP2, PIM)
- ✅ Controle de presença e frequência
- ✅ Geração de relatórios em PDF e CSV
- ✅ Interface web moderna com Streamlit
- ✅ Modo terminal para operações rápidas
- ✅ Sistema de chat de ajuda integrado
- ✅ Criptografia de senhas (SHA-256)
- ✅ Sessão persistente ("Lembrar-me")
- ✅ Vinculação automática de aluno ao curso ao vincular à turma
- ✅ Relatórios completos com download de boletim em PDF

### Funcionalidades

#### 👥 Para Alunos

- 📘 **Visualização de Notas** - Consulta de notas por disciplina (NP1, NP2, PIM) com cálculo automático de média e indicadores visuais (verde/vermelho)
- 📅 **Controle de Presença** - Acompanhamento de frequência e taxa de presença
- 📖 **Cronograma** - Visualização do cronograma de aulas
- 📔 **Bloco de Anotações** - Espaço pessoal para anotações
- 📄 **Relatórios Completos** - Aba dedicada com relatórios detalhados de notas e faltas
- 📥 **Download de Boletim** - Geração e download de boletim em PDF
- 💬 **Chat de Ajuda** - Suporte via chatbot integrado

#### 👨‍🏫 Para Professores

- 📚 **Gerenciamento de Disciplinas** - Visualização e gestão das disciplinas vinculadas
- 📘 **Lançamento de Notas** - Cadastro e atualização de notas dos alunos por disciplina (NP1, NP2, PIM)
- 📅 **Registro de Presença** - Controle de presença dos alunos por disciplina
- 📊 **Relatórios de Desempenho** - Geração de relatórios detalhados por aluno e disciplina
- 📖 **Cronograma** - Gerenciamento do cronograma de aulas
- 🗒️ **Bloco de Anotações** - Espaço para anotações pessoais
- 📥 **Download de Relatórios** - Exportação de relatórios em PDF
- 💬 **Chat de Ajuda** - Suporte via chatbot integrado

#### 🗂️ Para Secretaria

- 👥 **Gerenciamento de Usuários** - CRUD completo de alunos, professores e secretaria com validações
- 📚 **Gerenciamento de Turmas** - Criação, listagem, exclusão e vinculação de turmas a cursos
- 📖 **Gerenciamento de Disciplinas** - CRUD completo de disciplinas com vinculação a cursos e turmas
- 🎓 **Gerenciamento de Cursos** - Criação e gestão de cursos
- 🔗 **Vinculações Inteligentes** - Vinculação de professores, alunos e disciplinas a turmas e cursos (aluno vinculado à turma é automaticamente vinculado ao curso da turma)
- 🔑 **Reset de Senhas** - Redefinição de senhas de usuários
- 📄 **Relatórios Avançados** - Geração de relatórios de alunos, turmas, disciplinas e cursos
- 📥 **Exportação** - Exportação de relatórios em CSV e PDF
- 💬 **Chat de Ajuda** - Suporte via chatbot integrado

### Tecnologias Utilizadas

**Frontend:**
- 🐍 **Python 3.8+** - Linguagem principal
- 🚀 **Streamlit** - Framework web para interface gráfica
- 📊 **Pandas** - Manipulação e análise de dados
- 🎨 **HTML/CSS** - Estilização e layout

**Backend:**
- 🗄️ **SQLite** - Banco de dados relacional
- 🔐 **Hashlib (SHA-256)** - Criptografia de senhas
- 📄 **ReportLab** - Geração de relatórios em PDF
- 💬 **Requests** - Integração com API de chat

**Arquitetura:**
- 📁 **Modular** - Separação entre interface web e terminal
- 🔄 **Reutilizável** - Módulos compartilhados entre interfaces
- 🛡️ **Seguro** - Validação de dados e proteção contra SQL injection

---

## 🚀 Começando

### Pré-requisitos

**Para executar o projeto:**

- **Python** 3.8 ou superior
- **pip** (gerenciador de pacotes Python)
- **Navegador moderno** (para interface web)

**Dependências opcionais:**

- **ReportLab** - Para geração de PDFs (opcional, mas recomendado)
  ```bash
  pip install reportlab
  ```

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/Sistema-Acad-mico-PIM-II-IA.git
   cd Sistema-Acad-mico-PIM-II-IA
   ```

2. **Crie um ambiente virtual (recomendado):**

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **O banco de dados será criado automaticamente** na primeira execução do sistema.

### Executando a Aplicação

#### Modo Interface Web (Streamlit)

**Windows:**
```bash
run.bat
```
ou
```bash
streamlit run interface/app.py
```

**Linux/Mac:**
```bash
./run.sh
```
ou
```bash
streamlit run interface/app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

#### Modo Terminal (CLI)

```bash
python terminal/main.py
```

---

## 📚 Tutorial do Sistema

### Primeiro Acesso

1. **Execute o sistema** usando `run.bat` (Windows) ou `run.sh` (Linux/Mac)
2. **Crie sua conta** através da aba "Cadastro" na tela de login
3. **Faça login** com suas credenciais

> **Nota:** O sistema permite cadastro de novos usuários diretamente pela interface. Você pode criar contas de Aluno, Professor ou Secretaria através da tela de cadastro.

### Fluxo de Uso

#### Para Alunos
1. Faça login com sua matrícula ou email
2. Acesse a aba **Notas** para visualizar suas notas por disciplina
3. Consulte a aba **Presenças** para acompanhar sua frequência
4. Visualize o **Cronograma** de aulas
5. Use o **Bloco do Aluno** para fazer anotações pessoais
6. Acesse **Relatórios** para gerar e baixar seu boletim em PDF

#### Para Professores
1. Faça login com seu email ou matrícula
2. Acesse **Minhas Disciplinas** para ver suas disciplinas vinculadas
3. Use a sub-aba **Lançar Notas** para cadastrar notas dos alunos
4. Registre presenças na sub-aba **Presença**
5. Gere relatórios de desempenho dos alunos
6. Gerencie o cronograma de aulas

#### Para Secretaria
1. Faça login com suas credenciais
2. Acesse **Gerenciamento de Usuários** para cadastrar novos usuários
3. Crie e gerencie **Turmas**, **Disciplinas** e **Cursos**
4. Vincule professores, alunos e disciplinas conforme necessário
5. Gere relatórios completos do sistema
6. Exporte dados em CSV ou PDF

---

## 📁 Estrutura do Projeto

```
Sistema-Acad-mico-PIM-II-IA/
│
├── 📱 interface/                    # Interface Web (Streamlit)
│   ├── __init__.py
│   ├── app.py                      # Aplicação principal Streamlit
│   └── telas/
│       ├── __init__.py
│       ├── login.py                # Tela de login e cadastro
│       ├── area_aluno.py            # Área do aluno
│       ├── area_professor.py       # Área do professor
│       └── area_secretaria.py      # Área da secretaria
│
├── 💻 terminal/                     # Modo Terminal (CLI)
│   ├── __init__.py
│   ├── main.py                     # Executar: python terminal/main.py
│   └── menus/
│       ├── __init__.py
│       ├── aluno_menu.py           # Menu do aluno
│       ├── professor_menu.py       # Menu do professor
│       └── secretaria_menu.py      # Menu da secretaria
│
├── 🔧 sistema/                      # Módulos Compartilhados
│   ├── __init__.py
│   ├── database.py                 # Gerenciamento do banco de dados
│   ├── funcoes.py                  # Funções de negócio
│   ├── classes.py                  # Classes do sistema
│   ├── chat.py                     # Integração ChatBot
│   └── relatorios.py               # Geração de relatórios
│
├── 📊 diagramas/                    # Diagramas UML (PlantUML)
│   ├── README.md                   # Documentação dos diagramas
│   ├── 01_caso_uso.puml            # Diagrama de casos de uso
│   ├── 02_classes.puml             # Diagrama de classes
│   ├── 03_sequencia_professor_lanca_nota.puml
│   ├── 04_sequencia_secretaria_cria_turma.puml
│   ├── 05_sequencia_aluno_consulta_notas.puml
│   └── 06_rede_lan.puml            # Diagrama de rede LAN
│
├── 📖 Documentação/                 # Documentação do projeto
│   ├── MDs/                        # Arquivos Markdown de documentação
│   │   ├── MANUAL_USUARIO.md
│   │   ├── README_INTERFACE.md
│   │   ├── GUIA_RAPIDO.md
│   │   ├── INSTALACAO.md
│   │   ├── EXEMPLOS_USO.md
│   │   └── ... (outros documentos)
│   └── ... (outros arquivos de documentação)
│
├── 🤖 chatbot/                      # Integração com chatbot
│   ├── system prompt.txt
│   └── teste.py
│
├── 📋 requirements.txt              # Dependências do projeto
├── 🪟 run.bat                       # Script de execução (Windows)
├── 🐧 run.sh                        # Script de execução (Linux/Mac)
├── 📄 README.md                     # Este arquivo
│
└── 💾 sistema_academico.db          # Banco de dados SQLite (criado automaticamente)
```

---

## 📚 Documentação

### Diagramas UML

O projeto inclui diagramas UML completos em formato PlantUML na pasta [`diagramas/`](diagramas/):

- 📊 **Diagrama de Casos de Uso** - Todos os casos de uso do sistema
- 🏗️ **Diagrama de Classes** - Estrutura de classes e relacionamentos
- 🔄 **Diagramas de Sequência** - Fluxos de processos principais:
  - Professor lança nota
  - Secretaria cria turma
  - Aluno consulta notas
- 🌐 **Diagrama de Rede LAN** - Arquitetura de rede do sistema

Para visualizar os diagramas, consulte o [README dos Diagramas](diagramas/README.md).

### Manual do Usuário

Para um guia completo de uso do sistema, consulte o **[Manual do Usuário](Documentação/MDs/MANUAL_USUARIO.md)**, que inclui:

- ✅ Guia passo a passo para cada tipo de usuário
- ✅ Instruções detalhadas de todas as funcionalidades
- ✅ Perguntas frequentes (FAQ)
- ✅ Troubleshooting e soluções de problemas
- ✅ Dicas e melhores práticas

### Outros Documentos

A documentação completa está disponível na pasta [`Documentação/MDs/`](Documentação/MDs/):

- **[README_INTERFACE.md](Documentação/MDs/README_INTERFACE.md)** - Documentação técnica da interface
- **[GUIA_RAPIDO.md](Documentação/MDs/GUIA_RAPIDO.md)** - Guia rápido de instalação
- **[EXEMPLOS_USO.md](Documentação/MDs/EXEMPLOS_USO.md)** - Exemplos práticos de uso
- **[ESTRUTURA_PROJETO.md](Documentação/MDs/ESTRUTURA_PROJETO.md)** - Estrutura detalhada do projeto

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError: No module named 'reportlab'"
```bash
pip install reportlab
```
> **Nota:** O reportlab é opcional. O sistema funciona sem ele, mas sem geração de PDFs. A funcionalidade de PDF será desabilitada automaticamente.

### Erro: "ModuleNotFoundError: No module named 'sistema'"
Certifique-se de estar executando o comando a partir da raiz do projeto:
```bash
cd Sistema-Acad-mico-PIM-II-IA
streamlit run interface/app.py
```

### Erro: "Connection refused" ou problemas com banco de dados
O banco de dados SQLite é criado automaticamente. Se houver problemas:
1. Delete o arquivo `sistema_academico.db` (se existir)
2. Execute o sistema novamente - o banco será recriado automaticamente

### A aplicação não abre no navegador
Acesse manualmente: `http://localhost:8501`

### Porta já em uso
```bash
streamlit run interface/app.py --server.port 8502
```

### Erro ao executar no Windows
Certifique-se de usar o script `run.bat` ou execute:
```powershell
python -m streamlit run interface/app.py
```

### Erro ao executar no Linux/Mac
Certifique-se de usar o script `run.sh` (com permissão de execução) ou execute:
```bash
chmod +x run.sh
./run.sh
```

---

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais. 

© Conekta - Todos os direitos reservados

---

## 📞 Contato

**ConektaAcademy** - Sistema de Gerenciamento Acadêmico

- 📖 **Documentação Completa:** [Documentação/MDs/](Documentação/MDs/)
- 📊 **Diagramas UML:** [diagramas/](diagramas/)
- 🎓 **Versão:** 1.0
- 📅 **Última Atualização:** 2024

---

<div align="center">

**Desenvolvido com ❤️ usando Python e Streamlit**

![Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-Conekta-green?style=for-the-badge)

**[⬆ Voltar ao topo](#-conektaacademy)**

</div>

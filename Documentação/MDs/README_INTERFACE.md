# 🎓 ConektaAcademy - Interface Gráfica com Streamlit

![Status](https://img.shields.io/badge/status-production-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)
![License](https://img.shields.io/badge/license-MIT-green)

> **Interface web moderna e intuitiva para gerenciamento acadêmico** construída com Streamlit e Python.

---

## 📸 Visão Geral

Uma aplicação completa de gerenciamento acadêmico com interface gráfica responsiva, suportando **3 tipos de usuários** (Aluno, Professor, Secretaria) com funcionalidades específicas para cada um.

### ✨ Destaques

- 🎯 **Interface Intuitiva** - Design moderno com Streamlit
- 🔐 **Autenticação Segura** - Login com validação
- 📱 **Responsivo** - Funciona em desktop, tablet e mobile
- 🚀 **Rápido** - Desenvolvido com Streamlit (sem complexidade)
- 💾 **Integrado** - Usa banco de dados SQLite existente
- 📚 **Bem Documentado** - 8 guias de documentação
- ⚡ **Fácil de Usar** - 3 passos para começar

---

## 🎯 Funcionalidades

### 👥 Para Alunos
```
✅ Visualizar notas (NP1, NP2, PIM) por disciplina
✅ Consultar presenças e taxa de frequência
✅ Calcular média automática
✅ Ver cronograma de aulas
✅ Fazer anotações pessoais
✅ Relatórios completos de notas e faltas
✅ Download de boletim em PDF
```

### 👨‍🏫 Para Professores
```
✅ Gerenciar disciplinas vinculadas
✅ Lançar notas de alunos por disciplina
✅ Registrar e atualizar presença
✅ Gerar relatórios de desempenho
✅ Gerenciar cronograma de aulas
✅ Fazer anotações
✅ Download de relatórios em PDF
```

### 🗂️ Para Secretaria
```
✅ Gerenciar usuários (CRUD)
✅ Gerenciar turmas (CRUD)
✅ Gerenciar disciplinas (CRUD)
✅ Gerenciar cursos (CRUD)
✅ Vincular professores a turmas
✅ Vincular alunos a turmas
✅ Vincular disciplinas a turmas e cursos
✅ Resetar senhas
✅ Gerar relatórios de alunos, turmas, disciplinas e cursos
✅ Exportar relatórios em CSV e PDF
```

---

## 🚀 Início Rápido

### Windows
```powershell
# 1. Clone/extraia o projeto
cd Sistema-Acad-mico-PIM-II-IA

# 2. Crie ambiente virtual
python -m venv venv
.\venv\Scripts\Activate

# 3. Instale e execute
pip install -r requirements.txt
streamlit run interface/app.py
```

### macOS/Linux
```bash
# 1. Clone/extraia o projeto
cd Sistema-Acad-mico-PIM-II-IA

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale e execute
pip install -r requirements.txt
streamlit run interface/app.py
```

### Executável Direto
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

---

## 📋 Requisitos

- **Python** 3.8+
- **pip** (gerenciador de pacotes)
- **2GB RAM** mínimo
- **50MB** espaço em disco
- Navegador moderno

---

## 📦 Instalação

### 1. Clonar/Extrair Projeto
```bash
git clone https://github.com/duprp/Sistema-Acad-mico-PIM-II-IA.git
cd Sistema-Acad-mico-PIM-II-IA
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\Activate  # Windows
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar Aplicação
```bash
streamlit run interface/app.py
```

A aplicação abrirá em `http://localhost:8501`

---

## 🧪 Testando a Aplicação

### Credenciais de Teste

> **Nota:** O sistema permite criar novos usuários diretamente pela interface através da aba "Cadastro" na tela de login. Não é necessário popular o banco manualmente - o banco de dados é criado automaticamente na primeira execução.

### Cenários de Teste
1. **Login com aluno** → Ver notas → Ver presença
2. **Login com professor** → Lançar nota → Gerar relatório
3. **Login com secretaria** → Criar usuário → Gerenciar turma

---

## 📚 Documentação

| Documento | Propósito | Tempo |
|-----------|-----------|-------|
| **GUIA_RAPIDO.md** | ⚡ Começar em 3 passos | 5 min |
| **INSTALACAO.md** | 📥 Setup passo a passo | 20 min |
| **EXEMPLOS_USO.md** | 💡 Cenários de teste | 30 min |
| **ESTRUTURA_INTERFACE.md** | 🎨 Design e wireframes | 15 min |
| **PREVIEW_VISUAL.md** | 🖼️ Screenshots ASCII | 10 min |
| **RESUMO_IMPLEMENTACAO.md** | 📋 O que foi criado | 10 min |
| **INDICE.md** | 📑 Índice completo | 5 min |

**👉 [Leia a documentação completa](INDICE.md)**

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────┐
│   Streamlit Web Interface       │
│  (interface/app.py)              │
│  └─ interface/telas/            │
│     ├─ login.py                 │
│     ├─ area_aluno.py            │
│     ├─ area_professor.py        │
│     └─ area_secretaria.py       │
└─────────────┬───────────────────┘
              │
┌─────────────▼───────────────────┐
│  Backend (Sistema Acadêmico)    │
│  ├─ sistema/funcoes.py          │
│  ├─ sistema/classes.py          │
│  ├─ sistema/database.py         │
│  ├─ sistema/chat.py             │
│  ├─ sistema/relatorios.py       │
│  └─ terminal/ (CLI)             │
└─────────────┬───────────────────┘
              │
┌─────────────▼───────────────────┐
│  SQLite Database                │
│  sistema_academico.db           │
└─────────────────────────────────┘
```

---

## 🎨 Interface

### Temas
- **Primária:** Roxo (#667eea)
- **Secundária:** Roxo Escuro (#764ba2)
- **Fundo:** Branco (#ffffff)
- **Status:** Verde (sucesso), Vermelho (erro)

### Componentes
- ✅ Login/Cadastro
- ✅ Dashboards personalizados
- ✅ Abas (Tabs)
- ✅ Tabelas interativas
- ✅ Cards de métrica
- ✅ Formulários validados
- ✅ Sidebar com informações

---

## 🔧 Estrutura do Projeto

```
Sistema-Acad-mico-PIM-II-IA/
├── interface/                   ⭐ INTERFACE WEB
│   ├── app.py                  # Arquivo principal Streamlit
│   └── telas/
│       ├── login.py
│       ├── area_aluno.py
│       ├── area_professor.py
│       └── area_secretaria.py
│
├── terminal/                    💻 MODO TERMINAL
│   ├── main.py                 # Executar: python terminal/main.py
│   └── menus/
│       ├── aluno_menu.py
│       ├── professor_menu.py
│       └── secretaria_menu.py
│
├── sistema/                     🔧 MÓDULOS COMPARTILHADOS
│   ├── database.py             # Gerenciamento do banco de dados
│   ├── funcoes.py              # Funções de negócio
│   ├── classes.py              # Classes do sistema
│   ├── chat.py                 # Integração ChatBot
│   └── relatorios.py           # Geração de relatórios
│
├── 📊 diagramas/                # Diagramas UML (PlantUML)
│   ├── README.md
│   ├── 01_caso_uso.puml
│   ├── 02_classes.puml
│   └── ... (outros diagramas)
│
├── 📖 Documentação/            # Documentação do projeto
│   └── MDs/                    # Arquivos Markdown
│       ├── README.md
│       ├── README_INTERFACE.md
│       ├── GUIA_RAPIDO.md
│       └── ... (outros documentos)
│
├── requirements.txt            # Dependências do projeto
├── run.bat                     # Script de execução (Windows)
├── run.sh                      # Script de execução (Linux/Mac)
│
└── 📊 DADOS
    └── sistema_academico.db    # Banco de dados (criado automaticamente)
```

---

## 🔄 Fluxo de Autenticação

```
Tela Inicial
    ↓
┌─────────────────────┐
│ Login    │ Cadastro │
└─────────────────────┘
    ↓
Validar Credenciais
    ↓
Dashboard Personalizado
├─ Aluno
├─ Professor
└─ Secretaria
```

---

## 📊 Tecnologias

| Tecnologia | Uso | Versão |
|-----------|-----|--------|
| **Python** | Linguagem | 3.8+ |
| **Streamlit** | Framework Web | 1.28+ |
| **Pandas** | Manipulação de dados | 2.0+ |
| **SQLite3** | Banco de dados | 3.x |

---

## 🐛 Troubleshooting

### Erro: Python não encontrado
```bash
# Instale Python de https://www.python.org
# Ou use seu gerenciador de pacotes
```

### Erro: Streamlit não instalado
```bash
pip install streamlit --upgrade
```

### Erro: Porta em uso
```bash
streamlit run interface/app.py --server.port 8502
```

### Erro: Banco de dados corrompido
```bash
# Delete e será recriado
rm sistema_academico.db
streamlit run interface/app.py
```

### Erro: ModuleNotFoundError: No module named 'reportlab'
```bash
pip install reportlab
```
> **Nota:** O reportlab é opcional. O sistema funciona sem ele, mas sem geração de PDFs.

**📖 [Veja guia completo de troubleshooting](INSTALACAO.md#troubleshooting-de-teste)**

---

## 🚀 Deploy

### Streamlit Cloud (Recomendado)
1. Push código para GitHub
2. Acesse https://share.streamlit.io
3. Conecte repositório
4. Deploy com 1 clique

### Servidor Próprio
1. Configure servidor Linux
2. Instale Python e dependências
3. Configure NGINX como proxy reverso
4. Use systemd para rodar como serviço

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run interface/app.py
```

---

## 📈 Estatísticas

- 📄 **Módulos organizados** (interface/telas/)
- 🔧 **50+** funcionalidades
- 📚 **8** documentos
- ⏱️ **~2h** tempo total de leitura
- 🎯 **100%** funcionalidade implementada

---

## 🎓 Fluxos de Uso

### Para Aluno
1. Login com matrícula
2. Dashboard → Notas
3. Ver frequência
4. Consultar cronograma
5. Fazer anotações

### Para Professor
1. Login com email
2. Dashboard → Lançar Notas
3. Registrar presença
4. Gerar relatório
5. Gerenciar cronograma

### Para Secretaria
1. Login com email
2. Dashboard → Usuários
3. Criar/Gerenciar usuários
4. Gerenciar turmas e disciplinas
5. Vincular recursos

---

## 🔐 Segurança

✅ **Autenticação**
- Login com email/matrícula
- Senhas criptografadas com SHA-256
- Validação de senha
- Sessão por usuário
- Opção "Lembrar-me" para sessão persistente

✅ **Validação**
- Entrada validada
- Tipos de dados verificados
- SQL injection prevenida

✅ **Privacidade**
- Dados isolados por usuário
- Sem dados sensíveis em URLs
- Logout seguro

---

## 💡 Melhorias Futuras

### Curto Prazo
- [x] Exportar relatórios em PDF
- [ ] Gráficos de desempenho
- [ ] Notificações por email
- [ ] Recuperação de senha

### Médio Prazo
- [ ] Dashboard com KPIs
- [ ] Integração com Google Classroom
- [ ] API REST
- [ ] App mobile

### Longo Prazo
- [ ] IA para recomendações
- [ ] Portal dos pais
- [ ] Sistema de pagamento
- [ ] Integração com SIS

---

## 🤝 Contribuindo

Sinta-se à vontade para:
- 🐛 Reportar bugs
- 💡 Sugerir features
- 📝 Melhorar documentação
- 🔧 Fazer pull requests

---

## 📞 Suporte

- 📖 **Documentação:** [INDICE.md](INDICE.md)
- 💬 **Issues:** GitHub Issues
- 📧 **Email:** Veja repositório

---

## 📄 Licença

Este projeto está sob licença MIT. Veja LICENSE para mais detalhes.

---

## 👨‍💻 Desenvolvido com

- ❤️ Python
- 🚀 Streamlit
- 💪 Paixão por educação

---

## 🎉 Começe Agora!

```bash
# 1. Clone
git clone https://github.com/duprp/Sistema-Acad-mico-PIM-II-IA.git

# 2. Instale
cd Sistema-Acad-mico-PIM-II-IA
pip install -r requirements.txt

# 3. Execute
streamlit run interface/app.py
```

**👉 [Leia o GUIA_RAPIDO.md para mais detalhes](GUIA_RAPIDO.md)**

---

<div align="center">

**🎓 ConektaAcademy | Interface Gráfica com Streamlit**

© Conekta - Todos os direitos reservados

![Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-red?style=for-the-badge)
![Love](https://img.shields.io/badge/Made%20with-❤️-pink?style=for-the-badge)

**[⬆ voltar ao topo](#-sistema-acadêmico---interface-gráfica-com-streamlit)**

</div>

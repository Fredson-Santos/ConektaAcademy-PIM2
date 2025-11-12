# 🚀 Guia Rápido - Sistema Acadêmico Streamlit

## ⚡ Iniciar em 3 passos

### Windows (PowerShell)
```powershell
# 1. Abra PowerShell na pasta do projeto

# 2. Crie ambiente virtual
python -m venv venv
.\venv\Scripts\Activate

# 3. Instale e execute
pip install -r requirements.txt
streamlit run app.py
```

### Windows (Simples)
```
Duplo clique em: run.bat
```

### macOS / Linux
```bash
# 1. Abra Terminal na pasta do projeto

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale e execute
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux (Simples)
```bash
chmod +x run.sh
./run.sh
```

## 📱 Interface

Após executar, a aplicação abrirá em `http://localhost:8501`

### Layout
- **Sidebar (esquerda):** Informações do usuário e logout
- **Conteúdo principal:** Funcionalidades por perfil
- **Abas:** Organize recursos por categoria

## 👤 Tipos de Usuários

### 1️⃣ ALUNO
**O que pode fazer:**
- 📘 Ver suas notas em cada matéria
- 📅 Consultar presença e frequência
- 📖 Visualizar cronograma de aulas
- 📔 Fazer anotações pessoais

**Como cadastrar:**
- Email: qualquer email (não use @prof ou @sec)
- Matrícula: código do aluno
- Exemplo: `aluno@email.com` / Matrícula: `2024001`

### 2️⃣ PROFESSOR
**O que pode fazer:**
- 📘 Lançar notas dos alunos
- 📅 Registrar presença
- 📄 Gerar relatórios
- 📖 Gerenciar cronograma
- 🗒️ Anotações pessoais

**Como cadastrar:**
- Email: **deve conter @prof** + disciplina
  - `usuario@profmatematica`
  - `usuario@profportugues`
  - `usuario@profciencias`
  - `usuario@profgeografia`
- Matrícula: deixe em branco
- Exemplo: `prof.silva@profmatematica` / Matrícula: vazio

### 3️⃣ SECRETARIA
**O que pode fazer:**
- 👥 Gerenciar todos os usuários
- 📚 Criar e gerenciar turmas
- 📖 Criar e gerenciar disciplinas
- 🔗 Vincular professores a turmas

**Como cadastrar:**
- Email: **deve conter @sec**
  - `usuario@sec` ou `secretaria@sec`
- Matrícula: pode deixar em branco
- Exemplo: `maria@sec` / Matrícula: vazio

## 🔑 Sistema de Autenticação

### Login
```
Email ou Matrícula: usuario@email.com (ou matrícula)
Senha: sua_senha_123
```

### Cadastro
1. Clique em "Cadastro" na tela de login
2. Preencha os dados
3. Escolha o tipo baseado no email
4. Clique em "Cadastrar"

⚠️ **Importante:** O tipo de usuário é detectado automaticamente pelo email!

## 🎯 Fluxo Comum

### Para Aluno
1. Login → Dashboard do Aluno
2. Ver Notas → Selecionar matéria → Ver NP1, NP2, PIM
3. Ver Presenças → Consultar frequência
4. Ver Cronograma → Ver aulas agendadas
5. Bloco → Fazer anotações

### Para Professor
1. Login → Dashboard do Professor
2. Lançar Notas → Preencher matrícula, avaliação e nota
3. Presença → Registrar frequência do aluno
4. Relatórios → Gerar relatório do aluno
5. Cronograma → Ver/adicionar aulas
6. Bloco → Fazer anotações

### Para Secretaria
1. Login → Dashboard da Secretaria
2. Usuários → Listar, criar, editar ou deletar usuários
3. Turmas → Gerenciar turmas
4. Disciplinas → Gerenciar disciplinas
5. Vincular → Associar professores a turmas

## 📊 Dados Salvos

### Banco de Dados
- Arquivo: `sistema_academico.db`
- Tipo: SQLite
- Salva automaticamente

### Anotações
- Aluno: `bloco_MATRICULA.txt`
- Professor: `bloco_professor.txt`
- Local: Pasta do projeto

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| "streamlit não encontrado" | Execute: `pip install streamlit` |
| "ModuleNotFoundError" | Execute: `pip install -r requirements.txt` |
| Aplicação não abre | Abra manualmente `http://localhost:8501` |
| Erro de banco de dados | Delete `sistema_academico.db` e reinicie |
| Página não atualiza | Pressione F5 no navegador |

## 💡 Dicas Profissionais

✅ **Faça:**
- Fazer backup do `sistema_academico.db`
- Resetar senha regularmente
- Verificar presenças frequentemente

❌ **Não faça:**
- Deletar arquivos `.db` durante execução
- Compartilhar senhas
- Executar múltiplas instâncias no mesmo banco

## 🔗 Links Úteis

- Streamlit: https://streamlit.io
- Python: https://www.python.org
- SQLite: https://www.sqlite.org
- Pandas: https://pandas.pydata.org

## 📞 Suporte

**Erros comuns:**
1. Verifique a versão do Python (3.8+)
2. Reinstale dependências: `pip install -r requirements.txt --force-reinstall`
3. Limpe cache: Delete pasta `__pycache__`

**Mais informações:**
- Veja `README.md` para documentação completa
- Consulte código em `sistema/` para entender a lógica

---

**Boa sorte! 🎓**

# 📥 Instalação Passo a Passo

## 🖥️ Requisitos Mínimos

- **Windows 10+, macOS 10.13+, ou Linux**
- **Python 3.8+**
- **2GB de RAM**
- **50MB de espaço em disco**
- **Conexão com a internet (primeira execução)**

---

## ⚙️ Instalação do Python

### Windows

1. **Acesse:** https://www.python.org/downloads/
2. **Baixe:** "Download Python 3.x.x" (versão mais recente)
3. **Execute o instalador**
4. ⚠️ **IMPORTANTE:** Marque "Add Python to PATH"
5. Clique "Install Now"
6. Aguarde a instalação

**Verificar instalação:**
```powershell
python --version
```

### macOS

1. **Via Homebrew (recomendado):**
```bash
brew install python3
```

2. **Ou acesse:** https://www.python.org/downloads/
3. **Baixe:** macOS installer
4. Execute o instalador

**Verificar instalação:**
```bash
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Verificar instalação:**
```bash
python3 --version
pip3 --version
```

---

## 📂 Setup do Projeto

### Passo 1: Clone ou Extraia o Projeto

**Opção A: Via Git**
```bash
git clone https://github.com/duprp/Sistema-Acad-mico-PIM-II-IA.git
cd Sistema-Acad-mico-PIM-II-IA
```

**Opção B: Arquivo ZIP**
1. Baixe o arquivo ZIP
2. Extraia em um local da sua escolha
3. Abra Terminal/PowerShell na pasta extraída

### Passo 2: Criar Ambiente Virtual

O ambiente virtual isola as dependências do projeto.

#### Windows (PowerShell)

```powershell
# Criar ambiente
python -m venv venv

# Ativar ambiente
.\venv\Scripts\Activate
```

Você verá `(venv)` no seu terminal.

#### Windows (CMD)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### macOS/Linux

```bash
# Criar ambiente
python3 -m venv venv

# Ativar ambiente
source venv/bin/activate
```

Você verá `(venv)` no seu terminal.

### Passo 3: Instalar Dependências

Com o ambiente ativo, execute:

```bash
pip install -r requirements.txt
```

**Conteúdo de requirements.txt:**
```
streamlit>=1.28.0
pandas>=2.0.0
requests>=2.31.0
```

Se tiver problemas, tente:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Verificar Instalação

```bash
streamlit --version
```

Você deve ver a versão do Streamlit.

---

## 🚀 Executar a Aplicação

### Opção 1: Linha de Comando (Recomendado)

Com o ambiente ativo:

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

### Opção 2: Script Executável

#### Windows
```
Duplo clique em: run.bat
```

#### macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

### Opção 3: Manual no Navegador

Se não abrir automaticamente:
1. Abra seu navegador
2. Acesse: `http://localhost:8501`

---

## ✅ Checklist Pós-Instalação

- [ ] Python instalado e acessível
- [ ] Pasta do projeto extraída/clonada
- [ ] Ambiente virtual criado
- [ ] Ambiente virtual ativado
- [ ] `requirements.txt` instalado
- [ ] `app.py` executa sem erros
- [ ] Aplicação abre no navegador
- [ ] Pode fazer login/cadastro

---

## 🔍 Troubleshooting

### ❌ Erro: "python: command not found"

**Solução:**
```bash
# Tente:
python3 --version

# Se funcionar, use python3 em todos os comandos
python3 -m venv venv
```

### ❌ Erro: "Permission denied" (Linux/Mac)

**Solução:**
```bash
chmod +x run.sh
./run.sh
```

### ❌ Erro: "No module named streamlit"

**Solução 1:**
Certifique-se de que o ambiente está **ativado** (veja o `(venv)` no terminal)

**Solução 2:**
Reinstale:
```bash
pip install -r requirements.txt --force-reinstall
```

### ❌ Erro: "Address already in use"

**Solução:**
Outra aplicação está usando a porta 8501. Execute:
```bash
streamlit run app.py --server.port 8502
```

### ❌ Erro: "ModuleNotFoundError: No module named 'sistema'"

**Solução:**
Certifique-se de que:
1. Você está na pasta raiz do projeto
2. A pasta `sistema/` existe
3. O arquivo `app.py` está no mesmo nível que `sistema/`

### ❌ Aplicação lenta ou trava

**Solução:**
```bash
# Limpe cache
rm -rf __pycache__
rm -rf .streamlit/cache

# Reinicie
streamlit run app.py
```

### ❌ Erro ao acessar banco de dados

**Solução:**
```bash
# Delete banco existente
rm sistema_academico.db

# Será recriado automaticamente
streamlit run app.py
```

---

## 📊 Verificação de Ambiente

Execute este comando para verificar tudo:

```python
python -c "
import sys
import streamlit
import pandas
import sqlite3
print('✅ Python:', sys.version)
print('✅ Streamlit:', streamlit.__version__)
print('✅ Pandas:', pandas.__version__)
print('✅ SQLite:', sqlite3.version)
print('✅ Tudo pronto!')
"
```

---

## 🔐 Segurança Pós-Instalação

1. **Altere as senhas padrão:**
   - Se houver usuários de teste
   - Recrie credenciais seguras

2. **Proteça o banco de dados:**
   ```bash
   # Certifique-se que sistema_academico.db tem permissões apropriadas
   chmod 600 sistema_academico.db  # Linux/Mac
   ```

3. **Faça backup:**
   ```bash
   # Cópia do banco de dados
   cp sistema_academico.db sistema_academico.backup.db
   ```

---

## 📚 Próximos Passos

1. ✅ Instalação completa
2. 📖 Leia `GUIA_RAPIDO.md`
3. 🧪 Consulte `EXEMPLOS_USO.md`
4. 🎨 Veja `ESTRUTURA_INTERFACE.md`
5. 📚 Leia `README.md` completo

---

## 🎓 Ambientes Comuns

### Escola/Instituição
```
1. Instale em servidor compartilhado
2. Configure IP fixo
3. Compartilhe URL com usuários
4. Implemente HTTPS
```

### Pessoal/Testes
```
1. Instale localmente
2. Execute em http://localhost:8501
3. Compartilhe via ngrok se necessário
```

### Produção
```
1. Use Streamlit Cloud: https://streamlit.io/cloud
2. Ou deploy em servidor (AWS, Heroku, etc)
3. Configure banco de dados remoto
4. Implemente backups automáticos
```

---

## 📞 Suporte

Se tiver problemas:

1. Verifique a **versão do Python**: `python --version`
2. Verifique **permissões de pasta**
3. Limpe **cache e cache do navegador**
4. Teste em **navegador diferente**
5. Consulte **log do terminal**

---

**Pronto para começar! 🚀**

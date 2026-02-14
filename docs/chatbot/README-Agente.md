# 🤖 Agente de Suporte - Fluxo N8N

Este documento descreve a arquitetura e o funcionamento do **Agente de Suporte** do Sistema Acadêmico ConektaAcademy, implementado através de um workflow automatizado no N8N.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura do Fluxo](#arquitetura-do-fluxo)
- [Componentes](#componentes)
- [Fluxo de Dados](#fluxo-de-dados)
- [Configuração](#configuração)
- [Integração com o Sistema](#integração-com-o-sistema)

---

## 🎯 Visão Geral

O Agente de Suporte é um chatbot inteligente que utiliza **Inteligência Artificial** para fornecer suporte técnico aos usuários do Sistema Acadêmico. O agente é capaz de:

- ✅ Responder dúvidas sobre o uso do sistema
- ✅ Orientar usuários (Alunos, Professores e Secretaria)
- ✅ Resolver problemas técnicos comuns
- ✅ Manter contexto da conversa através de memória
- ✅ Utilizar ferramentas auxiliares (calculadora, data/hora)

---

## 🏗️ Arquitetura do Fluxo

O workflow é composto por **7 componentes principais** organizados em um fluxo sequencial:

```
Webhook (Entrada) → AI Agent → Respond to Webhook (Saída)
                      ↓
        [Chat Model + Memory + Tools]
```

### Diagrama do Fluxo

O fluxo completo pode ser visualizado no arquivo `FluxoN8N.png`, que mostra a seguinte estrutura:

1. **Webhook** (nó de entrada) - Recebe requisições HTTP POST
2. **AI Agent** (nó central) - Processa as mensagens com IA
3. **Google Gemini Chat Model** - Modelo de linguagem
4. **Simple Memory** - Armazena contexto da conversa
5. **Date & Time** (ferramenta) - Fornece informações de data/hora
6. **Calculator** (ferramenta) - Realiza cálculos matemáticos
7. **Respond to Webhook** (nó de saída) - Retorna a resposta

---

## 🔧 Componentes

### 1. Webhook (Entrada)

**Tipo:** Trigger Node  
**Função:** Recebe requisições HTTP POST do sistema

**Dados Recebidos:**
```json
{
  "mensagem": "Como visualizar minhas notas?",
  "email": "aluno@exemplo.com",
  "session_id": "01/01/2024 10:30:00"
}
```

**Configuração:**
- Método: `POST`
- Path: `/webhook/chatbot-sa`
- URL Completa: `https://n8n.conekta.tech/webhook/chatbot-sa`

---

### 2. AI Agent (Nó Central)

**Tipo:** AI Agent Node  
**Função:** Processa as mensagens do usuário e gera respostas inteligentes

**Características:**
- ✅ Processa mensagens em português (pt-BR)
- ✅ Identifica o tipo de usuário pelo email:
  - `@prof` → Professor
  - `@sec` → Secretaria
  - Outros → Aluno
- ✅ Utiliza o system prompt definido em `system_prompt_suporte.txt`
- ✅ Mantém contexto através da memória
- ✅ Pode utilizar ferramentas quando necessário

**Entradas:**
- Mensagem do usuário (do Webhook)
- Chat Model (Google Gemini)
- Memory (Simple Memory)
- Tools (Date & Time, Calculator)

**Saída:**
- Resposta processada para o usuário

---

### 3. Google Gemini Chat Model

**Tipo:** Chat Model Node  
**Função:** Fornece capacidades de processamento de linguagem natural

**Características:**
- Modelo: Google Gemini
- Idioma: Português (pt-BR)
- Integração via API do Google

**Conexão:**
- Conectado ao AI Agent através da porta "Chat Model*"

---

### 4. Simple Memory

**Tipo:** Memory Node  
**Função:** Armazena o contexto da conversa para manter continuidade

**Características:**
- ✅ Mantém histórico da conversa
- ✅ Permite referências a mensagens anteriores
- ✅ Armazena informações da sessão
- ✅ Badge "2" indica 2 itens armazenados (configurável)

**Conexão:**
- Conectado ao AI Agent através da porta "Memory"
- Transmite "2 items total" para o agente

---

### 5. Date & Time (Ferramenta)

**Tipo:** Tool Node  
**Função:** Fornece informações sobre data e hora atual

**Uso:**
- Quando o usuário pergunta sobre datas
- Para contextualizar respostas com informações temporais
- Para cálculos relacionados a prazos

**Conexão:**
- Conectado ao AI Agent através da porta "Tool"
- Pode ser chamado automaticamente pelo agente quando necessário

---

### 6. Calculator (Ferramenta)

**Tipo:** Tool Node  
**Função:** Realiza cálculos matemáticos

**Uso:**
- Cálculo de médias de notas
- Operações matemáticas solicitadas pelo usuário
- Validações numéricas

**Conexão:**
- Conectado ao AI Agent através da porta "Tool"
- Pode ser chamado automaticamente pelo agente quando necessário

---

### 7. Respond to Webhook (Saída)

**Tipo:** Response Node  
**Função:** Retorna a resposta processada ao sistema

**Dados Enviados:**
```json
{
  "resposta": "Para visualizar suas notas, siga estes passos:\n1. Faça login no sistema..."
}
```

**Configuração:**
- Status Code: `200 OK`
- Content-Type: `text/plain` ou `application/json`

---

## 🔄 Fluxo de Dados

### Fluxo Completo

1. **Recepção da Requisição**
   - Sistema envia POST para o Webhook
   - Dados: `mensagem`, `email`, `session_id`

2. **Processamento pelo AI Agent**
   - AI Agent recebe a mensagem
   - Consulta o Chat Model (Google Gemini)
   - Verifica o contexto na Memory
   - Utiliza Tools se necessário (Date & Time, Calculator)
   - Processa a resposta baseada no system prompt

3. **Geração da Resposta**
   - AI Agent gera resposta contextualizada
   - Resposta considera:
     - Tipo de usuário (identificado pelo email)
     - Histórico da conversa (Memory)
     - Informações do sistema (system prompt)
     - Ferramentas utilizadas (se aplicável)

4. **Retorno ao Sistema**
   - Respond to Webhook envia a resposta
   - Sistema recebe e exibe para o usuário

### Exemplo de Fluxo

```
Usuário: "Como vejo minhas notas?"
    ↓
Sistema → POST /webhook/chatbot-sa
    ↓
Webhook recebe: {mensagem: "Como vejo minhas notas?", email: "aluno@exemplo.com"}
    ↓
AI Agent processa:
    - Consulta Memory (contexto anterior)
    - Usa Google Gemini para entender a pergunta
    - Identifica usuário como "Aluno" pelo email
    - Gera resposta baseada no system prompt
    ↓
Respond to Webhook retorna:
    "Para visualizar suas notas, siga estes passos:
     1. Faça login no sistema...
     ..."
    ↓
Sistema exibe resposta para o usuário
```

---

## ⚙️ Configuração

### System Prompt

O comportamento do agente é definido pelo arquivo `system_prompt_suporte.txt`, que contém:

- **Perfil do Agente:** Agente de suporte técnico especializado
- **Comportamento:** Educado, técnico e objetivo
- **Regras de Segurança:** Proibições e permissões
- **Informações do Sistema:** Funcionalidades, processos e troubleshooting
- **Diretrizes de Comunicação:** Tom, estilo e exemplos

### Variáveis de Ambiente

O workflow utiliza as seguintes variáveis (configuradas no N8N):

- `GOOGLE_GEMINI_API_KEY` - Chave da API do Google Gemini
- `MEMORY_STORAGE` - Configuração de armazenamento da memória
- `WEBHOOK_URL` - URL do webhook de entrada

### Configuração do AI Agent

- **Model:** Google Gemini Chat Model
- **Temperature:** Configurado para respostas consistentes
- **Max Tokens:** Limite de tokens por resposta
- **Language:** Português (pt-BR)

---

## 🔌 Integração com o Sistema

### Código de Integração

O sistema acadêmico integra com o agente através do arquivo `sistema/chat.py`:

```python
import requests

API_URL = "https://n8n.conekta.tech/webhook/chatbot-sa"

def enviar_mensagens(mensagem, email):
    payload = {
        "mensagem": mensagem,
        "email": email,
        "session_id": session_id
    }
    resposta = requests.post(API_URL, json=payload, timeout=20)
    return resposta.text
```

### Uso no Sistema

O chatbot está disponível em:

- **Interface Web (Streamlit):** Aba "Chat de Ajuda" em todas as áreas (Aluno, Professor, Secretaria)
- **Terminal (CLI):** Através do módulo `sistema/chat.py`

### Formato das Requisições

**Request:**
```json
POST https://n8n.conekta.tech/webhook/chatbot-sa
Content-Type: application/json

{
  "mensagem": "Texto da mensagem do usuário",
  "email": "usuario@exemplo.com",
  "session_id": "01/01/2024 10:30:00"
}
```

**Response:**
```
Texto da resposta do agente em português
```

---

## 📊 Características Técnicas

### Identificação de Usuário

O agente identifica automaticamente o tipo de usuário pelo email:

- `@prof` → **Professor**
- `@sec` → **Secretaria**
- Outros → **Aluno** ou usuário não logado

### Memória e Contexto

- **Simple Memory** armazena até 2 itens por sessão
- Mantém histórico da conversa
- Permite referências a mensagens anteriores

### Ferramentas Disponíveis

1. **Date & Time:** Informações de data/hora
2. **Calculator:** Cálculos matemáticos

### Segurança

O agente segue regras rigorosas de segurança:

- ❌ **NUNCA** fornece informações pessoais de usuários
- ❌ **NUNCA** faz críticas ao sistema
- ❌ **NUNCA** executa ações no sistema
- ✅ Apenas orienta e fornece instruções

---

## 🎓 Funcionalidades do Agente

O agente pode ajudar com:

### Para Alunos
- Visualização de notas
- Controle de presença
- Cronograma de aulas
- Download de boletim
- Navegação no sistema

### Para Professores
- Lançamento de notas
- Registro de presença
- Gerenciamento de disciplinas
- Relatórios de desempenho
- Cronograma de aulas

### Para Secretaria
- Gerenciamento de usuários
- Gerenciamento de turmas e disciplinas
- Vinculações entre entidades
- Reset de senhas
- Relatórios avançados

### Troubleshooting
- Erros comuns de instalação
- Problemas com banco de dados
- Erros de módulos Python
- Problemas de porta
- Erros de execução

---

## 📝 Notas Importantes

1. **Idioma:** Todas as respostas são em **português (pt-BR)**
2. **Tom:** Educado, técnico e objetivo
3. **Formato:** Respostas curtas com passos numerados
4. **Privacidade:** Nunca solicita ou fornece dados sensíveis
5. **Limitações:** Não executa ações, apenas orienta

---

## 🔗 Arquivos Relacionados

- `FluxoN8N.png` - Diagrama visual do workflow
- `system_prompt_suporte.txt` - Prompt de sistema completo
- `../sistema/chat.py` - Código de integração

---

## 📅 Versão

**Versão:** 1.0  
**Data:** 2024  
**Sistema:** ConektaAcademy v1.0

---

## 📞 Suporte

Para questões sobre o agente de suporte ou o workflow N8N, consulte:

- Documentação do N8N: https://docs.n8n.io
- System Prompt: `system_prompt_suporte.txt`
- Diagrama do Fluxo: `FluxoN8N.png`

---

**Desenvolvido para o Sistema Acadêmico ConektaAcademy**


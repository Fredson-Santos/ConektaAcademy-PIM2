# 📚 Exemplos de Uso - Sistema Acadêmico

## Cenários de Teste

### Cenário 1: Aluno Consultando Notas

1. **Login:**
   - Email/Matrícula: `1001`
   - Senha: `aluno123`

2. **Navegação:**
   - Clique em "📘 Notas"
   - Selecione a matéria
   - Visualize NP1, NP2, PIM

3. **Resultado esperado:**
   - Notas exibidas em cards
   - Média calculada automaticamente

---

### Cenário 2: Professor Lançando Notas

1. **Login:**
   - Email: `prof@profmatematica`
   - Senha: `prof123`

2. **Lançar Nota:**
   - Vá para "📘 Lançar Notas"
   - Matrícula: `1001`
   - Tipo: `NP1`
   - Nota: `8.5`
   - Clique "✅ Lançar Nota"

3. **Resultado esperado:**
   - Mensagem de sucesso
   - Nota salva no banco de dados

---

### Cenário 3: Secretaria Criando Usuário

1. **Login:**
   - Email: `secretaria@sec`
   - Senha: `sec123`

2. **Criar Usuário:**
   - Aba "👥 Gerenciar Usuários"
   - Sub-aba "Cadastrar"
   - Tipo: `aluno`
   - Nome: `João Silva`
   - Email: `joao@school.com`
   - Matrícula: `2024002`
   - Senha: `senha123`
   - Clique "✅ Cadastrar Usuário"

3. **Resultado esperado:**
   - Usuário criado
   - Pode fazer login com as novas credenciais

---

## Fluxos de Trabalho

### Fluxo: Professor registrando presença

```
1. Login como professor
2. "📅 Presença"
3. Preencher:
   - Matrícula do Aluno
   - Data (calendário)
   - Status (Presente/Faltou)
4. Clicar "✅ Atualizar Presença"
5. ✅ Sucesso
```

### Fluxo: Secretaria gerenciando turma

```
1. Login como secretaria
2. "📚 Turmas"
3. "Criar"
4. Preencher:
   - Nome: "1º Ano A"
   - Ano: "2024"
5. "➕ Criar Turma"
6. ✅ Turma criada
7. "Vincular Professor"
8. Matrícula professor + Nome turma
9. "🔗 Vincular"
10. ✅ Vínculo criado
```

---

## Testes de Validação

### ✅ Teste: Cadastro com Email Inválido

**Esperado:** Deve aceitar qualquer formato de email (validação simples)

```
Email: teste@email.com
Resultado: ✅ Aceito
```

### ✅ Teste: Senha Vazia

**Esperado:** Deve rejeitar com mensagem de erro

```
Senha: (vazio)
Resultado: ❌ "Senha não pode ficar em branco"
```

### ✅ Teste: Login com Credenciais Erradas

**Esperado:** Mostrar erro

```
Email: user@email.com
Senha: senhaerrada
Resultado: ❌ "Email/Matrícula ou senha incorretos"
```

### ✅ Teste: Visualizar Notas sem Registro

**Esperado:** Mostrar aviso

```
Aluno sem notas
Resultado: ⚠️ "Nenhuma nota registrada"
```

---

## Dados de Teste Preparados

### Usuários Pré-configurados (se existirem)

| Tipo | Email/Matrícula | Senha | Nome |
|------|---|---|---|
| Aluno | 1001 | aluno123 | João Aluno |
| Prof | prof@profmatematica | prof123 | Prof Matemática |
| Secretaria | secretaria@sec | sec123 | Maria Secretaria |

> **Nota:** Se não existirem, crie via tela de cadastro

---

## Checklist de Funcionalidades

### Aluno ✓
- [x] Login/Logout
- [x] Ver notas por matéria
- [x] Ver presenças e frequência
- [x] Visualizar cronograma
- [x] Fazer anotações

### Professor ✓
- [x] Login/Logout
- [x] Lançar notas
- [x] Registrar presença
- [x] Gerar relatórios
- [x] Gerenciar cronograma
- [x] Fazer anotações

### Secretaria ✓
- [x] Login/Logout
- [x] Listar usuários
- [x] Criar usuários
- [x] Excluir usuários
- [x] Resetar senhas
- [x] Gerenciar turmas
- [x] Gerenciar disciplinas
- [x] Vincular professor-turma

---

## Troubleshooting de Teste

### "Erro ao lançar nota"
- Verifique se a matrícula existe no banco
- Valide o formato dos dados
- Cheque o console para mensagens de erro

### "Usuário não encontrado ao resetar senha"
- Confirme a matrícula correta
- Use a mesma matrícula do cadastro

### "Arquivo de anotações não existe"
- Primeira vez criando: será criado automaticamente
- Verifique permissões da pasta

---

## Performance e Limites

| Item | Limite | Recomendação |
|------|--------|--------------|
| Usuários | 10,000+ | Sem problema |
| Registros Presença | 100,000+ | Considerar índices |
| Tamanho DB | 100MB+ | Performance OK |
| Usuários simultâneos | Depende servidor | Streamlit local: 1-5 |

---

## Casos de Uso Avançados

### Caso 1: Importação em Massa
*Não implementado ainda*
- Seria útil adicionar CSV upload

### Caso 2: Relatórios Exportáveis
*Não implementado ainda*
- Botão para baixar relatório em PDF

### Caso 3: Notificações
*Não implementado ainda*
- Email de notas lançadas
- SMS de ausências

---

## Melhorias Futuras

1. 📱 Versão mobile nativa
2. 📧 Sistema de notificações
3. 📊 Dashboard com gráficos
4. 📥 Importação de dados
5. 🔐 Autenticação avançada
6. 🌍 Suporte a múltiplos idiomas

---

**Pronto para testar? Execute:**
```bash
streamlit run app.py
```

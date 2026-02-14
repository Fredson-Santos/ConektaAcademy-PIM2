# 📘 Manual do Usuário - ConektaAcademy

**Sistema de Gerenciamento Acadêmico**

---

## 📑 Sumário

1. [Introdução](#introdução)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Área do Aluno](#área-do-aluno)
4. [Área do Professor](#área-do-professor)
5. [Área da Secretaria](#área-da-secretaria)
6. [Perguntas Frequentes (FAQ)](#perguntas-frequentes-faq)
7. [Suporte](#suporte)

---

## 📖 Introdução

Bem-vindo ao **ConektaAcademy**! Este manual irá guiá-lo através de todas as funcionalidades do sistema, desde o primeiro acesso até o uso avançado das ferramentas disponíveis.

O sistema oferece três áreas distintas, cada uma com funcionalidades específicas:
- 👥 **Área do Aluno** - Consulta de notas, presenças e relatórios
- 👨‍🏫 **Área do Professor** - Lançamento de notas, controle de presença e relatórios
- 🗂️ **Área da Secretaria** - Gerenciamento completo do sistema

---

## 🔐 Acesso ao Sistema

### Primeiro Acesso

1. **Abra o navegador** e acesse o endereço fornecido pela instituição (geralmente `http://localhost:8501`)

2. **Na tela inicial**, você verá três abas:
   - **Login** - Para usuários já cadastrados
   - **Cadastro** - Para criar uma nova conta
   - **💬 Chat de Ajuda** - Para tirar dúvidas

### Criar uma Nova Conta

1. Clique na aba **"Cadastro"**

2. Preencha os campos:
   - **Nome Completo** (obrigatório)
   - **Email** (deixe em branco se for aluno)
   - **Matrícula** (deixe em branco se for professor)
   - **Senha** (obrigatório)
   - **Confirmar Senha** (obrigatório)

3. **Regras de cadastro:**
   - Email com `@prof` → cria conta de **Professor**
   - Email com `@sec` → cria conta de **Secretaria**
   - Sem email ou email sem `@prof`/`@sec` → cria conta de **Aluno**

4. Clique em **"✅ Cadastrar"**

5. Após o cadastro, faça login na aba **"Login"**

### Fazer Login

1. Na aba **"Login"**, insira:
   - **Email ou Matrícula**
   - **Senha**

2. (Opcional) Marque **"💾 Lembrar-me"** para manter a sessão ativa

3. Clique em **"🔓 Entrar"**

4. Você será redirecionado para sua área específica

### Chat de Ajuda

- Disponível na tela de login e em todas as áreas do sistema
- Permite fazer perguntas sobre o sistema
- Funciona mesmo sem estar logado

---

## 👥 Área do Aluno

Após fazer login como aluno, você terá acesso às seguintes funcionalidades:

### 📘 Aba: Notas

**Visualização de Notas por Disciplina**

1. A aba **"Notas"** exibe todas as disciplinas vinculadas a você

2. Para cada disciplina, você verá:
   - **NP1** - Nota da primeira avaliação
   - **NP2** - Nota da segunda avaliação
   - **PIM** - Nota do Projeto Integrador Multidisciplinar
   - **Média** - Calculada automaticamente: (NP1 + NP2 + PIM) / 3

3. **Cores indicativas:**
   - 🟢 **Verde** - Média ≥ 7.0 (Aprovado)
   - 🔴 **Vermelho** - Média < 7.0 (Reprovado)

4. Se não houver notas lançadas, aparecerá "-" no lugar

**Observação:** Se você não estiver vinculado a nenhuma disciplina, entre em contato com a secretaria.

### 📅 Aba: Presenças

**Controle de Frequência**

1. A aba **"Presenças"** mostra seu histórico de presença

2. **Métricas exibidas:**
   - **Total de Dias** - Quantidade total de dias registrados
   - **Dias Presentes** - Quantidade de dias em que você esteve presente
   - **Taxa de Presença** - Percentual de presença calculado automaticamente

3. **Tabela de Presenças:**
   - Lista todas as datas registradas
   - Status: ✅ Presente ou ❌ Faltou

4. Se não houver registros, aparecerá a mensagem: "ℹ️ Nenhum registro de presença ainda."

### 📖 Aba: Cronograma

**Visualização do Cronograma de Aulas**

1. A aba **"Cronograma"** exibe todas as aulas agendadas

2. **Informações mostradas:**
   - **Sala** - Local da aula
   - **Data** - Data da aula
   - **Dia da Semana** - Dia da semana
   - **Conteúdo** - Assunto da aula

3. O cronograma é compartilhado entre todos os usuários do sistema

### 📔 Aba: Bloco do Aluno

**Anotações Pessoais**

1. A aba **"Bloco do Aluno"** é seu espaço pessoal para anotações

2. Digite suas anotações no campo de texto

3. Clique em **"💾 Salvar Anotações"** para salvar

4. Suas anotações são salvas em um arquivo pessoal e ficam disponíveis na próxima vez que você acessar

### 📄 Aba: Relatórios

**Relatórios Completos e Boletim**

1. A aba **"Relatórios"** oferece relatórios detalhados

2. **Relatório Completo:**
   - **Informações do Aluno:** Nome, email, matrícula, curso, turma
   - **Relatório de Notas:** Tabela com todas as disciplinas e notas
   - **Relatório de Faltas:** Estatísticas e tabela de presenças

3. **Download de Boletim PDF:**
   - Clique em **"📥 Baixar Boletim PDF"**
   - Um boletim completo será gerado
   - Clique em **"⬇️ Baixar Boletim PDF"** para fazer o download

**Observação:** Para gerar PDFs, é necessário ter a biblioteca `reportlab` instalada.

### 💬 Aba: Chat de Ajuda

- Mesma funcionalidade do chat da tela de login
- Disponível em todas as áreas do sistema

---

## 👨‍🏫 Área do Professor

Após fazer login como professor, você terá acesso às seguintes funcionalidades:

### 📚 Aba: Minhas Disciplinas

Esta aba contém duas sub-abas principais:

#### 📘 Sub-aba: Lançar Notas

**Cadastro de Notas dos Alunos**

1. **Selecione a Disciplina:**
   - No campo "Selecione a Disciplina", escolha a disciplina desejada
   - O formato exibido é: "Nome da Disciplina - Nome do Curso" (ex: "Programação I - ADS")

2. **Selecione o Aluno:**
   - No campo "Selecione o Aluno", escolha o aluno
   - Apenas alunos vinculados à disciplina selecionada aparecerão
   - O formato exibido é: "(Matrícula: XXX) - Nome do Aluno"

3. **Digite as Notas:**
   - **NP1** - Nota da primeira avaliação (0.0 a 10.0)
   - **NP2** - Nota da segunda avaliação (0.0 a 10.0)
   - **PIM** - Nota do Projeto Integrador Multidisciplinar (0.0 a 10.0)

4. Clique em **"✅ Lançar Notas"**

5. **Tabela de Notas:**
   - Abaixo do formulário, há uma tabela mostrando todos os alunos da disciplina
   - Exibe: Nome, Matrícula, NP1, NP2, PIM e Média calculada automaticamente

**Observação:** A média é calculada automaticamente como (NP1 + NP2 + PIM) / 3

#### 📅 Sub-aba: Presença

**Registro de Presença dos Alunos**

1. **Selecione a Disciplina:**
   - No campo "Selecione a Disciplina", escolha a disciplina desejada

2. **Selecione o Aluno:**
   - No campo "Selecione o Aluno", escolha o aluno
   - Apenas alunos vinculados à disciplina selecionada aparecerão

3. **Selecione a Data:**
   - No campo "Data", escolha a data da aula

4. **Marque a Presença:**
   - Selecione **"✅ Presente"** ou **"❌ Faltou"**

5. Clique em **"✅ Registrar Presença"**

6. **Tabela de Presenças:**
   - Abaixo do formulário, há uma tabela mostrando todos os alunos da disciplina
   - Exibe: Nome, Matrícula, Presentes, Faltas e Percentual de Presença

**Observação:** Você pode atualizar a presença de um aluno na mesma data clicando novamente em "Registrar Presença"

### 📄 Aba: Gerar Relatório

**Relatórios de Desempenho**

1. A aba **"Gerar Relatório"** permite gerar relatórios de alunos

2. **Selecione o Aluno:**
   - No campo "Selecione o Aluno", escolha o aluno desejado

3. Clique em **"📊 Gerar Relatório"**

4. O relatório exibirá:
   - Informações do aluno
   - Notas por disciplina
   - Estatísticas de presença

5. **Download PDF:**
   - Clique em **"📥 Download PDF"** para baixar o relatório em PDF

### 📖 Aba: Cronograma

**Gerenciamento do Cronograma**

1. A aba **"Cronograma"** permite adicionar aulas ao cronograma

2. **Adicionar Nova Aula:**
   - **Sala** - Digite o número da sala
   - **Data** - Selecione a data da aula
   - **Dia da Semana** - Selecione o dia (será preenchido automaticamente)
   - **Conteúdo** - Digite o assunto da aula

3. Clique em **"✅ Adicionar Aula"**

4. **Visualizar Cronograma:**
   - Abaixo do formulário, há uma tabela com todas as aulas agendadas

### 🗒️ Aba: Bloco do Professor

**Anotações Pessoais**

1. A aba **"Bloco do Professor"** é seu espaço pessoal para anotações

2. Digite suas anotações no campo de texto

3. Clique em **"💾 Salvar Anotações"** para salvar

### 💬 Aba: Chat de Ajuda

- Mesma funcionalidade do chat da tela de login

---

## 🗂️ Área da Secretaria

Após fazer login como secretaria, você terá acesso a todas as funcionalidades de gerenciamento do sistema:

### 👥 Aba: Gerenciamento de Usuários

Esta aba contém três sub-abas:

#### 📝 Sub-aba: Cadastrar Novo Usuário

1. Preencha os campos:
   - **Nome Completo** (obrigatório)
   - **Email** (deixe em branco se for aluno)
   - **Matrícula** (deixe em branco se for professor)
   - **Senha** (obrigatório)
   - **Tipo de Usuário** - Selecione: Aluno, Professor ou Secretaria

2. Clique em **"✅ Cadastrar Usuário"**

#### 📋 Sub-aba: Listar Usuários

1. Visualize todos os usuários cadastrados no sistema

2. A tabela exibe:
   - ID, Nome, Email, Matrícula, Tipo de Usuário, Curso, Turma

3. Use o campo de busca para filtrar usuários

#### 🗑️ Sub-aba: Excluir Usuário

1. **Selecione o Usuário:**
   - No campo "Selecione o Usuário", escolha o usuário a ser excluído

2. Clique em **"🗑️ Excluir Usuário"**

3. Confirme a exclusão

**Observação:** A exclusão é permanente e não pode ser desfeita.

### 📚 Aba: Gerenciamento de Turmas

Esta aba contém quatro sub-abas:

#### 📋 Sub-aba: Listar

1. Visualize todas as turmas cadastradas

2. A tabela exibe:
   - ID, Nome, Ano, Curso, Professor Email

3. **Ver Alunos por Turma:**
   - Use o expander "Ver alunos por turma" para ver os alunos de cada turma

#### ➕ Sub-aba: Criar

1. Preencha os campos:
   - **Nome da Turma** (obrigatório) - Ex: "1ano-a"
   - **Ano** (obrigatório) - Ex: 2024
   - **Selecione o Curso*** (obrigatório) - Selecione um curso da lista
   - **Vincular Professor** (opcional) - Selecione um professor da lista

2. Clique em **"✅ Criar Turma"**

#### 🔗 Sub-aba: Vincular Turmas

**Vincular Aluno a Turma:**

1. **Selecione o Aluno:**
   - No campo "Selecione o Aluno", escolha o aluno

2. **Selecione a Turma:**
   - No campo "Selecione a Turma", escolha a turma

3. Clique em **"🔗 Vincular Aluno"**

**Observação:** Ao vincular um aluno a uma turma, ele é automaticamente vinculado ao curso daquela turma.

**Vincular Professor a Turma:**

1. **Selecione o Professor:**
   - No campo "Selecione o Professor", escolha o professor

2. **Selecione a Turma:**
   - No campo "Selecione a Turma", escolha a turma

3. Clique em **"🔗 Vincular Professor"**

#### 🗑️ Sub-aba: Excluir

1. **Selecione o Curso:**
   - No campo "Selecione o Curso", escolha o curso

2. **Selecione a Turma:**
   - No campo "Selecione a Turma", escolha a turma a ser excluída

3. Clique em **"🗑️ Excluir Turma"**

4. Confirme a exclusão

### 📖 Aba: Gerenciamento de Disciplinas

Esta aba contém quatro sub-abas:

#### 📋 Sub-aba: Listar

1. Visualize todas as disciplinas cadastradas

2. A tabela exibe:
   - ID, Nome, Professor, Curso, Turma, Carga Horária

#### ➕ Sub-aba: Criar

1. Preencha os campos:
   - **Nome da Disciplina** (obrigatório) - Ex: "Programação I"
   - **Professor** (opcional) - Selecione um professor da lista
   - **Carga Horária** (obrigatório) - Ex: 80
   - **Curso** (opcional) - Selecione um curso da lista
   - **Turma** (opcional) - Selecione uma turma da lista

2. Clique em **"✅ Criar Disciplina"**

#### 🔗 Sub-aba: Vincular Disciplinas

**Vincular Turma a Disciplina:**

1. **Selecione a Disciplina:**
   - No campo "Selecione a Disciplina", escolha a disciplina

2. **Selecione a Turma:**
   - No campo "Selecione a Turma", escolha a turma

3. Clique em **"🔗 Vincular Turma"**

**Observação:** Ao vincular uma turma a uma disciplina, todos os alunos daquela turma são automaticamente vinculados à disciplina.

**Vincular Professor a Disciplina:**

1. **Selecione a Disciplina:**
   - No campo "Selecione a Disciplina", escolha a disciplina

2. **Selecione o Professor:**
   - No campo "Selecione o Professor", escolha o professor

3. Clique em **"🔗 Vincular Professor"**

**Vincular Curso a Disciplina:**

1. **Selecione a Disciplina:**
   - No campo "Selecione a Disciplina", escolha a disciplina

2. **Selecione o Curso:**
   - No campo "Selecione o Curso", escolha o curso

3. Clique em **"🔗 Vincular Curso"**

#### 🗑️ Sub-aba: Excluir

1. **Selecione a Disciplina:**
   - No campo "Selecione a Disciplina", escolha a disciplina a ser excluída

2. Clique em **"🗑️ Excluir Disciplina"**

3. Confirme a exclusão

### 🎓 Aba: Gerenciamento de Cursos

Esta aba contém três sub-abas:

#### 📋 Sub-aba: Listar

1. Visualize todos os cursos cadastrados

2. A tabela exibe:
   - ID, Nome, Início, Duração

#### ➕ Sub-aba: Criar

1. Preencha os campos:
   - **Nome do Curso** (obrigatório) - Ex: "Análise e Desenvolvimento de Sistemas"
   - **Início** (obrigatório) - Ex: "2024/1"
   - **Duração** (obrigatório) - Duração em semestres - Ex: 6

2. Clique em **"✅ Criar Curso"**

#### 🗑️ Sub-aba: Excluir

1. **Selecione o Curso:**
   - No campo "Selecione o Curso", escolha o curso a ser excluído

2. Clique em **"🗑️ Excluir Curso"**

3. Confirme a exclusão

### 📄 Aba: Relatórios

Esta aba permite gerar relatórios detalhados de diferentes entidades:

#### 📊 Relatório de Alunos

1. **Selecione o Aluno:**
   - No campo "Selecione o Aluno", escolha o aluno

2. Clique em **"📊 Gerar Relatório"**

3. O relatório exibirá:
   - Informações do aluno
   - Notas por disciplina
   - Estatísticas de presença

4. **Download PDF:**
   - Clique em **"📥 Download PDF"** para baixar

#### 📊 Relatório de Turmas

1. Clique em **"📊 Gerar Relatório de Turmas"**

2. O relatório exibirá:
   - Lista de todas as turmas
   - Estatísticas por turma (quantidade de alunos, disciplinas, etc.)

3. **Exportar CSV:**
   - Clique em **"📥 Exportar CSV"** para baixar

#### 📊 Relatório de Disciplinas

1. Clique em **"📊 Gerar Relatório de Disciplinas"**

2. O relatório exibirá:
   - Lista de todas as disciplinas
   - Estatísticas por disciplina (quantidade de alunos, professor, etc.)

3. **Exportar CSV:**
   - Clique em **"📥 Exportar CSV"** para baixar

#### 📊 Relatório de Cursos

1. Clique em **"📊 Gerar Relatório de Cursos"**

2. O relatório exibirá:
   - Lista de todos os cursos
   - Estatísticas por curso (quantidade de turmas, alunos, etc.)

3. **Exportar CSV:**
   - Clique em **"📥 Exportar CSV"** para baixar

### 💬 Aba: Chat de Ajuda

- Mesma funcionalidade do chat da tela de login

---

## ❓ Perguntas Frequentes (FAQ)

### Geral

**P: Esqueci minha senha. Como recuperar?**
R: Entre em contato com a secretaria para redefinir sua senha.

**P: Posso usar o sistema em dispositivos móveis?**
R: Sim, o sistema é responsivo e funciona em tablets e smartphones.

**P: Os dados são salvos automaticamente?**
R: Sim, todos os dados são salvos automaticamente no banco de dados.

**P: Como faço logout?**
R: Clique no botão **"🚪 Logout"** na barra lateral esquerda.

### Alunos

**P: Não vejo minhas notas. O que fazer?**
R: Verifique se você está vinculado a uma disciplina. Se não estiver, entre em contato com a secretaria.

**P: Como é calculada a média?**
R: A média é calculada automaticamente como: (NP1 + NP2 + PIM) / 3

**P: Posso baixar meu boletim?**
R: Sim, na aba "Relatórios", clique em "📥 Baixar Boletim PDF".

**P: O que significa a cor verde/vermelha nas notas?**
R: Verde = Média ≥ 7.0 (Aprovado), Vermelho = Média < 7.0 (Reprovado)

### Professores

**P: Como lanço notas para meus alunos?**
R: Acesse "Minhas Disciplinas" → "Lançar Notas", selecione a disciplina e o aluno, e preencha as notas.

**P: Posso atualizar uma nota já lançada?**
R: Sim, basta lançar novamente as notas para o mesmo aluno. A nota será atualizada.

**P: Como registro presença?**
R: Acesse "Minhas Disciplinas" → "Presença", selecione a disciplina, aluno e data, e marque presente/faltou.

**P: Posso ver todas as notas dos alunos de uma disciplina?**
R: Sim, na sub-aba "Lançar Notas", há uma tabela mostrando todos os alunos e suas notas.

### Secretaria

**P: Como crio uma nova turma?**
R: Acesse "Gerenciamento de Turmas" → "Criar", preencha os campos obrigatórios e clique em "Criar Turma".

**P: Como vinculo um aluno a uma turma?**
R: Acesse "Gerenciamento de Turmas" → "Vincular Turmas" → "Vincular Aluno", selecione o aluno e a turma.

**P: O que acontece quando vinculo uma turma a uma disciplina?**
R: Todos os alunos daquela turma são automaticamente vinculados à disciplina.

**P: Como gero relatórios?**
R: Acesse a aba "Relatórios" e escolha o tipo de relatório desejado (Alunos, Turmas, Disciplinas ou Cursos).

**P: Posso exportar dados?**
R: Sim, os relatórios podem ser exportados em CSV ou PDF.

---

## 🐛 Troubleshooting

### Problemas de Acesso

**Erro: "Email/Matrícula ou senha incorretos"**
- Verifique se você digitou corretamente suas credenciais
- Certifique-se de que a conta foi criada corretamente
- Entre em contato com a secretaria se o problema persistir

**Erro: "Aplicação não abre no navegador"**
- Acesse manualmente: `http://localhost:8501`
- Verifique se o servidor está rodando

### Problemas de Funcionalidade

**Erro ao gerar PDF: "Biblioteca reportlab não instalada"**
- Instale a biblioteca: `pip install reportlab`
- O sistema funciona normalmente sem ela, mas sem geração de PDFs

**Notas não aparecem**
- Verifique se você está vinculado à disciplina (alunos)
- Verifique se as notas foram lançadas pelo professor
- Entre em contato com a secretaria se necessário

**Presenças não aparecem**
- Verifique se o professor registrou as presenças
- Certifique-se de que você está vinculado à disciplina

### Problemas Técnicos

**Sistema lento**
- Verifique sua conexão com a internet
- Limpe o cache do navegador
- Feche outras abas do navegador

**Dados não salvam**
- Verifique se você clicou no botão de salvar
- Verifique sua conexão com a internet
- Tente novamente

---

## 📞 Suporte

### Contato

Para dúvidas, problemas ou sugestões:

- 📧 **Email:** [Email de suporte]
- 💬 **Chat de Ajuda:** Disponível no sistema
- 📖 **Documentação:** Consulte os arquivos README.md e README_INTERFACE.md

### Informações Importantes

- ⚠️ **Backup:** Faça backup regular dos dados importantes
- 🔒 **Segurança:** Não compartilhe suas credenciais de acesso
- 📱 **Compatibilidade:** Use navegadores modernos (Chrome, Firefox, Edge, Safari)
- 🔄 **Atualizações:** Mantenha o sistema atualizado

---

## 📝 Notas Finais

Este manual foi criado para facilitar o uso do sistema ConektaAcademy. Se você encontrar algum problema ou tiver sugestões de melhoria, entre em contato com o suporte.

**Versão do Manual:** 1.0  
**Última Atualização:** 2024

---

<div align="center">

**© Conekta - Todos os direitos reservados**

**ConektaAcademy - Sistema de Gerenciamento Acadêmico**

</div>


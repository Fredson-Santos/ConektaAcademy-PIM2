# 📊 Diagramas do Sistema ConektaAcademy

Esta pasta contém os diagramas UML e de arquitetura do sistema em formato PlantUML.

## 📋 Diagramas Disponíveis

### 1. Diagrama de Casos de Uso
**Arquivo:** `01_caso_uso.puml`

Mostra todos os casos de uso do sistema, organizados por ator (Aluno, Professor, Secretaria) e por pacote funcional.

**Como visualizar:**
- Use um editor PlantUML online: http://www.plantuml.com/plantuml/uml/
- Ou instale a extensão PlantUML no VS Code
- Ou use: `java -jar plantuml.jar 01_caso_uso.puml`

### 2. Diagrama de Classes
**Arquivo:** `02_classes.puml`

Representa a estrutura de classes do sistema, incluindo:
- Classes principais (SistemaAcademico, Database)
- Entidades (Usuario, Turma, Disciplina, Curso, Nota, Presenca, Cronograma)
- Funções de negócio organizadas por módulo
- Relacionamentos entre classes

### 3. Diagramas de Sequência

#### 3.1. Professor Lança Nota
**Arquivo:** `03_sequencia_professor_lanca_nota.puml`

Mostra o fluxo completo de quando um professor lança notas de um aluno, incluindo:
- Seleção de disciplina e aluno
- Validação de dados
- Inserção/atualização no banco de dados

#### 3.2. Secretaria Cria Turma
**Arquivo:** `04_sequencia_secretaria_cria_turma.puml`

Demonstra o processo de criação de uma nova turma pela secretaria, incluindo:
- Validação de dados
- Verificação de duplicatas
- Inserção no banco de dados

#### 3.3. Aluno Consulta Notas
**Arquivo:** `05_sequencia_aluno_consulta_notas.puml`

Ilustra como um aluno consulta suas notas, incluindo:
- Autenticação
- Busca de disciplinas vinculadas
- Cálculo de médias
- Aplicação de estilos condicionais

### 4. Diagrama de Rede LAN
**Arquivo:** `06_rede_lan.puml`

Representa a arquitetura de rede local (LAN) do sistema, mostrando:
- Servidor principal com aplicação Streamlit
- Estações de trabalho (Secretaria, Professor, Aluno)
- Terminal CLI para administração
- Integração com API externa de Chat
- Configurações de IP e rede

## 🛠️ Como Usar

### Opção 1: Editor Online (Mais Simples)
1. Acesse: http://www.plantuml.com/plantuml/uml/
2. Copie o conteúdo do arquivo `.puml`
3. Cole no editor
4. O diagrama será gerado automaticamente

### Opção 2: VS Code
1. Instale a extensão "PlantUML" no VS Code
2. Abra o arquivo `.puml`
3. Pressione `Alt+D` para visualizar o diagrama

### Opção 3: Linha de Comando
```bash
# Instalar PlantUML
# Windows: baixe plantuml.jar de https://plantuml.com/download
# Linux: sudo apt-get install plantuml

# Gerar diagrama PNG
java -jar plantuml.jar diagramas/01_caso_uso.puml

# Gerar todos os diagramas
java -jar plantuml.jar diagramas/*.puml
```

### Opção 4: Docker
```bash
docker run -v $(pwd)/diagramas:/work plantuml/plantuml /work/*.puml
```

## 📝 Notas

- Todos os diagramas estão em formato PlantUML (`.puml`)
- Os diagramas podem ser editados em qualquer editor de texto
- PlantUML é uma linguagem de texto para diagramas UML
- Os diagramas são versionáveis e fáceis de manter

## 🔄 Atualizações

Quando o sistema for atualizado, os diagramas devem ser revisados e atualizados conforme necessário:
- Adição de novas funcionalidades → Atualizar diagrama de casos de uso
- Mudanças na estrutura de classes → Atualizar diagrama de classes
- Novos fluxos → Adicionar novos diagramas de sequência
- Mudanças na arquitetura → Atualizar diagrama de rede

## 📚 Referências

- [Documentação PlantUML](https://plantuml.com/)
- [Sintaxe PlantUML](https://plantuml.com/guide)
- [Exemplos PlantUML](https://real-world-plantuml.com/)

---

**Última atualização:** 2024  
**Versão dos diagramas:** 1.0


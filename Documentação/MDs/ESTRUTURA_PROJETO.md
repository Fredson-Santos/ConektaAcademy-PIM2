# Estrutura do Projeto

O sistema foi organizado em duas interfaces distintas: **Terminal** e **Interface Web**.

## 📁 Estrutura de Pastas

```
Sistema-Acad-mico-PIM-II-IA/
├── terminal/              # Modo Terminal (CLI)
│   ├── main.py           # Arquivo principal do terminal
│   └── menus/            # Menus do terminal
│       ├── aluno_menu.py
│       ├── professor_menu.py
│       └── secretaria_menu.py
│
├── interface/            # Modo Interface Web (Streamlit)
│   ├── app.py           # Arquivo principal da interface web
│   └── telas/           # Telas da interface web
│       ├── login.py
│       ├── area_aluno.py
│       ├── area_professor.py
│       └── area_secretaria.py
│
└── sistema/             # Módulos compartilhados
    ├── database.py      # Gerenciamento do banco de dados
    ├── funcoes.py       # Funções de negócio
    ├── classes.py       # Classes do sistema
    ├── chat.py          # Integração com chatbot
    └── relatorios.py    # Geração de relatórios
```

## 🚀 Como Executar

### Modo Terminal
```bash
python terminal/main.py
```

### Modo Interface Web
```bash
streamlit run interface/app.py
```

## 📝 Notas

- Os módulos em `sistema/` são compartilhados entre ambas as interfaces
- Cada interface tem seus próprios arquivos de apresentação
- A lógica de negócio permanece centralizada em `sistema/`


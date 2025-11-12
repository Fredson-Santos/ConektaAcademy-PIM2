# 🧪 Como Testar se a Função C Está Funcionando

Este guia mostra como verificar se a função C está compilada e funcionando corretamente no sistema.

## 📋 Métodos de Teste

### Método 1: Script de Teste Automático (Recomendado)

1. **Abra o terminal/PowerShell** na pasta do projeto

2. **Execute o script de teste:**
   ```bash
   python testar_c.py
   ```

3. **O script irá:**
   - ✅ Verificar se o wrapper pode ser importado
   - ✅ Verificar se a função C está disponível
   - ✅ Testar vários casos de cálculo de média
   - ✅ Comparar resultados C vs Python (se C estiver disponível)

**Exemplo de saída esperada:**

```
==================================================
  TESTE DA FUNÇÃO C - ConektaAcademy
==================================================

1. Testando importação do wrapper...
   ✅ Wrapper importado com sucesso!

2. Verificando se a função C está disponível...
   ✅ Função C está disponível e carregada!

3. Testando cálculo de média...

   Casos de teste:
   ---------------------------------------------
   NP1      NP2      PIM      Esperado  Resultado  Status
   ---------------------------------------------
   8.0      7.5      9.0      8.17       8.17       ✅ OK
   6.0      7.0      8.0      7.00       7.00       ✅ OK
   ...

==================================================
  RESUMO
==================================================

✅ Todos os testes passaram!
✅ Função C está funcionando corretamente!
```

### Método 2: Teste Manual no Python

1. **Abra o Python interativo:**
   ```bash
   python
   ```

2. **Execute os seguintes comandos:**
   ```python
   from sistema.calcular_media_wrapper import calcular_media, c_disponivel
   
   # Verificar se C está disponível
   print("Função C disponível:", c_disponivel())
   
   # Testar cálculo
   resultado = calcular_media(8.0, 7.5, 9.0)
   print(f"Média calculada: {resultado}")
   print(f"Esperado: 8.17")
   ```

**Saída esperada:**
```
Função C disponível: True  (ou False se não compilado)
Média calculada: 8.166666666666666
Esperado: 8.17
```

### Método 3: Teste no Sistema (Interface Web)

1. **Execute o sistema:**
   ```bash
   streamlit run interface/app.py
   ```

2. **Faça login como aluno ou professor**

3. **Acesse a área de notas:**
   - Como **Aluno**: Aba "Notas"
   - Como **Professor**: Aba "Minhas Disciplinas" → Lançar Notas

4. **Verifique se as médias estão sendo calculadas corretamente**

5. **A função C será usada automaticamente se estiver compilada**

### Método 4: Verificar Arquivo Compilado

**Windows:**
```powershell
# Verificar se o arquivo .dll existe
Test-Path sistema\calcular_media.dll
```

**Linux:**
```bash
# Verificar se o arquivo .so existe
ls -la sistema/calcular_media.so
```

**macOS:**
```bash
# Verificar se o arquivo .dylib existe
ls -la sistema/calcular_media.dylib
```

## 🔍 Interpretando os Resultados

### ✅ Função C Funcionando

Se você ver:
- `Função C disponível: True`
- Todos os testes passando
- Resultados corretos nos cálculos

**Significa:** A função C está compilada e funcionando perfeitamente!

### ⚠️ Função C Não Compilada (Mas Sistema Funcionando)

Se você ver:
- `Função C disponível: False`
- Mensagem: "Função C não está disponível (usando Python)"
- Todos os testes passando

**Significa:** O sistema está funcionando normalmente, mas usando Python em vez de C. Isso é **normal e esperado** se você não compilou a função C.

**Para compilar:**
- Windows: Execute `compilar_c.bat`
- Linux/Mac: Execute `./compilar_c.sh`

### ❌ Erros

Se você ver erros como:
- `ModuleNotFoundError`: Verifique se está na pasta correta do projeto
- `ImportError`: Verifique se o arquivo `calcular_media_wrapper.py` existe
- Erros de compilação: Verifique se o GCC está instalado

## 📊 Comparação de Performance

A função C oferece melhor performance, mas a diferença é mínima para este caso de uso. O importante é que **ambas funcionam corretamente**.

## 💡 Dicas

1. **A função C é opcional** - O sistema funciona perfeitamente sem ela
2. **Compilar é simples** - Basta executar o script de compilação
3. **Teste sempre após compilar** - Use `python testar_c.py` para verificar
4. **Não se preocupe** - Se não compilar, o sistema usa Python automaticamente

## 🆘 Problemas Comuns

### "Função C não está disponível"
**Solução:** Compile a função C usando `compilar_c.bat` (Windows) ou `./compilar_c.sh` (Linux/Mac)

### "gcc: command not found"
**Solução:** Instale o GCC:
- Windows: Instale MinGW-w64
- Linux: `sudo apt-get install gcc`
- macOS: `xcode-select --install`

### "Erro ao carregar biblioteca"
**Solução:** Verifique se o arquivo compilado está na pasta `sistema/` com o nome correto para seu sistema operacional

---

**Última atualização:** 2024


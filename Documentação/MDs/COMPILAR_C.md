# 🔧 Como Compilar a Função C

Este documento explica como compilar a função C `calcular_media.c` para uso no sistema ConektaAcademy.

## 📋 Pré-requisitos

Você precisa ter um compilador C instalado:

- **Windows:** [MinGW-w64](https://www.mingw-w64.org/) ou [MSVC](https://visualstudio.microsoft.com/)
- **Linux:** `gcc` (geralmente já instalado)
- **macOS:** Xcode Command Line Tools (`xcode-select --install`)

## 🚀 Compilação

### Windows

```powershell
# Com MinGW
gcc -shared -o sistema\calcular_media.dll sistema\calcular_media.c

# Com MSVC (Visual Studio)
cl /LD sistema\calcular_media.c /Fe:sistema\calcular_media.dll
```

### Linux

```bash
gcc -shared -fPIC -o sistema/calcular_media.so sistema/calcular_media.c
```

### macOS

```bash
gcc -shared -fPIC -o sistema/calcular_media.dylib sistema/calcular_media.c
```

## ✅ Verificação

Após compilar, você deve ter um dos seguintes arquivos na pasta `sistema/`:

- **Windows:** `calcular_media.dll`
- **Linux:** `calcular_media.so`
- **macOS:** `calcular_media.dylib`

## 📝 Notas Importantes

1. **O sistema funciona sem a função C** - Se a biblioteca não estiver compilada, o sistema usará o cálculo Python padrão
2. **A função C é opcional** - Não é necessário compilar para o sistema funcionar
3. **Performance** - A função C oferece melhor performance, mas a diferença é mínima para este caso de uso

## 🧪 Teste

Para testar se a função C está funcionando:

```python
from sistema.calcular_media_wrapper import calcular_media, c_disponivel

# Verificar se C está disponível
if c_disponivel():
    print("✅ Função C disponível!")
    resultado = calcular_media(8.0, 7.5, 9.0)
    print(f"Média calculada: {resultado}")
else:
    print("⚠️ Função C não disponível, usando Python")
    resultado = calcular_media(8.0, 7.5, 9.0)
    print(f"Média calculada: {resultado}")
```

## 🔍 Troubleshooting

### Erro: "gcc: command not found"
**Solução:** Instale o compilador C conforme seu sistema operacional

### Erro: "undefined reference"
**Solução:** Certifique-se de usar as flags corretas (`-shared -fPIC` no Linux/Mac)

### Biblioteca não carrega no Python
**Solução:** Verifique se o arquivo está na pasta `sistema/` e se tem o nome correto para seu sistema operacional


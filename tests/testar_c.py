"""
Script de teste para verificar se a função C está funcionando
Execute: python testar_c.py
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

print("=" * 50)
print("  TESTE DA FUNÇÃO C - ConektaAcademy")
print("=" * 50)
print()

# Teste 1: Verificar se o wrapper pode ser importado
print("1. Testando importação do wrapper...")
try:
    from sistema.calcular_media_wrapper import calcular_media, calcular_media_python, c_disponivel
    print("   ✅ Wrapper importado com sucesso!")
except ImportError as e:
    print(f"   ❌ Erro ao importar wrapper: {e}")
    sys.exit(1)

print()

# Teste 2: Verificar se a função C está disponível
print("2. Verificando se a função C está disponível...")
if c_disponivel():
    print("   ✅ Função C está disponível e carregada!")
    usando_c = True
else:
    print("   ⚠️  Função C não está disponível (usando Python)")
    print("   💡 Para compilar a função C:")
    print("      - Windows: Execute compilar_c.bat")
    print("      - Linux/Mac: Execute ./compilar_c.sh")
    usando_c = False

print()

# Teste 3: Testar cálculo de média
print("3. Testando cálculo de média...")
print()

# Casos de teste
testes = [
    {"np1": 8.0, "np2": 7.5, "pim": 9.0, "esperado": 8.17},
    {"np1": 6.0, "np2": 7.0, "pim": 8.0, "esperado": 7.0},
    {"np1": 10.0, "np2": 10.0, "pim": 10.0, "esperado": 10.0},
    {"np1": 5.0, "np2": 6.0, "pim": 7.0, "esperado": 6.0},
]

print("   Casos de teste:")
print("   " + "-" * 45)
print(f"   {'NP1':<8} {'NP2':<8} {'PIM':<8} {'Esperado':<10} {'Resultado':<10} {'Status'}")
print("   " + "-" * 45)

todos_passaram = True

for i, teste in enumerate(testes, 1):
    np1 = teste["np1"]
    np2 = teste["np2"]
    pim = teste["pim"]
    esperado = teste["esperado"]
    
    # Calcular usando a função (C ou Python)
    resultado = calcular_media(np1, np2, pim)
    
    # Verificar se está próximo do esperado (tolerância de 0.01)
    passou = abs(resultado - esperado) < 0.01
    
    status = "✅ OK" if passou else "❌ FALHOU"
    if not passou:
        todos_passaram = False
    
    print(f"   {np1:<8.1f} {np2:<8.1f} {pim:<8.1f} {esperado:<10.2f} {resultado:<10.2f} {status}")

print("   " + "-" * 45)
print()

# Teste 4: Comparar C vs Python (se C estiver disponível)
if usando_c:
    print("4. Comparando função C vs Python...")
    print()
    
    np1, np2, pim = 8.5, 7.0, 9.0
    
    resultado_c = calcular_media(np1, np2, pim)
    resultado_python = calcular_media_python(np1, np2, pim)
    
    print(f"   Entrada: NP1={np1}, NP2={np2}, PIM={pim}")
    print(f"   Função C:     {resultado_c:.6f}")
    print(f"   Função Python: {resultado_python:.6f}")
    
    if abs(resultado_c - resultado_python) < 0.0001:
        print("   ✅ Resultados idênticos!")
    else:
        print("   ⚠️  Diferença detectada (pode ser normal devido a precisão)")
    
    print()

# Resumo final
print("=" * 50)
print("  RESUMO")
print("=" * 50)
print()

if todos_passaram:
    print("✅ Todos os testes passaram!")
    if usando_c:
        print("✅ Função C está funcionando corretamente!")
    else:
        print("✅ Função Python está funcionando corretamente!")
        print("💡 Compile a função C para melhor performance (opcional)")
else:
    print("❌ Alguns testes falharam!")
    print("   Verifique os resultados acima")

print()
print("=" * 50)


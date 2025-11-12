"""
Wrapper Python para a função C de cálculo de média
Usa ctypes para chamar a função C compilada
"""

import os
import sys
import platform

# Tentar carregar a biblioteca C compilada
_C_LIBRARY = None
_C_AVAILABLE = False

def _load_c_library():
    """Tenta carregar a biblioteca C compilada"""
    global _C_LIBRARY, _C_AVAILABLE
    
    if _C_LIBRARY is not None:
        return _C_AVAILABLE
    
    try:
        import ctypes
        
        # Determinar o nome da biblioteca baseado no sistema operacional
        sistema = platform.system().lower()
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
        if sistema == 'windows':
            lib_name = 'calcular_media.dll'
        elif sistema == 'darwin':  # macOS
            lib_name = 'calcular_media.dylib'
        else:  # Linux e outros
            lib_name = 'calcular_media.so'
        
        lib_path = os.path.join(diretorio_atual, lib_name)
        
        # Tentar carregar a biblioteca
        if os.path.exists(lib_path):
            _C_LIBRARY = ctypes.CDLL(lib_path)
            
            # Configurar a assinatura da função
            _C_LIBRARY.calcular_media.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
            _C_LIBRARY.calcular_media.restype = ctypes.c_double
            
            _C_AVAILABLE = True
            return True
        else:
            # Biblioteca não encontrada - sistema funcionará sem ela
            _C_AVAILABLE = False
            return False
            
    except Exception as e:
        # Qualquer erro ao carregar - sistema funcionará sem a função C
        _C_AVAILABLE = False
        return False

# Tentar carregar na importação
_load_c_library()

def calcular_media_c(np1, np2, pim):
    """
    Calcula a média usando a função C (se disponível)
    Se a função C não estiver disponível, retorna None
    
    Args:
        np1: Nota da primeira avaliação (0-10)
        np2: Nota da segunda avaliação (0-10)
        pim: Nota do PIM (0-10)
    
    Returns:
        float: Média calculada ou None se a função C não estiver disponível
    """
    if not _C_AVAILABLE:
        return None
    
    try:
        import ctypes
        return float(_C_LIBRARY.calcular_media(
            ctypes.c_double(float(np1)),
            ctypes.c_double(float(np2)),
            ctypes.c_double(float(pim))
        ))
    except Exception:
        return None

def calcular_media_python(np1, np2, pim):
    """
    Calcula a média usando Python (fallback)
    
    Args:
        np1: Nota da primeira avaliação (0-10)
        np2: Nota da segunda avaliação (0-10)
        pim: Nota do PIM (0-10)
    
    Returns:
        float: Média calculada
    """
    return (float(np1) + float(np2) + float(pim)) / 3.0

def calcular_media(np1, np2, pim):
    """
    Calcula a média de três notas
    Tenta usar a função C primeiro, se não estiver disponível usa Python
    
    Args:
        np1: Nota da primeira avaliação (0-10)
        np2: Nota da segunda avaliação (0-10)
        pim: Nota do PIM (0-10)
    
    Returns:
        float: Média calculada
    """
    # Tentar usar função C
    resultado_c = calcular_media_c(np1, np2, pim)
    if resultado_c is not None:
        return resultado_c
    
    # Fallback para Python
    return calcular_media_python(np1, np2, pim)

def c_disponivel():
    """Verifica se a função C está disponível"""
    return _C_AVAILABLE


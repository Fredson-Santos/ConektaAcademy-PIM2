import sys
import os

# Adicionar o diretório raiz ao path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sistema.database import criar_tabelas
from terminal.menus.secretaria_menu import area_secretaria
from terminal.menus.professor_menu import area_professor
from terminal.menus.aluno_menu import area_aluno


# === SISTEMA PRINCIPAL ===
class SistemaAcademico:
    def __init__(self):
        criar_tabelas()

    # --- ÁREA DA SECRETARIA ---
    def area_secretaria(self, secretaria):
        area_secretaria(secretaria)

    # --- ÁREA DO PROFESSOR ---
    def area_professor(self, professor):
        area_professor(professor)

    # --- ÁREA DO ALUNO ---
    def area_aluno(self, aluno):
        area_aluno(aluno)

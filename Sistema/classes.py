from database import criar_tabelas
from menus.secretaria_menu import area_secretaria
from menus.professor_menu import area_professor
from menus.aluno_menu import area_aluno


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

"""
Módulo de Relatórios
Contém funções para gerar relatórios do sistema acadêmico
"""

from datetime import datetime
from io import BytesIO
import sys
import os

# Adicionar o diretório raiz ao path para imports absolutos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sistema import database as db
from sistema.funcoes import buscar_dados_completos_aluno, listar

# Tentar importar reportlab (opcional)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_DISPONIVEL = True
except ImportError:
    REPORTLAB_DISPONIVEL = False


def gerar_relatorio_pdf(matricula):
    """Gera relatório em PDF do aluno"""
    if not REPORTLAB_DISPONIVEL:
        return None
    
    try:
        # Buscar dados completos
        dados = buscar_dados_completos_aluno(matricula)
        
        if not dados or not dados['aluno']:
            return None
        
        aluno = dados['aluno']
        notas = dados['notas']
        presencas = dados['presencas']
        
        # Criar buffer para PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12
        )
        
        # Título
        story.append(Paragraph("RELATORIO ACADEMICO", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Dados do aluno
        story.append(Paragraph(f"<b>Nome:</b> {aluno[1]}", styles['Normal']))
        story.append(Paragraph(f"<b>Matricula:</b> {aluno[3] or 'N/A'}", styles['Normal']))
        story.append(Paragraph(f"<b>Email:</b> {aluno[2] or 'N/A'}", styles['Normal']))
        story.append(Paragraph(f"<b>Data do Relatorio:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Notas por Disciplina
        if notas:
            story.append(Paragraph("NOTAS POR DISCIPLINA", heading_style))
            
            # Criar tabela de notas
            table_data = [['Disciplina', 'NP1', 'NP2', 'PIM', 'Media']]
            
            for nota_disc in notas:
                np1 = nota_disc['np1'] if nota_disc['np1'] else 0
                np2 = nota_disc['np2'] if nota_disc['np2'] else 0
                pim = nota_disc['pim'] if nota_disc['pim'] else 0
                
                # Calcular média
                notas_validas = [n for n in [np1, np2, pim] if n and n > 0]
                media = sum(notas_validas) / len(notas_validas) if notas_validas else 0
                
                table_data.append([
                    nota_disc['disciplina'],
                    f"{np1:.1f}" if np1 else "-",
                    f"{np2:.1f}" if np2 else "-",
                    f"{pim:.1f}" if pim else "-",
                    f"{media:.1f}" if media > 0 else "-"
                ])
            
            table = Table(table_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
        else:
            story.append(Paragraph("NOTAS POR DISCIPLINA", heading_style))
            story.append(Paragraph("Nenhuma nota registrada.", styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Presenças
        if presencas:
            story.append(Paragraph("REGISTRO DE PRESENCAS", heading_style))
            
            # Calcular estatísticas
            total_dias = len(presencas)
            dias_presentes = sum(1 for _, p in presencas if p)
            percentual = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
            
            story.append(Paragraph(f"<b>Total de Dias:</b> {total_dias}", styles['Normal']))
            story.append(Paragraph(f"<b>Dias Presentes:</b> {dias_presentes}", styles['Normal']))
            story.append(Paragraph(f"<b>Taxa de Presenca:</b> {percentual:.1f}%", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Tabela de presenças
            pres_table_data = [['Data', 'Status']]
            for data, presente in presencas[:20]:  # Limitar a 20 registros
                status = "Presente" if presente else "Faltou"
                pres_table_data.append([data, status])
            
            if len(presencas) > 20:
                pres_table_data.append([f"... e mais {len(presencas) - 20} registros", ""])
            
            pres_table = Table(pres_table_data, colWidths=[3*inch, 2*inch])
            pres_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(pres_table)
        else:
            story.append(Paragraph("REGISTRO DE PRESENCAS", heading_style))
            story.append(Paragraph("Nenhum registro de presenca.", styles['Normal']))
        
        # Rodapé
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"<i>Relatorio gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}</i>", 
                                ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8)))
        
        # Gerar PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
    except Exception as e:
        return None


def gerar_dados_relatorio_turmas():
    """Gera dados para o relatório de turmas"""
    try:
        # Buscar todas as turmas
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, ano, professor_id, curso_id FROM turmas ORDER BY nome")
        turmas = cursor.fetchall()
        conn.close()
        
        if not turmas:
            return None, None, None, None
        
        # Preparar dados para o relatório
        dados_relatorio_turmas = []
        total_turmas = len(turmas)
        total_alunos_geral = 0
        
        for turma in turmas:
            turma_id = turma[0]
            nome_turma = turma[1]
            ano_turma = turma[2] if turma[2] else "N/A"
            professor_id = turma[3] if turma[3] else None
            curso_id = turma[4] if turma[4] else None
            
            # Buscar nome do curso
            curso_nome = "N/A"
            if curso_id:
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM cursos WHERE id = ?", (curso_id,))
                curso = cursor.fetchone()
                conn.close()
                if curso:
                    curso_nome = curso[0]
            
            # Buscar email do professor
            professor_email = "N/A"
            if professor_id:
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT email FROM usuarios WHERE id = ? AND tipo_usuario = 'professor'", (professor_id,))
                prof = cursor.fetchone()
                conn.close()
                if prof and prof[0]:
                    professor_email = prof[0]
            
            # Buscar alunos da turma
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE turma_id = ? AND tipo_usuario = 'aluno'", (nome_turma,))
            num_alunos = cursor.fetchone()[0]
            conn.close()
            total_alunos_geral += num_alunos
            
            dados_relatorio_turmas.append({
                "ID": turma_id,
                "Nome": nome_turma,
                "Ano": ano_turma,
                "Curso": curso_nome,
                "Professor": professor_email,
                "Nº de Alunos": num_alunos
            })
        
        media_alunos = total_alunos_geral / total_turmas if total_turmas > 0 else 0
        
        return dados_relatorio_turmas, total_turmas, total_alunos_geral, media_alunos
    except Exception as e:
        return None, None, None, None


def gerar_dados_relatorio_disciplinas():
    """Gera dados para o relatório de disciplinas"""
    try:
        # Buscar todas as disciplinas
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id, d.nome, d.carga_horaria, d.professor_id, d.curso_id, d.turma_id,
                   COALESCE(c.nome, 'Sem curso') as nome_curso
            FROM disciplinas d
            LEFT JOIN cursos c ON d.curso_id = c.id
            ORDER BY d.nome
        """)
        disciplinas = cursor.fetchall()
        conn.close()
        
        if not disciplinas:
            return None, None, None, None
        
        # Preparar dados para o relatório
        dados_relatorio_disc = []
        total_disciplinas = len(disciplinas)
        total_carga_horaria = 0
        
        for disc in disciplinas:
            disc_id = disc[0]
            nome_disc = disc[1]
            carga_horaria = disc[2] if disc[2] else 0
            professor_id = disc[3] if disc[3] else None
            curso_id = disc[4] if disc[4] else None
            turma_id = disc[5] if disc[5] else None
            nome_curso = disc[6] if disc[6] else "N/A"
            
            total_carga_horaria += carga_horaria
            
            # Buscar nome do professor
            professor_nome = "N/A"
            if professor_id:
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM usuarios WHERE id = ? AND tipo_usuario = 'professor'", (professor_id,))
                prof = cursor.fetchone()
                conn.close()
                if prof and prof[0]:
                    professor_nome = prof[0]
            
            # Contar alunos da disciplina (via turma)
            num_alunos_disc = 0
            if turma_id:
                conn = db.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE turma_id = ? AND tipo_usuario = 'aluno'", (turma_id,))
                num_alunos_disc = cursor.fetchone()[0]
                conn.close()
            
            dados_relatorio_disc.append({
                "ID": disc_id,
                "Nome": nome_disc,
                "Carga Horária": carga_horaria,
                "Curso": nome_curso,
                "Professor": professor_nome,
                "Turma": turma_id if turma_id else "N/A",
                "Nº de Alunos": num_alunos_disc
            })
        
        media_carga = total_carga_horaria / total_disciplinas if total_disciplinas > 0 else 0
        
        return dados_relatorio_disc, total_disciplinas, total_carga_horaria, media_carga
    except Exception as e:
        return None, None, None, None


def gerar_dados_relatorio_cursos():
    """Gera dados para o relatório de cursos"""
    try:
        # Buscar todos os cursos
        cursos = listar("cursos", "id", "nome", "inicio", "duracao")
        
        if not cursos:
            return None, None, None
        
        # Preparar dados para o relatório
        dados_relatorio_cursos = []
        total_cursos = len(cursos)
        
        for curso in cursos:
            curso_id = curso[0]
            nome_curso = curso[1]
            inicio = curso[2] if len(curso) > 2 and curso[2] else "N/A"
            duracao = curso[3] if len(curso) > 3 and curso[3] else "N/A"
            
            # Contar turmas do curso
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM turmas WHERE curso_id = ?", (curso_id,))
            num_turmas = cursor.fetchone()[0]
            conn.close()
            
            # Contar disciplinas do curso
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM disciplinas WHERE curso_id = ?", (curso_id,))
            num_disciplinas = cursor.fetchone()[0]
            conn.close()
            
            # Contar alunos do curso (via turmas)
            conn = db.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM usuarios u
                INNER JOIN turmas t ON u.turma_id = t.nome
                WHERE t.curso_id = ? AND u.tipo_usuario = 'aluno'
            """, (curso_id,))
            num_alunos = cursor.fetchone()[0]
            conn.close()
            
            dados_relatorio_cursos.append({
                "ID": curso_id,
                "Nome": nome_curso,
                "Início": inicio,
                "Duração": f"{duracao} semestres" if duracao != "N/A" else "N/A",
                "Nº de Turmas": num_turmas,
                "Nº de Disciplinas": num_disciplinas,
                "Nº de Alunos": num_alunos
            })
        
        total_turmas_curso = sum(c['Nº de Turmas'] for c in dados_relatorio_cursos)
        
        return dados_relatorio_cursos, total_cursos, total_turmas_curso
    except Exception as e:
        return None, None, None


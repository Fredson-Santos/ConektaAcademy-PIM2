def consultar_aluno(matricula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT nome from usuarios WHERE matricula = ?",(matricula,))
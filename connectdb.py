import sqlite3 as sql


def connection():
        conn = sql.connect('cursos.sqlite3',check_same_thread=False)
        conn.row_factory = sql.Row
        return conn

def select():
        conn = connection()
        return conn.execute('SELECT id,nome,descricao,carga_horaria FROM cursos;').fetchall()


def insert(id=None,nome=None,descricao=None,carga_horaria=None):
        conn = connection()
        insere = conn.execute('''INSERT INTO cursos
                VALUES (
                ?,
                ?,
                ?,
                ?
                );''',(id,nome,descricao,carga_horaria))
        conn.commit()
        return insere

def consulta_edit(id):
        conn = connection()
        curso = conn.execute("select * from cursos where id=?",[id]).fetchone()
        return curso

def edit(nome,descricao,cargah,id):
        conn = connection()
        editar = conn.execute('UPDATE cursos SET nome = ?, descricao = ?, carga_horaria = ? WHERE id = ?;',[nome,descricao,cargah,id])
        conn.commit()
        return editar

def delete(id):
        conn = connection()
        delete = conn.execute('DELETE FROM cursos WHERE id = ?',[id])
        conn.commit()
        return delete
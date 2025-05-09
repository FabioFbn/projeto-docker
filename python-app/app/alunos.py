from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection

alunos_bp = Blueprint('alunos', __name__)

# Listar todos os alunos
@alunos_bp.route('/alunos', methods=['GET'])
def get_alunos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT aluno_id, nome, endereco, cidade, estado, cep, pais, telefone FROM alunos')
    alunos = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)

    return jsonify([
        {
            "aluno_id": aluno[0],
            "nome": aluno[1],
            "endereco": aluno[2],
            "cidade": aluno[3],
            "estado": aluno[4],
            "cep": aluno[5],
            "pais": aluno[6],
            "telefone": aluno[7]
        }
        for aluno in alunos
    ])

# Cadastrar um novo aluno
@alunos_bp.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    aluno_id = data.get('aluno_id')
    nome = data.get('nome')
    endereco = data.get('endereco')
    cidade = data.get('cidade')
    estado = data.get('estado')
    cep = data.get('cep')
    pais = data.get('pais')
    telefone = data.get('telefone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING aluno_id
        ''',
        (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone)
    )
    aluno_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "aluno_id": aluno_id,
        "nome": nome,
        "endereco": endereco,
        "cidade": cidade,
        "estado": estado,
        "cep": cep,
        "pais": pais,
        "telefone": telefone
    }), 201

# Atualizar um aluno existente
@alunos_bp.route('/alunos/<string:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    nome = data.get('nome')
    endereco = data.get('endereco')
    cidade = data.get('cidade')
    estado = data.get('estado')
    cep = data.get('cep')
    pais = data.get('pais')
    telefone = data.get('telefone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE alunos
        SET nome = %s, endereco = %s, cidade = %s, estado = %s, cep = %s, pais = %s, telefone = %s
        WHERE aluno_id = %s
        ''',
        (nome, endereco, cidade, estado, cep, pais, telefone, aluno_id)
    )
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "aluno_id": aluno_id,
        "nome": nome,
        "endereco": endereco,
        "cidade": cidade,
        "estado": estado,
        "cep": cep,
        "pais": pais,
        "telefone": telefone
    })

# Excluir um aluno
@alunos_bp.route('/alunos/<string:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM alunos WHERE aluno_id = %s', (aluno_id,))
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({"message": f"Aluno com id {aluno_id} foi excluído com sucesso"})
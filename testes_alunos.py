import pytest
from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    """Testa a rota principal."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API CRUD para a tabela alunos da base escola"}

def test_get_alunos(client, mocker):
    """Testa a rota de listar alunos."""
    # Simulação (mock) da conexão ao banco de dados
    mock_conn = mocker.patch('database.get_db_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'João', 'Rua A', 'Cidade X', 'Estado Y', '12345-678', 'Brasil', '1111-1111')
    ]

    response = client.get('/alunos')
    assert response.status_code == 200
    assert response.get_json() == [
        {
            "aluno_id": 1,
            "nome": "João",
            "endereco": "Rua A",
            "cidade": "Cidade X",
            "estado": "Estado Y",
            "cep": "12345-678",
            "pais": "Brasil",
            "telefone": "1111-1111"
        }
    ]

def test_create_aluno(client, mocker):
    """Testa a rota de cadastro de aluno."""
    # Mock da conexão ao banco de dados
    mock_conn = mocker.patch('database.get_db_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]

    aluno = {
        "aluno_id": 1,
        "nome": "Maria",
        "endereco": "Rua B",
        "cidade": "Cidade Y",
        "estado": "Estado Z",
        "cep": "12345-123",
        "pais": "Brasil",
        "telefone": "2222-2222"
    }

    response = client.post('/alunos', json=aluno)
    assert response.status_code == 201
    assert response.get_json() == aluno

def test_delete_aluno(client, mocker):
    """Testa a exclusão de um aluno."""
    # Mock da conexão ao banco de dados
    mock_conn = mocker.patch('database.get_db_connection')
    mock_cursor = mocker.Mock()
    mock_conn.return_value.cursor.return_value = mock_cursor

    response = client.delete('/alunos/1')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Aluno com id 1 foi excluído com sucesso"}
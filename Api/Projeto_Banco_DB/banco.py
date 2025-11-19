import sqlite3

def conectar_banco():
    """
    Cria (ou abre, se já existir) o banco de dados local 'banco.sqlite'.
    Retorna o objeto de conexão.
    """
    conexao = sqlite3.connect("banco.sqlite")
    return conexao


def criar_tabelas():
    """
    Cria as tabelas principais do sistema bancário.
    - clientes
    - contas
    - transacoes
    Executa apenas se não existirem.
    """
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            data_nascimento TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            agencia TEXT DEFAULT '0001',
            saldo REAL DEFAULT 0.0,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conta_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (conta_id) REFERENCES contas (id)
        )
        """)

        conexao.commit()
        print("Tabelas criadas com sucesso!")

    except sqlite3.Error as erro:
        print(" Erro ao criar tabelas:", erro)
        conexao.rollback()

    finally:
        conexao.close()


criando_tabelas = criar_tabelas()
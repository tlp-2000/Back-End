import sqlite3
from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco

    # ---------------------------
    # SALVAR CLIENTE NO BANCO
    # ---------------------------
    def salvar(self):
        """
        Insere o cliente no banco de dados.
        Se o CPF já existir, ignora e avisa.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            # Inserção de dados do cliente
            cursor.execute("""
                INSERT INTO clientes (nome, cpf, data_nascimento, endereco)
                VALUES (?, ?, ?, ?)
            """, (self.nome, self.cpf, self.data_nascimento, self.endereco))

            conexao.commit()
            print(f"Cliente {self.nome} salvo com sucesso!")

        except sqlite3.IntegrityError:
            print(f"Já existe um cliente com o CPF {self.cpf}.")
        except sqlite3.Error as erro:
            print("Erro ao salvar cliente:", erro)
        finally:
            conexao.close()

    # ---------------------------
    # BUSCAR CLIENTE PELO CPF
    # ---------------------------
    @staticmethod
    def buscar_por_cpf(cpf):
        """
        Retorna um objeto Cliente a partir do CPF, se existir.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, cpf, data_nascimento, endereco FROM clientes WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()

            if resultado:
                nome, cpf, data_nascimento, endereco = resultado
                print(f"Cliente encontrado: {nome}")
                return Cliente(nome, cpf, data_nascimento, endereco)
            else:
                print("Nenhum cliente encontrado com esse CPF.")
                return None

        except sqlite3.Error as erro:
            print("Erro ao buscar cliente:", erro)
        finally:
            conexao.close()

    # ---------------------------
    # LISTAR TODOS OS CLIENTES
    # ---------------------------
    @staticmethod
    def listar_todos():
        """
        Exibe todos os clientes cadastrados no banco.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, cpf, data_nascimento, endereco FROM clientes")
            clientes = cursor.fetchall()

            if not clientes:
                print("Nenhum cliente cadastrado.")
                return

            print("\n=== LISTA DE CLIENTES ===")
            for id, nome, cpf, dta, endereco in clientes:
                print(f"ID: {id} | Nome: {nome} | CPF: {cpf} | Nascimento: {dta} | Endereço: {endereco}")

        except sqlite3.Error as erro:
            print("Erro ao listar clientes:", erro)
        finally:
            conexao.close()

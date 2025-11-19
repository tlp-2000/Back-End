from datetime import datetime
import sqlite3

class Transacao:

    def __init__(self, conta_id, tipo,valor):
        """
        conta_id (int) -> ID da conta
        tipo (str) -> "deposito" / "saque"
        valor (float)
        data -> gerada automaticamente
        """
        self._conta_id = conta_id
        self._tipo = tipo
        self._valor = valor
        self._data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # formato ISO


    def salvar(self):
        """
        Insere uma transação na tabela transacoes.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO transacoes (conta_id, tipo, data, valor)
                VALUES (?, ?, ?, ?)
            """, (self._conta_id, self._tipo, self._data, self._valor))

            conexao.commit()
            print(f"Transação '{self._tipo}' salva com sucesso para a conta {self._conta_id}.")

        except sqlite3.Error as e:
            print("Erro ao salvar transação:", e)

        finally:
            conexao.close()


    @staticmethod
    def listar_por_conta(conta_id):
        """
        Lista todas as transações de uma conta.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, tipo, data, valor
                FROM transacoes
                WHERE conta_id = ?
            """, (conta_id,))

            transacoes = cursor.fetchall()

            if transacoes:
                print(f"\n=== Transações da conta {conta_id} ===")
                for id, tipo, data, valor in transacoes:
                    print(f"ID: {id} | Tipo: {tipo} | Data: {data} | Valor: {valor:.2f}")
            else:
                print("Nenhuma transação encontrada para esta conta.")

        except sqlite3.Error as e:
            print("Erro ao listar:", e)

        finally:
            conexao.close()


    @staticmethod
    def listar_todas():
        """
        Lista todas as transações do banco.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, conta_id, tipo, data, valor 
                FROM transacoes
            """)

            transacoes = cursor.fetchall()

            if transacoes:
                print("\n=== TODAS AS TRANSAÇÕES ===")
                for id, conta_id, tipo, data, valor in transacoes:
                    print(f"ID: {id} | Conta: {conta_id} | Tipo: {tipo} | Data: {data} | Valor: {valor:.2f}")
            else:
                print("Nenhuma transação registrada.")

        except sqlite3.Error as e:
            print("Erro ao listar:", e)

        finally:
            conexao.close()


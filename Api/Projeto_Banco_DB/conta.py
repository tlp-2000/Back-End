import sqlite3

import sqlite3

class Conta:
    def __init__(self, cliente_id, numero, agencia="0001", conta_id=None, saldo=0.0):
        """
        Construtor da classe Conta.
        """
        self._conta_id = conta_id
        self._cliente_id = cliente_id
        self._numero = numero
        self._agencia = agencia
        self._saldo = saldo

    # ========================================================
    # MÉTODO: salvar()
    # ========================================================
    def salvar(self):
        """
        Insere uma nova conta no banco de dados.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO contas (cliente_id, numero, agencia, saldo)
                VALUES (?, ?, ?, ?)
            """, (self._cliente_id, self._numero, self._agencia, self._saldo))

            conexao.commit()

            # Recupera o ID gerado automaticamente
            self._conta_id = cursor.lastrowid

            print(f"Conta {self._numero} salva com sucesso! (ID: {self._conta_id})")

        except sqlite3.IntegrityError:
            print(f"Já existe uma conta com o número {self._numero}.")

        except sqlite3.Error as erro:
            print("Erro ao salvar conta:", erro)

        finally:
            conexao.close()

    # ========================================================
    # MÉTODO: buscar_por_numero()
    # ========================================================
    @staticmethod
    def buscar_por_numero(numero):
        """
        Retorna um objeto Conta e também o ID da conta.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, cliente_id, numero, agencia, saldo
                FROM contas
                WHERE numero = ?
            """, (numero,))

            resultado = cursor.fetchone()

            if resultado:
                conta_id, cliente_id, numero, agencia, saldo = resultado

                conta = Conta(
                    cliente_id=cliente_id,
                    numero=numero,
                    agencia=agencia,
                    saldo=saldo,
                    conta_id=conta_id
                )

                print(f"Conta encontrada: Nº {numero} | ID {conta_id}")
                return conta

            print("Nenhuma conta encontrada com esse número.")
            return None

        except sqlite3.Error as erro:
            print("Erro ao buscar conta:", erro)

        finally:
            conexao.close()

    # ========================================================
    # MÉTODO: buscar_por_id()
    # ========================================================
    @staticmethod
    def buscar_por_id(conta_id):
        """
        Retorna uma conta pesquisando pelo ID.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, cliente_id, numero, agencia, saldo
                FROM contas
                WHERE id = ?
            """, (conta_id,))

            resultado = cursor.fetchone()

            if resultado:
                conta_id, cliente_id, numero, agencia, saldo = resultado

                conta = Conta(
                    cliente_id=cliente_id,
                    numero=numero,
                    agencia=agencia,
                    saldo=saldo,
                    conta_id=conta_id
                )

                print(f"Conta encontrada pelo ID {conta_id}.")
                return conta

            print("Nenhuma conta encontrada com esse ID.")
            return None

        except sqlite3.Error as erro:
            print("Erro ao buscar a conta:", erro)

        finally:
            conexao.close()

    

    # ========================================================
    # MÉTODO: listar_contas()
    # ========================================================
    @staticmethod
    def listar_contas():
        """
        Lista todas as contas cadastradas no banco SQLite.

        - Usa comando SQL SELECT sem cláusula WHERE.
        - Exibe as contas no terminal.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            # Corrigido: vírgula removida antes do FROM
            cursor.execute("""
                SELECT id, cliente_id, numero, agencia, saldo
                FROM contas
            """)

            contas = cursor.fetchall()

            if contas:
                print("\n=== 🏦 LISTA DE CONTAS CADASTRADAS ===")
                for id, cliente_id, numero, agencia, saldo in contas:
                    print(f"ID: {id} | Cliente_ID: {cliente_id} | "
                          f"Número: {numero} | Agência: {agencia} | Saldo: R${saldo:.2f}")
            else:
                print("Nenhuma conta cadastrada no banco de dados.")

        except sqlite3.Error as erro:
            print("Erro ao listar as contas:", erro)

        finally:
            conexao.close()
            

    def atualizar_saldo(self,novo_saldo):
        """
        Atualiza o saldo da conta no banco de dados SQLite.

        Parâmetros:
            novo_saldo (float): O novo saldo a ser atualizado.
        """
        try:
            conexao = sqlite3.connect("banco.sqlite")
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE contas
                SET saldo = ?
                WHERE numero = ?
            """, (novo_saldo, self._numero))

            conexao.commit()
            self._saldo = novo_saldo  # Atualiza o saldo do objeto também
            print(f"Saldo da conta {self._numero} atualizado para R${novo_saldo:.2f}.")

        except sqlite3.Error as erro:
            print("Erro ao atualizar o saldo:", erro)

        finally:
            conexao.close()
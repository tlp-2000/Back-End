import sqlite3
from conta import Conta
from transaçoes import Transacao


# ============================
# FUNÇÃO PARA CADASTRAR CLIENTE
# ============================

def cadastrar_cliente():
    print("\n=== CADASTRAR CLIENTE ===")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    data = input("Data de nascimento (dd/mm/aaaa): ")
    end = input("Endereço: ")

    try:
        conexao = sqlite3.connect("banco.sqlite")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO clientes (nome, cpf, data_nascimento, endereco)
            VALUES (?, ?, ?, ?)
        """, (nome, cpf, data, end))

        conexao.commit()
        print("Cliente cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print("Erro: Já existe um cliente com esse CPF.")

    finally:
        conexao.close()


def criar_conta():
    try:
        numero = int(input("Número da conta: "))
        cliente_id = int(input("CPF do cliente: "))
        conta = Conta(cliente_id=cliente_id, numero=numero)
        conta.salvar()
        print("CONTA CRIADA COM SUCESSO!",conta)

        conta.buscar_por_numero(numero)


    except ValueError:
        print("Número de conta inválido. Deve ser um número inteiro.")
        return None
          


def deposito():
    try:
        numero = int(input("Número da conta: "))
        conta = Conta.buscar_por_numero(numero)

        if conta is None:
            print("Conta não encontrada.")
            return 

        valor = float(input("Valor do depósito: "))
        if valor <= 0:
            print("Valor de depósito deve ser positivo.")
            return

        # calcula o novo saldo
        novo_saldo = conta._saldo + valor

        # atualiza no banco e no objeto
        conta.atualizar_saldo(novo_saldo)

        transacao = Transacao(
            conta_id = conta._conta_id,
            valor = valor,
            tipo = "DEPÓSITO"
        )
        
        transacao.salvar()

        print(f"Depósito de R${valor:.2f} realizado com sucesso.")

    except ValueError:
        print("Número da conta ou valor inválido.")



def saque():
    try:
        numero = int(input("DIGITE O NUMERO DA CONTA: "))
        conta = Conta.buscar_por_numero(numero)

        if not conta:
            print("CONTA NAO ENCONTRADA")
            return

        else:
            try:
                valor_saque = float(input("DIGITE O VALOR DO SAQUE: "))

                if valor_saque <= 0:
                    print("O valor do saque deve ser positivo.")
                    return
                
                if conta._saldo < valor_saque:
                    print("NAO POSSUI ESSE VALOR NA CONTA DISPONIVEL PARA SACAR")
                    return 

                novo_saldo = conta._saldo - valor_saque
                conta.atualizar_saldo(novo_saldo)

                transacao = Transacao(conta_id=conta._conta_id, tipo="saque", valor=valor_saque)
                transacao.salvar()

                print(f"Depósito de R${valor_saque:.2f} realizado com sucesso.")

            except ValueError:
                print("VALOR DE SAQUE INVALIDO")

    except ValueError:
        print("Número da conta")


# ============================
# FUNÇÃO PRINCIPAL (MENU)
# ============================

def menu():
    while True:
        print("\n===== SISTEMA BANCÁRIO =====")
        print("1 - Cadastrar cliente")
        print("2 - Criar conta")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Sair")

        opc = input("Escolha uma opção: ")

        if opc == "1":
            cadastrar_cliente()

        elif opc == "2":
            criar_conta()

        elif opc == "3":
            deposito()

        elif opc == "4":
            saque()

        elif opc == "5":
            print("Encerrando o sistema...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

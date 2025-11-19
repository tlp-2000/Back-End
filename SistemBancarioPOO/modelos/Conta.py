import random
from abc import ABC, abstractmethod
from datetime import datetime


# ========================================
# CLASSE ABSTRATA DE TRANSACAO
# ========================================
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


# ========================================
# CLASSE DE DEPÓSITO
# ========================================
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.deposito(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ========================================
# CLASSE DE SAQUE
# ========================================
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ========================================
# CLASSE HISTÓRICO
# ========================================
class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "Operação": transacao.__class__.__name__,
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Valor": transacao.valor
        })

    def __str__(self):
        if not self._transacoes:
            return "Nenhuma transação realizada."
        linhas = [
            f"{t['Data']} | {t['Operação']} | R${t['Valor']:.2f}"
            for t in self._transacoes
        ]
        return "\n".join(linhas)


# ========================================
# CLASSE CONTA
# ========================================
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self.historico = Historico()
        self._numero_saques = 0

    @property
    def saldo(self):
        return self._saldo

    def deposito(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
            return True
        else:
            print("Valor inválido para depósito.")
            return False

    def sacar(self, valor, limite=500, LIMITE_SAQUES=3):
        if valor <= 0:
            print("Valor inválido para saque.")
            return False

        if valor > self._saldo:
            print("Operação falhou. Saldo insuficiente.")
            return False
        elif valor > limite:
            print("Operação falhou. Valor acima do limite de saque.")
            return False
        elif self._numero_saques >= LIMITE_SAQUES:
            print("Operação falhou. Limite de saques atingido.")
            return False
        else:
            self._saldo -= valor
            self._numero_saques += 1
            print(f"Saque de R${valor:.2f} realizado com sucesso.")
            return True

    def __str__(self):
        return f"Agência: {self._agencia} | Conta: {self._numero} | Saldo: R${self._saldo:.2f}"


# ========================================
# CLASSE CONTA CORRENTE
# ========================================
class ContaConrente(Conta):
    def __init__(self, cliente, numero, limite=500, LIMITE_SAQUE=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.LIMITE_SAQUE = LIMITE_SAQUE


# ========================================
# CLASSE CLIENTE
# ========================================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self._contas = []

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def listar_contas(self):
        for conta in self._contas:
            print(conta)


# ========================================
# CLASSE PESSOA FÍSICA
# ========================================
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento


# ========================================
# FUNÇÕES DE MENU
# ========================================
def menu():
    print("""
    ========== MENU ==========
    [c]  Cadastrar Cliente
    [cc] Criar Conta
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [l]  Listar Contas
    [q]  Sair
    ==========================
    """)
    return input("Escolha uma opção: ").lower()


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "c":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            data = input("Data de nascimento (AAAA-MM-DD): ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(nome, cpf, data, endereco)
            clientes.append(cliente)
            print(" Cliente cadastrado com sucesso!\n")

        elif opcao == "cc":
            if not clientes:
                print(" Nenhum cliente cadastrado. Cadastre um cliente primeiro.\n")
                continue
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c._cpf == cpf), None)
            if not cliente:
                print("Cliente não encontrado.\n")
                continue
            numero = len(contas) + 1
            conta = ContaConrente(cliente, numero)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print(f" Conta criada com sucesso! Número: {numero}\n")

        elif opcao == "d":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c._cpf == cpf), None)
            if not cliente or not cliente._contas:
                print("Cliente não encontrado ou sem conta.\n")
                continue
            valor = float(input("Valor do depósito: "))
            conta = cliente._contas[0]
            deposito = Deposito(valor)
            cliente.realizar_transacao(conta, deposito)

        elif opcao == "s":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c._cpf == cpf), None)
            if not cliente or not cliente._contas:
                print("Cliente não encontrado ou sem conta.\n")
                continue
            valor = float(input("Valor do saque: "))
            conta = cliente._contas[0]
            saque = Saque(valor)
            cliente.realizar_transacao(conta, saque)

        elif opcao == "e":
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c._cpf == cpf), None)
            if not cliente or not cliente._contas:
                print("Cliente não encontrado ou sem conta.\n")
                continue
            conta = cliente._contas[0]
            print("\n--- Histórico de Transações ---")
            print(conta.historico)
            print("-------------------------------\n")

        elif opcao == "l":
            print("\n--- Contas Cadastradas ---")
            for cliente in clientes:
                print(f"Cliente: {cliente._nome}")
                cliente.listar_contas()
            print("---------------------------\n")

        elif opcao == "q":
            print("Saindo do sistema... ")
            break

        else:
            print("Opção inválida!\n")


# ========================================
# EXECUÇÃO PRINCIPAL
# ========================================
if __name__ == "__main__":
    main()

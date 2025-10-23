import random
from abc import ABC, abstractmethod
from datetime import datetime


# ========================================
# CLASSE ABSTRATA DE TRANSACAO
# ========================================
class Transacao(ABC):
    """Classe abstrata base para transações bancárias."""

    @abstractmethod
    def registrar(self, conta):
        """Método abstrato para registrar uma transação em uma conta."""
        pass


# ========================================
# CLASSE DE DEPÓSITO
# ========================================
class Deposito(Transacao):
    """Classe que representa uma transação de depósito."""

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        self._valor = valor

    def registrar(self, conta):
        """Registra o depósito na conta e adiciona ao histórico."""
        sucesso_transacao = conta.deposito(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ========================================
# CLASSE DE SAQUE
# ========================================
class Saque(Transacao):
    """Classe que representa uma transação de saque."""

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra o saque na conta e adiciona ao histórico."""
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ========================================
# CLASSE HISTÓRICO
# ========================================
class Historico:
    """Classe responsável por armazenar e listar o histórico de transações."""

    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação com data e valor ao histórico."""
        self._transacoes.append({
            "Operaçao": transacao.__class__.__name__,
            "DATA": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "VALOR": transacao.valor
        })

    def listar_transacao(self):
        """Retorna a lista de transações registradas."""
        return self._transacoes

    def __str__(self):
        """Exibe o histórico em formato legível."""
        linhas = []
        for a in self._transacoes:
            linhas.append(f"{a['DATA']} | {a['Operaçao']} | {a['VALOR']:.2F}")
        return "\n".join(linhas) if linhas else "Nenhum Transaçao Realizada"


# ========================================
# CLASSE CONTA
# ========================================
class Conta:
    """Classe que representa uma conta bancária genérica."""

    def __init__(self, cliente, numero: int, agencia: str = "0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self.historico = Historico()

    # ================================
    # Propriedades e Setters
    # ================================
    @property
    def saldo(self):
        """Retorna o saldo atual."""
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        """Define o saldo, impedindo valores negativos."""
        if valor > 0:
            self._saldo = valor
        else:
            raise ValueError('ERRO! Não pode ter saldo negativo')

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, nome):
        self._cliente = nome

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, novo_numero=None):
        """Gera um novo número de conta aleatório."""
        b = random.randint(0, 10)
        novo_numero = b
        self._numero = novo_numero

    @property
    def agencia(self):
        return self._agencia

    @agencia.setter
    def agencia(self, a=None):
        """Define uma nova agência aleatória."""
        a = random.randint(0, 10)
        try:
            a = str(a)
        except (TypeError, ValueError) as erro:
            return f'HOUVE UM ERRO {erro}'
        self._agencia = a

    # ================================
    # Métodos principais da conta
    # ================================
    def ver_saldo(self):
        """Retorna o saldo formatado."""
        return f"O saldo atual é de R${self._saldo:.2f}"

    def deposito(self, valor) -> bool:
        """Realiza depósito e atualiza saldo."""
        try:
            valor = float(valor)
        except (ValueError, TypeError) as erro:
            return f'ERRO NA DIGITAÇÃO DO VALOR {erro}'

        if valor > 0:
            self._saldo += valor
            print(f"Saldo atualizado! Valor R${self._saldo:.2f}")
            return True
        else:
            print("Valor inválido para depósito.")
            return False

    def sacar(self, valor_sacar: float, LIMITE_SAQUES=None, limite=None) -> bool:
        """Realiza saque, verificando limites e saldo."""
        if not hasattr(self, "_numero_saques"):
            self._numero_saques = 0

        # Caso sem limites definidos
        if limite is None or LIMITE_SAQUES is None:
            if valor_sacar > 0:
                if valor_sacar > self._saldo:
                    print("Operação falhou. Saldo insuficiente.")
                    return False
                self._saldo -= valor_sacar
                self._numero_saques += 1
                print(f"Saque realizado com sucesso no valor de R${valor_sacar:.2f}")
                return True
            else:
                print("Valor inválido para saque.")
                return False

        # Caso com limites definidos
        else:
            if isinstance(valor_sacar, float):
                excedeu_saldo = valor_sacar > self._saldo
                excedeu_valor_saque = valor_sacar > limite
                excedeu_saques = self._numero_saques >= LIMITE_SAQUES

                if excedeu_saldo:
                    print("Operação falhou. Saldo insuficiente.")
                    return False
                elif excedeu_valor_saque:
                    print("Operação falhou. Valor acima do limite de saque.")
                    return False
                elif excedeu_saques:
                    print("Operação falhou. Limite de saques excedido.")
                    return False
                elif valor_sacar > 0:
                    self._saldo -= valor_sacar
                    self._numero_saques += 1
                    print(f"Saque realizado com sucesso no valor de R${valor_sacar:.2f}")
                    return True
                else:
                    print("Valor inválido para saque.")
                    return False
            else:
                print("Tipo de valor inválido para saque.")
                return False

    @classmethod
    def adicionar_conta(cls, cliente, numero: int):
        """Cria e retorna uma nova conta vinculada a um cliente."""
        return cls(cliente, numero)


# ========================================
# CLASSE CONTA CORRENTE (HERDA DE CONTA)
# ========================================
class ContaConrente(Conta):
    """Classe que representa uma conta corrente com limites."""

    def __init__(self, cliente, numero: int, limite: float = 500, LIMITE_SAQUE: int = 3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.LIMITE_SAQUE = LIMITE_SAQUE


# ========================================
# CLASSE CLIENTE
# ========================================
class Cliente:
    """Classe que representa um cliente genérico."""

    def __init__(self, endereco):
        self.endereco = endereco
        self._contas = []

    def adicionar_conta(self, conta):
        """Adiciona uma conta ao cliente."""
        if isinstance(conta, Conta):
            self._contas.append(conta)
            print("Conta adicionada com sucesso ao cliente.")
        else:
            return 'Erro ao adicionar a conta'

    def realizar_transaçao(self, conta, transacao: Transacao):
        """Executa uma transação (depósito ou saque) em uma conta."""
        if isinstance(conta, Conta):
            transacao.registrar(conta)

    def listar_contas(self):
        """Lista todas as contas associadas ao cliente."""
        if not self._contas:
            print("Nenhuma conta associada ao cliente.")
        else:
            for conta in self._contas:
                print(f"Agência: {conta.agencia} | Número: {conta.numero} | Saldo: R${conta.saldo:.2f}")


# ========================================
# CLASSE PESSOA FÍSICA (HERDA DE CLIENTE)
# ========================================
class PessoaFisica(Cliente):
    """Classe que representa um cliente pessoa física."""

    def __init__(self, nome: str, cpf: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento


# ========================================
# TESTE PRINCIPAL
# ========================================
if __name__ == "__main__":
    # Criação do cliente e da conta
    cliente = PessoaFisica("Gon", "12345678900", "2000-01-01", "Rua da Lua")
    conta = ContaConrente(cliente, 1)

    # Associação da conta ao cliente
    cliente.adicionar_conta(conta)

    # Realização de depósito e saque
    deposito = Deposito(200.0)
    cliente.realizar_transaçao(conta, deposito)

    saque = Saque(50.0)
    cliente.realizar_transaçao(conta, saque)

    # Exibição do histórico de transações
    print("\nHistórico de transações:")
    print(conta.historico)

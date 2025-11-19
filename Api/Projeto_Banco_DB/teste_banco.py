from conta import Conta           # importe conforme o nome do seu arquivo
from transaçoes import Transacao   # idem
import sqlite3
from datetime import datetime


print("\n=== TESTE 1: Criando uma CONTA ===")
conta_teste = Conta(cliente_id=1, numero=9999)
conta_teste.salvar()


print("\n=== TESTE 2: Buscando a conta criada ===")
conta_encontrada = Conta.buscar_por_numero(9999)
if conta_encontrada:
    print(f"Conta encontrada: Agência {conta_encontrada._agencia}, Saldo: {conta_encontrada._saldo}")


print("\n=== TESTE 3: Criando TRANSAÇÃO de DEPÓSITO ===")
t = Transacao(
    conta_id=1,
    valor=250.00,
    tipo="deposito"
)
t.salvar()


print("\n=== TESTE 4: Listando transações da conta ===")
Transacao.listar_por_conta(1)


print("\n=== TESTE 5: Listando TODAS as transações ===")
Transacao.listar_todas()


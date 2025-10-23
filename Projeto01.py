# ==========================================================
# SISTEMA DE BANCO SIMPLES EM PYTHON
# ==========================================================

# ----------------------------------------------------------
# Descrição:
#   - Simula operações bancárias simples:
#       depósito, saque, extrato, cadastro de usuário,
#       criação de contas e geração de logs.
#   - Usa listas planas para armazenamento temporário.
#   - Salva logs de operações em um arquivo "log.txt".
# ==========================================================

# Importa o módulo random para gerar números aleatórios
import random  # gera números para agencia/conta
from datetime import datetime

# Lista global que armazenará todas as contas (dados salvos em sequência)
contalista = []  # formato: [agencia, numero_conta, titular, agencia2, ...] (listas planas)

# Lista global que armazenará todos os usuários (dados salvos em sequência)
usuarios = []  # formato: [nome, cpf, dta, endereco, nome2, cpf2, ...]

# Lista global que armazenará todos os CPFs cadastrados
cpfcliente = []  # formato: ['12345678900', '98765432100', ...]

# Saldo do cliente (variável global única neste script)
saldo = 0.0  # float para operações financeiras

# Limite individual por saque
limite = 500  # valor máximo por saque permitido

# Histórico simples de extrato (string acumulada)
extrato = ''  # armazena linhas de movimentação

# Contador de saques realizados (para controlar número máximo por período)
numero_saques = 0  # começa em zero

# Limite máximo de saques permitidos (por exemplo, por dia)
LIMITE_SAQUES = 3  # máximo de saques permitidos

# Opção escolhida no menu (string)
opcao = ""  # inicializada vazia; atualizada pela função menu()


# Função que exibe o menu e lê a opção escolhida pelo usuário
def menu():
    global opcao  # usa/atualiza a variável global 'opcao'
    print(  # imprime o menu para o usuário
        """

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        [c] Cadastro Usuario
        [cc] Cria Conta
        [i] Iterar Conta
        [g] Gerador Relatorio

        => """
    )
    try:
        opcao = input("Digite: ").lower()  # lê opção e normaliza para minúscula
    except (ValueError, TypeError) as erro:
        # captura exceções inesperadas do input (raro) e notifica o usuário
        print("VOCE ERROU NA DIGITAÇAO", erro)



def log(function):
    def wrapper(*args,**kwargs):
        resultado = function(*args,**kwargs)
        data_hora_transaçao = datetime.now().strftime("%H:%M:%S")

        with open("log.txt", "a",encoding="utf-8") as arquivo:
         arquivo.write( 
                        f"[{data_hora_transaçao}]"
                        f" Operação {function.__name__}"
                        f" com argumentos {args} {kwargs}."
                        f" Retornou o resultado {resultado}\n")

        return resultado
    return wrapper


def gerador_relatorio(tipo = None,valor_min = None): 
    try:
        with open("log.txt",'r',encoding ="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if tipo and tipo not in linha:
                    continue

                if valor_min is not None:
                    partes = linha.split("resultado")
                    if len(partes) > 1:
                        trecho = partes[-1].replace("(","").replace(")","").replace(",","")
                        palavras = trecho.split()
                        for p in palavras:
                            try:
                                valor = float(p)
                                if valor < valor_min:
                                    linha = None
                                break
                            except ValueError as erro:
                                print("ERRO DE VALOR",erro)
                                continue

                if linha :
                    print(linha)
    except Exception as erro:
        print(f"Erro ao gerar relatório: {erro}")



                



# Função para depositar valor — removi '/' para compatibilidade com < Python 3.8
@log
def depositor(valor):
    global saldo  # modifica a variável global 'saldo'
    global extrato  # modifica a variável global 'extrato'
    try:
        valor = float(valor)  # tenta converter a entrada para float (pode lançar ValueError)
    except (ValueError, TypeError):
        # caso a conversão falhe, informa usuário e retorna sem alterar nada
        print("Valor inválido! Digite um número.")
        return

    if valor > 0:
        saldo += valor  # soma o depósito ao saldo global
        extrato += f"Depósito de {valor:.2f} RS\n"  # registra no extrato com formatação 2 casas decimais
        print(f"Saldo Atualizado! Valor {saldo:.2f}")  # mostra o saldo atualizado
        print(extrato)  # imprime o extrato atual
        return saldo, extrato  # retorna valores atualizados opcionalmente
    else:
        # valor não positivo é inválido para depósito
        print("Valor inválido para depósito.")



# Função para realizar saque
@log
def sacar(valor):
    global extrato  # modifica o extrato global
    global saldo  # modifica o saldo global
    global numero_saques  # necessário para incrementar o contador de saques sem erro

    try:
        valor = float(valor)  # tenta converter o valor informado para float
    except (ValueError, TypeError):
        # se falhar, informa e retorna sem alterações
        print("Valor inválido! Digite um número.")
        return

    excedeu_saldo = valor > saldo  # verifica se o valor é maior que o saldo disponível
    excedeu_limite = numero_saques >= LIMITE_SAQUES  # verifica se já atingiu o limite de saques
    excedeu_valor_saque = valor > limite  # verifica se o valor excede o limite por saque

    if excedeu_limite:
        # caso tenha atingido limite de saques, bloqueia operação
        print("OPERAÇAO FALHOU. LIMITE DE SAQUES ATINGIDO.")
    elif excedeu_saldo:
        # caso saldo insuficiente
        print("OPERAÇAO FALHOU. SALDO INSUFICIENTE.")
    elif excedeu_valor_saque:
        # caso valor maior que limite por saque
        print("OPERAÇAO FALHOU. VALOR ACIMA DO LIMITE.")
    else:
        if valor > 0:
            saldo -= valor  # subtrai o valor do saldo
            numero_saques += 1  # incrementa o contador de saques (por isso precisa do global)
            extrato += f"Saque de {valor:.2f} RS\n"  # registra no extrato
            print(f"SAQUE REALIZADO COM SUCESSO NO VALOR DE {valor:.2f}")  # confirma saque
            print(f"Saldo atual: {saldo:.2f}")  # mostra saldo atualizado
            return saldo, extrato  # retorna os valores atualizados
        else:
            # proteção contra valores não positivos
            print("Valor inválido para saque.")


# Função que mostra o extrato atual e o saldo
def mostrar_extrato():
    global extrato, saldo  # usa as variáveis globais 'extrato' e 'saldo'
    print("-----------------------")  # separador visual
    print("EXTRATO DO USUARIO:")  # título do extrato
    # imprime o extrato se existir; caso contrário, avisa que não há movimentações
    print(extrato if extrato else "Nenhuma movimentação registrada.")
    print(f"SALDO ATUAL: {saldo:.2f} RS")  # exibe sald o formatado
    print("-----------------------")  # separador final


# Função que finaliza a execução (mensagem de saída)
def sair():
    print("SAINDO DA CONTA........")  # mensagem de saída
    print('------------------')  # linha decorativa
    print("VOLTE SEMPRE")  # mensagem final amistosa


# Função para criar uma nova conta associada a um usuário (listas planas)
def criarconta(usuario):
    # 'usuario' é o nome do titular da conta (string esperada)
    global contalista  # indica que vamos modificar a lista global de contas

    numero_conta = "0"  # inicia número da conta com '0' 
    agencia = "1"  # inicia agência com '1' 

    # Gera 4 dígitos para agência e 4 para número da conta concatenando dígitos aleatórios
    for a in range(0, 4):
        numeros = random.randint(0, 9)  # gera um dígito aleatório de 0 a 9
        agencia += str(numeros)  # concatena ao código da agência

        numeros2 = random.randint(0, 9)  # gera outro dígito para a conta
        numero_conta += str(numeros2)  # concatena ao número da conta

    # Armazena os dados da conta em sequência na lista plana contalista
    contalista.append(agencia)  # acrescenta agência
    contalista.append(numero_conta)  # acrescenta número da conta
    contalista.append(usuario)  # acrescenta nome do titular da conta

    # Confirmação ao usuário que a conta foi criada
    print("Conta criada com sucesso!")
    print(f"Agência: {agencia} | Conta: {numero_conta} | Titular: {usuario}")


# Função para criar um novo usuário (listas planas)
def criarusuario(nome='', cpf='', dta='', endereco=''):
    global usuarios  # modificaremos a lista global 'usuarios'
    global cpfcliente  # modificaremos a lista global 'cpfcliente' com o CPF novo

    # Mantém CPF como string para preservar zeros à esquerda e qualquer formatação que o usuário possa fornecer
    if cpf in cpfcliente:
        # se CPF já estiver cadastrado, informa e sai sem duplicar
        print("USUÁRIO JÁ CADASTRADO!")
        return

    # Converte valores para string e prepara para inserir na lista plana 'usuarios'
    nome_usuario = str(nome)  # converge nome para string
    cpf_usuario = str(cpf)  # garante CPF como string
    dta_usuario = str(dta)  # data como string
    endereco_usuario = str(endereco)  # endereco como string

    # Adiciona as informações do usuário na lista 'usuarios' em sequência (listas planas)
    usuarios.append(nome_usuario)  # adiciona nome
    usuarios.append(cpf_usuario)  # adiciona cpf
    usuarios.append(dta_usuario)  # adiciona data de nascimento
    usuarios.append(endereco_usuario)  # adiciona endereço

    # Adiciona o CPF na lista de CPFs cadastrados para controle de duplicatas
    cpfcliente.append(cpf_usuario)

    # Confirmação visual para o usuário (mostra a lista completa de usuários)
    print("Usuário cadastrado com sucesso!")
    print(usuarios)



def conta_iterador(lista):
    if not lista:
        print("Nenhum Conta Cadastrada")
        return
    else:
        for a in range(0,len(lista),3):
            agencia = lista[a]
            num_conta = lista[a+1]
            titula_conta = lista[a+2]
            print(f"AGENCIA {agencia} Com Numero De Conta {num_conta} Com O Titula {titula_conta}")


# Função que verifica se o CPF já existe e, se não existir, cadastra novo usuário
def filtrarusuario(numero):
    global cpfcliente  # vamos consultar/modificar a lista de cpfs

    numero = str(numero)  # converte a entrada para string para comparação consistente

    if numero in cpfcliente:
        # se já cadastrado, informa que o usuário existe
        print("VOCÊ JÁ ESTÁ CADASTRADO COMO USUÁRIO...")
    else:
        # caso não esteja cadastrado, pede os dados e cria o cadastro
        try:
            nome = input("DIGITE O NOME: ")  # solicita nome ao usuário
            cpf = input("DIGITE SEU CPF (somente números): ")  # solicita cpf
            dta = input("DIGITE SUA DATA DE NASCIMENTO (DD/MM/AAAA): ")  # solicita data
            endereco = input("DIGITE SEU ENDEREÇO (LOGRADOURO - NRO - BAIRRO - CIDADE - UF): ")  # solicita endereco

            criarusuario(nome, cpf, dta, endereco)  # cria o usuário com os dados fornecidos
            criarconta(nome)  # opcional: cria uma conta automaticamente para o novo usuário

        except (KeyboardInterrupt):
            # trata Ctrl+C de forma amigável
            print("\nVOCÊ SAIU DO PROGRAMA.")
        except Exception as erro:
            # captura outros erros e exibe a mensagem
            print("ERRO AO CRIAR USUÁRIO:", erro)


# === Observação: a chamada abaixo é um teste inicial que aparece antes do menu interativo ===
# Se não quiser que o script peça dados ao iniciar, remova/comment essa linha.
filtrarusuario("230")  # executa o filtro para o CPF "230" (vai pedir dados porque cpfcliente está vazio)

# Exibe o estado atual das listas após o teste de cadastro inicial (debug)
print("\n=== DADOS FINAIS ===")  # cabeçalho para saída de depuração
print("CPFs:", cpfcliente)  # imprime todos os CPFs cadastrados
print("Usuários:", usuarios)  # imprime a lista plana de usuários
print("Contas:", contalista)  # imprime a lista plana de contas


# Função principal de interação com o menu; mantém o loop até o usuário sair
def interacao():
    while True:  # loop infinito que só quebra quando a opção 'q' é escolhida
        menu()  # exibe menu e atualiza 'opcao' global

        if opcao == 'd':  # opção depósito
            valor = input("DIGITE O VALOR DO DEPÓSITO: ")  # pede o valor de depósito
            depositor(valor)  # chama a função que realiza o depósito

        elif opcao == 's':  # opção saque
            valor = input("DIGITE O VALOR DO SAQUE: ")  # pede o valor de saque
            sacar(valor)  # chama função de saque

        elif opcao == 'e':  # opção extrato
            mostrar_extrato()  # exibe o extrato atual

        elif opcao == 'q':  # opção sair
            sair()  # exibe mensagem de saída
            break  # encerra o loop principal

        elif opcao == 'c':  # opção cadastrar usuário
            # solicita dados completos antes de criar usuário para evitar inserção de valores vazios
            nome = input("DIGITE SEU NOME: ")
            cpf = input("DIGITE SEU CPF (somente números): ")
            dta = input("DIGITE SUA DATA DE NASCIMENTO (DD/MM/AAAA): ")
            endereco = input("DIGITE SEU ENDEREÇO: ")
            criarusuario(nome, cpf, dta, endereco)  # cria o usuário com os dados informados

        elif opcao == 'cc':  # opção para criar conta (apenas pede nome do titular)
            nome = str(input("DIGITE SEU NOME: "))  # lê o nome que será titular da conta
            criarconta(nome)  # cria a conta associada ao nome informado

        elif opcao == 'i':
            conta_iterador(contalista)



        elif opcao == 'g':
            tipo = input("Filtrar por tipo de transação (ex: sacar, depositor): ").strip()
            try:
                valor_procura = float(input("Valor mínimo para filtrar: "))
            except ValueError:
                valor_procura = None
            gerador_relatorio(tipo or None, valor_procura)


        else:
            # qualquer opção inválida cai aqui
            print("OPÇÃO INVÁLIDA!")


# EXECUÇÃO PRINCIPAL
# ==========================================================
if __name__ == "__main__":
    # Executa o sistema bancário
    interacao()

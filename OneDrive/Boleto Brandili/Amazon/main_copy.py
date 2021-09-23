import funcoes_de_procura
import validade_cpf
import validade_email
import erros
from cria_produtos import produtos
import filtrar_compra

#Class

class Cliente:
    def __init__(self, nome ,sobrenome, email, senha, cpf, limite_credito):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.limite_credito = limite_credito
        self.compras = []
        self.total_de_gastos = 0

#Checar senha do Cadastro

def checar_senha(senha):
    try:
        senha_numeros = int(senha)
        if len(senha) < 6:
            return False
        return senha
    except ValueError: 
        return False

#Checar senha especial


def checar_senha_especial():
    for i in range(3):
        try:
            senha = int(input("Senha de acesso: "))
            if senha == 123456:
                return senha
        except ValueError:
            print("Senha inválida!")
        else:
            print("Senha inválida!")
    return -1

#checar quantidade

def checar_quant():
    while True:
            try:
                quantidade = int(input("Quantidade: "))
            except ValueError:
                print("Quantidade inválida!")      
            else:
                if quantidade >= 0:
                    return quantidade
                else:
                    print("Quantidade inválida!")  



#Options Página Inicial

def clientes(main):
    if checar_senha_especial() == -1:
        print("Você ultrapassou o limite de tentativas e será redirecionado à Pagina Inicial.")
    else:
        listar_ou_procurar = erros.entre_com_int("1. Listar todos clientes\n2. Procurar Cliente\n",
        1, 2, "Opção Inválida!\n")
        if listar_ou_procurar == 1:
            if len(main) == 0:
                print("Não há nenhum cliente!")
            else:
                for cliente in range(len(main)):
                    print(f"Cliente {cliente+1}:\nNome: {main[cliente].nome}\nSobrenome: {main[cliente].sobrenome}\n")
        elif listar_ou_procurar == 2:
            nome = input("Nome: ")
            sobrenome = input("Sobrenome: ")
            achar_cliente = funcoes_de_procura.nome(main, nome, sobrenome)
            if achar_cliente == -1:
                print("\nCliente não existe.\n")
                oque_checar = erros.entre_com_int("\n1. Dados Cadastrais\n2. Lista de Compras\n", 1, 2, "Opção Inválida!\n")
                if oque_checar == 1:
                    print(f"\nNome: {main[achar_cliente].nome}\nSobrenome: {main[achar_cliente].sobrenome}")
                    print(f"Email: {main[achar_cliente].email}\nSenha: {main[achar_cliente].senha}")
                    print(f"CPF: {main[achar_cliente].cpf}\nLimite de crédito: {(main[achar_cliente].limite_credito):.2f}\n")
                elif oque_checar == 2:
                    if len(main[achar_cliente].compras) == 0:
                        print("A lista está vazia.")
                    else:
                        for compra in range(len(main[achar_cliente].compras)):
                            print(f"\n{compra+1}. {main[achar_cliente].compras[compra][1]} - {main[achar_cliente].compras[compra][0]} - R$ {(main[achar_cliente].compras[compra][2]):.2f}\n")


def cadastro(main):
    nome = input("Primeiro nome: ") 
    sobrenome = input("Sobrenome: ")
    while True:
        email = validade_email.verifica_email(input("Email: "))
        if email != False:      
            break
        else:
            print("Email inválido")
    senha = checar_senha(input("Senha (6 dígitos): ")) 
    while senha == False:       
        print("Senha inválida!")
        senha = checar_senha(input("Senha (6 dígitos): "))
    while True:
        cpf = validade_cpf.verifica_cpf(input("CPF: "))
        if cpf != False:         
            break
        else:
            print("CPF inválido!")
    limite_credito = erros.entre_com_float("Limite de crédito: ", 12.00, 1000.00, 
    "Valor inválido. Por favor, escolha um valor entre R$ 12.00 e R$ 1000.00.")
    if funcoes_de_procura.nome(main, nome, sobrenome) != -1 or funcoes_de_procura.email(main, email) != -1 or funcoes_de_procura.cpf(main, cpf) != -1:
        print("O usuário já existe.")
        return 0
    else:
        person = Cliente(nome, sobrenome, email, senha, cpf, limite_credito)
        return person

def login(main):
    for i in range(3):
        email = funcoes_de_procura.email(main, input("\nEmail: "))
        senha = input("Senha: ")
        if email != -1 and main[email].senha == senha:
            return email
        else:
            print("Email ou senha inválidos!") 
    print("O número de tentativas foi ultrapassado e você será redirecionado à Pagina Inicial.\n")
    return -1

#Options Menu Principal    

def comprar(main, lista_de_produtos, usuario_atual):
    print("\n1- Sem filtro\n2- Com filtro")
    filtro_ou_nao = erros.entre_com_int("", 1, 2, "Opção inválida!")
    if filtro_ou_nao == 1:
        mostrar_produtos = lista_de_produtos
    else:
        mostrar_produtos = filtrar_compra.filtro(lista_de_produtos)
    print("\nLista de Produtos:\n")
    for item in range(len(mostrar_produtos)):
        print(f"{item+1}. {mostrar_produtos[item].titulo} - R$ {(mostrar_produtos[item].valor):.2f}")
    print("\nEscolha os produtos que desejas comprar.\n")
    while True:
        codigo = erros.entre_com_int("Escreva o código do produto que desejas comprar: ", 
        1, len(mostrar_produtos), "Opção inválida.\n")
        quantidade = checar_quant()      
        if main[usuario_atual].limite_credito - (mostrar_produtos[codigo-1].valor*quantidade) < 0:
            print("Você não possui crédito suficiente para realizar esta compra. Efetue o pagamento de sua conta.")
        else:
            for quant in range(quantidade):
                main[usuario_atual].limite_credito -= mostrar_produtos[codigo-1].valor
                main[usuario_atual].compras.append([mostrar_produtos[codigo-1].tipo, mostrar_produtos[codigo-1].titulo, 
                mostrar_produtos[codigo-1].valor])
                main[usuario_atual].total_de_gastos += mostrar_produtos[codigo-1].valor
        while True:
            continuar = input("Continuar a comprar? (s-sim n-não) ").lower()
            if continuar == "s" or continuar == "n":
                break
            else:
                print("Opção inválida!")
        if continuar == "n":
            break


def carrinho(main, usuario_atual):
    print(f"Total de gastos: R$ {(main[usuario_atual].total_de_gastos):.2f}")
    ver_itens = erros.entre_com_int("1. Listar todos os itens\n2. Sair\n", 1, 2, 
    "Opção Inválida!\n")
    if ver_itens == 2:
        print("Você escolheu sair do Carrinho.\n")
    else:
        if len(main[usuario_atual].compras) == 0:
            print("A lista está vazia!")
        else:
            for item in range(len(main[usuario_atual].compras)):
                print(f"{item+1}. {main[usuario_atual].compras[item][1]} - {main[usuario_atual].compras[item][0]} - R$ {(main[usuario_atual].compras[item][2]):.2f}")

def pagamento(main, usuario_atual):
    while True:
        try:
            valor_pagar = float(input("Valor que desejas pagar: "))
        except ValueError:
            print("Valor inválido.")
        else:
            if valor_pagar >= 1.00 and main[usuario_atual].limite_credito + valor_pagar <= 1000.00:
                break
            else:
                print("Valor inválido. O valor é menor que R$ 1.00 ou ultrapassa o limite de R$ 1000.00.")
    main[usuario_atual].limite_credito += valor_pagar
    main[usuario_atual].compras = []
    main[usuario_atual].total_de_gastos -= valor_pagar
    print(f"O valor foi inserido com sucesso. Seu crédito atual é de R$ {(main[usuario_atual].limite_credito):.2f}.")

main = []

lista_de_produtos = []
produtos(lista_de_produtos)

while True:
    option = erros.entre_com_int("\nPágina Inicial\n\n1-Clientes\n2-Cadastro\n3-Login\n4-Sair\n", 1, 4, 
    "Opção Inválida!\n")
    if option == 4:
        print("\nVocê escolheu a opção 4. A sessão será encerrada.")
        break
    else:   
        if option == 1:   
            clientes(main)
            continue
        elif option == 2:
            novo = cadastro(main)
            if novo == 0:
                continue
            else:
                main.append(novo)
                usuario_atual = funcoes_de_procura.email(main, novo.email)
        elif option == 3:
            if len(main) == 0:
                print("Não há nenhum cliente!")
                continue
            else:
                usuario_atual = login(main)
                if usuario_atual == -1:
                    continue
        while True:
            print(f"\n{main[usuario_atual].nome}, bem-vindo(a) ao Sistema da AmazonCC!\n\n")
            option_menu = erros.entre_com_int("Menu Principal:\n\n1-Comprar\n2-Carrinho\n3-Pagar a conta\n4-Sair\n", 1, 4, "Opção inválida.\n")
            if option_menu == 4:
                print("\nVocê escolheu a opção 4. Redirecionando-o à Página Principal.\n")
                break
            else:
                if option_menu == 1:
                    comprar(main, lista_de_produtos, usuario_atual)
                if option_menu == 2:
                    carrinho(main, usuario_atual)
                if option_menu == 3:
                    pagamento(main, usuario_atual)
               
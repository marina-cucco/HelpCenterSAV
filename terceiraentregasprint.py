def menu():
    print(f"""
    
    BEM VINDO AO HELP CENTER DO SAV:
    1 - Simular cotação pós vistoria
    2 - Realizar cadastro da bike
    3 - Exibir cadastro
    4 - Remover bicicleta cadastrada
    5 - Consultar status da vistoria
    0 - Finalizar atendimento
""")

def validacao_cotacao(variavel):
    while True:
        if variavel != 'NÃO' and variavel != 'SIM' and variavel != 'NAO':
            print("Resposta inválida. Por favor, apenas 'sim' ou 'não'")
            variavel = input("Digite novamente:").upper()
            break
        else:
            return variavel


def cotacao():
    while True:
        print(f"""
        SIMULAÇÃO DE VISTORIA
        Responda com "sim ou "não": """)
        estado = input("1. A documentação da bicicleta está em dia (nota fiscal e número de série)?").upper()
        validacao_cotacao(estado)
        preco = input("2. O valor da sua bicicleta é menor do que 10.000 reais?").upper()
        validacao_cotacao(preco)
        seguranca = input("3. A sua bicicleta possui cadeado?").upper()
        validacao_cotacao(seguranca)
        armazenamento = input("4. A sua bicicleta fica armazenada em ambiente fechado (garagem)?").upper()
        validacao_cotacao(armazenamento)
        tipo = input("5. Sua bicileta é para uso não esportivo?").upper()
        validacao_cotacao(tipo)
        tempo = input("A duração do seguro seria para 1 ano ou menos?").upper()
        validacao_cotacao(tempo)
        lista = [estado, preco, seguranca, armazenamento, tipo, tempo]
        sim = 0
        nao = 0
        for i in range(len(lista)):
            if lista[i] == "SIM":
                sim += 10
            elif lista[i] == "NAO" or lista[i] == "NÃO":
                nao += 20

        print(f"""
                    SIMULAÇÃO DE COTAÇÃO:
                    O valor do seu seguro, caso a vistoria confirmasse
                    as cincunstâncias do questionário, 
                    seria em torno de R${sim + nao} mensais.

                    Cadastre sua bicileta! :)
                    Estamos o redirecionando ao menu principal:""")

        break


def cadastro_ou_menu():
    while True:
        tchau = input(f"\nFeito! :)"
                      f"\nDeseja cadastrar nova bicicleta ou volta ano menu principal? "
                      f"\nDigite 'cadastro' ou 'menu': ").upper()
        if tchau == "MENU":
            break
        elif tchau != "CADASTRO" and tchau != "MENU":
            print("Invalido, te direcionando pro menu principal")
            break
        else:
            cadastro()
        break

tabela_cadastros = []
def cadastro():
    while True:
        erro = False
        print("CADASTRO DE BICICLETA")
        # marca, modelo, valor, ano , marca, cor
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        valor = input("Valor (use . para marcar centavos e nada para marcar milhares. Exemplo: 2050.69): ")
        if valor.replace(",", "").replace(".", "").isnumeric():
            if "," in valor:
                print("Não use vírgulas! :)")
                valor = input("Digite o valor novamente, agora sem usar virgulas: ")

        else:
            print("Digite um valor usando números e não use ponto para marcar milhares! :)")
            valor = input("Valor (use . para marcar centavos e nada para marcar milhares. Exemplo: 2050.69): ")

        if float(valor) < 2000:
            print(f"Sua bike tem valor menor do que 2000. Nesse caso, não a cobrimos. "
                  f"Volte ao menu principal para que possa finalizar o programa ou começar o cadastro de outra bike:")
            erro = True

        if erro == True:
            break

        ano = input("Ano: ")
        if ano.isnumeric() is not True or len(ano) < 4 or int(ano) > 2023:
            print("Digite um ano válido!")
            ano = input("Ano: ")

        cor = input("Cor: ")
        if cor.isnumeric() is True or len(cor) < 3:
            print("Digite uma cor válida!")
            cor = input("Ano: ")

        notafiscal = str(
            input("Digite o código que se encontra na área DANFE da sua nota fiscal:"))

        cadastro_bike = {'Marca': marca, 'Modelo': modelo, 'Valor': valor, 'Ano': ano, 'Cor': cor, 'Nota fiscal': notafiscal}
        id = cadastro_bike['Marca'] + cadastro_bike['Nota fiscal']
        cadastro_bike['id'] = id
        tabela_cadastros.append(cadastro_bike.copy())
        print(f"O id da sua bike é {id}. Você precisará dele no futuro quando for realizar a vistoria!")
        cadastro_ou_menu()
        break

def remover(lista):
    while True:
        inputt = int(input("Digite qual cadastro deseja deletar (1 para primeira bicicleta cadastrada, 2 para a segunda, etc): "))
        if inputt > len(lista):
            tentar = input("Esse número não corresponde a nenhum cadastro! Digite 'tentar' para tentar novamente ou 'menu' para voltar ao menu:")
            if tentar == 'tentar':
                continue
            else:
                break

        inputtt = inputt - 1
        del lista[inputtt]
        print(f"Bicicleta {inputt} deletada. Volte ao menu:\n")

        break


def status():
    diasuteis = int(input("Há quantos dias úteis sua vistoria online foi feita?"))
    if diasuteis <= 1:
        print(f'''
                        Você assinalou que fez a vistoria há {diasuteis} dia útil.
                        Nosso sistema pede pelo menos dois dias úteis de espera para que sua vistoria seja confirmada e aceita.
                        Mandaremos e-mail quando estiver pronta! :)''')

    else:
        print(f'''
                        Você assinalou que fez a vistoria há {diasuteis} dias úteis.
                        Isso significa que ela já foi revisada! O resultado foi enviado para o e-mail fornecido no cadastro pessoal da porto.
                        Cheque sua caixa de spam e, caso não o tenha recebido, nos contacte pelo nosso site www.portoseguro.com.
                        ''')

def exibir():
    while True:
        for cadastro in tabela_cadastros:
            print(f"\n\nBICICLETA:")
            for k, v in cadastro.items():
                print(f"""{k}......: {v}""")
            print("\n")
        break

while True:
    menu()
    opcao = input("\nDigite o número da opção desejada: ")
    if opcao == '1':
        cotacao()
    elif opcao == '2':
        cadastro()
    elif opcao == '3':
        if len(tabela_cadastros) == 0:
            print(f"\n\nAinda sem cadastros! \nVolte ao menu principal para realizá-lo(s):\n\n")
        else:
            exibir()
    elif opcao == '4':
        remover(tabela_cadastros)
    elif opcao == '5':
        status()
    elif opcao == '0':
        print("\nAtendimento encerrado. Agradecemos!\n")
        break
    else:
        print("\nOpção inválida. Digite um número de 0 a 3:\n")
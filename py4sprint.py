import requests
import pandas as pd
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\oracle\instantclient-basic-windows.x64-19.21.0.0.0dbru\instantclient_19_21")

try:
    dsnStr = cx_Oracle.makedsn("oracle.fiap.com.br", "1521", "ORCL")

    conn = cx_Oracle.connect(user='RM551569', password="210797", dsn=dsnStr)

    inst_cadastro = conn.cursor()
    inst_exclusao = conn.cursor()
    inst_consulta = conn.cursor()
except Exception as e:
    print("Erro: ", e)
    conexao = False
else:
    conexao = True
    margem = ' ' * 4 
    
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

def get_cep_info():
    while True:
        try:
            numero_cep = input("Digite o CEP para confirmar a região da bicicleta a ser segurada: ")
            response = requests.get(f"https://viacep.com.br/ws/{numero_cep}/json/")
            data = response.json()
            if 'erro' in data:
                print("CEP inválido ou não encontrado")
                raise ValueError("CEP não encontrado.")
            else:
                cidade = data['localidade']
                rua = data['logradouro']
                bairro = data['bairro']
                estado = data['uf']

                texto = f'''
                    Cidade: {cidade}
                    Estado: {estado}
                    Rua: {rua}
                    Bairro: {bairro}

                     '''

                print(texto)
                break
        except Exception:
            print("Erro. Tente novamente, apenas com números e semc caracteres especiais")


def validacao_cotacao(variavel):
    while True:
        if variavel != 'N' and variavel != 'S':
            print("Resposta inválida. Por favor, apenas 'sim' ou 'não'")
            variavel = input("Digite novamente:").upper()
            break
        else:
            return variavel


def cotacao():
    while True:
        print(f"""
        SIMULAÇÃO DE VISTORIA
        Responda com [s]im ou [n]ão: """)
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
            if lista[i] == "S":
                sim += 10
            elif lista[i] == "N":
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
    while conexao:
        erro = False
        print("CADASTRO DE BICICLETA")
        # marca, modelo, valor, ano , marca, cor.
        #O cep é usado apenas para confirmação, e sua validação ocorre instantaneamente. Não entra para o arquivo em texto.
        get_cep_info()
        confirma_cep = input("Deseja continuar com esse endereço? [s]im ou [n]ão")
        while confirma_cep == 'n':
            get_cep_info()
            confirma_cep = input("Deseja continuar com esse endereço? [s]im ou [n]ão")
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
        while ano.isnumeric() is not True or len(ano) > 4 or int(ano) > 2023:
            print("Digite um ano válido!")
            ano = input("Ano: ")

        cor = input("Cor: ")
        if cor.isnumeric() is True or len(cor) < 3:
            print("Digite uma cor válida!")
            cor = input("Cor: ")

        notafiscal = str(
            input("Digite o código que se encontra na área DANFE da sua nota fiscal:"))

        cadastro_bike = {'Marca': marca, 'Modelo': modelo, 'Valor': valor, 'Ano': ano, 'Cor': cor, 'Nota fiscal': notafiscal}
        id = cadastro_bike['Marca'] + cadastro_bike['Nota fiscal']
        cadastro_bike['id'] = id
        tabela_cadastros.append(cadastro_bike.copy())
        arq = open("dados_bike.txt", "w", encoding="utf-8")
        for index, dict_item in enumerate(tabela_cadastros):
            arq.write(f'\n\nBicicleta {index + 1}:\n')
            
            for key, value in dict_item.items():
                arq.write(f'{key}: {value}\n')

        arq.close()
        try:
            cadastro = f""" INSERT INTO T_BIKE_PY (NOTA_FISCAL, MARCA, MODELO, VALOR, ANO, COR)VALUES ('{notafiscal}','{marca}', '{modelo}', '{valor}', '{ano}', '{cor}') """
            inst_cadastro.execute(cadastro)
            conn.commit()
        except ValueError:
                print("Digite um número na idade!")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print("Erro de banco de dados: ", error.code)
            print("Descrição do erro: ", error.message)
        except:
                print("Erro na transação do BD")
        else:
                print("\n##### Dados GRAVADOS #####")
                input("Pressione ENTER")
    
        cadastro_ou_menu()
        break

def remover(lista):
    while True:
        exibir()
        inputt = input("Digite qual cadastro deseja deletar (1 para primeira bicicleta cadastrada, 2 para a segunda, etc): ")
        if inputt.isdigit():
            inputt = int(inputt)
            if inputt > len(lista) or inputt <= 0:
                tentar = input("Esse número não corresponde a nenhum cadastro! Digite 'tentar' para tentar novamente ou 'menu' para voltar ao menu:")
                if tentar == 'tentar':
                    continue
                else:
                    break
        else:
            tentar = input("Digite números apenas! digite 'tentar' para tentar novamente:")
            if tentar == 'tentar':
                continue
            else:
                break

        inputtt = inputt - 1
        del lista[inputtt]
        arq = open("dados_bike.txt", "w", encoding="utf-8")
        for index, dict_item in enumerate(lista):
            arq.write(f'\n\nBicicleta {index + 1}:\n')
            for key, value in dict_item.items():
                arq.write(f'{key}: {value}\n')
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
    arq = open("dados_bike.txt", "r", encoding="utf-8")
    print(arq.read())
    arq.close()

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
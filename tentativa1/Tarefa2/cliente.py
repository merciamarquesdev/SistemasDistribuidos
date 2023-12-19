import json
import http.client

def conectarBanco():
    banco = input("Insira o banco desejado (Para finalizar a sessão, insira 'sair'): \n")
    if banco.lower() == "sair":
        return None

    try:
        with open(f'./bancos/{banco}.json') as arquivo:
            contas = json.load(arquivo)
            host = "localhost"
            porta = contas["porta"][0]
            return http.client.HTTPConnection(f"{host}:{porta}")
    except FileNotFoundError:
        print(f"Arquivo para o banco {banco} não encontrado. Tente novamente.")
        return conectarBanco()

def enviarRequisicao(conn, endpoint, data=None):
    headers = {'Content-type': 'application/json'}
    conn.request('POST', endpoint, json.dumps(data) if data else None, headers)
    response = conn.getresponse()
    return response.read().decode()

def cadastrarConta(conn):
    conta = (input("Insira a conta: "))
    return enviarRequisicao(conn, '/cadastro', {'conta': conta})

def fazerDeposito(conn):
    conta = input("Insira a conta: ")
    valor = int(input("Insira o valor do depósito: "))
    return enviarRequisicao(conn, '/deposito', {'conta': conta, 'valor': valor})

def fazerTransferencia(conn):
    conta1 = input("Insira a conta que transferirá: ")
    conta2 = input("Insira a conta que receberá: ")
    valor = int(input("Insira o valor da transferência: "))
    return enviarRequisicao(conn, '/transferencia', {'conta1': conta1, 'conta2': conta2, 'valor': valor})

def fazerConsulta(conn):
    conta = (input("Insira a conta: "))
    return enviarRequisicao(conn, '/consulta', {'conta': conta})


def main():
    while True:
        servidor = conectarBanco()
        if servidor is None:
            break

        while True:
            print("******* Boas vindas! *******")
            print("* O que deseja fazer hoje? *")
            print("Insira 1 para Consultar")
            print("Insira 2 para Transferir")
            print("Insira 3 para Depositar")
            print("Insira 4 para Cadastrar")
            print("Insira 5 para Sair")
            digito = input("Insira o dígito: ")
            
            if digito == "1":
                print(fazerConsulta(servidor))
            elif digito == "2":
                print(fazerTransferencia(servidor))
            elif digito == "3":
                print(fazerDeposito(servidor))
            elif digito == "4":
                print(cadastrarConta(servidor))
            elif digito == "5":
                print("Finalizando sessão...")
                break
            else:
                print("Erro: Tente novamente.")

if __name__ == "__main__":
    main()



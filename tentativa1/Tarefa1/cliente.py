import http.client
import json

banco = input("Insira o nome do Banco: \n")

with open(f'bancos\\{banco}.json') as arquivo:
    contas = json.load(arquivo)
    porta = contas["porta"]

while True:
    conta1 = input("Insira a conta que transferirá: \n")
    if conta1 == 'sair':
        exit()
    conta2 = input("Digite a conta que receberá: \n")
    valor = int(input("Digite o valor da transferência: \n"))

    with http.client.HTTPConnection(f"localhost:{porta}") as conn:
        payload = {
            "conta1": conta1,
            "conta2": conta2,
            "valor": valor
        }
        conn.request('POST', '/transferencia', json.dumps(payload), headers={'Content-type': 'application/json'})
        response = conn.getresponse()
        result = response.read().decode()
        print(result)

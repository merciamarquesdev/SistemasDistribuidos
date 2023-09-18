import xmlrpc.client
import json

banco = input("Digite o Banco: \n")

with open('bancos\\'+banco+'.json') as arquivo:
    contas = json.load(arquivo)
    porta = contas["porta"]
    with xmlrpc.client.ServerProxy("http://localhost:"+str(porta)+"/RPC2") as s:
        while True:
            contaA = input("Digite a sua Conta: \n")
            if contaA == 'sair':
                exit()
            contaB = input("Digite a Conta para a qual irá Transferir: \n")
            moedas = int(input("Digite as Moedas: \n"))
            print(s.transferencia(contaA, contaB, moedas))
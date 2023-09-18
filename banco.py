from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client

import os
import json
import random

nomeBanco = input("Digite o nome do Banco: \n")
caminhoBanco = 'bancos\\'+nomeBanco+'.json'
if os.path.isfile(caminhoBanco):
    porta = random.randint(8000, 8900)
    contas = {"porta": porta}
else:
    with open(caminhoBanco, 'r+') as arquivo:
        contas = json.load(arquivo)
        porta = contas["porta"]

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2')

class Banco():
    def __init__(self):
        self.contas = contas
        self.salvar()
    def salvar(self):
        with open(caminhoBanco, 'w') as arquivo:
            json.dump(self.contas, arquivo)
    def deposito(self, conta, moedas):
        if conta in self.contas:
            self.contas[conta] += moedas
        else:
            self.contas[conta] = moedas
        self.salvar()
        return "Operacao Concluída"
    def transferencia(self, contaA, contaB, moedas):
        if contaA not in self.contas or self.contas[contaA] < moedas:
            return "Operacao Invalida"
        if contaB not in self.contas:
            bancos = os.listdir('./bancos')
            for i in range(0, len(bancos)):
                with open('./bancos/'+bancos[i]) as B:
                    contas = json.load(B)
                    if contaB in contas:
                        with xmlrpc.client.ServerProxy("http://localhost:"+str(contas["porta"])+"/RPC2") as b:
                            self.contas[contaA] -= moedas
                            b.deposito(contaB, moedas)
                            self.salvar()
                            return "Operacao Concluída"
            return "Operacao Invalida"
        self.contas[contaA] -= moedas
        self.contas[contaB] += moedas
        self.salvar()
        return "Operacao Concluída"

with SimpleXMLRPCServer(('localhost', porta), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    NovoBanco = Banco()
    while True:
        conta = input("Digite Conta")
        if conta == 'sair':
            break
        moedas = int(input("Digite Moedas"))
        NovoBanco.deposito(conta, moedas)
    server.register_instance(NovoBanco)
    server.serve_forever()
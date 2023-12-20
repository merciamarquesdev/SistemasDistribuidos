from conta import Conta
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class Banco:
    def __init__(self, nome, endereco, porta):
        self.nome = nome
        self.endereco = endereco
        self.porta = porta
        self.contas = []

    def criar_conta(self, numero, saldo_inicial):
        conta = Conta(numero, saldo_inicial)
        self.contas.append(conta)

    def depositar(self, numero_conta, valor):
        for conta in self.contas:
            if conta.numero == numero_conta:
                conta.depositar(valor)
                return True
        return False

    def sacar(self, numero_conta, valor):
        for conta in self.contas:
            if conta.numero == numero_conta:
                return conta.sacar(valor)
        return False

    def obter_saldo(self, numero_conta):
        for conta in self.contas:
            if conta.numero == numero_conta:
                return conta.saldo
        return None

    def obter_contas(self):
        return self.contas

    def iniciar_servidor_xmlrpc(self):
        server = SimpleXMLRPCServer((self.endereco, self.porta), requestHandler=SimpleXMLRPCRequestHandler)
        server.register_instance(self)
        print(f"Iniciando servidor XML-RPC em {self.endereco}:{self.porta}")
        server.serve_forever()

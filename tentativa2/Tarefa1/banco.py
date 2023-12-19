from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class Banco:
    def __init__(self, nome, endereco, porta):
        self.nome = nome
        self.contas = {}
        self.endereco = endereco
        self.porta = porta

        self.server = SimpleXMLRPCServer((self.endereco, self.porta), requestHandler=RequestHandler)
        self.server.register_function(self.depositar, 'depositar')

    def criar_conta(self, numero_conta, saldo_inicial):
        self.contas[numero_conta] = saldo_inicial

    def transferir(self, conta_origem, conta_destino, valor):
        if conta_origem in self.contas and conta_destino in self.contas:
            if conta_origem[:3] == conta_destino[:3]:
                self.transferencia_local(conta_origem, conta_destino, valor)
            else:
                self.transferencia_remota(conta_origem, conta_destino, valor)
        else:
            print("Conta(s) inválida(s).")

    def transferencia_local(self, conta_origem, conta_destino, valor):
        if self.contas[conta_origem] >= valor:
            self.contas[conta_origem] -= valor
            self.contas[conta_destino] += valor
            print(f"Transferência local de {valor} de {conta_origem} para {conta_destino} realizada com sucesso.")
        else:
            print(f"Saldo insuficiente na conta {conta_origem}.")

    def transferencia_remota(self, conta_origem, conta_destino, valor):
        if self.contas[conta_origem] >= valor:
            self.contas[conta_origem] -= valor
            self.depositar(conta_destino, valor)
            print(f"Transferência remota de {valor} de {conta_origem} para {conta_destino} realizada com sucesso.")
        else:
            print(f"Saldo insuficiente na conta {conta_origem}.")

    def depositar(self, conta_destino, valor):
        if conta_destino in self.contas:
            self.contas[conta_destino] += valor
            return True
        else:
            return False

    def iniciar_servidor_xmlrpc(self):
        print(f"Iniciando servidor XML-RPC em {self.endereco}:{self.porta}")
        self.server.serve_forever()

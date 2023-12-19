import xmlrpc.client

class Cliente:
    def __init__(self, nome, banco, contas_e_transferencias):
        self.nome = nome
        self.banco = banco
        self.contas_e_transferencias = contas_e_transferencias

    def realizar_transferencias(self):
        for origem, destino, valor in self.contas_e_transferencias:
            self.banco.transferir(origem, destino, valor)

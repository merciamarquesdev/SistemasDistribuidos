import xmlrpc.client

class Cliente:
    def __init__(self, nome, banco, transferencias):
        self.nome = nome
        self.banco = banco
        self.transferencias = transferencias

    def realizar_transferencias(self):
        for transferencia in self.transferencias:
            conta_origem = transferencia[0]
            conta_destino = transferencia[1]
            valor = transferencia[2]

            if conta_origem.split("_")[0] == conta_destino.split("_")[0]:
                # Transferência local
                sucesso = self.banco.sacar(conta_origem, valor)
                if sucesso:
                    self.banco.depositar(conta_destino, valor)
                    print(f"Transferência local: {self.nome} transferiu R$ {valor},00 de {conta_origem} para {conta_destino}")
            else:
                # Transferência entre bancos
                valor_sacado = self.banco.sacar(conta_origem, valor)
                if valor_sacado:
                    endereco_destino = f"localhost:{int(conta_destino.split('_')[1])}"
                    proxy_destino = xmlrpc.client.ServerProxy(f"http://{endereco_destino}")
                    proxy_destino.depositar(conta_destino, valor)
                    print(f"Transferência entre bancos: {self.nome} transferiu R$ {valor},00 de {conta_origem} para {conta_destino}")

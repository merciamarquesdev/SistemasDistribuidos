class Conta:
    def __init__(self, numero, saldo_inicial):
        self.numero = numero
        self.saldo = saldo_inicial

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        else:
            return False

from banco import Banco
from cliente import Cliente
import random

def gerar_transferencias(bancos, num_transferencias):
    transferencias = []
    for _ in range(num_transferencias):
        origem_banco = random.choice(bancos)
        destino_banco = random.choice(bancos)
        origem_conta = f"{origem_banco.nome}_Conta_{random.randint(0, len(origem_banco.contas) - 1)}"
        destino_conta = f"{destino_banco.nome}_Conta_{random.randint(0, len(destino_banco.contas) - 1)}"
        valor = random.randint(2, 5)
        transferencias.append((origem_conta, destino_conta, valor))
    return transferencias

if __name__ == "__main__":
    num_bancos = 2
    num_contas_por_banco = 3
    bancos = [Banco(f"Banco_{i}", "localhost", 8000 + i) for i in range(num_bancos)]
    for banco in bancos:
        for i in range(num_contas_por_banco):
            conta_numero = f"{banco.nome}_Conta_{i}"
            banco.criar_conta(conta_numero, saldo_inicial=1000)

    num_clientes = 5
    clientes = []
    for i in range(num_clientes):
        transferencias_cliente = gerar_transferencias(bancos, random.randint(1, 5))
        clientes.append(Cliente(f"Cliente_{i}", random.choice(bancos), transferencias_cliente))
    for cliente in clientes:
        cliente.realizar_transferencias()

    for banco in bancos:
        print(f"\nEstado atual do banco {banco.nome}:")
        for conta in banco.obter_contas():
            print(f"Conta {conta.numero}: Saldo = {conta.saldo}")

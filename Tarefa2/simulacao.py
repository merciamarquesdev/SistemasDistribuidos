from banco import Banco
from cliente import Cliente
import random
import time

def gerar_transferencias(bancos, num_transferencias):
    transferencias = []
    for _ in range(num_transferencias):
        origem_banco = random.choice(bancos)
        destino_banco = random.choice(bancos)
        origem_conta = f"{origem_banco.nome}_Conta_{random.randint(0, len(origem_banco.contas) - 1)}"
        destino_conta = f"{destino_banco.nome}_Conta_{random.randint(0, len(destino_banco.contas) - 1)}"
        valor = random.randint(50, 200)
        transferencias.append((origem_conta, destino_conta, valor))
    return transferencias

if __name__ == "__main__":
    num_bancos = 10
    num_contas_por_banco = 5
    bancos = [Banco(f"Banco_{i}", "localhost", 8000 + i) for i in range(num_bancos)]

    for banco in bancos:
        for i in range(num_contas_por_banco):
            conta_numero = f"{banco.nome}_Conta_{i}"
            banco.criar_conta(conta_numero, saldo_inicial=1000)

    num_clientes = 200
    clientes = []
    for i in range(num_clientes):
        transferencias_cliente = gerar_transferencias(bancos, random.randint(1, 5))
        clientes.append(Cliente(f"Cliente_{i}", random.choice(bancos), transferencias_cliente))

    tempo_inicial = time.time()
    for cliente in clientes:
        cliente.realizar_transferencias()
    tempo_final = time.time()

    for banco in bancos:
        print(f"\nEstado atual do banco {banco.nome}:")
        for conta in banco.obter_contas():
            print(f"Conta {conta.numero}: Saldo = {conta.saldo}")

    tempo_total = tempo_final - tempo_inicial
    num_transferencias_total = sum(len(cliente.transferencias) for cliente in clientes)
    tempo_medio_por_operacao = tempo_total / num_transferencias_total if num_transferencias_total > 0 else 0
    throughput = num_transferencias_total / tempo_total if tempo_total > 0 else 0

    print("\nMétricas:")
    print(f"Tempo total: {tempo_total:.2f} segundos")
    print(f"Número total de transferências: {num_transferencias_total}")
    print(f"Tempo médio por operação: {tempo_medio_por_operacao:.6f} segundos")
    print(f"Throughput: {throughput:.6f} operações por segundo")

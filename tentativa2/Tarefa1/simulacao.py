from tentativa2.Tarefa1.banco import Banco
from tentativa2.Tarefa1.cliente import Cliente
import threading

def main():
    num_bancos = 3
    num_contas_por_banco = 5
    num_clientes = 2

    bancos = [Banco(f"Banco_{i}", "localhost", 8000 + i) for i in range(num_bancos)]

    for banco in bancos:
        for i in range(num_contas_por_banco):
            banco.criar_conta(f"{banco.nome}_Conta_{i}", saldo_inicial=1000)

    for banco in bancos:
        server_thread = threading.Thread(target=banco.iniciar_servidor_xmlrpc)
        server_thread.daemon = True
        server_thread.start()

    clientes = []
    for i in range(num_clientes):
        transferencias_cliente = [
            (f"Banco_{i % num_bancos}_Conta_{i % num_contas_por_banco}",
             f"Banco_{(i + 1) % num_bancos}_Conta_{(i + 1) % num_contas_por_banco}",
             100) for i in range(3)
        ]
        clientes.append(Cliente(f"Cliente_{i}", bancos[i % num_bancos], transferencias_cliente))

    for cliente in clientes:
        cliente.realizar_transferencias()

if __name__ == "__main__":
    main()

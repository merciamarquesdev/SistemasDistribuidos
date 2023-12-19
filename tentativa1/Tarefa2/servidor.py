import os
import json
import http.server
import http.client
import asyncio
import threading
import time

class Banco:
    def __init__(self, nome, porta, contas):
        self.nome = nome
        self.porta = porta
        self.contas = contas
        self.temposOperacoes = []
        self.salvar()

    def salvar(self):
        with open(f'./bancos/{self.nome}.json', 'w') as arquivo:
            json.dump(self.contas, arquivo)

    def cadastrar(self, conta):
        if conta not in self.contas:
            self.contas[conta] = [0, {}]
            self.salvar()
            return f"Conta {conta} criada com sucesso!"
        else:
            return "Esta conta já existe!"

    def consultar(self, conta):
        if conta not in self.contas:
            return "Esta conta não existe!" 
        else:
            return f"Conta {conta}: {self.contas[conta]}"

    def depositar(self, conta, valor):
        if conta not in self.contas:
            return "Esta conta não existe!" 
        elif valor <= 0:
            return "O valor do depósito deve ser maior que zero."
        else:
            self.contas[conta][0] += valor
            self.salvar()
            return f"Depósito concluído com sucesso! Saldo {conta}: {self.contas[conta][0]}"

    def transferencia(self, conta1, conta2, valor):
        if valor <= 0:
            return "O valor do depósito deve ser maior que zero."
        elif conta1 not in self.contas:
            return f"Esta conta não existe!"
        elif self.contas[conta1][0] < valor:
            return f"Saldo insuficiente."
        elif conta2 in self.contas: 
            self.contas[conta1][0] -= valor
            self.contas[conta2][0] += valor
            self.salvar()
            return "Transferência concluída com sucesso!"
        else:
            bancos = os.listdir('./bancos')
            for i in range(len(bancos)):
                with open(f'./bancos/{bancos[i]}') as B:
                    contas = json.load(B)
                    if conta2 in contas:
                        id_transacao = self.nome + str(len(self.contas[conta1][1]))
                        self.contas[conta1][0] -= valor 
                        self.contas[conta1][1][id_transacao] = {
                                "ID": id_transacao,
                                "Origem": [self.nome, self.porta, conta1],
                                "Destino": [bancos[i].split(".")[0], contas["porta"][0], conta2],
                                "Valor": valor,
                                "Resposta": 0
                            }
                        self.salvar()
                        return "Transação em andamento..."
        return f"A conta {conta2} não existe!"

    def resposta(self, transacao):
        print(f"> Resposta {transacao['Resposta']} <")
        if transacao["Resposta"] == 0:
            if transacao["ID"] in self.contas[transacao["Destino"][2]][1]:
                return "Resposta já recebida!" 
            transacao["Resposta"] = 1
            self.contas[transacao["Destino"][2]][1][transacao["ID"]] = transacao
        elif transacao["Resposta"] == 1:
            if self.contas[transacao["Origem"][2]][1][transacao["ID"]]["Resposta"] == 2:
                return "Resposta já recebida!" 
            transacao["Resposta"] = 2
            self.contas[transacao["Origem"][2]][1][transacao["ID"]] = transacao
        elif transacao["Resposta"] == 2:
            if self.contas[transacao["Destino"][2]][1][transacao["ID"]]["Resposta"] == 3:
                transacao["Resposta"] = 5
                self.contas[transacao["Destino"][2]][1][transacao["ID"]] = transacao
                return "Resposta já recebida!"
            else:
                transacao["Resposta"] = 3
                self.contas[transacao["Destino"][2]][0] += transacao["Quantia"]
                self.contas[transacao["Destino"][2]][1][transacao["ID"]] = transacao
        elif transacao["Resposta"] == 3:
            transacao["Resposta"] = 4
            self.contas[transacao["Origem"][2]][1][transacao["ID"]] = transacao
        self.salvar_arquivo()
        return "Done"
    
    def calcularTempoMedio(self):
        if not self.temposOperacoes:
            return 0  # Nenhuma operação registrada
        return sum(self.temposOperacoes) / len(self.temposOperacoes)

    def calcularThroughput(self, tempoTotal):
        if not self.temposOperacoes:
            return 0
        return len(self.temposOperacoes) / tempoTotal


def conectarBanco():
    banco = input("Insira o banco desejado (Para finalizar a sessão, insira 'sair'): \n")
    if banco.lower() == "sair":
        return None
    try:
        with open(f'./bancos/{banco}.json','a+') as arquivo:
            print('cu')
            contas = json.load(arquivo)
            print('boo')
            return Banco(banco, contas["porta"][0], contas)
    except FileNotFoundError:
        print(f"Arquivo para o banco {banco} não encontrado. Tente novamente.")
        return conectarBanco()
   

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def doPOST(self):
        contentLength = int(self.headers['Content-Length'])
        postData = self.rfile.read(contentLength).decode('utf-8')
        data = json.loads(postData)

        banco = conectarBanco()
        if banco is None:
            return

        if self.path == '/cadastro':
            response = banco.cadastro(data['conta'])
        elif self.path == '/consulta':
            response = banco.consulta(data['conta'])
        elif self.path == '/deposito':
            response = banco.deposito(data['conta'], data['valor'])
        elif self.path == '/transferencia':
            response = banco.transferencia(data['conta1'], data['conta2'], data['valor'])
        elif self.path == '/resposta':
            response = banco.resposta(data)
        else:
            response = 'Endpoint inválido.'

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode())


def startBank(porta):
    with http.server.HTTPServer(('localhost', porta), RequestHandler) as server:
        server.serve_forever()

def startTransactions():
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    new_loop.run_until_complete(loop())

async def loop():
    while True:
        await pendingTransactions(banco)
        await asyncio.sleep(2)
            

async def pendingTransactions(banco):
    print("> Pending Transactions <")
    for conta in banco.contas:
        for transacao in banco.contas[conta][1]:
            transacao = banco.contas[conta][1][transacao]
            if transacao["Origem"][0] == banco.nome:
                porta = transacao["Destino"][1]
            else:
                porta = transacao["Origem"][1]   
            if transacao["Resposta"] != 3 and transacao["Resposta"] != 4:
                if transacao["Resposta"] == 5:
                    transacao["Resposta"] = 3
                try:
                    with http.client.HTTPConnection(f"localhost:{porta}") as conn:
                        enviarRequisicao(conn, '/resposta', transacao)
                except Exception as e:
                    print("Resposta falhou! Erro: {}".format(str(e)))


def enviarRequisicao(conn, endpoint, data=None):
    headers = {'Content-type': 'application/json'}
    conn.request('POST', endpoint, json.dumps(data) if data else None, headers)
    response = conn.getresponse()
    return response.read().decode()



if __name__ == "__main__":
    banco = conectarBanco()
    if banco is not None:
        threading.Thread(target=startBank).start()
        threading.Thread(target=loop).start()
        
    def main():
        while True:
            startTime = time.time() 
            endTime = time.time()
            tempoOperacao = endTime - startTime
            banco.tempos_operacoes.append(tempoOperacao)  
            
    def start(porta):
        startTimeTotal = time.time() 
        with http.server.HTTPServer(('localhost', porta), RequestHandler) as server:
            endTimeTotal = time.time()  
            tempoTotal = endTimeTotal - startTimeTotal
            tempoMedio = banco.calcularTempoMedio()
            throughput = banco.calcularThroughput(tempoTotal)

        print(f"Tempo Médio por Operação: {tempoMedio} segundos")
        print(f"Throughput: {throughput} operações por segundo")

import http.server
import http.client
import json
import random

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        if self.path == '/deposito':
            response = banco.deposito(data['conta'], data['valor'])
        elif self.path == '/transferencia':
            response = banco.transferencia(data['conta1'], data['conta2'], data['valor'])
        else:
            response = 'Endpoint inválido!'

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode())

nome_banco = input("Insira o nome do Banco: \n")
caminho_banco = f'bancos\\{nome_banco}.json'

if os.path.isfile(caminho_banco):
    porta = random.randint(8000, 8900)
    contas = {"porta": porta}
else:
    with open(caminho_banco, 'r+') as arquivo:
        contas = json.load(arquivo)
        porta = contas["porta"]

class Banco:
    def __init__(self):
        self.contas = contas
        self.salvar()

    def salvar(self):
        with open(caminho_banco, 'w') as arquivo:
            json.dump(self.contas, arquivo)

    def deposito(self, conta, valor):
        if conta in self.contas:
            self.contas[conta] += valor
        else:
            self.contas[conta] = valor
        self.salvar()
        return "Transação finalizada com sucesso!"

    def transferencia(self, conta1, conta2, valor):
        if conta1 not in self.contas or self.contas[conta1] < valor:
            return "Erro. Esta transação é inválida."
        if conta2 not in self.contas:
            bancos = os.listdir('./bancos')
            for i in range(0, len(bancos)):
                with open(f'./bancos/{bancos[i]}') as b:
                    contas = json.load(b)
                    if conta2 in contas:
                        with http.client.HTTPConnection(f"localhost:{contas['porta']}") as conn:
                            enviar_requisicao(conn, '/deposito', {"conta": conta2, "valor": valor})
                            self.contas[conta1] -= valor
                            self.salvar()
                            return "Transação finalizada com sucesso!"
            return "Erro. Esta transação é inválida."
        self.contas[conta1] -= valor
        self.contas[conta2] += valor
        self.salvar()
        return "Transação finalizada com sucesso!"

def enviar_requisicao(conn, endpoint, data=None):
    headers = {'Content-type': 'application/json'}
    conn.request('POST', endpoint, json.dumps(data) if data else None, headers)
    response = conn.getresponse()
    return response.read().decode()

with http.server.HTTPServer(('localhost', porta), RequestHandler) as server:
    banco = Banco()
    server.serve_forever()

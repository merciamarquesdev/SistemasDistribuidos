import subprocess
import time
import http.client

comando = "/usr/bin/python3"
servidor = "./servidor.py"
cliente = "./cliente.py"

cs = [comando, servidor]
ss = [comando, cliente]
inputFileS = "input/S"+str(i)+".txt"
outputFileS = "output/S"+str(i)+".txt"
inputFileC = "input/C"+str(i)+".txt"
outputFileC = "output/C"+str(i)+".txt"

def iniciarServidor(inputFileS, outputFileS):
    with open(inputFileS, "rb") as infile, open(outputFileS, "w+") as outfile:
        S = subprocess.Popen([comando, servidor], stdout=output_file, stderr=output_file, stdin=input_file)
        conn = http.client.HTTPConnection('localhost', 8000)  # servidor está na porta 8000
        conn.request('POST', '/', body=infile.read(), headers={'Content-type': 'application/octet-stream'})
        response = conn.getresponse()
        outfile.write(response.read().decode())

def iniciarCliente(inputFileC, outputFileC):
    with open(inputFileC, "rb") as infile, open(outputFileC, "w+") as outfile:
        C = subprocess.Popen([comando, cliente], stdin=input_file, stderr=output_file, stdout=output_file)
        conn = http.client.HTTPConnection('localhost', 8000)  # servidor está na porta 8000
        conn.request('POST', '/', body=infile.read(), headers={'Content-type': 'application/octet-stream'})
        response = conn.getresponse()
        outfile.write(response.read().decode())

for i in range(2):
    iniciarServidor(f"input/S{i}.txt", f"output/S{i}.txt")
    time.sleep(6)

for i in range(2):
    iniciarCliente(f"input/C{i}.txt", f"output/C{i}.txt")
    
print("Simulação finalizada!")

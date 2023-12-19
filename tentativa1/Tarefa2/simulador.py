import http.client
import subprocess
import time

comando = "/usr/bin/python3"
servidor = "./servidor.py"
cliente = "./cliente.py"

cs = [comando, servidor]
ss = [comando, cliente]

for i in range(1,3):
    with open("input/S"+str(i)+".txt", "rb") as inputFile:
        with open("output/S"+str(i)+".txt", "w+") as outputFile:
            S = subprocess.Popen([comando, servidor], stdout=outputFile, stderr=outputFile, stdin=inputFile)
            time.sleep(5)

for i in range(1,3):
    with open("input/C"+str(i)+".txt", "rb") as inputFile:
        with open("output/C"+str(i)+".txt", "w+") as outputFile:
            C = subprocess.Popen([comando, cliente], stdin=inputFile, stderr=outputFile, stdout=outputFile)


print("Simulação finalizada!")

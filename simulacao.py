import subprocess
import time

bancos = 2
clientes = 2

for i in range(bancos):
    with open("input/servidor"+str(i+1)+".txt", "rb") as input_file:
        with open("output/servidor"+str(i+1)+".txt", "w+") as output_file:
            S = subprocess.Popen(['python3', 'banco.py'], stdout=output_file, stderr=output_file, stdin=input_file)
            time.sleep(2)

for i in range(clientes):
    with open("input/cliente"+str(i+1)+".txt", "rb") as input_file:
        with open("output/cliente"+str(i+1)+".txt", "w+") as output_file:
            C = subprocess.Popen(['python3', 'cliente.py'], stdin=input_file, stderr=output_file, stdout=output_file)

time.sleep(5)

print("Fim da Simulacao")
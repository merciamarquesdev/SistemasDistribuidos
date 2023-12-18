import http.client
import time
import threading
import json

def start_server(input_file, output_file):
    with open(input_file, "rb") as infile, open(output_file, "w+") as outfile:
        conn = http.client.HTTPConnection('localhost', 8000)  # o servidor está na porta 8000
        conn.request('POST', '/', body=infile.read(), headers={'Content-type': 'application/octet-stream'})
        response = conn.getresponse()
        outfile.write(response.read().decode())

def start_client(input_file, output_file):
    with open(input_file, "rb") as infile, open(output_file, "w+") as outfile:
        conn = http.client.HTTPConnection('localhost', 8000)  # o servidor está na porta 8000
        conn.request('POST', '/', body=infile.read(), headers={'Content-type': 'application/octet-stream'})
        response = conn.getresponse()
        outfile.write(response.read().decode())

for i in range(2):
    threading.Thread(target=start_server, args=(f"input/servidor{i+1}.txt", f"output/servidor{i+1}.txt")).start()
    time.sleep(2)

for i in range(2):
    threading.Thread(target=start_client, args=(f"input/cliente{i+1}.txt", f"output/cliente{i+1}.txt")).start()

time.sleep(5)

print("Simulação finalizada!")

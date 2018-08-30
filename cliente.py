#!/usr/bin/python3

import socket
import os

os.system('clear')

HOST = '10.25.2.58'
PORT = 50000

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT))

print("Conectado com: " + str(HOST))
print('Para sair use EXIT\n')

msg = None

while True:
	msg = input('Digite a mensagem: ')
	msg = msg.encode('utf-8')
	tcp_socket.send(msg)

	if msg.decode('utf-8') == 'EXIT':
		txt = tcp_socket.recvfrom(1024)
		tcp_socket.close()
		print("As mensagens guardadas no servidor: \n['" + txt[0].decode('utf-8') + "']")
		print("Conexão finalizada...")
		break

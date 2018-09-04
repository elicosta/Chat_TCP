#!/usr/bin/python3

import socket
import os

os.system('clear')

HOST = '10.20.2.23'
PORT = 50000
NOME = None

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT))

NOME = input('Digite nome de usuário: ')

print("Conectado com: " + str(NOME))
print('Para sair use EXIT\n')

NOME = NOME.encode('utf-8')
tcp_socket.send(NOME)

msg = None

while True:
	
	msg = input('Digite a mensagem: ')
	msg = msg.encode('utf-8')
	tcp_socket.send(msg)

	if msg.decode('utf-8') == 'EXIT':
		BD = tcp_socket.recvfrom(1024)
		BD = BD[0].decode('utf-8')
		tcp_socket.close()
		print("As mensagens guardadas no servidor: \n" + BD)
		print("Conexão finalizada...")
		break

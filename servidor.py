#!/usr/bin/python3

import socket
import os

os.system('clear')

HOST = ''
PORT = 50000

mensagens = []

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT))
tcp_socket.listen(1)

print('Aguardando conexão')

while True:
	con, cliente = tcp_socket.accept()
	print("Conectado com: " + str(cliente[0]))
	while True:
		msg = con.recvfrom(1024)
		if msg[0].decode('utf-8') == 'EXIT':
			data = "' , '".join(mensagens)
			data = data.encode('utf-8')
			#a, b, c, d, e = mensagens.split(",")
			con.send(data)
			print("Ultimas mensagens recebidas pelo servidor:\n " + str(mensagens))
			con.close()
			break
		else:
			mensagens.append(msg[0].decode('utf-8'))
			if len(mensagens) == 6:
				del mensagens[0]
			print("Host " + cliente[0] +": ", msg[0].decode('utf-8'))

	break
  
print('Finalizando conexão do cliente ', cliente)

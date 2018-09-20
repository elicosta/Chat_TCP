#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
import os
import threading
import time

HOST = 'localhost'
PORT = 50000

mensagens = []

#def enviar(con, username, msg):
#	broad = str(username + ": " + msg)
#	broad = broad.encode('utf-8')
#	con.send(broad)

def conection(con, cliente):
	username = con.recv(1024)
	username = username.decode('utf-8')

	print(username + " conectou com o servidor...")

	while True:
		msg = con.recv(1024)
		msg = msg.decode('utf-8')

		if msg == '\x18':
			data = "\n".join(mensagens)
			data = data.encode('utf-8')
			con.send(data)
			time.sleep(1)
			break
		else:
			mensagens.append(username + ": " + msg)
			print(username + ": " + msg)

	print(username + " desconectou do servidor...")
	con.close()

#------------------------------------------------------------
# Bloco principal
#------------------------------------------------------------
os.system('clear')

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((HOST, PORT))
tcp_socket.listen(1)

print('Servidor TCP iniciado no IP', HOST, 'na porta', PORT)
print('\nAguardando conexão')
	
while True:
	#Aceitando conexão
	con, cliente = tcp_socket.accept()

	# Thread de conexão
	connect = threading.Thread(target=conection, args=(con, cliente))

	#Iniciando a Thread e ativando daemon
	connect.setDaemon(True)
	connect.start()

tcp_socket.close()

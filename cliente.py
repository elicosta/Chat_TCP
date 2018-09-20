#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import os
import threading
import time

os.system('clear')

def escutar(con):
	while True:
		recvmsg = con.recv(1024)
		recvmsg = recvmsg.decode('utf-8')
		print("<Servidor>>> \n" + recvmsg)

#------------------------------------------------------------------------------------------
#Bloco Principal
#------------------------------------------------------------------------------------------
host = input('HOST: ')
port = int(input('PORT: '))

if (len(host) > 0):
	host = host
else:
	host = 'localhost'

if (port > 0 and port < 65535):
	port = int(port)
else:
	print("porta inválida!!!\nUsando porta padrão: 50000")
	port = 50000

tcp_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_connect.connect((host, port))

ouvir = threading.Thread(target=escutar, args=(tcp_connect,))
ouvir.setDaemon(True)


nick = input('Digite nome de usuário: ')
tcp_connect.send(nick.encode('utf-8'))

print("Conectado como: " + str(nick))
print('Para sair use CTRL+X\n')

ouvir.start()

while True:

	msg = input('Digite a mensagem: ')
	msg = msg.encode('utf-8')
	tcp_connect.send(msg)

	if msg.decode('utf-8') == '\x18':
		time.sleep(1)
		break
		
tcp_connect.close()
print("\nConexão finalizada...")

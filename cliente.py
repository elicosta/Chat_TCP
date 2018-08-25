#!/usr/bin/python3

import socket
import os

os.system('clear')

HOST = '192.168.0.19'
PORT = 50000

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT))

print("Conectado com: " + str(HOST))
print('Para sair use EXIT\n')

msg = input('Digite a mensagem: ') 
while msg != 'EXIT':
	msg = msg.encode('utf-8')
	tcp_socket.send(msg)
	print("Você enviou a mensagem: " + str(msg.decode('utf-8')))
	msg = input('Digite a mensagem: ')

msg = msg.encode('utf-8')
tcp_socket.send(msg)
print("Você enviou a mensagem: " + msg.decode('utf-8'))

#tcp_socket.bind((HOST, PORT))
#tcp_socket.listen(1)
#con, servidor = tcp_socket.accept()
mensagens = tcp_socket.recvfrom(1024)
print("As mensagens recebidas: \n['" + mensagens[0].decode('utf-8') + "']")
tcp_socket.close()

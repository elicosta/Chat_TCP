#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import threading
import socketserver

HOST = ''
PORT = 50000

clientes = []
nomes = []

class MyTCPServer(socketserver.BaseRequestHandler):

	def handle(self):
		clientes.append(self.request)
		self.setnick()
		#time.sleep(3)

		print(self.connection())
		welcome = str("Hora local: " + time.strftime('%H:%M') + " | " + str(len(clientes)) + " usuário(s)\n")
		self.request.send(welcome.encode('utf-8'))
		self.broadcast(self.connection())
		time.sleep(1)

		print(str(len(clientes)) + " usuários online\n")
        
		while True:
			try:
				data = self.request.recv(1024)
				data = data.decode('utf-8')
				print (self.nickname + "(" + self.client_address[0] + "): " + data)
				out = str(self.nickname + ": " + data)
				self.broadcast(out)
		        
			except:
				print(self.disconnection())
				clientes.remove(self.request)
				nomes.remove(self.nickname)
				self.broadcast(self.disconnection())
				self.request.close()
				print(str(len(clientes)) + " usuários online\n")

				return
        
	def broadcast(self, data):
		for user in clientes:
			if user != clientes:
				user.send(data.encode('utf-8'))

	def disconnection(self):
		return "\n" + self.nickname + "(" + self.client_address[0] + ") Desconectado de " + time.strftime('%H:%M')

	def connection(self):
		return "\n" + self.nickname + "(" + self.client_address[0] + ") Conectado de " + time.strftime('%H:%M')

	def setnick(self):
		self.nickname = self.request.recv(1024)
		self.request.send(b"Bem-Vindo, " + self.nickname + b"\n")
		self.nickname = self.nickname.decode('utf-8')
		nomes.append(self.nickname)

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

server = ThreadingTCPServer((HOST, PORT), MyTCPServer)

#------------------------------------------------------------
# Bloco principal
#------------------------------------------------------------
os.system('clear')

print("Bem-vindo ao CHAT\n")
print("Hora local: " + time.strftime('%H:%M') + " | " + str(len(clientes)) + " usuário(s)")  
print('Servidor iniciado no IP na porta', PORT)
print('\nAguardando conexões')

#Criando Servidor com base no IP e porta 50000
server_thread = threading.Thread(target=server.serve_forever)
# Terminar quando o main terminar
#server_thread.daemon = True
server_thread.start()

#server.shutdown()
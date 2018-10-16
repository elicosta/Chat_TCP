#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import socketserver

HOST = ''
PORT = 50000

clientes = []
nomes = []
mensagens = []

#------------------------------------------------------------------------------------------
#Funções do servidor
#------------------------------------------------------------------------------------------
class MyTCPServer(socketserver.BaseRequestHandler):

	def handle(self):
		clientes.append(self.request)
		self.setnick()

		print(self.connection())
		welcome = str("Hora local: " + time.strftime('%H:%M') + " | " + str(len(clientes)) + " usuário(s)\n")
		self.request.send(welcome.encode('utf-8'))
		self.broadcast(self.connection())

		print(str(len(clientes)) + " usuários online")

		#Envio das mensagens que estão armazenadas no servidor
		BD = "\n".join(mensagens)
		self.request.send(BD.encode('utf-8'))

		time.sleep(1)

		while True:
			try:
				data = self.request.recv(1024) #Recebendo informações dos clientes
				data = data.decode('utf-8')
				print (self.nickname + "(" + self.client_address[0] + "): " + data)
				out = str("- " + self.nickname + ": " + data)
				mensagens.append(out) #Armazenando informações no servidor
				self.broadcast(out) #Envio das mensagens para seus clientes
		        
			except:
				#Quando é finalizado conexão do cliente para o Servidor
				print(self.disconnection())
				clientes.remove(self.request)
				nomes.remove(self.nickname)
				self.broadcast(self.disconnection())
				self.request.close()
				print(str(len(clientes)) + " usuários online\n")

				return
        
	def broadcast(self, data):
		for user in clientes:
			user.send(data.encode('utf-8'))

	def disconnection(self):
		return "\n" + self.nickname + "(" + self.client_address[0] + ") Desconectado de " + time.strftime('%H:%M') + "\n"

	def connection(self):
		return "\n" + self.nickname + "(" + self.client_address[0] + ") Conectado de " + time.strftime('%H:%M') + "\n"

	def setnick(self):
		self.nickname = self.request.recv(1024)
		self.request.send(b"Bem-Vindo, " + self.nickname + b"\n")
		self.nickname = self.nickname.decode('utf-8')
		nomes.append(self.nickname)

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
		pass

#Criando Servidor com base no IP e porta 50000
server = ThreadingTCPServer((HOST, PORT), MyTCPServer)

#------------------------------------------------------------
# Bloco principal
#------------------------------------------------------------
os.system('clear')

print("Bem-vindo ao CHAT\n")
print("Hora local: " + time.strftime('%H:%M') + " | " + str(len(clientes)) + " usuário(s)")  
print('Servidor iniciado no IP na porta', PORT)
print('Para encerrar use CTRL+C\n')
print('\nAguardando conexões')

#Iniciando servidor socket
server.serve_forever()

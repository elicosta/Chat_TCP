#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import socketserver
import psycopg2

HOST = ''
PORT = 50000

clientes = []
nomes = []
mensagens = []

###Comando de conexões ao Banco###
ConexaoDefault  = "dbname=postgres user=postgres host=localhost password=aluno"
ConexaoDBmgs = "dbname=bdmgs user=postgres host=localhost password=aluno"
SQLCriaDatabase = "CREATE DATABASE bdmgs"

###Criar Tabela###
SQLCriaTable = "CREATE TABLE bdmgs (nome VARCHAR(100), data VARCHAR(20), hora VARCHAR(20), mensagem VARCHAR(200), endereco VARCHAR(30));"


#------------------------------------------------------------------------------------------
#Funções para o Banco de Dados
#------------------------------------------------------------------------------------------
def tabela_existe(NomeTabela):
	strSQL1 = "SELECT EXISTS(SELECT datname FROM pg_database WHERE datname='{0}')".format(NomeTabela)
	strSQL = "SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{0}')".format(NomeTabela)

	conn = psycopg2.connect(ConexaoDefault)
	curbd = conn.cursor()
	curbd.execute(strSQL1)
	existeBD = curbd.fetchone()[0]

	if(existeBD == True):
		con = psycopg2.connect(ConexaoDBmgs)
		cur = con.cursor()
		cur.execute(strSQL)
		existe = cur.fetchone()[0]
		cur.close()
		con.close()
	else:
		existe = False

	curbd.close()
	conn.close()

	return existe

def criarBanco():
	from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
	conn = psycopg2.connect(ConexaoDefault)
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute(SQLCriaDatabase)
	conn = psycopg2.connect(ConexaoDBmgs)
	cur = conn.cursor()
	cur.execute(SQLCriaTable)
	conn.commit()
	cur.close()
	conn.close()

def Guardarmsg(nome, data, hora, mensagem, endereco):
	conn = psycopg2.connect(ConexaoDBmgs)
	cur = conn.cursor()
	SQLInsereDados = "INSERT INTO bdmgs (nome, data, hora, mensagem, endereco) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(nome, data, hora, mensagem, endereco)
	cur.execute(SQLInsereDados)
	conn.commit()
	cur.close()
	conn.close()

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

		time.sleep(1)

		while True:
			try:
				mensagem = self.request.recv(1024) #Recebendo informações dos clientes
				mensagem = mensagem.decode('utf-8')
				hora = time.strftime('%H:%M:%S')
				data = time.strftime('%d-%m-%Y')

				print (self.nickname + "(" + self.client_address[0] + "): " + mensagem)
				out = str("- " + self.nickname + ": " + mensagem)
				self.broadcast(out) #Envio das mensagens para seus clientes

				if(mensagem !=''):
					Guardarmsg(self.nickname, data, hora, mensagem, self.client_address[0])
				
		        
			except:
				#Quando é finalizado conexão do cliente para o Servidor
				print(self.disconnection())
				clientes.remove(self.request)
				nomes.remove(self.nickname)
				self.broadcast(self.disconnection())
				self.request.close()
				print(str(len(clientes)) + " usuários online\n")

				return			
        
	def broadcast(self, mensagem):
		for user in clientes:
			user.send(mensagem.encode('utf-8'))

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

if (tabela_existe("bdmgs") == False):
	criarBanco()

#Iniciando servidor socket
server.serve_forever()

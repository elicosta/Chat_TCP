#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import os
import threading
import time
import json
import requests
import getpass

os.system('clear')

#------------------------------------------------------------------------------------------
#Recebendo mensagens do servidor TCP
#------------------------------------------------------------------------------------------

def escutar(con):
	while True:
		recvmsg = con.recv(1024)
		recvmsg = recvmsg.decode('utf-8')
		print(recvmsg)
		print("Digite sua mensagem: ")

#------------------------------------------------------------------------------------------
#Recebendo dados do SUAP
#------------------------------------------------------------------------------------------

#Login para autenticar ao Chat TCP
matricula = input("Informe sua matrícula: ")
senha = getpass.getpass("Infome sua senha: ")

autenticacao = {
    "username": str(matricula),
    "password": str(senha)
}

urls = { "token":"https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
         "dados":"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"}

def getToken():
    response = requests.post(urls['token'], data=autenticacao)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))['token']
    return None

cabecalho={'Authorization': 'JWT {0}'.format(getToken())}

def getInformacoes():
    response = requests.get(urls['dados'], headers=cabecalho)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None

informacoes = json.loads(getInformacoes())

#------------------------------------------------------------------------------------------
#Bloco Principal
#------------------------------------------------------------------------------------------
os.system('clear')

print("Por padrão:\nHOST: localhost\nPORT: 50000")

host = input('HOST: ')
port = input('PORT: ')

os.system('clear')

if (len(host) > 0):
	host = host
else:
	host = 'localhost'

if (len(port) > 0):
	port = int(port)
else:
	port = 50000

#Estabelecendo conexão
tcp_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_connect.connect((host, port))

#Criando thread para o broadcast do Servidor
ouvir = threading.Thread(target=escutar, args=(tcp_connect,))
ouvir.setDaemon(True)

#Enviando informação da API do SUAP para o Servidor
tcp_connect.send(informacoes['nome_usual'].encode('utf-8'))

print("Conectado como: " + informacoes['nome_usual'])
print('Para sair use CTRL+X\n')

#Ativando broadcast do cliente
ouvir.start()

time.sleep(1)

#Estrutura de envio de mensagens para o servidor
while True:
	msg = input()
	if msg == '\x18':
		break
	else:
		tcp_connect.send(msg.encode('utf-8'))
	
#Finalizando conexão
tcp_connect.close()
print("\nConexão finalizada...")

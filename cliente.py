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

#------------------------------------------------------------------------------------------
#Recebendo dados do SUAP
#------------------------------------------------------------------------------------------
#Login para autenticar ao Chat TCP
matricula = input("Informe sua matrícula: ")
senha = getpass.getpass("Infome sua senha: ")
#senha = input("Infome sua senha: ")

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

host = input('HOST: ')
port = int(input('PORT: '))

os.system('clear')

if (len(host) > 0):
	host = host
else:
	host = 'localhost'

if (len(host) > 0):
	port = int(port)
else:
	port = 50000

tcp_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_connect.connect((host, port))

ouvir = threading.Thread(target=escutar, args=(tcp_connect,))
ouvir.setDaemon(True)

tcp_connect.send(informacoes['nome_usual'].encode('utf-8'))

print("Conectado como: " + informacoes['nome_usual'])
print('Para sair use CTRL+X\n')

ouvir.start()

time.sleep(2)
while True:
	time.sleep(0.5)
	msg = input()
	msg = msg.encode('utf-8')
	tcp_connect.send(msg)

	if msg.decode('utf-8') == '\x18':
		#BD = tcp_connect.recv(1024)
		#BD = BD.decode('utf-8')
		#print("As mensagens guardadas no servidor: \n" + BD)
		break
		
tcp_connect.close()
print("\nConexão finalizada...")

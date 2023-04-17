import threading
import socket
import json

# Criando o socket do cliente (IPV4/TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 3000))

def mensagem(msg):
    json_mensagem = json.dumps(msg)
    client.sendall(json_mensagem.encode())
    data = client.recv(1024).decode('utf-8')
    msg = json.loads(data)
    return msg

# Thread para enviar mensagens
def sendMessages():
    while True:
        try:
            # Solicitando ao usuário que digite a mensagem
            method = int(input('Escolha uma opção\n 1- Exibir produtos da lista \n 2- Adicionar produto \n 3- Deletar um produto\n 4- Sair\n'))
            if(method == 1):
                request = {'method': 'GET'}
                response = mensagem(request)
                print(response, '\n')
            elif(method == 2):
                nome = input('Digite nome do produto:\n')
                preço = input('Digite preço do produto:\n')
                msg = {'nome': nome, 'preço': preço}
                request = {'method': 'POST', 'mensagem': msg}
                response = mensagem(request)
                print(response, '\n')
            elif(method == 3):
                id = int(input('Digite o id do item para deletar:\n'))
                msg = {'id': id}
                request = {'method': 'DELETE', 'mensagem': msg}
                response = mensagem(request)
                print(response, '\n')
            elif(method == 4):
                break
            else:
                # Enviando a mensagem para o servidor 
                print({'statusCode': '400' , 'msg' : 'BadRequest'})
        except:
            # Caso ocorra erro na conexão, finaliza e sai da função
            return


sendMessages()

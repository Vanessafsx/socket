import threading
import socket

# request = {'method': 'POST', 'mensagem': msg}

clients = []

 # cria um objeto de socket (IPV4/TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 3000))
server.listen()



# função para tratar as mensagens do cliente
def messagesTreatment(client):
    while True:
        try:
            # lê a mensagem do cliente
            msg = client.recv(2048)
            # envia a mensagem para todos os outros clientes conectados
            broadcast(msg, client)
        except:
            # remove o cliente da lista de clientes ao fechar a conexão ou dar erro de conexão com o cliente
            break

# função para enviar uma mensagem para todos os outros clientes conectados
def broadcast(msg, client):
    if msg.startswith("ERROR"):
        # envia a mensagem de erro para o cliente que enviou a mensagem
        try:
            client.send(msg.encode())
        except:
            # remove o cliente da lista de clientes conectados se houver um erro no envio da mensagem
            return
    
    else:
        # envia a mensagem para todos os outros clientes conectados
        for clientItem in clients:
            if clientItem != client:
                try:
                    # envia a mensagem para o cliente
                    clientItem.send(msg)
                except:
                    # remove o cliente da lista de clientes conectados se houver um erro no envio da mensagem
                    return


while True:
    # aceita a conexão do cliente
    client, addr = server.accept()
    # adiciona o objeto de socket do cliente à lista de clientes conectados
    clients.append(client)
    # cria uma nova thread para lidar com as mensagens do cliente
    thread = threading.Thread(target=messagesTreatment, args=[client])
    thread.start()
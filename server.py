import threading
import socket

clients = []

def main():

    # cria um objeto de socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # vincula o servidor a um endereço IP e porta especificados
        server.bind(('localhost', 3000))
        # coloca o servidor em um estado de escuta para aceitar conexões de clientes
        server.listen()
    except:
        # exibe uma mensagem de erro se a ligação falhar
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        # aceita a conexão do cliente
        client, addr = server.accept()
        # adiciona o objeto de socket do cliente à lista de clientes conectados
        clients.append(client)
        # cria uma nova thread para lidar com as mensagens do cliente
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

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

            
            deleteClient(client)
            break

# função para enviar uma mensagem para todos os outros clientes conectados
def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                # envia a mensagem para o cliente
                clientItem.send(msg)
            except:
                # remove o cliente da lista de clientes conectados se houver um erro no envio da mensagem
                deleteClient(clientItem)

# função para remover um cliente da lista de clientes conectados
def deleteClient(client):
    clients.remove(client)

# chama a função main para iniciar o servidor
main()
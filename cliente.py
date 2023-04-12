import threading
import socket

# Função principal
def main():
    # Criando o socket do cliente (IPV4/TCP)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Tentando conectar ao servidor
        client.connect(('localhost', 3000))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    # Solicitando o nome de usuário do cliente
    username = input('Usuário>')
    print('Conectado')

    # Inicializando as threads para receber e enviar mensagens
    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    # Iniciando as threads
    thread1.start()
    thread2.start()

# Thread para receber mensagens
def receiveMessages(client):
    #enquanto servidor estiver conectado está mandando algo para cliente
    while True:
        try:
            # Recebendo a mensagem do servidor
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            # Caso ocorra erro na conexão, finaliza o cliente, será desconectado
            print('\nNão foi possível se conectar com o servidor! Tecle <Enter>\n')
            client.close()
            break

# Thread para enviar mensagens
def sendMessages(client, username):
    while True:
        try:
            # Solicitando ao usuário que digite a mensagem
            msg = input('\n')
            # Enviando a mensagem para o servidor com o nome de usuário do cliente
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            # Caso ocorra erro na conexão, finaliza o cliente e sai da função
            return

# Iniciando a função principal
main()

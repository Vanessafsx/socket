import threading
import socket
import json

# request = {'method': 'POST', 'mensagem': msg}

 # cria um objeto de socket (IPV4/TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 3000))
server.listen()

# Array para armazenar os dados
clients = []
id = 0

# Função para lidar com um cliente
def handle_client(conn):
    global id
    while True:
        # Recebe os dados do cliente
        data = conn.recv(1024).decode()
        if not data:
            break

        # Converte a mensagem JSON recebida em um dicionário Python
        request = json.loads(data)
        print("HTTP Request: ",request)
        
        # Verifica o tipo de mensagem
        if request['method'] == 'POST':
            # Adiciona os dados recebidos ao array
            request['mensagem']['id'] = id
            id += 1
            clients.append(request['mensagem'])
            # Envia uma mensagem de confirmação com código de status HTTP 201
            response = {'status': '201 OK', 'content-type': 'text/plain', 'msg': 'Item adicionado com sucesso.'}
            conn.sendall(json.dumps(response).encode())

        elif request['method'] == 'DELETE':

            indice = request['mensagem']['id']
            for x in clients: 
                if(x['id'] == indice):
                    clients.remove(x)
                    response = {'status': '200 OK', 'content-type': 'application/json', 'dados':clients}
                    conn.sendall(json.dumps(response).encode())
                    break

        elif request['method'] == 'GET':
            # Envia os dados armazenados no array
            if len(clients) == 0:
                # Envia uma mensagem de erro com código de status HTTP 404
                response = {'status': '404 Not Found', 'content-type': 'text/plain', 'msg': 'Nenhum produto cadastrado.','dados':clients}
                conn.sendall(json.dumps(response).encode())
            else:
                # Envia uma mensagem de sucesso com código de status HTTP 200
                response = {'status': '200 OK', 'content-type': 'application/json', 'dados':clients}
                conn.sendall(json.dumps(response).encode())

        else:
            # Envia uma mensagem de erro com código de status HTTP 400
            response = {'status': '400 Bad Request', 'content-type': 'text/plain', 'msg': 'Opção inválida.'}
            conn.sendall(json.dumps(response).encode())

    
    
    # Fecha a conexão
    conn.close()

while True:
    # aceita a conexão do cliente
    client, addr = server.accept()
    # cria uma nova thread para lidar com as mensagens do cliente
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()

import socket
import threading

# Соединение
host = '127.0.0.1'
port = 55555

# создание сокета
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# списки клиентов и их имен
AppClients = []
UserNames = []

def streamToAll(message):
    for client in AppClients:
        client.send(message)

def handler(client):
    while True:
        try:
            # вывод сообщения
            message = client.recv(1024)
            streamToAll(message)
        except:
            # удаление клиентов
            index = AppClients.index(client)
            AppClients.remove(client)
            client.close()
            nickname = UserNames[index]
            streamToAll('{} вышел!'.format(nickname).encode('utf-8'))
            UserNames.remove(nickname)
            break

def receive():
    while True:
        # подтверждения подключения
        client, address = server.accept()
        print("Подключился {}".format(str(address)))
        client.send('name'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        UserNames.append(nickname)
        AppClients.append(client)
        # подключение клиента
        print("Пользователь {}".format(nickname))
        streamToAll("{} присоединился!".format(nickname).encode('utf-8'))
        client.send('Подключен!'.encode('utf-8'))
        # создание потока клиента
        thread = threading.Thread(target=handler, args=(client,))
        thread.start()

receive()
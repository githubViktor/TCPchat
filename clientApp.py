import socket
import threading

# Ввод имени
UserName = input("Введите свое имя:")

# Подключение
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


def receive():
    while True:
        try:
            # получение сообщения
            message = client.recv(1024).decode('utf-8')
            if message == 'name':
                client.send(UserName.encode('utf-8'))
            else:
                print(message)
        except:
            # ошибка подключения
            print("ошибка подключения")
            client.close()
            break

# отправка сообщений
def write():
    while True:
        message = '{}: {}'.format(UserName, input(''))
        client.send(message.encode('utf-8'))


# создание потоков(чтение и отправка)
rec_thread = threading.Thread(target=receive)
rec_thread.start()
wr_thread = threading.Thread(target=write)
wr_thread.start()


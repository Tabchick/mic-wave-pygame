import socket
import threading

HOST = '0.0.0.0'
PORT = 8080

clients = []
clients_lock = threading.Lock()  # Исправлена опечатка (было threarding)


def broadcast(data, exclude_socket=None):  # Исправлено имя функции (было boardcast)
    with clients_lock:
        current_clients = list(clients)
    
    # Исправлена переменная цикла: for client in current_clients
    for client in current_clients:
        if client != exclude_socket:
            try:
                client.sendall(data)
            except Exception as e:
                print(f"[ERROR] Помилка відправки клієнту: {e}")
                remove_client(client)


def remove_client(client_socket):  # Имя функции приведено к стандарту remove_client
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
            try:
                client_socket.close()  # Исправлено: закрываем client_socket, а не socket
            except:
                pass


def handle_client(client_socket, addr):
    print(f"[+ NEW CONNECTION] Клієнт {addr} підключився")
    
    # Добавляем подключенного клиента в список
    with clients_lock:
        clients.append(client_socket)
    
    while True:
        try:
            chunk = client_socket.recv(65536)
            if not chunk:
                break
            
            broadcast(chunk, exclude_socket=client_socket)
            
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"[ERROR] Помилка з клієнтом {addr}: {e}")
            break
        
    print(f"[- DISCONNECT] Клієнт {addr} відключився")
    remove_client(client_socket)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"[SERVER STARTED] Сервер запущено на {HOST}:{PORT}")
        
        # Добавлен цикл приема подключений
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()

    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
import socket
import threading
import logging

# Default log file name
DEFAULT_LOG_FILE = "loadbalancer.log"

# Set up logging with the default log file
logging.basicConfig(filename=DEFAULT_LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    protocol, method, message = request.split(' ', 2)

    if protocol == "TCP":
        server_address = ("127.0.0.1", 8000)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(server_address)
        http_request = f"{method} / HTTP/1.1\r\nContent-Length: {len(message)}\r\n\r\n{message}"
        server_socket.send(http_request.encode())
        response = server_socket.recv(1024)
        server_socket.close()
    elif protocol == "UDP":
        server_address = ("127.0.0.1", 8080)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        http_request = f"{method} {message}"
        server_socket.sendto(http_request.encode(), server_address)
        response, _ = server_socket.recvfrom(1024)

    client_socket.send(response)
    log_message = f"Load Balancer: Sent {method} {message} to {protocol} Server"
    print(log_message)
    logging.info(log_message)
    client_socket.close()

def main():
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    load_balancer_socket.bind(("0.0.0.0", 9999))
    print("Load Balancer listening on port 9999")
    logging.info("Load Balancer listening on port 9999")

    while True:
        load_balancer_socket.listen(5)
        client_socket, addr = load_balancer_socket.accept()
        log_message = f"Accepted connection from {addr}"
        print(log_message)
        logging.info(log_message)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
import socket
import threading
import logging

DEFAULT_LOG_FILE = "loadbalancer.log"
logging.basicConfig(filename=DEFAULT_LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        protocol, method, message = request.split(' ', 2)

        if protocol.upper() == "TCP":
            server_address = ("127.0.0.1", 8000)
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(server_address)
            server_socket.send(message.encode())
            response = server_socket.recv(1024)
            server_socket.close()
        elif protocol.upper() == "UDP":
            server_address = ("127.0.0.1", 8080)
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.sendto(message.encode(), server_address)
            response, _ = server_socket.recvfrom(1024)
        else:
            response = b"Unsupported protocol"

        client_socket.send(response)
        client_socket.close()
        logging.info(f"Load Balancer: Sent {message} to {protocol} Server")

    except Exception as e:
        logging.error(f"Load Balancer error: {e}")
        client_socket.close()

def main():
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    load_balancer_socket.bind(("0.0.0.0", 9999))
    print("Load Balancer listening on port 9999")
    logging.info("Load Balancer listening on port 9999")

    while True:
        try:
            load_balancer_socket.listen(5)
            client_socket, addr = load_balancer_socket.accept()
            logging.info(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

        except Exception as e:
            logging.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()

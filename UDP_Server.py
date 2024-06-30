import socket
import logging
import argparse

# Default log file name
DEFAULT_LOG_FILE = "udp_server.log"

# Set up logging with the default log file
logging.basicConfig(filename=DEFAULT_LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def main(logfile):
    server_address = ('localhost', 8080)
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(server_address)
        print(f"UDP Server listening on {server_address}")
        logging.info(f"UDP Server listening on {server_address}")

        while True:
            data, addr = server_socket.recvfrom(buffer_size)
            message = data.decode()
            print(f"Received message from {addr}: {message}")
            logging.info(f"Received message from {addr}: {message}")

            # Parse the method and message
            try:
                method, msg = message.split(' ', 1)
            except ValueError:
                method = message
                msg = ""

            if method == "GET":
                response = "HTTP/1.1 200 OK\r\n\r\n" + f"UDP Server received: {msg}"
            elif method == "POST":
                response = "HTTP/1.1 201 Created\r\n\r\n" + f"UDP Server received: {msg}"
            elif method == "DELETE":
                response = "HTTP/1.1 204 No Content\r\n\r\n"
            else:
                response = "HTTP/1.1 400 Bad Request\r\n\r\n" + "Invalid request method"

            server_socket.sendto(response.encode(), addr)
            print(f"Sent response to {addr}: {response}")
            logging.info(f"Sent response to {addr}: {response}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-logfile', default=DEFAULT_LOG_FILE, help='Log file name')
    args = parser.parse_args()

    main(args.logfile)

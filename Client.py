import socket

load_balancer_address = ('localhost', 9999)

def main():
    while True:
        try:
            protocol = input("Connect to (TCP/UDP): ").upper()
            method = input("Method (GET/POST/DELETE): ").upper()
            message = input("Message: ")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
                lb_socket.connect(load_balancer_address)
                request = f"{protocol} {method} {message}"
                lb_socket.sendall(request.encode())

                lb_response = lb_socket.recv(1024)
                print(f"Received response from Load Balancer: {lb_response.decode()}")

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()

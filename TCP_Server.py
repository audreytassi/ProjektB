from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import logging

DEFAULT_LOG_FILE = "tcp_server.log"
logging.basicConfig(filename=DEFAULT_LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"GET request received")

    def do_POST(self):
        self.send_response(201)
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.wfile.write(b"POST request received")

    def do_DELETE(self):
        self.send_response(204)
        self.end_headers()
        self.wfile.write(b"DELETE request received")

def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting TCP server on port {port}")
    logging.info(f"Starting TCP server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

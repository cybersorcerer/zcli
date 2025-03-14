import http.server
import ssl
import logging

class EchoRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"GET request received")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data.decode('utf-8')}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"POST request received")

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        logging.info(f"PUT request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{put_data.decode('utf-8')}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"PUT request received")

    def do_DELETE(self):
        logging.info(f"DELETE request,\nPath: {self.path}\nHeaders:\n{self.headers}")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"DELETE request received")

def run(server_class=http.server.HTTPServer, handler_class=EchoRequestHandler, port=4443):
    logging.basicConfig(level=logging.INFO)
    server_address = ('192.168.9.39', port)
    httpd = server_class(server_address, handler_class)

    # Create an SSL context with TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.pem')

    # Wrap the server's socket with the SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    logging.info(f'Starting https server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
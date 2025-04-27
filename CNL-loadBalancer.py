import socket
import ssl
import threading
import random
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# ==========================
#   CyberNet Labs - Secure Python Load Balancer
#   Version 2.0
# ==========================

stats = {
    "total_requests": 0,
    "backend_hits": {},
    "mode": "",
}

def cybernet_banner():
    banner = """
   ____             _                  _   _        _     
  / ___| _   _ _ __| |_ _   _ _ __ ___ | \ | | ___  | |__  
  \___ \| | | | '__| __| | | | '_ ` _ \|  \| |/ _ \ | '_ \ 
   ___) | |_| | |  | |_| |_| | | | | | | |\  |  __/ | |_) |
  |____/ \__,_|_|   \__|\__,_|_| |_| |_|_| \_|\___| |_.__/ 

                Secure Load Balancing System
                   Developed by CyberNet Labs
    """
    print(banner)

def get_user_inputs():
    cybernet_banner()
    print("Welcome to the CyberNet Labs Secure Load Balancer\n")

    backends = []
    while True:
        url = input("Enter backend server IP (e.g., 127.0.0.1:5000) or type 'done' to finish: ").strip()
        if url.lower() == 'done':
            break
        if ':' not in url:
            print("Invalid format. Please use IP:PORT format.")
            continue
        backends.append(url)

    if not backends:
        print("\n[!] No backend servers provided. Exiting...")
        sys.exit(1)

    try:
        listen_port = int(input("\nEnter Load Balancer listening port (e.g., 8443): ").strip())
    except ValueError:
        print("[!] Invalid port. Defaulting to 8443.")
        listen_port = 8443

    mode = input("\nSelect balancing mode - [round_robin/random] (default: round_robin): ").strip().lower()
    if mode not in ['round_robin', 'random']:
        print("[*] Defaulting to round_robin mode.")
        mode = 'round_robin'

    stats["mode"] = mode

    return backends, listen_port, mode

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('dashboard.html', 'r') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
        else:
            self.send_response(404)
            self.end_headers()

class LoadBalancer:
    def __init__(self, backends, port, mode):
        self.backends = backends
        self.listen_port = port
        self.mode = mode
        self.index = 0
        self.lock = threading.Lock()

    def select_backend(self):
        if self.mode == 'random':
            return random.choice(self.backends)
        else:
            with self.lock:
                backend = self.backends[self.index]
                self.index = (self.index + 1) % len(self.backends)
            return backend

    def handle_client(self, client_socket):
        backend = self.select_backend()
        backend_ip, backend_port = backend.split(':')
        backend_port = int(backend_port)

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((backend_ip, backend_port))
            print(f"[+] Forwarding traffic to backend {backend_ip}:{backend_port}")

            stats["total_requests"] += 1
            stats["backend_hits"][backend] = stats["backend_hits"].get(backend, 0) + 1

            threading.Thread(target=self.forward, args=(client_socket, server_socket)).start()
            threading.Thread(target=self.forward, args=(server_socket, client_socket)).start()

        except Exception as e:
            print(f"[!] Failed to connect to backend {backend_ip}:{backend_port} - {e}")
            client_socket.close()

    def forward(self, source, destination):
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)
        except Exception:
            pass
        finally:
            source.close()
            destination.close()

    def start(self):
        lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lb_socket.bind(('0.0.0.0', self.listen_port))
        lb_socket.listen(100)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        print(f"\n[*] CyberNet Labs Secure Load Balancer running on HTTPS port {self.listen_port}")
        print(f"[*] Balancing mode: {self.mode.upper()}")
        print(f"[*] Backend servers: {', '.join(self.backends)}")
        print("\n[*] Waiting for incoming secure client connections...\n")
        print(f"[*] Dashboard available at: https://localhost:{self.listen_port}/dashboard")

        threading.Thread(target=self.start_dashboard_server).start()

        while True:
            client_socket, addr = lb_socket.accept()
            secure_socket = context.wrap_socket(client_socket, server_side=True)
            print(f"[+] Accepted secure connection from {addr}")
            threading.Thread(target=self.handle_client, args=(secure_socket,)).start()

    def start_dashboard_server(self):
        server = HTTPServer(('0.0.0.0', 9090), DashboardHandler)
        print("[*] Dashboard web server running on http://localhost:9090")
        server.serve_forever()

if __name__ == "__main__":
    backends, listen_port, mode = get_user_inputs()
    load_balancer = LoadBalancer(backends, listen_port, mode)
    load_balancer.start()

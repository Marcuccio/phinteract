import http.server
from urllib.parse import urlparse
import socketserver
import csv
import os
from datetime import datetime

LOG_FILE = "/var/log/phinteract.csv"
PORT = 8080
WHITELISTED_PATHS = {"/recaptcha"}

# Assicura che il file di log esista
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Client IP", "User-Agent", "Path"])

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_path = urlparse(self.path).path
        print(url_path)

        if url_path in WHITELISTED_PATHS:
            timestamp = datetime.now()
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', '-')
            path = self.path

            print(f"[!!] {timestamp} - {client_ip} - {user_agent} - {path}")
            with open(LOG_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, client_ip, user_agent, path])
        else:
            print(f"{self.path} skipped")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        

if __name__ == "__main__":
    print(f"see log at: {LOG_FILE}")
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"[*] Server running on port {PORT}...")
        httpd.serve_forever()
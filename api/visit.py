from http.server import BaseHTTPRequestHandler
import requests
import os
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

        if not BOT_TOKEN or not CHAT_ID:
            self.send_response(500)
            self.wfile.write(json.dumps({'error': 'Missing env vars'}).encode('utf-8'))
            return

        ip_address = self.headers.get('X-Forwarded-For', 'Không rõ IP')
        user_agent = self.headers.get('User-Agent', 'Không rõ trình duyệt')

        message_text = (
            f"👤 Khách truy cập Bộ Lọc!\n\n"
            f"**IP:** `{ip_address}`\n"
            f"**Trình duyệt:** `{user_agent}`"
        )
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = { 'chat_id': CHAT_ID, 'text': message_text, 'parse_mode': 'Markdown' }
        requests.post(url, json=payload)

        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
        return
        
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return

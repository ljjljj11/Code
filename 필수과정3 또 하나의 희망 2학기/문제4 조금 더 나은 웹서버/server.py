#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from typing import Optional
import json

HOST = '0.0.0.0'
PORT = 8080


class IndexRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        client_ip = self.client_address[0]
        location = self._lookup_geo_ip(client_ip)
        access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if location:
            print(f'접속 시간: {access_time}, 클라이언트 IP: {client_ip}, 위치: {location}')
        else:
            print(f'접속 시간: {access_time}, 클라이언트 IP: {client_ip}, 위치: 확인 불가')

        if self.path in ('/', '/index.html'):
            self._serve_index()
            return

        self._send_not_found()

    def _serve_index(self) -> None:
        try:
            with open('index.html', 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            message = 'index.html 파일을 찾을 수 없습니다.'
            data = message.encode('utf-8')
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_not_found(self) -> None:
        message = '요청하신 리소스를 찾을 수 없습니다.'
        data = message.encode('utf-8')
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _lookup_geo_ip(self, client_ip: str) -> Optional[str]:
        if client_ip in ('127.0.0.1', '::1'):
            return '로컬호스트'

        url = f'http://ip-api.com/json/{client_ip}?fields=status,message,country,regionName,city'
        req = Request(url, headers={'User-Agent': 'Python-urllib/3'})
        try:
            with urlopen(req, timeout=2) as resp:
                payload = resp.read().decode(resp.headers.get_content_charset() or 'utf-8')
                data = json.loads(payload)
        except (URLError, HTTPError, json.JSONDecodeError, TimeoutError, ValueError):
            return None

        if data.get('status') != 'success':
            return None

        country = data.get('country') or ''
        region = data.get('regionName') or ''
        city = data.get('city') or ''
        parts = [p for p in (country, region, city) if p]
        return ' / '.join(parts) if parts else None


def run_server() -> None:
    httpd = HTTPServer((HOST, PORT), IndexRequestHandler)
    print(f'HTTP 서버가 시작되었습니다: http://{HOST}:{PORT}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n서버가 종료됩니다.')
    finally:
        httpd.server_close()


if __name__ == '__main__':
    run_server()

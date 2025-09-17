import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5000
ENCODING = 'utf-8'
BUF_SIZE = 4096
LINE_SEP = '\n'


def recv_loop(conn: socket.socket) -> None:
    while True:
        try:
            data = conn.recv(BUF_SIZE)
        except OSError:
            break
        if not data:
            break
        msg = data.decode(ENCODING, errors='ignore')
        print(msg, end='')
    print('\n[클라이언트] 서버 연결이 종료되었습니다.')


def main() -> None:
    print(f'[클라이언트] 서버 접속 {HOST}:{PORT}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        t = threading.Thread(target=recv_loop, args=(s,), daemon=True)
        t.start()

        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                text = line.rstrip('\r\n')
                s.sendall((text + LINE_SEP).encode(ENCODING))
                if text.strip() in ('/종료', '/quit', '/exit'):
                    break
        except KeyboardInterrupt:
            pass
    print('[클라이언트] 종료')


if __name__ == '__main__':
    main()

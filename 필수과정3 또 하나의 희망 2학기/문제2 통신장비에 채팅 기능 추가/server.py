import socket
import threading
from typing import Dict, Tuple

HOST = '0.0.0.0'
PORT = 5000
BACKLOG = 50
ENCODING = 'utf-8'
BUF_SIZE = 4096
LINE_SEP = '\n'

clients_lock = threading.Lock()
clients: Dict[str, socket.socket] = {}  # nickname -> socket


def broadcast(message: str, *, exclude: str | None = None) -> None:
    """모든 클라이언트에 메시지 방송. exclude 닉네임은 제외."""
    data = f'{message}{LINE_SEP}'.encode(ENCODING, errors='ignore')
    with clients_lock:
        to_remove = []
        for nick, conn in clients.items():
            if exclude and nick == exclude:
                continue
            try:
                conn.sendall(data)
            except OSError:
                to_remove.append(nick)
        for nick in to_remove:
            _safe_remove(nick)


def _safe_remove(nickname: str) -> None:
    """클라이언트 딕셔너리에서 안전하게 제거."""
    conn = clients.pop(nickname, None)
    if conn:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            conn.close()
        except OSError:
            pass


def send_to_one(nickname: str, message: str) -> bool:
    """특정 사용자에게만 메시지 전송. 성공 시 True."""
    with clients_lock:
        conn = clients.get(nickname)
        if not conn:
            return False
        data = f'{message}{LINE_SEP}'.encode(ENCODING, errors='ignore')
        try:
            conn.sendall(data)
            return True
        except OSError:
            return False


def parse_command(text: str) -> Tuple[str, list[str]]:
    """
    명령 파싱.
    반환: (command, args)
      예) '/종료' -> ('/종료', [])
          '/w bob 안녕' -> ('/w', ['bob', '안녕'])
    """
    text = text.strip()
    if not text.startswith('/'):
        return '', []
    parts = text.split(maxsplit=2)
    if len(parts) == 1:
        return parts[0], []
    if len(parts) == 2:
        return parts[0], [parts[1]]
    return parts[0], [parts[1], parts[2]]


def request_unique_nickname(conn: socket.socket, addr: Tuple[str, int]) -> str | None:
    """클라이언트에게 닉네임을 받아 유일성 보장."""
    prompt = (
        '닉네임을 입력하세요 (공백 없이, 1~20자). 이미 사용 중이면 다시 요청됩니다.'
        f'{LINE_SEP}> '
    ).encode(ENCODING)
    try:
        conn.sendall(prompt)
    except OSError:
        return None

    while True:
        try:
            data = conn.recv(BUF_SIZE)
        except OSError:
            return None
        if not data:
            return None
        nickname = data.decode(ENCODING, errors='ignore').strip()
        if not nickname or ' ' in nickname or len(nickname) > 20:
            try:
                conn.sendall(f'잘못된 닉네임입니다. 다시 입력하세요.{LINE_SEP}> '.encode(ENCODING))
            except OSError:
                return None
            continue

        with clients_lock:
            if nickname not in clients:
                clients[nickname] = conn
                return nickname
        try:
            conn.sendall(f'이미 사용 중인 닉네임입니다. 다시 입력하세요.{LINE_SEP}> '.encode(ENCODING))
        except OSError:
            return None


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """개별 클라이언트 스레드."""
    nickname = request_unique_nickname(conn, addr)
    if not nickname:
        try:
            conn.close()
        except OSError:
            pass
        return

    try:
        join_msg = f'{nickname}님이 입장하셨습니다.'
        broadcast(join_msg)

        help_msg = (
            '명령 도움말: /종료 (연결 종료), /w 닉 메시지 또는 /whisper 닉 메시지 (귓속말)'
        )
        send_to_one(nickname, help_msg)

        while True:
            try:
                data = conn.recv(BUF_SIZE)
            except OSError:
                break
            if not data:
                break

            text = data.decode(ENCODING, errors='ignore').rstrip('\r\n')
            if not text:
                continue

            cmd, args = parse_command(text)
            if cmd in ('/종료', '/quit', '/exit'):
                send_to_one(nickname, '연결을 종료합니다.')
                break

            if cmd in ('/w', '/whisper'):
                if len(args) < 2:
                    send_to_one(nickname, '형식: /w 대상닉 메시지')
                    continue
                target, msg = args[0], args[1]
                if target == nickname:
                    send_to_one(nickname, '자기 자신에게는 귓속말을 보낼 수 없습니다.')
                    continue
                ok = send_to_one(target, f'(귓속말) {nickname}> {msg}')
                if ok:
                    send_to_one(nickname, f'(귓속말 전송) {nickname} -> {target}> {msg}')
                else:
                    send_to_one(nickname, f'대상 \'{target}\'를 찾을 수 없습니다.')
                continue

            # 일반 메시지 브로드캐스트
            broadcast(f'{nickname}> {text}')
    finally:
        with clients_lock:
            existed = nickname in clients
        if existed:
            _safe_remove(nickname)
            broadcast(f'{nickname}님이 퇴장하셨습니다.')


def serve() -> None:
    """서버 메인 루프."""
    print(f'[INFO] 채팅 서버 시작: {HOST}:{PORT}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 포트 재사용
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(BACKLOG)
        print('[INFO] 클라이언트 접속 대기 중... (Ctrl+C로 종료)')

        try:
            while True:
                conn, addr = s.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                print(f'[INFO] 연결 수락: {addr[0]}:{addr[1]}')
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print('\n[INFO] 서버 종료 중...')
        finally:
            # 모든 클라이언트 종료
            with clients_lock:
                nicks = list(clients.keys())
            for nick in nicks:
                try:
                    send_to_one(nick, '서버가 종료됩니다.')
                finally:
                    _safe_remove(nick)
            print('[INFO] 서버가 정상 종료되었습니다.')


if __name__ == '__main__':
    serve()

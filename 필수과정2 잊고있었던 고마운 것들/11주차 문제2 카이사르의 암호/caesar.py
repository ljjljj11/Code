import os

def caesar_cipher_decode(target_text, dictionary):
    for shift in range(26):
        result = ''
        for char in target_text:
            if 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            elif 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                result += char

        print(f'[{shift}] {result}')

        words = result.lower().split()
        for word in words:
            if word in dictionary:
                print(f'[!] 사전 단어 발견: "{word}" → 자동 종료')
                return result, shift

    return None, None


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    password_path = os.path.join(base_dir, 'password.txt')
    result_path = os.path.join(base_dir, 'result.txt')

    try:
        with open(password_path, 'r') as f:
            cipher_text = f.read().strip()
    except FileNotFoundError:
        print('[!] password.txt 파일을 찾을 수 없습니다.')
        return

    print('[*] 복호화를 시작합니다.')

    dictionary = {
        'the', 'and', 'this', 'that', 'you', 'have', 'hello', 'from',
        'test', 'key', 'message', 'decode', 'found', 'success', 'open',
        'lock', 'data', 'file'
    }

    result, auto_index = caesar_cipher_decode(cipher_text, dictionary)

    try:
        if result is not None:
            final = result
        else:
            selected = input('[?] 해독된 것으로 보이는 번호를 입력하세요 (0-25): ')
            shift = int(selected)
            if not (0 <= shift < 26):
                print('[!] 잘못된 번호입니다.')
                return

            final = ''
            for char in cipher_text:
                if 'A' <= char <= 'Z':
                    final += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                elif 'a' <= char <= 'z':
                    final += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                else:
                    final += char

        with open(result_path, 'w') as result_file:
            result_file.write(final)
        print('[+] 결과가 result.txt에 저장되었습니다.')
    except Exception:
        print('[!] 번호 입력 중 오류가 발생했습니다.')


if __name__ == '__main__':
    main()

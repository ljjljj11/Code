import zipfile
import time
import string
import os
import multiprocessing

CHARS = string.ascii_lowercase + string.digits
ZIP_FILE_PATH = 'emergency_storage_key.zip'
PASSWORD_FILE_PATH = 'password.txt'
NUM_PROCESSES = multiprocessing.cpu_count()


def try_passwords(start_chars, file_list, found_flag):
    attempt_count = 0
    start_time = time.time()

    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_file:
        for c1 in start_chars:
            if found_flag.value:
                return
            for c2 in CHARS:
                for c3 in CHARS:
                    for c4 in CHARS:
                        for c5 in CHARS:
                            for c6 in CHARS:
                                if found_flag.value:
                                    return
                                password = f'{c1}{c2}{c3}{c4}{c5}{c6}'
                                attempt_count += 1
                                try:
                                    zip_file.open(file_list[0], pwd=password.encode('utf-8')).read(1)
                                    found_flag.value = 1

                                    elapsed = time.time() - start_time
                                    print(f'[+] 암호 발견: {password}')
                                    print(f'[+] 시도 횟수: {attempt_count}')
                                    print(f'[+] 소요 시간: {elapsed:.2f}초')

                                    with open(PASSWORD_FILE_PATH, 'w') as pw_file:
                                        pw_file.write(password)
                                    return
                                except Exception:
                                    if attempt_count % 100000 == 0:
                                        elapsed = time.time() - start_time
                                        print(f'[-] {attempt_count}회 시도 중... {elapsed:.1f}s 경과')
                                    continue


def unlock_zip():
    try:
        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_file:
            file_list = zip_file.namelist()
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f'[*] Brute-force 시작: {start_time}')

            total_chars = list(CHARS)
            chunk_size = len(total_chars) // NUM_PROCESSES
            chunks = [total_chars[i:i + chunk_size] for i in range(0, len(total_chars), chunk_size)]

            found_flag = multiprocessing.Value('i', 0)
            processes = []

            for chunk in chunks:
                p = multiprocessing.Process(target=try_passwords, args=(chunk, file_list, found_flag))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()
    except FileNotFoundError:
        print(f'[!] 파일을 찾을 수 없습니다: {ZIP_FILE_PATH}')
    except zipfile.BadZipFile:
        print(f'[!] 유효하지 않은 ZIP 파일입니다.')


if __name__ == '__main__':
    unlock_zip()

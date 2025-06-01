import os
import datetime
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


def make_records_dir():
    '''
    'records' 디렉토리가 존재하지 않으면 생성한다.
    '''
    records_path = os.path.join(os.getcwd(), 'records')
    if not os.path.exists(records_path):
        os.makedirs(records_path)
    return records_path


def create_file_path():
    '''
    현재 날짜와 시간을 기반으로 한 파일 경로를 생성한다.
    예: 20250601-153045.wav
    '''
    now = datetime.datetime.now()
    file_name = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    folder_path = make_records_dir()
    return os.path.join(folder_path, file_name)


def record_audio(duration_seconds=5, sample_rate=44100):
    '''
    마이크에서 음성을 녹음하고 파일로 저장한다.
    '''
    print('녹음을 시작합니다...')
    try:
        audio = sd.rec(int(duration_seconds * sample_rate),
                       samplerate=sample_rate,
                       channels=1,
                       dtype='int16')
        sd.wait()
        print('녹음이 완료되었습니다.')

        file_path = create_file_path()
        write(file_path, sample_rate, audio)
        print('파일이 저장되었습니다:', file_path)
    except Exception as e:
        print('녹음 중 오류가 발생했습니다:', str(e))


def main():
    '''
    메인 함수로, 사용자에게 녹음 시간을 입력받아 녹음을 수행한다.
    '''
    try:
        seconds = int(input('녹음할 시간을 초 단위로 입력하세요: '))
        if seconds <= 0:
            print('1초 이상 입력해야 합니다.')
            return
        record_audio(duration_seconds=seconds)
    except ValueError:
        print('숫자를 입력해주세요.')


if __name__ == '__main__':
    main()

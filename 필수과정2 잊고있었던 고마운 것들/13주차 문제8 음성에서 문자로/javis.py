import os
import csv
import speech_recognition as sr


def get_records_dir():
    '''
    상위 폴더의 '문제 16(코디세이)/records' 경로를 반환한다.
    '''
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    records_path = os.path.join(parent_path, '문제 16(코디세이)', 'records')
    return records_path


def get_output_dir():
    '''
    상위 폴더의 '문제 17(코디세이)' 경로를 반환한다.
    '''
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    output_path = os.path.join(parent_path, '문제 17(코디세이)')
    os.makedirs(output_path, exist_ok=True)
    return output_path


def get_wav_files():
    '''
    records 폴더 내의 모든 .wav 파일 목록을 반환한다.
    '''
    records_dir = get_records_dir()
    if not os.path.exists(records_dir):
        print('records 폴더가 존재하지 않습니다.')
        return []

    return [os.path.join(records_dir, f)
            for f in os.listdir(records_dir)
            if f.lower().endswith('.wav')]


def transcribe_audio(file_path):
    '''
    주어진 음성 파일 경로에서 텍스트를 추출하여 반환한다.
    '''
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='ko-KR')
        return text
    except sr.UnknownValueError:
        return '인식 실패'
    except sr.RequestError as e:
        return f'API 요청 실패: {e}'


def save_transcript(file_path, transcript):
    '''
    텍스트 결과를 문제 17 폴더에 .csv로 저장한다.
    '''
    output_dir = get_output_dir()
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    csv_path = os.path.join(output_dir, base_name + '.csv')

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['시간', '텍스트'])
        writer.writerow(['00:00:00', transcript])


def process_all_audio():
    '''
    모든 .wav 파일에 대해 STT 실행 및 csv 저장.
    '''
    wav_files = get_wav_files()
    if not wav_files:
        print('처리할 음성 파일이 없습니다.')
        return

    for wav_file in wav_files:
        print('처리 중:', wav_file)
        transcript = transcribe_audio(wav_file)
        save_transcript(wav_file, transcript)
        print('CSV 저장 완료:', wav_file)


def main():
    '''
    문제 16 폴더에서 음성 파일들을 불러와 STT 수행 및 CSV 저장.
    '''
    print('현재 작업 디렉토리:', os.getcwd())
    print('records 경로:', get_records_dir())
    print('CSV 저장 경로:', get_output_dir())
    process_all_audio()


if __name__ == '__main__':
    main()

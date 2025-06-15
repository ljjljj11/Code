import random
import time  
from datetime import datetime  


class DummySensor:
    '''
    화성 기지 환경 데이터를 시뮬레이션하는 더미 센서 클래스
    '''

    def __init__(self):
        '''환경 데이터 저장을 위한 사전 초기화'''
        self.env_values = {
            'mars_base_internal_temperature': None,        # 내부 온도
            'mars_base_external_temperature': None,        # 외부 온도
            'mars_base_internal_humidity': None,           # 내부 습도
            'mars_base_external_illuminance': None,        # 외부 광량
            'mars_base_internal_co2': None,                # 내부 CO2 농도
            'mars_base_internal_oxygen': None              # 내부 산소 농도
        }

    def set_env(self):
        '''환경 데이터를 랜덤 값으로 설정'''
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),      # 18~30도 사이의 내부 온도
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),       # 0~21도 사이의 외부 온도
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),         # 50~60% 사이의 내부 습도
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),    # 500~715 W/m² 사이의 외부 광량
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 4),           # 0.02~0.1% 사이의 CO2 농도
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2)              # 4~7% 사이의 산소 농도
        }

    def get_env(self):
        '''
        환경 데이터를 반환하고 로그 파일에 기록
        '''
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 시간 문자열로 변환

        # 로그 내용 문자열로 구성
        log_entry = (
            'Date and Time: ' + current_time + '\n' +
            'Internal Temperature: ' + str(self.env_values['mars_base_internal_temperature']) + '°C\n' +
            'External Temperature: ' + str(self.env_values['mars_base_external_temperature']) + '°C\n' +
            'Internal Humidity: ' + str(self.env_values['mars_base_internal_humidity']) + '%\n' +
            'External Illuminance: ' + str(self.env_values['mars_base_external_illuminance']) + ' W/m²\n' +
            'Internal CO2: ' + str(self.env_values['mars_base_internal_co2']) + '%\n' +
            'Internal Oxygen: ' + str(self.env_values['mars_base_internal_oxygen']) + '%\n\n'
        )

        # 로그를 파일에 저장
        try:
            with open('sensor_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print('파일 기록 중 오류 발생:', e)

        return self.env_values  # 환경 데이터를 반환


class MissionComputer:
    '''
    화성 기지 미션 컴퓨터 클래스
    '''

    def __init__(self):
        '''환경값 사전과 센서 인스턴스 초기화'''
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.ds = DummySensor()  # DummySensor 인스턴스 생성

    def get_sensor_data(self):
        '''
        센서 데이터를 받아 env_values에 저장하고
        JSON 형식처럼 출력하며 5초 간격으로 반복
        '''
        while True:
            self.ds.set_env()  # 센서 값 랜덤 생성
            self.env_values = self.ds.get_env()  # 센서 값을 받아 환경 데이터에 저장

            # 환경 데이터를 콘솔에 JSON 스타일로 출력
            print('{')
            for key in self.env_values:
                print('    \'' + key + '\': ' + str(self.env_values[key]) + ',')
            print('}\n')

            time.sleep(5)  # 5초 간격으로 반복


# 메인 실행부: 미션 컴퓨터 인스턴스 생성 및 센서 데이터 출력 시작
if __name__ == '__main__':
    run_computer = MissionComputer()
    run_computer.get_sensor_data()

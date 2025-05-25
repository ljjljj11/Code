import random 
import time  
from datetime import datetime  
import platform  
import json  
import os  
import sys  
import psutil  # 시스템 리소스 사용량(메모리, CPU 등)을 모니터링하는 외부 라이브러리

class DummySensor:
    '''
    화성 기지 내부/외부 환경 데이터를 가상으로 생성하는 센서 시뮬레이션 클래스.
    실제 센서가 없는 상황에서도 테스트를 위해 사용됨.
    '''

    def __init__(self):
        '''
        DummySensor 객체 생성 시 호출되는 생성자.
        측정할 환경 데이터를 담을 딕셔너리를 초기화한다.
        각 항목은 센서에서 측정될 데이터의 종류를 나타냄.
        '''
        self.env_values = {
            'mars_base_internal_temperature': None,  # 내부 온도 (℃)
            'mars_base_external_temperature': None,  # 외부 온도 (℃)
            'mars_base_internal_humidity': None,     # 내부 습도 (%)
            'mars_base_external_illuminance': None,  # 외부 조도 (W/m²)
            'mars_base_internal_co2': None,          # 내부 이산화탄소 농도 (%)
            'mars_base_internal_oxygen': None        # 내부 산소 농도 (%)
        }

    def set_env(self):
        '''
        센서 측정값을 랜덤한 값으로 생성해 self.env_values에 저장한다.
        시뮬레이션 환경에서의 측정값 변화를 표현함.
        '''
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),  
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),  
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),     
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2), 
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 4),        
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2)           
        }

    def get_env(self):
        '''
        현재 시점의 환경 데이터를 로그에 기록하고, 해당 데이터를 반환한다.
        실시간 모니터링 및 사후 분석용 기록 파일로 활용 가능.
        '''
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 시간 문자열로 포맷팅

        # 로그 파일에 기록할 문자열 구성
        log_entry = (
            'Date and Time: ' + current_time + '\n'
            'Internal Temperature: ' + str(self.env_values['mars_base_internal_temperature']) + '°C\n'
            'External Temperature: ' + str(self.env_values['mars_base_external_temperature']) + '°C\n'
            'Internal Humidity: ' + str(self.env_values['mars_base_internal_humidity']) + '%\n'
            'External Illuminance: ' + str(self.env_values['mars_base_external_illuminance']) + ' W/m²\n'
            'Internal CO2: ' + str(self.env_values['mars_base_internal_co2']) + '%\n'
            'Internal Oxygen: ' + str(self.env_values['mars_base_internal_oxygen']) + '%\n\n'
        )

        try:
            with open('sensor_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print('파일 기록 중 오류 발생:', e)

        # 측정값 딕셔너리 반환
        return self.env_values

class MissionComputer:
    '''
    화성 기지의 중앙 제어 시스템을 담당하는 미션 컴퓨터 클래스.
    센서 데이터 수집, 시스템 정보 및 부하 상태 점검 기능을 제공한다.
    '''

    def __init__(self):
        '''
        MissionComputer 객체 생성자.
        환경 데이터 초기화 및 DummySensor 객체 생성.
        '''
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.ds = DummySensor()  # 센서 시뮬레이터 객체 생성

    def get_sensor_data(self):
        '''
        센서를 통해 새로운 환경 데이터를 생성하고, 내부 상태(env_values)에 저장한다.
        호출 시점마다 새로운 무작위 측정값을 받아온다.
        '''
        self.ds.set_env()  # 센서 데이터 랜덤 생성
        self.env_values = self.ds.get_env()  # 로그 기록 및 값 수집

    def get_mission_computer_info(self):
        '''
        현재 미션 컴퓨터의 시스템 사양(OS, CPU, 메모리 등)을 JSON 형식으로 출력하고 반환한다.
        JSON 형식은 다른 시스템과의 연동에도 유리하다.
        '''
        try:
            total_memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # 바이트 → GB 변환
            info = {
                'OS': platform.system(),               # 운영체제 이름 (Windows, Linux 등)
                'OS Version': platform.version(),      # 상세 버전
                'CPU Type': platform.processor(),      # CPU 정보 (예: Intel i7)
                'CPU Cores': os.cpu_count(),           # CPU 코어 수
                'Total Memory (GB)': total_memory_gb   # 총 물리 메모리 크기
            }
        except Exception as e:
            info = {'error': '시스템 정보를 가져오는 중 오류 발생: {}'.format(e)}

        print(json.dumps(info, indent=4)) 
        return info

    def get_mission_computer_load(self):
        '''
        미션 컴퓨터의 실시간 시스템 부하 상태를 출력하고 반환.
        CPU 사용률과 메모리 사용률을 1초 단위로 측정한다.
        '''
        try:
            cpu_load = psutil.cpu_percent(interval=1)         # 1초 간격 CPU 사용률 측정
            memory_load = psutil.virtual_memory().percent     # 메모리 점유율 측정
            load = {
                'CPU Usage (%)': cpu_load,
                'Memory Usage (%)': memory_load
            }
        except Exception as e:
            load = {'error': '시스템 부하 정보를 가져오는 중 오류 발생: {}'.format(e)}

        print(json.dumps(load, indent=4))  # 출력
        return load

if __name__ == '__main__':
    # MissionComputer 인스턴스 생성
    run_computer = MissionComputer()

    # 시스템 정보 및 부하 상태 확인
    run_computer.get_mission_computer_info()
    run_computer.get_mission_computer_load()

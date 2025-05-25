import random
from datetime import datetime

class DummySensor:
    """
    화성 기지 환경 데이터를 시뮬레이션하는 더미 센서 클래스
    """
    def __init__(self):
        """환경 데이터 저장을 위한 사전 초기화"""
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }

    def set_env(self):
        """환경 데이터를 랜덤 값으로 설정"""
        self.env_values = {
            'mars_base_internal_temperature': round(random.uniform(18, 30), 2),
            'mars_base_external_temperature': round(random.uniform(0, 21), 2),
            'mars_base_internal_humidity': round(random.uniform(50, 60), 2),
            'mars_base_external_illuminance': round(random.uniform(500, 715), 2),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 4),
            'mars_base_internal_oxygen': round(random.uniform(4, 7), 2)
        }
    
    def get_env(self):
        """환경 데이터를 반환하고 로그 파일에 기록"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (f"Date and Time: {current_time}\n"
                     f"Internal Temperature: {self.env_values['mars_base_internal_temperature']}°C\n"
                     f"External Temperature: {self.env_values['mars_base_external_temperature']}°C\n"
                     f"Internal Humidity: {self.env_values['mars_base_internal_humidity']}%\n"
                     f"External Illuminance: {self.env_values['mars_base_external_illuminance']} W/m²\n"
                     f"Internal CO2: {self.env_values['mars_base_internal_co2']}%\n"
                     f"Internal Oxygen: {self.env_values['mars_base_internal_oxygen']}%\n\n")
        
        try:
            with open('sensor_log.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry + '\n')
        except Exception as e:
            print(f'파일 기록 중 오류 발생: {e}')
        
        return self.env_values

# 실행 코드
if __name__ == "__main__":
    ds = DummySensor()  # 인스턴스 생성
    ds.set_env()  # 환경 값 설정
    env_data = ds.get_env()  # 환경 값 가져오기
    print(env_data)  # 콘솔 출력

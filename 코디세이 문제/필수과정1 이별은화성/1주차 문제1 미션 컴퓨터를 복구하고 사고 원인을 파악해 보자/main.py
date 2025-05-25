def main():
    print('Hello Mars')  # Python이 정상적으로 실행되는지 확인
    
    log_file = 'mission_computer_main.log'  # 분석할 로그 파일 경로
    error_file = 'error_logs.txt'  # 문제가 있는 로그를 저장할 파일
    report_file = 'log_analysis.md'  # 로그 분석 결과를 저장할 파일
    
    try:
        # 로그 파일을 읽기 모드로 열고 UTF-8 인코딩을 사용하여 내용을 가져옴
        with open(log_file, 'r', encoding='utf-8') as file:
            logs = file.readlines()
        
        logs.reverse()  # 로그를 최신순으로 정렬하여 최근 이벤트가 먼저 출력되도록 함
        
        # 전체 로그 출력
        print('--- 로그 내용 (최신순) ---')
        for log in logs:
            print(log.strip())  # 각 줄의 앞뒤 공백 제거 후 출력
        
        # 특정 키워드('unstable', 'explosion')가 포함된 로그만 필터링하여 저장
        error_logs = [log for log in logs if 'unstable' in log or 'explosion' in log]
        
        # 문제가 있는 로그를 별도 파일에 저장
        if error_logs:
            with open(error_file, 'w', encoding='utf-8') as err:
                err.writelines(error_logs)  # 필터링된 문제 로그를 파일에 씀
            print(f'문제 로그가 {error_file} 파일에 저장되었습니다.')
            
            # 로그 분석 보고서 작성 (Markdown 형식)
            with open(report_file, 'w', encoding='utf-8') as report:
                report.write('# 로그 분석 보고서\n\n')  # 제목 작성
                report.write('## 개요\n이 보고서는 미션 컴퓨터 로그를 분석한 결과입니다.\n\n')  # 개요 작성
                report.write('## 문제 발생 로그\n')  # 문제 로그 섹션 추가
                for log in error_logs:
                    report.write(f'- {log.strip()}\n')  # Markdown 목록 형식으로 문제 로그 작성
            print(f'로그 분석 보고서가 {report_file} 파일에 저장되었습니다.')
        
    except FileNotFoundError:
        # 로그 파일이 존재하지 않을 경우 오류 메시지 출력
        print(f'오류: {log_file} 파일을 찾을 수 없습니다.')
    except Exception as e:
        # 기타 예기치 않은 오류가 발생할 경우 오류 메시지 출력
        print(f'예상치 못한 오류 발생: {e}')

# 프로그램 실행: Python 파일을 직접 실행할 경우 main() 함수 실행
if __name__ == '__main__':
    main()

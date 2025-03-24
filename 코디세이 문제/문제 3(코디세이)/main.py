csv_filename = 'Mars_Base_Inventory_List.csv'  # 원본 CSV 파일
output_csv_filename = 'Mars_Base_Inventory_danger.csv'  # 위험 화물 목록 CSV
binary_filename = 'Mars_Base_Inventory_List.bin'  # 정렬된 데이터를 저장할 이진 파일

def read_csv_file(filename):
    '''CSV 파일을 읽고 리스트로 변환하는 함수'''
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if not lines:
            print(f'파일이 비어 있습니다: {filename}')
            return None, None  # 파일이 비어 있으면 None 반환

        header = lines[0].strip().split(',')
        data = [line.strip().split(',') for line in lines[1:]]
        
        # 인화성 지수를 실수(float)로 변환
        for row in data:
            row[4] = float(row[4])
        
        return header, data
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {filename}')
        return None, None  # 파일이 없을 경우 None 반환
    except Exception as e:
        print(f'파일을 읽는 중 오류 발생: {e}')
        return None, None  # 기타 오류 발생 시 None 반환

def sort_by_flammability(data):
    '''인화성 지수를 기준으로 내림차순 정렬하는 함수'''
    return sorted(data, key=lambda x: x[4], reverse=True)

def filter_dangerous_items(data, threshold=0.7):
    '''인화성 지수가 특정 값 이상인 항목만 필터링하는 함수'''
    return [item for item in data if item[4] >= threshold]

def write_csv_file(filename, header, data):
    '''리스트 데이터를 CSV 파일로 저장하는 함수'''
    if not data:
        print(f'저장할 데이터가 없습니다. 파일을 생성하지 않습니다: {filename}')
        return  # 저장할 데이터가 없으면 파일 생성하지 않음

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(','.join(header) + '\n')
            for row in data:
                file.write(','.join(map(str, row)) + '\n')
        print(f'CSV 파일 저장 완료: {filename}')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')  # 파일 저장 중 오류 발생 시 출력

def write_binary_file(filename, data):
    '''정렬된 데이터를 이진 파일로 저장하는 함수'''
    try:
        with open(filename, 'wb') as file:
            for row in data:
                line = ','.join(map(str, row)) + '\n'
                file.write(line.encode('utf-8'))
        print(f'이진 파일 저장 완료: {filename}')
    except Exception as e:
        print(f'이진 파일 저장 중 오류 발생: {e}')  # 오류 발생 시 출력

def read_binary_file(filename):
    '''저장된 이진 파일을 읽고 출력하는 함수'''
    try:
        with open(filename, 'rb') as file:
            content = file.read().decode('utf-8')
            print('\n[이진 파일 내용 출력]')
            print(content)
    except Exception as e:
        print(f'이진 파일 읽기 중 오류 발생: {e}')  # 오류 발생 시 출력

def main():
    '''프로그램 실행 흐름''' 
    header, data = read_csv_file(csv_filename)
    if data is None:
        return  # 파일이 없거나 오류 발생 시 프로그램 종료
    
    print('\n[CSV 파일 내용 출력]')
    for row in data[:5]:
        print(row)
    
    sorted_data = sort_by_flammability(data)
    print('\n[정렬된 화물 목록 (인화성 높은 순)]')
    for row in sorted_data[:5]:
        print(row)
    
    dangerous_items = filter_dangerous_items(sorted_data)
    print('\n[인화성 0.7 이상인 위험 화물 목록]')
    for row in dangerous_items[:5]:
        print(row)
    
    write_csv_file(output_csv_filename, header, dangerous_items)
    write_binary_file(binary_filename, sorted_data)
    read_binary_file(binary_filename)

if __name__ == '__main__':
    main()

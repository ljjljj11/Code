def read_csv_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f'오류: 파일 "{file_path}"을 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'오류 발생: {e}')
        return None

def write_csv_file(file_path, header, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(','.join(header) + '\n')
            for row in data:
                file.write(','.join(row) + '\n')
    except Exception as e:
        print(f'오류 발생: {e}')

def main():
    file_path = 'Mars_Base_Inventory_List.csv'
    lines = read_csv_file(file_path)

    if lines is None:
        return

    header = lines[0].strip().split(',')
    data = [line.strip().split(',') for line in lines[1:]]

    # 전체 파일 내용 출력
    print("파일 내용:")
    for line in lines:
        print(line.strip())  # lines의 내용을 출력

    # 인화성 지수를 기준으로 정렬
    data.sort(key=lambda x: float(x[4]), reverse=True)

    # 인화성 지수가 0.7 이상인 항목 필터링
    high_flammability = [row for row in data if float(row[4]) >= 0.7]

    # 인화성 지수가 0.7 이상인 항목 출력
    print('인화성 지수가 0.7 이상인 목록:')
    for item in high_flammability:
        print(item)

    # 인화성 지수가 0.7 이상인 항목을 CSV 파일로 저장
    danger_file_path = 'Mars_Base_Inventory_danger.csv'
    write_csv_file(danger_file_path, header, high_flammability)

if __name__ == '__main__':
    main()

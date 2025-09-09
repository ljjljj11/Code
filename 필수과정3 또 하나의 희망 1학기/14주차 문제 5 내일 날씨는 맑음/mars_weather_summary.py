import mysql.connector

def connect_to_mysql():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',        # ⚠️ 사용자 환경에 맞게 수정
        password='root',     # ⚠️ 사용자 환경에 맞게 수정
        database='mars_db'   # ⚠️ 사용자 환경에 맞게 수정
    )
    return connection

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(1, len(lines)):  # 헤더 제외
            line = lines[i].strip()
            if line:
                parts = line.split(',')
                if len(parts) == 4:
                    mars_date = parts[1].strip()
                    temp = float(parts[2].strip())
                    storm = int(parts[3].strip())
                    data.append((mars_date, temp, storm))
    return data

def insert_data(connection, data):
    cursor = connection.cursor()
    for entry in data:
        mars_date, temp, storm = entry
        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )
        cursor.execute(query, (mars_date, temp, storm))
    connection.commit()
    cursor.close()

def main():
    file_path = 'mars_weathers_data.CSV'
    connection = connect_to_mysql()
    data = read_csv_file(file_path)
    insert_data(connection, data)
    connection.close()
    print('[✅] CSV 데이터를 MySQL에 저장 완료')

if __name__ == '__main__':
    main()

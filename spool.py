import csv
import pymysql
import schedule
import time
import os

CSV_FOLDER = '/home/student/final/spool'

SQL_QUERY = 'SELECT * FROM students'

def fetch_data_to_csv():
    conn = pymysql.connect(host='localhost', port=3306, user='student', password='student', database='final')
    print('Connected to db')
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    total_rows = len(rows)
    rows_limit = round(total_rows * 0.05)
    num_files = (total_rows + rows_limit - 1) // rows_limit

    for i in range(num_files):
        time.sleep(10)
        file_name = f"data{i+1}.csv"
        file_path = os.path.join(CSV_FOLDER, file_name)
        start_index = i * rows_limit
        end_index = start_index + rows_limit if start_index + rows_limit < total_rows else total_rows
        data = rows[start_index:end_index]
        print(i)

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            print(f'Data fetched and saved to file {file_name}')

def job():
    print('Fetching data...')
    fetch_data_to_csv()

schedule.every(5).seconds.do(job)
while True:
    schedule.run_pending()

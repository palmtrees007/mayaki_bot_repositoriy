import sqlite3

def convert_to_bin(file):
    with open(file, 'rb') as file_n:
        blob_data = file_n.read()
    return blob_data

def insert_mayak(mayak_id, name, image, url, history):
    try:
        conn = sqlite3.connect('D:\pythonproj\mayaki_bot\database.db')
        cursor = conn.cursor()

        #command = '''
#INSERT INTO mayaki (id, name, path_image, url, path_his)
#VALUES (?, ?, ?, ?, ?);
#'''
        command = '''
UPDATE mayaki
SET path_his = ?
WHERE id = ?;
'''
        m_image = image
        data_tuple = (#mayak_id,
                      #name,
                      #m_image,
                      #url,
                      history,
                      mayak_id)
        cursor.execute(command, data_tuple)
        conn.commit()
        print('Загружено')
        cursor.close
    except sqlite3.Error as error:
        print('Ошибка: ', error)
    finally:
        if conn:
            conn.close()
            print('Соединение закрыто')

with open(file="C:/Users/HP OMEN/Documents/project_2024_2025/history_hers.txt", mode='r') as file:
    hist = file.read()



insert_mayak(3, 'Маяк на мысе Сарыч', 'Sarich.jpeg', None, 'his_sarich.txt')

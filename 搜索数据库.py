import mysql.connector
from docx import Document

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'pan',
    'password': 'panjun1994',
    'database': 'search_db'
}

def read_word_file(file_path):
    doc = Document(file_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return '\n'.join(content)

# 插入数据
def insert_data(file_path):
    cursor = None
    conn = None
    try:
        content = read_word_file(file_path)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = """
        INSERT INTO articles (title, content, author, created_at, updated_at, effective_date, type) 
        VALUES (%s, %s, %s, NOW(), NOW(), %s, %s)
        """
        title = '指导案例225号：江某某正当防卫案'
        author = '湖南省湘西土家族苗族自治州中级人民法院'
        effective_date = '2022-11-09'
        type = '案例'

        cursor.execute(sql, (title, content, author, effective_date, type))
        conn.commit()
        print("插入成功")

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

# 调用插入函数
file_path = input("请输入 Word 文档的完整路径：")
insert_data(file_path)
def search_data(keyword):
    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        search_term = f"%{keyword}%"
        sql = """
        SELECT id, title, content, author, effective_date, created_at 
        FROM articles 
        WHERE (title LIKE %s OR content LIKE %s)
        """
        cursor.execute(sql, (search_term, search_term))
        results = cursor.fetchall()

        for result in results:
            print(result)

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()

# 调用搜索函数
keyword = input("请输入搜索关键词：")
search_data(keyword)
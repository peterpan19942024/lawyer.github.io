import mysql.connector
from PyPDF2 import PdfReader
import os

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'pan',  # 替换为您的MySQL用户名
    'password': 'panjun1994',  # 替换为您的MySQL密码
    'database': 'search_db'  # 替换为您的数据库名
}

# 读取 PDF 文档内容
def read_pdf_file(file_path):
    content = []
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content.append(page.extract_text())
    return '\n'.join(content)  # 将所有页面内容合并为一个字符串

# 插入数据
cursor = None  # 初始化 cursor
conn = None  # 初始化 conn

try:
    # 提示用户输入 PDF 文档路径
    file_path = input("请输入 PDF 文档的完整路径（例如：C:/path/to/document.pdf）：")

    # 读取 PDF 文档内容
    content = read_pdf_file(file_path)

    # 获取文件名
    file_name = os.path.basename(file_path)  # 获取文件名（不包含路径）

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    sql = """
    INSERT INTO articles (title, content, author, created_at, updated_at, effective_date, type, file_name) 
    VALUES (%s, %s, %s, NOW(), NOW(), %s, %s, %s)
    """
    title = '关于人身损害赔偿项目计算标准的指引'  # 替换为法规标题
    author = '浙江省高级人民法院'  # 替换为作者名
    effective_date = '2022-08-24'  # 使用合适的日期格式
    type = '法规'  # 替换为类型

    # 确保传递的参数数量与 SQL 语句中的占位符数量匹配
    cursor.execute(sql, (title, content, author, effective_date, type, file_name))
    conn.commit()
    print("插入成功")

except FileNotFoundError:
    print("错误：指定的文件未找到，请检查路径是否正确。")
except mysql.connector.Error as err:
    print(f"数据库错误: {err}")
except Exception as e:
    print(f"发生错误: {e}")

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None and conn.is_connected():
        conn.close()
import mysql.connector

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'pan',  # 替换为您的MySQL用户名
    'password': 'panjun1994',  # 替换为您的MySQL密码
    'database': 'search_db'  # 替换为您的数据库名
}


def find_articles(keyword):
    """根据关键词查找文章"""
    try:
        # 连接到数据库
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # SQL SELECT 语句
        sql = "SELECT id, title FROM articles WHERE title LIKE %s OR content LIKE %s"
        search_term = f"%{keyword}%"
        cursor.execute(sql, (search_term, search_term))

        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"查询数据时出错: {err}")
        return []

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_articles_by_keyword(keyword):
    """根据关键词删除文章"""
    articles = find_articles(keyword)
    if not articles:
        print("没有找到符合条件的文章。")
        return

    print("找到以下文章：")
    for article in articles:
        print(f"ID: {article['id']}, 标题: {article['title']}")

    # 确认删除
    confirm = input("您确定要删除这些文章吗？(y/n): ")
    if confirm.lower() == 'y':
        try:
            # 连接到数据库
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # SQL DELETE 语句
            sql = "DELETE FROM articles WHERE id = %s"
            for article in articles:
                cursor.execute(sql, (article['id'],))

            # 提交更改
            conn.commit()
            print("成功删除文章。")

        except mysql.connector.Error as err:
            print(f"删除数据时出错: {err}")

        finally:
            # 关闭游标和连接
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    else:
        print("取消删除。")


# 示例：根据关键词删除文章
delete_articles_by_keyword("正当防卫")
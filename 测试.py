@app.route('/search/')
def search():
    """搜索路由"""
    keyword = request.args.get('keyword', '')
    search_type = request.args.get('type', '')  # 获取搜索类型

    if not keyword:
        return render_template('index.html')

    try:
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 使用通配符进行模糊搜索
        search_term = f"%{keyword}%"
        sql = """
        SELECT id, title, content, author, effective_date, created_at, type, file_name, file_type 
        FROM articles 
        WHERE (title LIKE %s OR content LIKE %s)
        """

        # 根据搜索类型调整查询
        if search_type:
            sql += " AND type = %s"
            # 使用元组传递参数
            cursor.execute(sql, (search_term, search_term, search_type))
        else:
            # 使用元组传递参数
            cursor.execute(sql, (search_term, search_term))

        results = cursor.fetchall()

        # 处理结果
        for result in results:
            result['created_at'] = result['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            result['effective_date'] = result['effective_date'].strftime('%Y-%m-%d') if result['effective_date'] else None
            result['content'] = result['content'].replace('\r\n', '\n')
            if len(result['content']) > 500:
                result['content'] = result['content'][:500] + '...'

        return render_template('search_results.html',
                               keyword=keyword,
                               results=results)

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")  # 打印错误信息
        return render_template('search_results.html',
                               keyword=keyword,
                               error=f"数据库错误: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
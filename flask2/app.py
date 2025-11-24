# Работа с БД
import sqlite3
from flask import Flask, jsonify
from random import choice  # Импортируем функцию choice из модуля random
from flask import request

from pathlib import Path
BASE_DIR = Path(__file__).parent
path_to_db = "store.db" # <- тут путь к БД


app = Flask (__name__)
app.config['JSON_AS_ASCII'] = False

about_me ={
 "name": "Алексей",
 "surname": "Фадин",
 "email": "alexeyfadin75@gmail.com"
}


def get_db_connection():
    conn = sqlite3.connect(path_to_db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/quotes", methods=['GET'])
def get_quotes():
    select_quotes="SELECT * FROM quotes"
    conn = sqlite3.connect("store.db")
    cursor=conn.cursor()
    cursor.execute(select_quotes)
    quotes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Преобразуем строки в словари
    keys=("id", "autor", "text")
    quotes = []
    for quote_db in quotes_db:
        quote=dict(zip(keys,quotes_db))
        quotes.append(quote)
    return jsonify(quotes)

    

@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    select_quotes="SELECT * FROM quotes WHERE id = ?" 
    conn = sqlite3.connect("store.db")
    cursor=conn.cursor()
    cursor.execute(select_quotes,(quote_id,))
    quotes_db = cursor.fetchall()
    cursor.close()
    conn.close()
     # Преобразуем строки в словари
    keys=("id", "autor", "text")   
    quotes = []
    for quote_db in quotes_db:
        quote=dict(zip(keys,quotes_db))
        quotes.append(quote)
    return jsonify(quotes)
    

@app.route("/quotes/count")
def get_quotes_count():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM quotes').fetchone()[0]
    conn.close()
    return {"count": count}

 

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/about")
def about():
    return about_me

@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    
    # Проверяем обязательные поля
    if not new_quote.get('author') or not new_quote.get('text'):
        return {"error": "Поля 'author' и 'text' обязательны"}, 400
    
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO quotes (author, text) VALUES (?, ?)',
        (new_quote['author'], new_quote['text'])
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"id": new_id, "message": "Цитата создана"}, 201

@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete_quote(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем существование цитаты
    quote = cursor.execute(
        'SELECT * FROM quotes WHERE id = ?', 
        (id,)
    ).fetchone()
    
    if quote is None:
        conn.close()
        return {"error": f"Цитата с id={id} не найдена"}, 404
    
    cursor.execute('DELETE FROM quotes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Цитата с id {id} удалена"}), 200

@app.route("/quotes/<int:id>", methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Проверяем существование цитаты
    quote = cursor.execute(
        'SELECT * FROM quotes WHERE id = ?', 
        (id,)
    ).fetchone()
    
    if quote is None:
        conn.close()
        return {"error": f"Цитата с id={id} не найдена"}, 404
    
    # Формируем запрос на обновление
    update_fields = []
    update_values = []
    
    if "author" in new_data:
        update_fields.append("author = ?")
        update_values.append(new_data["author"])
    
    if "text" in new_data:
        update_fields.append("text = ?")
        update_values.append(new_data["text"])
    
    
    if not update_fields:
        conn.close()
        return {"error": "Нет полей для обновления"}, 400
    
    update_values.append(id)
    update_query = f"UPDATE quotes SET {', '.join(update_fields)} WHERE id = ?"
    
    cursor.execute(update_query, update_values)
    conn.commit()
    
    # Получаем обновленную цитату
    updated_quote = cursor.execute(
        'SELECT * FROM quotes WHERE id = ?', 
        (id,)
    ).fetchone()
    
    conn.close()
    
    return {
        "id": updated_quote["id"],
        "author": updated_quote["author"],
        "text": updated_quote["text"]
    }, 200

  

if __name__ == "__main__":
     app.run(debug=True)
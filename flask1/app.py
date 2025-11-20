from flask import Flask, jsonify
from random import choice  # Импортируем функцию choice из модуля random
from flask import request

app = Flask (__name__)
app.config['JSON_AS_ASCII'] = False

about_me ={
 "name": "Алексей",
 "surname": "Фадин",
 "email": "alexeyfadin75@gmail.com"
}

quotes =[
  {"id":1, 
   "author":"Махатма Ганди",
   "text":"Грамм собственного опыта стоит дороже, чем тонны чужих наставлений",
   "rating":1
  },
  {"id":2, 
   "author":"Альберт Эйнштейн",
   "text":"Жизнь — как вождение велосипеда. Чтобы сохранить равновесие, ты должен двигаться",
   "rating":5
  }, 
  {"id":3, 
   "author":"Генри Форд",
   "text":"Неудача — это просто возможность начать снова, но уже более мудро",
   "rating":4
  } 
]

@app.route("/quotes",  methods=['GET'])
def get_quotes(): 
    return quotes

@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    # Ищем цитату по ID
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote
    # Если цитата не найдена, возвращаем сообщение об ошибке
    return {"error": f"Цитата с id={quote_id} не найдена"}, 404

@app.route("/quotes/count")
def get_quotes_count():
    count = len(quotes)
    return {"count": count}


@app.route("/quotes/random")
def get_random_quote():
    random_quote = choice(quotes)  # Выбираем случайную цитату из списка
    return random_quote

@app.route("/")
def hello_world():
  return "Hello, Word!"

@app.route("/about")
def about():
  return about_me

@app.route("/quotes", methods=['POST'])
def create_quote():
  new_quote = request.json
  last_quote = quotes[-1] # последняя цитата в списке
  new_id = last_quote["id"]+1
  new_quote["id"]=new_id
  quotes.append(new_quote)
  return {}, 201

@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete_quote(id):
  # удаляем цитату по ее id
  for quote in quotes:
      if quote["id"] == id:
         quotes.remove(quote) 
         return jsonify({"message":f"Quote with id {id} is deleted."}), 200
  return {"Error":f"Quote with id {id} not found"}, 404

@app.route("/quotes/<int:id>", methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    
    # Проверяем рейтинг, если он есть в запросе
    if "rating" in new_data:
        rating = new_data["rating"]
        if not isinstance(rating, int) or rating < 1 or rating > 10:
            return {"error": "Рейтинг должен быть целым числом от 1 до 10"}, 400
    
    # Ищем цитату по ID
    for quote in quotes:
        if quote["id"] == id:
            # Обновляем только те поля, которые пришли в запросе
            if "author" in new_data:
                quote["author"] = new_data["author"]
            if "text" in new_data:
                quote["text"] = new_data["text"]
            if "rating" in new_data:
                quote["rating"] = new_data["rating"]
            
            return quote, 200
    
    # Если цитата не найдена
    return {"error": f"Цитата с id={id} не найдена"}, 404

@app.route("/quotes/filter")
def get_quotes_filter():
    # Получаем все параметры запроса
    filters = request.args.to_dict()
    
    if not filters:
        return {"error": "Не указаны параметры фильтрации. Доступные параметры: author, rating"}, 400
    
    filtered_quotes = quotes.copy()
    
    # Применяем фильтры последовательно
    for field, value in filters.items():
        if field == "author":
            # Flask автоматически декодирует URL-encoded строки
            filtered_quotes = [quote for quote in filtered_quotes if quote["author"] == value]
        elif field == "rating":
            try:
                rating_value = int(value)
                filtered_quotes = [quote for quote in filtered_quotes if quote["rating"] == rating_value]
            except ValueError:
                return {"error": "Рейтинг должен быть числом"}, 400
        else:
            return {"error": f"Неизвестный параметр фильтра: {field}. Доступные параметры: author, rating"}, 400
    
    return {
        "count": len(filtered_quotes),
        "quotes": filtered_quotes
    }

if __name__=="__main__":
  app.run(debug=True)

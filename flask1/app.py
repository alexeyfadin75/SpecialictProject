from flask import Flask
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
   "text":"Грамм собственного опыта стоит дороже, чем тонны чужих наставлений"
  },
  {"id":2, 
   "author":"Альберт Эйнштейн",
   "text":"Жизнь — как вождение велосипеда. Чтобы сохранить равновесие, ты должен двигаться"
  }, 
  {"id":3, 
   "author":"Генри Форд",
   "text":"Неудача — это просто возможность начать снова, но уже более мудро"
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
  # delete quote with id
  for quote in quotes:
      if quote["id"] == id:
         quotes.remove(quote) 
         return f"Quote with id {id} is deleted.", 200

if __name__=="__main__":
  app.run(debug=True)

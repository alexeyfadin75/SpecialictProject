from flask import Flask
#app.json.ensure_ascii = False

app = Flask (__name__)

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


@app.route("/quotes")
def quotes
  return quotes

@app.route("/")
def hello_world():
  return "Hello, Word!"

@app.route("/about")
def about():
  return about_me



if __name__=="__main__":
  app.run(debug=True)

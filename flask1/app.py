from flask import Flask
#app.json.ensure_ascii = False

app = Flask (__name__)

about_me ={
 "name": "Алексей",
 "surname": "Фадин",
 "email": "alexeyfadin75@gmail.com"
}

quotes =[]


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

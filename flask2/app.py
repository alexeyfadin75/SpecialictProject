# Работа с БД

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


@app.route("/quotes",  methods=['GET'])
def get_quotes(): 


@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):

@app.route("/quotes/count")
def get_quotes_count():


@app.route("/quotes/random")
def get_random_quote():

@app.route("/")
def hello_world():
  return "Hello, Word!"

@app.route("/about")
def about():
  return about_me

@app.route("/quotes", methods=['POST'])
def create_quote():

@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete_quote(id):


if __name__=="__main__":
  app.run(debug=True)

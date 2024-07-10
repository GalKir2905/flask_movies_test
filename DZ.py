import re
from flask import Flask
from time import time
import requests
from python_s.log import logger
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return """
       <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>Новостной сайт</title>
     </head>
     <body>
       <h1>Скоро тут будут новости!</h1>
       <p>Следите за обновлениями.</p>
     </body>
   </html>
    """

@app.route('/news')
def news():
    return "Новости"

@app.route('/news_detail/<int:id>')
def news_detail(id):
    return f"Новость {id}"

@app.route('/category/<string:name>')
def category(name):
    return f"Категория {name}"


@app.route('/total/<int:a>/<int:b>')
def total(a, b):
    return f"""
       <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>Задание_1</title>
     </head>
     <body>
       <h1>Складываем {a} + {b}</h1>
       <p>Ответ:{a + b}.</p>
     </body>
   </html>
    """

# @app.route('/primes/<int:n>/')
def primes(n):
    prime = []
    for num in range(1, n + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                prime.append(num)
    return f"""
       <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>Задание_2</title>
     </head>
     <body>
       <h1>Первые простые числа {n} = {','.join(str(p) for p in prime)}</h1>
     </body>
   </html>
    """


app.add_url_rule("/primes/<int:n>", f"/primes/<int:n>", primes) #Походу должно быть одинаково

@app.route('/money')
def money():
    url_money = "https://www.cbr-xml-daily.ru/daily_json.js"
    respon = requests.get(url_money).json()
    cbr = []
    for each_money in respon['Valute'].values():
        cbr.append(
            f"Номинал:{each_money.get('Nominal')}, Валюта:{each_money.get('Name')}, Стоимость: {each_money.get('Value')}")

    return f"""
       <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>Задание_3</title>
     </head>
     <body>
       <p>{'<br>'.join(str(p) for p in cbr)}</p>
     </body>
   </html>
    """

@app.route('/date')
def date():
    return f"""
       <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>Задание_4</title>
     </head>
     <body>
       <h1>{(datetime.today()).strftime("%d.%m.%Y")}</h1>
     </body>
   </html>
    """

@app.route('/time')
def time():
    return f"""
       <!DOCTYPE html>
   <html>
     <head>
       <meta charset="utf-8">
       <title>Задание_4</title>
     </head>
     <body>
       <h1>{(datetime.today()).strftime("%H.%M")}</h1>
     </body>
   </html>
    """


@app.route('/<int:a>/<string:operation>/<int:b>')
def operation(a, operation, b):
    if operation in ['+', '-', '*', ':']:
        if operation == ':':
            ops = eval(str(a/b))
        else:
            ops = eval(f"{a}{operation}{b}")
        return f"""
                   <!DOCTYPE html>
               <html>
                 <head>
                   <meta charset="utf-8">
                   <title>Задание_5</title>
                 </head>
                 <body>
                   <h1>Операция {a}{operation}{b} = {ops}</h1>
                 </body>
               </html>
                """
    else:
        return f"""
           <!DOCTYPE html>
       <html>
         <head>
           <meta charset="utf-8">
           <title>Задание_5</title>
         </head>
         <body>
           <h1>ОШИБКА. Промежуточное "operation" должно быть ['+', '-', '*', ':']</h1>
         </body>
       </html>
        """


if __name__ == "__main__":
    app.run(debug=True)

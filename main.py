from flask import Flask
from datetime import datetime

# print(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    today = datetime.now()
    print(today)
    return f"<h1>Hello Flask!<br>{today}</h1>"


books = {1: "Python book", 2: "Java book", 3: "Flask book"}


@app.route("/books")
def show_books():
    return books


@app.route("/book/<int:id>")
def show_book(id):
    # 輸出有書 <h1>第一本書:xxx</h1>、沒書無此編號

    if id not in books:
        return f"<h2 style='color:red'>查無此書:{id}</h2>"

    return f"<h1>第{id}本書:{books[id]}</h1>"


@app.route("/sum/x=<x>&y=<y>")
def my_sum(x, y):
    try:
        total = eval(x) + eval(y)
        return f"<h1>{x}+{y}={total}</h1>"
    except Exception as e:
        print(e)
    return "<h2>參數不正確!</h2>"


@app.route("/bmi/name=<nm>&height=<h>&weight=<w>")
def get_bmi(nm, h, w):
    try:
        bmi = eval(w) / ((eval(h) / 100) ** 2)
        return f"<h1><span style='color:blue'>{nm}</span> BMI={round(bmi, 2)}</h1>"
    except Exception as e:
        print(e)
    return "<h2>參數不正確!</h2>"


app.run(debug=True)

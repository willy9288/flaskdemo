from flask import Flask, render_template, request
from datetime import datetime
from scrape import scrape_stocks, scrape_pm25, get_pm25_json
import json

# print(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    today = datetime.now()
    print(today)
    name = "ddd"
    # return f"<h1>Hello Flask!<br>{today}</h1>"
    return render_template("index.html", date=today, nm=name)


# books = {1: "Python book", 2: "Java book", 3: "Flask book"}
books = {
    1: {
        "name": "Python book",
        "price": 299,
        "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
    },
    2: {
        "name": "Java book",
        "price": 399,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
    },
    3: {
        "name": "C# book",
        "price": 499,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
    },
}


@app.route("/books")
def show_books():
    # print(books)
    for key in books:
        print(books[key])
    # return books
    return render_template("books.html", bks=books)


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


@app.route("/stocks")
def get_stocks():
    datas = scrape_stocks()
    # for data in datas:
    #     print(data[0], data[1])
    return render_template("stocks.html", dts=datas)


@app.route("/pm25", methods=["GET", "POST"])
def get_pm25():
    # print(scrape_pm25())

    # 前端要求 GET
    print(request.args)
    # 後端要求 POST
    print(request.form)
    today = datetime.now()
    # print(today)

    sort = False
    ascend = True
    if request.method == "POST":
        # 判斷是否按下排序按鈕
        if "sort" in request.form:
            # print("sort!!!!")

            # 取得 select的 option
            sort = True
            ascend = True if request.form.get("sort") == "true" else False
            # print(ascend)

    columns, values = scrape_pm25(sort, ascend)
    data = {
        "columns": columns,
        "values": values,
        "today": today.strftime("%Y/%m/%d %H:%M:%S"),
    }
    return render_template("pm25.html", dt=data)


@app.route("/pm25-data")
def pm25_data():

    try:
        json_data = get_pm25_json()
        return json.dumps(json_data, ensure_ascii=False)

    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "exception": str(e)})


@app.route("/pm25-chart")
def pm25_chart():
    return render_template("pm25-chart.html")


app.run(debug=True)

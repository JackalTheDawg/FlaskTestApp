from flask import Flask, render_template, request, redirect
import redis

app = Flask(__name__)

redisDB = redis.Redis()

@app.route("/")
def index():
    keys_bytes = redisDB.keys()
    keys = []

    for key in keys_bytes:
        keys.append(key.decode('utf-8'))

    if request.method == "GET" and request.args.get('name') is not None:
        data = request.args.get('name')
        if data in keys:
            return render_template('index.html', data=data)
        else:
            data = 'Ничего не найдено'
            return render_template('index.html', data=data)

    return render_template('index.html', keys=keys)



@app.route("/add-article", methods=["GET", "POST", "PUT"])
def add_article():

    if request.method == "POST" or request.method == "PUT":
        redisDB.mset({request.form.get('name'): request.form.get('description')})
        return redirect('/')

    return render_template('new_article.html')


@app.route("/article/<title>", methods=["GET", "PUT", "POST"])
def article(title):

    name = title
    description = redisDB.get(title)

    if request.method == "POST" or request.method == "PUT":
        redisDB.mset({title: request.form.get('change')})

    return render_template('article.html',
                           title=name,
                           description=description.decode('utf-8'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
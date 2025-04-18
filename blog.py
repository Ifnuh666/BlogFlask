from symtable import Class

from flask import Flask, render_template, url_for, request, redirect
from  flask_sqlalchemy import  SQLAlchemy
from  datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Создаем базу данных
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/posts")
def posts():
    posts = Article.query.order_by(Article.date).all()
    return render_template("posts.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        post = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect("/")
        except:
            return "При добавлении статьи произошла ошибка!"

    else:
        return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)
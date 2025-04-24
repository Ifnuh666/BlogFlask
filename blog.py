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
    posts = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", posts=posts)


#Декоратор для вывода определенной статьи (т.е. полностью ее текст)
@app.route("/posts/<int:id>")
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


#get_or_404 - в случае если пост не найден, будет вызываться ошибка 404

@app.route("/posts/<int:id>/delete")
def posts_delete(id):
    article = Article.query.get_or_404(id)
#Прописываем проверку на удаление поста
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "При удалении статьи произошла ошибка!"


@app.route("/posts/<int:id>/update", methods=['POST', 'GET'])
def posts_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/posts")
        except:
            return "При редактировании статьи произошла ошибка!"

    else:
        article = Article.query.get(id)
        return render_template("post_update.html", article=article)


@app.route("/about")
def about():
    return render_template("about.html")

#Добавление записи в бд
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
            return redirect("/posts")
        except:
            return "При добавлении статьи произошла ошибка!"

    else:
        return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)
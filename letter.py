from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)  # создаем объект и передаем название файла app.py Это основной файл.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lc.db'  # обращаемся к словарю config по ключу SQLAlchemy... и устанавливаем значение БД, с которой будем работать
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'adsgsdfhdsglhjdsaie46gjklsdjg'
db = SQLAlchemy(app)


class Letter(db.Model):  # наследуем от db.Model
    id = db.Column(db.Integer, primary_key=True)
    lc_number = db.Column(db.String(15), nullable=False)
    applicant_name = db.Column(db.String(100), nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)
    goods = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.String(10), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Letter %r>' % self.id  # Когда будем выбирать какую-то запись, то будет выдаваться сам объект и id

class Applicant(db.Model):  # наследуем от db.Model
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    region = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(20), nullable=False)
    room = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.String(10), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)

    #applicant_id = db.Column(db.)
    def __repr__(self):
        return '<Applicant %r>' % self.id  # Когда будем выбирать какую-то запись, то будет выдаваться сам объект и id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    psw = db.Column(db.String(100), nullable = True)
    date = db.Column(db.DateTime, default = datetime.utcnow)

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    old = db.Column(db.String(100), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/letters')  # ф-ция отслеживает url-адрес страницы posts.
def letter():
    letters_of_credit = Letter.query.order_by(Letter.id).all()
    return render_template('letters.html', letters_of_credit=letters_of_credit)  # вторым параметром передаем список LC в шаблон

@app.route('/letter_detail/<int:id>')
def letter_detail(id):
    letter = Letter.query.get(id)
    if letter is not None:
        return render_template('letter_detail.html', letter = letter)
    else:
        return render_template('letters.html')


@app.route('/letters/<path:applicant_name>')     #route for applicant's details (dinamic URL).
def applicant_detail(applicant_name):
    letters_of_credit = Letter.query.filter(Letter.applicant_name == applicant_name)     #создаем объект
    if letters_of_credit is not None:     #if applicant is in BD, render template applicant
        return render_template('applicant_detail.html', letters_of_credit = letters_of_credit, applicant_name = applicant_name)  #вторым параметром передаем список arcticles в шаблон
    else:                       #если нету, то переход на страницу posts
        redirect('/letters')
#
#
# @app.route('/posts/<int:id>/del')     #функция для отображения деталей поста (динамическое изменение адреса).
# def post_delete(id):
#     article = Article.query.get_or_404(id)    #создаем объект - находим запись в БД
#
#     try:
#         db.session.delete(article)     #удаляем из БД
#         db.session.commit()             #делаем commit в БД
#         return redirect('/posts')       #после удаления происходит перенаправление на страницу с постами
#     except:
#         return "При удалении статьи произошла ошибка"
#
# @app.route('/posts/<int:id>/update', methods = ['POST','GET'])     #ф-ция отслеживает url-адрес страницы для ввода информации.
# def post_update(id):
#     article = Article.query.get(id)         #находим объект, который изменяем
#     if request.method == "POST":            #если метод ПОСТ, то переменным присваиваем значения из полей формы, которые вводим на сайте.
#         article.title = request.form['title']
#         article.intro = request.form['intro']
#         article.text = request.form['text']
#
#         try:
#             db.session.commit()        #в данном случае только commit без add, так как мы только изменяем уже добавленную запись
#             return redirect('/posts')  #в случае успешного сохранения пользователя перенаправляем на главную страницу
#         except:
#             return "При обновлении статьи произошла ошибка"
#     else:
#         return render_template('post_update.html', article = article)  #второй аргумент указывается для его передачи в шаблон

@app.route('/add_lc', methods=['POST', 'GET'])  # ф-ция отслеживает url-адрес страницы для ввода информации.
def add_lc():
    if request.method == "POST":  # если метод ПОСТ, то переменным присваиваем значения из полей формы, которые вводим на сайте.

        lc_number = request.form["LC Number"]   #создаем переменные, которые получают значения из формы HTML по именни в скобках
        applicant_name = request.form["Applicant's Name"]
        beneficiary_name = request.form["Beneficiary's Name"]
        goods = request.form["Goods"]
        currency = request.form["Currency"]
        amount = request.form["Amount"]
        date_of_issue = str(lc_number[-6:-4]+'/'+lc_number[-4:-2]+'/'+'20'+lc_number[-2:]) #request.form["Date of Issue"]
        expiry_date = request.form["Expiry Date"]

        letter_of_credit = Letter(lc_number = lc_number, applicant_name = applicant_name, beneficiary_name = beneficiary_name,
                                 goods = goods, currency = currency, amount = amount, date_of_issue = date_of_issue, expiry_date = expiry_date)  #создаем объект, в поля которого записываем информацию из соотвествующих полей
        #затем объект нужно сохранить в Базе данных
        try:
            db.session.add(letter_of_credit)    #Добавляем в БД
            db.session.commit()         #Сохраняем в БД
            flash('LC has been successfully created')
            return redirect('/letters')  #в случае успешного сохранения пользователя перенаправляем на главную страницу
        except:
            return render_template('creating_error.html')
    else:
        return render_template('add_lc.html')


if __name__ == "__main__":  # если программа запускается через основной файл, т.е. app.py
    app.run(debug=True)  # #запускаем сервер и показываем ошибки.

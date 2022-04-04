from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from datetime import datetime, date


app = Flask(__name__)  # create object by saying to Flask to turn the main file (letter.py) into app This is the main file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lc.db'  # approach to the dict 'config' by key SQLAlchemy... and set value of DB which ara intending to work with
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SESSION_PERMANENT'] = False
#app.config['SESSION_TYPE'] = 'filesystem'
#Session(app)
app.config['SECRET_KEY'] = 'adsgsdfhdsglhjdsaie46gjklsdjg'
db = SQLAlchemy(app)            #create instance db
migrate = Migrate(app, db)      #create instance of migration mechanics

@app.route('/login')
def login():
    return render_template('login.html')

#create table letter in db
class Letter(db.Model):  # inherit from db.Model
    id = db.Column(db.Integer, primary_key=True)
    lc_number = db.Column(db.String(15), nullable=False, unique=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)
    goods = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.String(10), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Letter %r>' % self.id  # the way of representation of the object (just for developers)


#create table applicant in db
class Applicant(db.Model):  # inherit from db.Model
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=True)
    district = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=True)
    building = db.Column(db.String(20), nullable=False)
    room = db.Column(db.String(20), nullable=True)

    #applicant_id = db.Column(db.)

    def __repr__(self):
        return '<Applicant %r>' % self.id

#
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(120), unique = True)
#     psw = db.Column(db.String(100), nullable = True)
#     date = db.Column(db.DateTime, default = datetime.utcnow)
#
# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#     old = db.Column(db.String(100), nullable=True)
#
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/letters')  #  url for page letters
def letter():
    letters_of_credit = Letter.query.order_by(Letter.id).all()
    return render_template('letters.html', letters_of_credit=letters_of_credit)  # letters_of_credit - the second parameter is passed to the template

@app.route('/letter_detail/<int:id>', methods = ["POST", "GET"])
def letter_detail(id):
    if request.method == "POST":    # for choosing LC within select tag of html template
        if request.form.get('LC Number') == 'LC Number':
            return render_template('letters.html')
        else:
            letters = Letter.query.all()
            for letter in letters:
                if letter.lc_number == request.form.get('LC Number'):
                    return render_template('letter_detail.html', letter=letter)


    letter = Letter.query.get(id)
    if letter is not None:
        return render_template('letter_detail.html', letter = letter)
    else:
        return render_template('letters.html')




@app.route('/letters/<path:applicant_name>')     #route for applicant's details (dinamic URL).
def applicant_detail(applicant_name):
    letters_of_credit = Letter.query.filter(Letter.applicant_name == applicant_name)     #create an instance
    applicants = Applicant.query.all()          #choose all records from table applicant with further passing it to template
    if letters_of_credit is not None:           #if letter is in BD, render template applicant
        return render_template('applicant_detail.html', letters_of_credit = letters_of_credit, applicant_name = applicant_name, applicants = applicants)  #вторым параметром передаем список arcticles в шаблон
        #else:
        #    return render_template('applicant_detail2.html', letters_of_credit=letters_of_credit, applicant_name=applicant_name)
    else:                       #else redirection to letters page
        redirect('/letters')


@app.route('/letters/<int:id>/delete')     #url for deleting of letter (dinamic).
def letter_delete(id):
    letter = Letter.query.get_or_404(id)    #create instance from db
    try:
        db.session.delete(letter)     #try to delete record from db
        db.session.commit()             #make commit to db
        return redirect('/letters')       #redirecting to letters page after deleting of an item
    except:
        return "Error has occurred while deleting LC"

@app.route('/letters/<int:id>/edit', methods = ['POST','GET'])
def letter_edit(id):
    letter = Letter.query.get(id)         #find an instance(LC) to be edited
    if request.method == "POST":            #if method POST, we pass values from the form on the web-site
        letter.lc_number = request.form["LC Number"]  # create variables, which are get values from the HTML-form by the name in square brackets
        letter.applicant_name = request.form["Applicant's Name"]
        letter.beneficiary_name = request.form["Beneficiary's Name"]
        letter.goods = request.form["Goods"]
        letter.currency = request.form["Currency"]
        letter.amount = request.form["Amount"]
        letter.date_of_issue = str(letter.lc_number[-6:-4] + '/' + letter.lc_number[-4:-2] + '/' + '20' + letter.lc_number[-2:])  # request.form["Date of Issue"]
        letter.expiry_date = request.form["Expiry Date"]

        try:
            db.session.commit()        #only commit is applied as the imet is alreade in db, we just make corrections to the existing LC
            return redirect('/letters')  #redirecting to the letters page
        except:
            return "An error has occurred while editing the LC"
    else:
        return render_template('letter_update.html', letter = letter)  #letter is passed to the template

@app.route('/add_lc', methods=['POST', 'GET'])  # url for LC adding
def add_lc():
    if request.method == "POST":  # if POST method, then variables are got values from HTML-form after our input action

        lc_number = request.form["LC Number"]   #create variables, which are get values from the HTML-form by the name in square brackets
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
            db.session.add(letter_of_credit)    #add to dbДобавляем в БД
            db.session.commit()         #save changes to db
            flash('LC has been successfully created')
            return redirect('/letters')  #в случае успешного сохранения пользователя перенаправляем на главную страницу

        except:
            return render_template('creating_error.html')
    else:
        return render_template('add_lc.html')


if __name__ == "__main__":  # если программа запускается через основной файл, т.е. app.py
    app.run(debug=True)  # #запускаем сервер и показываем ошибки.

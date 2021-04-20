from flask import Flask, render_template, request, redirect, url_for, flash, Session, make_response, send_file, session, \
    send_from_directory
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from users import Users
import datetime
import database
import os
from blog import Blog
import base64
from io import BytesIO

UPLOAD_FOLDER = '/Users/eberechukwukathomas/Desktop/back_up/static'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'thommyebere'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thomasebere119@gmail.com'
app.config['MAIL_PASSWORD'] = 'prick123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/signup', methods=['POST', 'GET'])
def first_page():
    error = None
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        country = request.form['county']
        capital = request.form['capitaly']
        _id = 7000
        date = datetime.datetime.now()
        error = "A user with this email exist already. Proceed to log in"

        tools = Users(fname, lname, email, password, country, capital, date, _id)
        database.create_table()
        if tools.check_user(email):
            countt = Users.ret_country()
            return render_template('signup.html', countt=countt, error=error)
        else:

            tools.signup()
            return redirect(url_for('index', email=email))
    else:
        countt = Users.ret_country()
        return render_template('signup.html', countt=countt, error=error)


@app.route('/login', methods=['POST', 'GET'])
def user():
    error = None
    errorr = None
    if request.method == 'POST':
        session['user'] = request.form['email']
        password = request.form['password']
        error = "Are you sure you are registered? Click the below to signup"
        errorr = "Please check your password and try again"
        if Users.check_user(session['user']):
            email, pass_word, first_name, capital, image = Users.check_user(session['user'])
            if password == pass_word:
                firstname = first_name
                capitall = capital
                time = Users.get_city_time(capitall)
                image = image
                if image is None:
                    user = session['user']
                    return redirect(url_for('opp', user=user))
                else:
                    # image_path = _get_image(image)
                    user = session['user']
                    return redirect(url_for('firsttpage'))
                    # return render_template('firstpage.html', firstname=firstname, time=time, image_path=image_path)
            else:
                return render_template('login.html', errorr=errorr)

        else:
            return render_template('login.html', error=error)

    else:
        return render_template('login.html', error=error, errorr=errorr)


@app.route('/sage')
def firsttpage():
    if 'user' in session:
        user = session['user']
        email, pass_word, first_name, capital, image = Users.check_user(session['user'])
        firstname = first_name
        capitall = capital
        time = Users.get_city_time(capitall)
        image_path = _get_image(image)
        return render_template('firstpage.html', firstname=firstname, time=time, user=user, image_path=image_path)


@app.route('/firstpage', methods=['POST', 'GET'])
def opp():
    if 'user' in session:
        user = session['user']
        email, pass_word, first_name, capital, image = Users.check_user(session['user'])
        firstname = first_name
        capitall = capital
        time = Users.get_city_time(capitall)
        return render_template('second.html', firstname=firstname, time=time, user=user)
    else:
        return 'Nawa'


@app.route('/map', methods=['POST', 'GET'])
def topboy():
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            if Users.user_image(filename, user):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('firsttpage', user=user))
            else:
                flash('file not saved ')
                return redirect(url_for('opp'))
        else:
            return redirect(url_for('opp'))
    else:
        return redirect(url_for('user'))


@app.route("/t/<email>")
def index(email):
    email, pass_word, first_name, capital, image = Users.check_user(email)
    first_name = first_name
    msg = Message('Thanks for signing up', sender='thomasebere119@gmail.com', recipients=[email])
    msg.body = """ Hello {} Thank you for signing up to our platform.""".format(first_name)
    msg.html = """Click <a href="http://127.0.0.1:4000/login">Login</a> to go to the login page. Thanks"""
    mail.send(msg)
    return "Successful! Kindly check your email to continue with the signup process"


def _get_image(image):
    image_name = "static/{}".format(image)
    return image_name


@app.route('/createblog', methods=['POST', 'GET'])
def create_blog():
    if request.method == 'POST':
        if 'user' in session:
            user = session['user']
            blogtitle = request.form['blogtitle']
            file = request.files['file']
            content = request.form['content']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            blog = Blog(blogtitle, user, content, filename)
            database.create_table()
            blog.create_blog()
            return render_template('published_blog.html', user=user, filename=filename, content=content,
                                   blogtitle=blogtitle)

    return render_template('blog.html')


@app.route('/readblock')
def read_blog():
    blog_body = Blog.get_all_blogs()
    return render_template('readblog.html', blog_body=blog_body)


@app.route('/goodnews/<data>', methods=['GET', 'POST'])
def good_new(data):
    tag = Blog.get_a_post(data)
    return render_template('table.html', tag=tag)


if __name__ == '__main__':
    app.run(port=4000, debug=True)

# if 'user' in session:
#     user=session['user']

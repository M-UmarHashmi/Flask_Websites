# from crypt import methods
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from matplotlib.pyplot import title
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime

tech_blog = Flask(__name__)
tech_blog.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'u6859407@gmail.com',
    MAIL_PASSWORD=  'cngxnnwjvcosaxbh'
)
mail = Mail(tech_blog)
tech_blog.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/codingthunder'
db = SQLAlchemy(tech_blog)

# sno, name , email, phone message date
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    sub_title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(12), nullable=False)
    posted_by = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    img_file = db.Column(db.String(12), nullable=False)


@tech_blog.route("/")
def home():
    posts = Posts.query.filter_by().all()
    return render_template('index.html', posts=posts)

# @tech_blog.route("/home")
# def home_nav():
#     return render_template('index.html')

@tech_blog.route("/contact.html", methods=['GET','POST'])
def contact_nav():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        # date = request.form.get('date')
        entry = Contact(name=name,email=email,phone=phone,message=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=['u6859407@gmail.com'],
                          body=message + "\n" + name +"\n" + phone + "\n" + email
                          )



    return render_template('contact.html')

@tech_blog.route("/post/<string:post_slug>")
def post_nav(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template('post.html',post=post)

@tech_blog.route("/about.html")
def about_nav():
    return render_template('about.html')

tech_blog.run(debug=True)
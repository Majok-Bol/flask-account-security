from flask import Flask,redirect,url_for,request,flash,render_template
from flask_sqlalchemy import SQLAlchemy
import os
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,InputRequired,ValidationError
from dotenv import load_dotenv
from flask_wtf import FlaskForm,CSRFProtect
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import re
load_dotenv()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
app.config['SECRET_KEY']=os.getenv("CSRF_SECRET_KEY")
db=SQLAlchemy(app)
csrf=CSRFProtect()
csrf.init_app(app)
migrate=Migrate()
#initialize app and database with migrate
migrate.init_app(app,db)
bcrypt=Bcrypt()
bcrypt.init_app(app)
@app.route('/',methods=['POST','GET'])
def home():
    return render_template('home.html')
@app.route('/register',methods=['POST','GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        username=form.username.data
        print("Username: ",username)
        email=form.email.data
        print("Email: ",email)
        password=form.password.data
        print("Password: ",password)
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        user=User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print("Account created successfully","success")
        return redirect(url_for("login"))
    if form.is_submitted():
        print(form.errors)
    return render_template('register.html',form=form)
@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        #check if username exists
        username=form.username.data
        password=form.password.data
        user=User.query.filter_by(username=username).first()
        if not user or bcrypt.check_password_hash(user.password,password):
            print("Invalid username or password")
            return redirect(url_for("login"))
        return redirect(url_for("dashboard"))
    return render_template('login.html',form=form)
@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')
#strong password validator
def strong_password(form,field):
    password=field.data
    print("Password",password)
    if len(password)<8:
        raise ValidationError("Password must be atleast 8 characters")
    if not re.search(r"[A-Z]",password):
        raise ValidationError("Password must contain an uppercase letter")
    if not re.search(r"[a-z]",password):
        raise ValidationError("Password must contain a lowercase letter")
    if not re.search(r"\d",password):
        raise ValidationError("Password must contain a number")
    if not re.search(r"[!@#$%^&*]",password):
        raise ValidationError("Password must contain a special character")


#register form instance
class RegisterForm(FlaskForm):
    username=StringField("Username",validators=[InputRequired()])
    email=EmailField("Email address",validators=[InputRequired(),Email()])
    password=PasswordField("Password",validators=[InputRequired(),strong_password])
    confirm_password=PasswordField("Confirm password",validators=[EqualTo('password',message="passwords must match")])
    submit=SubmitField("Register")
#login form instance
class LoginForm(FlaskForm):
    username=StringField("Username",validators=[InputRequired()])
    password=PasswordField("Password",validators=[InputRequired()])
    submit=SubmitField("Login")

#database model
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)




if __name__=="__main__":
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(debug=True)
from flask import Flask,redirect,url_for,request,flash,render_template
from flask_sqlalchemy import SQLAlchemy
import os
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,InputRequired,ValidationError
from dotenv import load_dotenv
from flask_wtf import FlaskForm,CSRFProtect
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import(
    login_user,
    logout_user,
    login_required,
    LoginManager,
    UserMixin
)
from urllib.parse import urljoin,urlparse
from flask_limiter import  Limiter
from flask_limiter.util import get_remote_address
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
login_manager=LoginManager()
login_manager.init_app(app)
limiter=Limiter(get_remote_address,app=app)
#send users to login page first
login_manager.login_view="login"
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
        flash("Account created successfully","success")
        return redirect(url_for("login"))
    if form.is_submitted():
        print(form.errors)
    return render_template('register.html',form=form)
@app.route('/login',methods=['POST','GET'])
#add rate limit to prevent bruteforce attacks on login 
@limiter.limit("5 per minute")
def login():
    form=LoginForm()
    if form.validate_on_submit():
        #check if username exists
        username=form.username.data
        password=form.password.data
        user=User.query.filter_by(username=username).first()
        print("User: ",user)
        if not user or not bcrypt.check_password_hash(user.password,password):
            flash("Invalid username or password","warning")
            # print("Invalid username or password")
            return redirect(url_for("login"))
        #create user session
        login_user(user)
        #get next page
        #prevent open redirects
        next_page=request.args.get("next")
        print("Next page: ",next_page)
        if next_page and is_safe_url(next_page):
            return redirect(next_page)

        return redirect(url_for("dashboard"))
    return render_template('login.html',form=form)
@app.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out","success")
    return redirect(url_for('login'))
#load user from the database
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,user_id)
#prevent open redirects
def is_safe_url(target):
    host_url=urlparse(request.host_url)
    print("Host url: ",host_url)
    print("host url: ",host_url.netloc)
    redirect_url=urlparse(urljoin(request.host_url,target))
    print("Redirect url: ",redirect_url.netloc)
    return (redirect_url.scheme in("http","https") and host_url.netloc==redirect_url.netloc)
#add rate limit
@app.errorhandler(429)
def rate_limit_error(e):
    return render_template("429.html"),429
#strong password validator
def strong_password(form,field):
    password=field.data
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
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)




if __name__=="__main__":
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run(debug=True)
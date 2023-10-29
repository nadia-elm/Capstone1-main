from flask import Flask, render_template, request, redirect, url_for, flash,session
from forms import  RegisterForm,UserLoginForm as LoginForm

from flask_cors import CORS
from flask_bcrypt import Bcrypt
import requests
from models import db, connect_db, User, Favorites
import os
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktailsdb'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',postgresql:///cocktails)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['SQLALCHEMY_ECHO'] = True

if not app.config['SECRET_KEY'] or not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("Missing essential configurations.")


connect_db(app)
with app.app_context(): 
    db.create_all()


@app.route('/')
def home():
    cocktails = get_cocktails()
    return render_template('home.html', cocktails=cocktails)

def get_cocktails():
    url= "https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail"
   
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['drinks']
    return []


@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    if 'user_id' not in session:
        flash('Please login to add favorites','danger')
        return redirect(url_for('login'))
    else:
        user_id = session['user_id']
        cocktail_id = request.form['cocktail_id']
        cocktail_name = request.form['cocktail_name']
        cocktail_image = request.form['cocktail_image']  
        if cocktail_name and cocktail_id and user_id:
            favorite = Favorites(cocktail_name= cocktail_name, cocktail_id=cocktail_id,cocktail_image = cocktail_image, user_id=user_id)
        db.session.add(favorite)
        db.session.commit()
        flash('Favorite successfully added', 'success')
        return redirect(url_for('favorites'))


@app.route('/favorites')
def favorites():
    if 'user_id'  not in session:
        flash('Please login to view favorites','warning')
        return redirect(url_for('login'))
    else:
        user_id = session['user_id']
        favorites = Favorites.query.filter_by(user_id=user_id).all()
        return render_template('favorites.html', favorites=favorites)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data 
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'warning')
            return redirect(url_for('register'))
        user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering user', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username= form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('User successfully logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username/password', 'warning')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('User successfully logged out')
    return redirect(url_for('home'))



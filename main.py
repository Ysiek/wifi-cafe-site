from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ASBouy1g278saodhas'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

now = datetime.now()
today = now.strftime('%a').lower()


@login_manager.user_loader
def load_user(user_id):
    return db.session.scalars(db.select(User).where(User.id == user_id)).first()


class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    localization = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # FILTERS
    has_sockets = db.Column(db.Integer, nullable=False)
    quiet = db.Column(db.Integer, nullable=False)
    wifi = db.Column(db.Integer, nullable=False)
    groups = db.Column(db.Integer, nullable=False)
    coffee = db.Column(db.Integer, nullable=False)
    food = db.Column(db.Integer, nullable=False)
    alcohol = db.Column(db.Integer, nullable=False)
    parking = db.Column(db.Integer, nullable=False)
    toilet = db.Column(db.Integer, nullable=False)
    # 0 = doesn't exist
    # 1 = exist but work bad
    # 2 = exist work quite good
    # 3 = exist and work really well
    # RELATIONSHIP
    cafe = relationship('Cafe_hours', back_populates='cafe')


class Cafe_hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mon = db.Column(db.String(250), nullable=False)
    tue = db.Column(db.String(250), nullable=False)
    wed = db.Column(db.String(250), nullable=False)
    thu = db.Column(db.String(250), nullable=False)
    fri = db.Column(db.String(250), nullable=False)
    sat = db.Column(db.String(250), nullable=False)
    sun = db.Column(db.String(250), nullable=False)
    # RELATIONSHIP
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafe.id'))
    cafe = relationship("Cafe", back_populates='cafe')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)


class Register(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class Login(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

FILTERS = None

@app.route('/')
def home():
    global FILTERS

    if not FILTERS:
        all_cafes = db.session.scalars(db.select(Cafe)).all()
    if FILTERS == 'has_sockets':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.has_sockets.asc())).all()
    if FILTERS == 'quiet':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.quiet.asc())).all()
    if FILTERS == 'wifi':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.wifi.asc())).all()
    if FILTERS == 'groups':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.groups.asc())).all()
    if FILTERS == 'coffee':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.coffee.asc())).all()
    if FILTERS == 'food':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.food.asc())).all()
    if FILTERS == 'alcohol':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.alcohol.asc())).all()
    if FILTERS == 'parking':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.parking.asc())).all()
    if FILTERS == 'toilet':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.toilet.asc())).all()
    return render_template('index.html', all_cafes=all_cafes, today=today, user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/filter/<types>')
def filters_manager(types):
    global FILTERS
    FILTERS = types
    return redirect(url_for('home'))


@app.route('/cafe/<cafe_id>')
def cafe_site(cafe_id):
    cafe = db.session.scalars(db.select(Cafe).where(Cafe.id == cafe_id)).first()
    color_dict = {
        0: 'grey',
        1: 'red',
        2: 'yellow',
        3: 'green'
    }
    return render_template('cafe-site.html', cafe=cafe, color_dict=color_dict, user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_to_login = db.session.scalars(db.select(User).where(User.email == email)).first()
        print(db.session.scalars(db.select(User.password).where(User.email == email)))
        if not user_to_login:
            abort(403)
        if not check_password_hash(db.session.scalars(db.select(User.password).where(User.email == email)).first(),
                                   password):
            print("zle haslo")
        login_user(user_to_login)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data, 'pbkdf2', salt_length=8),
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

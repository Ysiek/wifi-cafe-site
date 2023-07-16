from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField
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
    # RELATIONSHIP WITH CAFE_HOURS
    cafe = relationship('Cafe_hours', back_populates='cafe')

    #RELATIONSHIP WITH USERSLIKED
    user_cafe = relationship('UsersLiked', back_populates='particular_cafe')



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


class UsersLiked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # RELATIONSHIP WITH USER
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='user')

    #RELATIONSHIP WITH CAFE
    cafe_id = db.Column(db.Integer, db.ForeignKey('cafe.id'))
    particular_cafe = relationship('Cafe', back_populates='user_cafe')




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    #RELATIONSHIP WITH USERSLIKED
    user = relationship('UsersLiked', back_populates='user')


class CafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    localization = StringField("Localization", validators=[DataRequired()])
    image = StringField("Image", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
    sockets = IntegerField("Sockets", validators=[DataRequired()])
    quiet = IntegerField("Quiet", validators=[DataRequired()])
    wifi = IntegerField("Wifi", validators=[DataRequired()])
    groups = IntegerField("Groups", validators=[DataRequired()])
    coffee = IntegerField("Coffee", validators=[DataRequired()])
    food = IntegerField("Food", validators=[DataRequired()])
    alcohol = IntegerField("Alcohol", validators=[DataRequired()])
    parking = IntegerField("Parking", validators=[DataRequired()])
    toilet = IntegerField("Toilet", validators=[DataRequired()])
    mon_fri = StringField("From monday-friday which hours cafe is open", validators=[DataRequired()])
    saturday = StringField("Saturday", validators=[DataRequired()])
    sunday = StringField("Sunday", validators=[DataRequired()])


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
    if not FILTERS or FILTERS == 'reset':
        all_cafes = db.session.scalars(db.select(Cafe)).all()
    elif FILTERS == 'liked' and current_user.is_authenticated:
        all_cafes = db.session.scalars(db.select(Cafe).join(UsersLiked).where(UsersLiked.user_id == current_user.id)).all()
    if FILTERS == 'sockets':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.has_sockets.desc())).all()
    if FILTERS == 'quiet':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.quiet.desc())).all()
    if FILTERS == 'wifi':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.wifi.desc())).all()
    if FILTERS == 'groups':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.groups.desc())).all()
    if FILTERS == 'coffee':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.coffee.desc())).all()
    if FILTERS == 'food':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.food.desc())).all()
    if FILTERS == 'alcohol':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.alcohol.desc())).all()
    if FILTERS == 'parking':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.parking.desc())).all()
    if FILTERS == 'toilet':
        all_cafes = db.session.scalars(db.select(Cafe).order_by(Cafe.toilet.desc())).all()
    return render_template('index.html', all_cafes=all_cafes, filter=FILTERS, today=today, user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route('/filter/<types>')
def filters_manager(types):
    global FILTERS
    FILTERS = types
    return redirect(url_for('home'))

def add_cafe_fun(current_user_id, cafe_id):
    new_user_like = UsersLiked(
        user_id=current_user_id,
        cafe_id=cafe_id
    )
    db.session.add(new_user_like)
    db.session.commit()

@app.route('/add/<int:cafe_id>/<int:current_user_id>')
def add_cafe(cafe_id, current_user_id):
    if not current_user.is_authenticated:
        abort(403)
    user = db.session.scalars(db.select(UsersLiked).where(UsersLiked.user_id == current_user_id)).all()
    if not user:
        add_cafe_fun(current_user_id, cafe_id)
    else:
        for u in user:
            if not u.cafe_id == cafe_id:
                add_cafe_fun(current_user_id, cafe_id)
    return redirect(url_for('home'))



@app.route('/cafe/<int:cafe_id>')
def cafe_site(cafe_id):
    cafe = db.session.scalars(db.select(Cafe).where(Cafe.id == cafe_id)).first()
    user_like = False
    if current_user.is_authenticated:
        sel_user = db.session.scalars(db.select(User).where(User.id == current_user.id)).first()
        if not hasattr(sel_user, 'user'):
            print('nie ma takiego atrybutu')
        for like_object in sel_user.user:
            if like_object.cafe_id == cafe_id:
                user_like = True

    color_dict = {
        0: 'grey',
        1: 'red',
        2: 'yellow',
        3: 'green'
    }
    return render_template('cafe-site.html', cafe=cafe, user_like=user_like, color_dict=color_dict, user=current_user,
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
    global FILTERS
    FILTERS = None
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

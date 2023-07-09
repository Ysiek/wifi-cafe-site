from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ASBouy1g278saodhas'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe.db"
db = SQLAlchemy(app)


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


class Register(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


@app.route('/')
def home():
    now = datetime.now()
    today = now.strftime('%a').lower()
    all_cafe = db.session.scalars(db.select(Cafe)).all()
    return render_template('index.html', all_cafes=all_cafe, today=today)


@app.route('/cafe/<cafe_id>')
def cafe_site(cafe_id):
    cafe = db.session.scalars(db.select(Cafe).where(Cafe.id == cafe_id)).first()
    color_dict = {
        0: 'grey',
        1: 'red',
        2: 'yellow',
        3: 'green'
    }
    return render_template('cafe-site.html', cafe=cafe, color_dict=color_dict)


@app.route('/register')
def register():
    form = Register()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

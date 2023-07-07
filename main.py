from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ASBouy1g278saodhas'


class Register(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafe')
def cafe_site():
    return render_template('cafe-site.html')


@app.route('/register')
def register():
    form = Register()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

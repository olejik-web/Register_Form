from datetime import datetime
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    login_or_mail = StringField('Login / email', 
                                     validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = StringField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])    
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

@app.route('/')
def index():
    db_session.global_init("db/mars.db")
    db_sess = db_session.create_session()
    jobs = [job for job in db_sess.query(Jobs).all()]
    users = [user for user in db_sess.query(User).all()]
    return render_template('works_journal.html', title='Journal works', 
                           jobs=jobs, users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_session.global_init("db/mars.db")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.login_or_mail.data     
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/register')
    return render_template('register_form.html', form=form)


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()


'''@app.route('/training/<prof>')


def training(prof):
    return render_template('training.html', prof=prof)'''


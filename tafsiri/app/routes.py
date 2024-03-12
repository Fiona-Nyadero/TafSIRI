from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/catalogue')
def catalogue():
    user = {'username' : 'StephFiona'}
    posts = [
        {
            'proponent': {'username': 'Stephanie'},
            'title': 'Voi Affordable Housing'
        },
        {
            'proponent': {'username': 'Fiona'},
            'title': 'Mwatate Recreational Park'
        }
    ]
    return render_template('catalogue.html', title='Catalogue', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me{}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
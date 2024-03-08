from flask import render_template
from app import app

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
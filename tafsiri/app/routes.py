from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User, Project
from app.forms import RegistrationForm, LoginForm, EditProfileForm, AddProjectForm, EditProjectForm
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app import app
from datetime import datetime, timezone

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/index2')
@login_required
def index2():
    return render_template('index2.html', title='Home')

@app.route('/catalogue')
def catalogue():
    query = sa.select(Project)
    projects = db.session.scalars(query)
    return render_template('catalogue.html', title='Catalogue', projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.Username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            Username=form.username.data,
            Email=form.email.data,
            Type=form.user_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.Username == username))
    if current_user.Type == 'Admin':
        return redirect(url_for('index'))
    projects = [
        {'author': user, 'title': 'Test post #1'},
        {'author': user, 'title': 'Test post #2'},
    ]
    return render_template('user.html', user=user, projects=projects)

@app.route('/project/<projectname>')
def project(projectname):
    project = db.first_or_404(sa.select(Project).where(Project.Title == projectname))
    return render_template('project.html', title=projectname, project=project)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.Last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.Username = form.username.data
        current_user.About_me = form.about_me.data
        current_user.Job_title = form.job_title.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.about_me.data = current_user.About_me
        form.job_title.data = current_user.Job_title
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/admin/<username>')
@login_required
def admin(username):
    user = db.first_or_404(sa.select(User).where(User.Username == username))
    if current_user.Type != 'Admin':
        return redirect(url_for('index'))
    projects = [
        {'author': user, 'title': 'Test post #1'},
        {'author': user, 'title': 'Test post #2'},
    ]
    return render_template('admin.html', user=user, projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if current_user.Type != 'Admin':
        return redirect(url_for('catalogue'))
    form = AddProjectForm()
    if form.validate_on_submit():
        project = Project(
            Title=form.title.data,
            Description=form.description.data,
            Background=form.background.data,
            Proposal=form.proposal.data,
            Deadline=form.deadline.data,
            SDGs=form.sdgs.data,
            Latitude=form.latitude.data,
            Longitude=form.longitude.data,
            Phase=form.phase.data,
            Category=form.category.data,
            County=form.county.data)
        db.session.add(project)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('/admin/<username>'))
    return render_template('add_project.html', title='Add Project', form=form)

@app.route('/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project():
    if current_user.Type != 'Admin':
        return redirect(url_for('index'))
    form = EditProjectForm()
    if form.validate_on_submit():
        Project.Title = form.title.data
        Project.Description = form.description.data
        Project.Phase = form.phase.data
        db.session.commit()
        flash('Your project changes have been saved')
        return redirect(url_for('edit_project'))
    elif request.method == 'GET':
        form.title.data = Project.Title
        form.description.data = Project.Description
        form.phase.data = Project.Phase
    return render_template('edit_project.html', title='Edit Project',
                           form=form)

@app.route('/manage_projects')
@login_required
def manage_projects():
    if current_user.Type != 'Admin':
        return redirect(url_for('index'))
    query = sa.select(Project)
    projects = db.session.scalars(query)
    return render_template('manage_projects.html', title='Manage Projects', projects=projects)
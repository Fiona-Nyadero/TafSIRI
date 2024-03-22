from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app import db
from app.models import User, Project, Feedback
from app.forms import RegistrationForm, LoginForm, EditProfileForm, AddProjectForm, EditProjectForm, FeedbackForm
from flask import render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
from urllib.parse import urlsplit
from app import app
from datetime import datetime, timezone
import json
from flask_moment import moment

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='Home')

@app.route('/landing')
@login_required
def landing():
    return render_template('landing.html', title='Home')

@app.route('/catalogue')
def catalogue():
    query = sa.select(Project)
    projects = db.session.scalars(query)
    
    projects_data = []
    for project in projects:
        project_data = {
            'title': project.Title,
            'latitude': project.Latitude,
            'longitude': project.Longitude
        }
        projects_data.append(project_data)

    projects_json = json.dumps(projects_data)

    return render_template('catalogue.html', title='Catalogue', projects=projects,
                           projects_json=projects_json)

@app.route('/projects')
def projects():
    query = sa.select(Project)
    projects = db.session.scalars(query)

    return render_template('projects.html', title='Projects', projects=projects)

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
    query = sa.select(Project)
    projects = db.session.scalars(query)
    return render_template('user.html', user=user, projects=projects)

@app.route('/admin/<username>')
@login_required
def admin(username):
    user = db.first_or_404(sa.select(User).where(User.Username == username))
    if current_user.Type != 'Admin':
        return redirect(url_for('index'))
    query = sa.select(Project)
    projects = db.session.scalars(query)
    return render_template('admin.html', user=user, projects=projects)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.Username = form.username.data
        current_user.About_me = form.about_me.data
        current_user.Job_title = form.job_title.data
        current_user.Type=form.user_type.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.about_me.data = current_user.About_me
        form.job_title.data = current_user.Job_title
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.Last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/project/<projectname>')
def project(projectname):
    project = db.first_or_404(sa.select(Project).where(Project.Title == projectname))
    return render_template('project.html', title=projectname, project=project)

@app.route('/project/<projectname>/feedback', methods=['GET', 'POST'])
def project_feedback(projectname):
    project = Project.query.filter_by(Title=projectname).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('catalogue'))
    user_id = current_user.id
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            Rating=form.rating.data,
            Rating_reason=form.rating_reason.data,
            Suggestions=form.suggestions.data,
            Responsee_id=user_id,
            Feedback_project_id=project.id
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully. Thank you for your feedback!')
        return redirect(url_for('project', projectname=projectname))
    return render_template('feedback.html', title='Have your Say!', project=project, form=form)

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
            SDGs=form.sdgs.data,
            Latitude=form.latitude.data,
            Longitude=form.longitude.data,
            Phase=form.phase.data,
            Category=form.category.data,
            County=form.county.data,
            Cover=form.cover.data,
            Plan=form.plan.data,
            User_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Success! You have a project entry!')
        return redirect(url_for('manage_projects'))
    return render_template('add_project.html', title='Add Project', form=form)

@app.route('/edit_project/<projectname>', methods=['GET', 'POST'])
@login_required
def edit_project(projectname):
    project = Project.query.filter_by(Title=projectname).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('catalogue'))
    if current_user.Type != 'Admin':
        return redirect(url_for('catalogue'))
    #if current_user != project.Author:
    #return redirect(url_for('project', projectname=projectname))
    form = EditProjectForm()
    if form.validate_on_submit():
        project.Title = form.title.data
        project.Description = form.description.data
        project.Phase = form.phase.data
        project.Cover=form.cover.data
        project.Plan=form.plan.data
        project.SDGs=form.sdgs.data
        project.Latitude=form.latitude.data
        project.Longitude=form.longitude.data
        project.Background=form.background.data
        project.Proposal=form.proposal.data
        project.Category=form.category.data
        project.County=form.county.data
        deadline_str = form.deadline.data
        project.Deadline=datetime.strptime(deadline_str, '%m/%d/%Y')
        db.session.commit()
        flash('Your project changes have been saved')
        return redirect(url_for('manage_projects'))
    elif request.method == 'GET':
        form.title.data = project.Title
        form.description.data = project.Description
        form.phase.data = project.Phase
        form.cover.data = project.Cover
        form.plan.data = project.Plan
        form.sdgs.data = project.SDGs
        form.latitude.data = project.Latitude
        form.longitude.data = project.Longitude
        form.background.data = project.Background
        form.proposal.data = project.Proposal
        form.category.data = project.Category
        form.county.data = project.County
        form.deadline.data = project.Deadline
    return render_template('edit_project.html', title='Edit Project',
                           project=project, form=form)

@app.route('/manage_projects')
@login_required
def manage_projects():
    if current_user.Type != 'Admin':
        return redirect(url_for('index'))
    query = sa.select(Project)
    projects = db.session.scalars(query)
    return render_template('manage_projects.html', title='Manage Projects', projects=projects)

@app.route('/test_fonts')
def test_fonts():
    return render_template('Xtest.html')

@app.route('/feedback/<projectname>', methods=['GET', 'POST'])
@login_required
def feedback(projectname):
    project = Project.query.filter_by(Title=projectname).first()
    if project is None:
        flash('Project not found.')
        return redirect(url_for('catalogue'))
    if current_user.Type != 'Admin':
        return redirect(url_for('catalogue'))
    if current_user != project.Author:
        return redirect(url_for('project', projectname=projectname))
    
    return render_template('feedbacklist.html', title='Project Feedback',
                           project=project)

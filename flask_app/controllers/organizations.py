from flask import render_template,redirect,session,request, flash
from flask_app.models.developer import Developer
from flask_app.models.skill import Skill
from flask_app.models.skill_of_developer import Skill_of_developer
from flask_app.models.count import Count
from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/orgs/jobs/availabledevs')
def availabledevs():
    return render_template('availabledevs.html')


@app.route('/orgs/jobs/new')
def addposition():
    return render_template('addposition.html')


@app.route('/orgs/dashboard_org')
def dashboard_org():
    return render_template('dashboard_org.html')


@app.route('/orgs/register')
def index_org():
    return render_template('registerorg.html')

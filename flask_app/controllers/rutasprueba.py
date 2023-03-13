
from flask import render_template,redirect,session,request, flash
from flask_app import app



@app.route('/registerdev')
def index():
    return render_template('registerdev.html')



@app.route('/registerorg')
def index2():
    return render_template('registerorg.html')



@app.route('/languages')
def index3():
    return render_template('skills.html')


@app.route('/dashboard')
def index4():
    return render_template('dashboard.html')




@app.route('/org/jobs/new')
def index5():
    return render_template('addposition.html')




from flask import render_template,redirect,session,request, flash
from flask_app import app



@app.route('/registerdev')
def index():
    return render_template('registerdev.html')



@app.route('/registerorg')
def index2():
    return render_template('registerorg.html')
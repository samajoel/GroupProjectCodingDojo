from flask import render_template,redirect,session,request, flash
from flask_app import app


@app.route('/registerorg')
def index2():
    return render_template('registerorg.html')
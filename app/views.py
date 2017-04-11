from flask import render_template, request, flash, redirect, url_for
from app import app, mongo

@app.route('/')
def index():
    return render_template('index.html')

from flask import render_template, request, flash, redirect, url_for
from app import app, mongo
from controller import get_files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
  if request.method == 'POST':
    keywords = request.form['keyword']
    language = request.form['language']
    paths = controller.get_files(keywords, language)
    #paths = ["http://hola.com/hola", "http://chao.com/chao"]
    return render_template('list.html', paths=paths)

  return redirect(url_for('index'))

@app.context_processor
def utility_processor():
  def get_name(filepath):
    file_name = filepath.split('/')
    return file_name[-1]
  return dict(get_name=get_name)

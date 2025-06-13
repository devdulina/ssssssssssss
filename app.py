import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import requests
from newsapi_key import NEWS_API_KEY  # Make sure this file exists with your API key

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USER_EMAIL = 'student.dulina@edu.com'
USER_PASSWORD = 'passwords@123'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

blogs = []

def save_blogs():
    with open('blogs.json', 'w', encoding='utf-8') as f:
        json.dump(blogs, f, indent=4, ensure_ascii=False)

def load_blogs():
    global blogs
    if os.path.exists('blogs.json'):
        with open('blogs.json', 'r', encoding='utf-8') as f:
            blogs = json.load(f)
    else:
        blogs = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    category = request.args.get('category', 'general')

    url = ('https://newsapi.org/v2/top-headlines?'
           f'country=us&category={category}&apiKey={NEWS_API_KEY}')
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    return render_template('home.html', blogs=blogs, articles=articles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == USER_EMAIL and password == USER_PASSWORD:
            session['user'] = email
            load_blogs()
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', blogs=blogs)

@app.route('/blog/<int:index>')
def view_blog(index):
    if 0 <= index < len(blogs):
        blog = blogs[index]
        return render_template('view_blog.html', blog=blog)
    else:
        return "Blog not found", 404


@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_filename = f'uploads/{filename}'  # Use forward slashes for URLs

        new_blog = {
            'title': request.form['title'],
            'content': request.form['content'],
            'image': image_filename,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'author': session['user']
        }
        blogs.insert(0, new_blog)  # Insert at start for recent first
        save_blogs()
        return redirect(url_for('dashboard'))
    return render_template('add_blog.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_blog(index):
    if 'user' not in session:
        return redirect(url_for('login'))
    if index < 0 or index >= len(blogs):
        return "Blog not found", 404

    blog = blogs[index]
    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                blog['image'] = f'uploads/{filename}'

        blog['title'] = request.form['title']
        blog['content'] = request.form['content']
        save_blogs()
        return redirect(url_for('dashboard'))

    return render_template('edit_blog.html', blog=blog, index=index)

@app.route('/delete/<int:index>')
def delete_blog(index):
    if 'user' not in session:
        return redirect(url_for('login'))
    if 0 <= index < len(blogs):
        blogs.pop(index)
        save_blogs()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    load_blogs()
    app.run(debug=True)

from flask import Flask, render_template ,redirect, url_for, request, make_response,flash,url_for,send_from_directory,jsonify
from pymongo import MongoClient
from functools import wraps
import string 
import random


app=Flask(__name__)
app.config['SECRET_KEY'] = '1234login'
client = MongoClient('mongodb://localhost:27017/users')
db = client['web_course']
collection = db['practice']
note = db['note']
S=10

def is_authenticated(request):
    username = request.cookies.get('username', '')
    token = request.cookies.get('token', '')
    db_username = collection.find_one({'username':username})
    if token:
        if username == db_username['username']:
            token == db_username['token']
            return True
        return False
    return False

def login_required(func):
    @wraps(func)
    def verify(*args, **kwargs):
        if is_authenticated(request):
            return func(*args, **kwargs)
        else:
            flash('Please login first!!!','error')
            return redirect(url_for('login'))
    return verify

@app.route('/')
def index():
    
    blog = list(note.find({},{'_id': False}))
    for x in blog:
        print(x)
    return render_template('index.html', note=blog)

@app.route('/profile/')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = collection.find_one({'username':request.form['username']})
        if user != None:
            if username == user['username']:
                if password == user['password']:
                    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
                    session_token = random_string
                    response = make_response(redirect(url_for('profile')))
                    response.set_cookie(key='username',value=username)
                    response.set_cookie(key='token',value=session_token)
                    collection.update_one({'username':username},{'$set':{'token':session_token}})
                    return response
                else:
                    flash('Username or password is invalid', 'error')  
            else:
                flash('Username or password is invalid', 'error')
        else:
            flash('Username or password is invalid!', 'error')

    return render_template('login.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = collection.find_one({'username':request.form['username']})
        if user:
            flash('Username is already existed', 'error')
            return render_template("signup.html")
        else:
            collection.insert_one({
                'username': request.form['username'],
                'password': request.form['password']
            })

        return render_template("login.html")

    return render_template('signup.html')

@app.route('/signout', methods=['GET', 'POST'])
@login_required
def signout():
    username = request.cookies.get('username', '')
    collection.update_one({'username':username},{'$set':{'token':' '}})
    response = make_response(redirect(url_for('login')))
    response.set_cookie(key='token',value='')
    flash('Sign Out successfully!', 'message')
    return response

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    blog = []
    cursor = note.find({},{'_id': False})
    for x in cursor:
        blog.append(x)
    return render_template('note.html', note=blog)

@app.route('/input', methods=['GET', 'POST'])
@login_required
def input():
    if request.method == 'POST':
        username = request.cookies.get('username', '')
        note.insert_one({'username':username ,'title':request.form['title'], 'note':request.form['post']})
        return redirect(url_for('index'))
    return render_template('input.html')
    
if __name__ == "__main__":
    app.run(debug=True)
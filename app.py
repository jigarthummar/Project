from flask import Flask, render_template ,redirect, url_for, session, request, make_response,flash,url_for,send_from_directory,jsonify
from pymongo import MongoClient
from functools import wraps
import string 
import random


app=Flask(__name__)
app.config['SECRET_KEY'] = '1234login'
client = MongoClient('mongodb://localhost:27017/')
db = client['Project']
collection = db['UserData']
user_coll = db['History']
study_coll = db['Videos']
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
    if 'username' in session:
        user = collection.find_one({'username': session['username']})
        return render_template('profile.html',
        fname = user['FirstName'],
        finame = user['FirstName'],
        sname = user['LastName'],
        uname = user['username'],
        bdate = user['Birthdate']
        )
    return redirect(url_for('login'))



@app.route('/admin',method=['POST'])
@login_required
def admin():
    if request.method == 'POST':
        
    return render_template('admin.html')
    

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = collection.find_one({'username':request.form['username']})
        if user != None:
            if username == user['username']:
                if password == user['password']:
                    session['username'] = request.form['username']
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
        elif username == "admin":
            if password == "Code'School":
                session['username'] = "admin"
                return render_template('admin.html')
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
        elif request.form['username'] == "admin":
            flash('Username is already existed', 'error')
            return render_template("signup.html")
        else:
            if request.form['password'] == request.form['cpassword']:
                collection.insert_one({
                    'username': request.form['username'],
                    'password': request.form['password'],
                    'FirstName' : request.form['firstname'],
                    'LastName' : request.form['lastname'],
                    'Birthdate' : request.form['birthdate']
                })
            else:
                flash('Please enter same password', 'error')
                return render_template("signup.html")

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
    session.pop('username',None)
    return response



@app.route('/wd')
@login_required
def wd():
    if 'username' in session:
        """study_coll.insert_one({
                        'Number' : 2,
                        'Course': "html",
                        'Link': 'https://www.youtube.com/embed/qz0aGYrrlhU'
                    })"""
        #username = session['username']
        #note.insert_one({'username':username ,'title':request.form['title'], 'note':request.form['post']})
        html_videos = study_coll.find({'Course' : "html"})
        css_videos = study_coll.find({'Course' : "css"})
        js_videos = study_coll.find({'Course' : "js"})
        return render_template('webdev.html', 
                                hvideos = html_videos,
                                cvideos = css_videos,
                                jvideos = js_videos)
    flash('Please log in', 'error')
    return render_template('login.html')

@app.route('/wd', methods = ['GET','POST'])
@login_required
def record_wd():
    if 'username' in session:
        user_coll.insert_one({
                        'username': session['username'],
                        'Link': request.form['first']
                    })
    return render_template('webdev.html')

    
if __name__ == "__main__":
    app.run(debug=True)
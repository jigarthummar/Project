from email import message
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
    if session['username'] == 'admin':
        return render_template('admin.html')
    elif 'username' in session:
        user = collection.find_one({'username': session['username']})
        return render_template('profile.html',
        fname = user['FirstName'],
        finame = user['FirstName'],
        sname = user['LastName'],
        uname = user['username'],
        bdate = user['Birthdate']
        )
    return redirect(url_for('login'))



@app.route('/admin',methods=['POST'])
@login_required
def admin():
    if request.method == 'POST':
        Course = request.form.get('webdev')
        if Course != "None":
            link = request.form.get('w_link')
            study_coll.insert_one({
                        'Number' : 4,
                        'Course': str(Course),
                        'Link': link
                    })
            return render_template('admin.html',message = "Success")

        Course = request.form.get('ml')
        if Course != "None":
            link = request.form.get('m_link')
            study_coll.insert_one({
                        'Number' : 4,
                        'Course': str(Course),
                        'Link': link
                    })
            return render_template('admin.html',message = "Success")
        
        Course = request.form.get('bc')
        if Course != "None":
            link = request.form.get('b_link')
            study_coll.insert_one({
                        'Number' : 4,
                        'Course': str(Course),
                        'Link': link
                    })
            return render_template('admin.html',message = "Success")

        Course = request.form.get('pl')
        if Course != "None":
            link = request.form.get('p_link')
            study_coll.insert_one({
                        'Number' : 4,
                        'Course': str(Course),
                        'Link': link
                    })
            return render_template('admin.html',message = "Success")

        Course = request.form.get('cs')
        if Course != "None":
            link = request.form.get('c_link')
            study_coll.insert_one({
                        'Number' : 4,
                        'Course': str(Course),
                        'Link': link
                    })
            return render_template('admin.html',message = "Success")

        Course = request.form.get('ds')
        if Course != "None":
            link = request.form.get('d_link')
            study_coll.insert_one({
                        'Number' : 4,
                        'Course': str(Course),
                        'Link': link
                    })
            return render_template('admin.html',message = "Success")

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
                    if username == "admin":
                        response = make_response(render_template('admin.html'))
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
        html_videos = study_coll.find({'Course' : "html"})
        css_videos = study_coll.find({'Course' : "css"})
        js_videos = study_coll.find({'Course' : "js"})
        njs_videos = study_coll.find({'Course' : "njs"})
        db_videos = study_coll.find({'Course' : "dbms"})
        re_videos = study_coll.find({'Course' : "react"})
        pr_videos = study_coll.find({'Course' : "w_project"})
        return render_template('webdev.html', 
                                hvideos = html_videos,cvideos = css_videos,
                                jvideos = js_videos,njvideos = njs_videos,
                                dbvideos = db_videos, revideos = re_videos,
                                project = pr_videos)
    flash('Please log in', 'error')
    return render_template('login.html')

@app.route('/bc')
@login_required
def bc():
    if 'username' in session:
        bc_videos = study_coll.find({'Course' : "blockchain"})
        tool_videos = study_coll.find({'Course' : "tools"})
        js_videos = study_coll.find({'Course' : "js"})
        solid_videos = study_coll.find({'Course' : "solid"})
        njs_videos = study_coll.find({'Course' : "njs"})
        re_videos = study_coll.find({'Course' : "react"})
        wb_videos = study_coll.find({'Course' : "wb3"})
        return render_template('blockchain.html', 
                                hvideos = bc_videos,
                                cvideos = tool_videos,
                                jvideos = js_videos,
                                svideos = solid_videos,
                                njvideos = njs_videos, 
                                revideos = re_videos,
                                project = wb_videos)
    flash('Please log in', 'error')
    return render_template('login.html')

@app.route('/ml')
@login_required
def ml():
    if 'username' in session:
        python_videos = study_coll.find({'Course' : "python"})
        dsa_videos = study_coll.find({'Course' : "m_dsa"})
        js_videos = study_coll.find({'Course' : "js"})
        mysql_videos = study_coll.find({'Course' : "mysql"})
        lib_videos = study_coll.find({'Course' : "library"})
        ms_videos = study_coll.find({'Course' : "maths"})
        mlc_videos = study_coll.find({'Course' : "mlc"})
        dlc_videos = study_coll.find({'Course' : "dlc"})
        project = study_coll.find({'Course' : "ml_project"})
        return render_template('machinel.html', 
                                pvideos = python_videos,
                                dsvideos = dsa_videos,
                                jvideos = js_videos,
                                mvideos = mysql_videos,
                                lvideos = lib_videos, 
                                msvideos = ms_videos,
                                mlcvideos = mlc_videos,
                                dlcvideos = dlc_videos,
                                project = project)
    flash('Please log in', 'error')
    return render_template('login.html')


@app.route('/pl')
@login_required
def pl():
    if 'username' in session:
        python_videos = study_coll.find({'Course' : "python"})
        c_videos = study_coll.find({'Course' : "c"})
        cc_videos = study_coll.find({'Course' : "c++"})
        j_videos = study_coll.find({'Course' : "java"})
        js_videos = study_coll.find({'Course' : "js"})
        s_videos = study_coll.find({'Course' : "swift"})
        go_videos = study_coll.find({'Course' : "go"})
        return render_template('Prog_lang.html', 
                                pvideos = python_videos,
                                csvideos = c_videos,
                                jvideos = j_videos,
                                jsvideos = js_videos,
                                ccvideos = cc_videos,
                                svideos = s_videos,
                                gvideos = go_videos)
    flash('Please log in', 'error')
    return render_template('login.html')

@app.route('/cs')
@login_required
def cs():
    if 'username' in session:
        hv_videos = study_coll.find({'Course' : "hv"})
        cbp_videos = study_coll.find({'Course' : "cbash"})
        sbp_videos = study_coll.find({'Course' : "sbash"})
        cn_videos = study_coll.find({'Course' : "cn"})
        return render_template('cyber_security.html', 
                                hvideos = hv_videos,
                                cbpvideos = cbp_videos,
                                sbpvideos = sbp_videos,
                                cnvideos = cn_videos)
    flash('Please log in', 'error')
    return render_template('login.html')

@app.route('/ds')
@login_required
def ds():
    if 'username' in session:
        excel_videos = study_coll.find({'Course' : "es"})
        lib_videos = study_coll.find({'Course' : "lib"})
        ml_videos = study_coll.find({'Course' : "mlc"})
        dlc_videos = study_coll.find({'Course' : "dlc"})
        db_videos = study_coll.find({'Course' : "mongo"})
        b_videos = study_coll.find({'Course' : "btools"})
        return render_template('data_science.html', 
                                evideos = excel_videos,
                                lvideos = lib_videos,
                                mlvideos = ml_videos,
                                dlcvideos = dlc_videos,
                                dbvideos = db_videos,
                                bvideos = b_videos)
    flash('Please log in', 'error')
    return render_template('login.html')

    
if __name__ == "__main__":
    app.run(debug=True)
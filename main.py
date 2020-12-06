from flask import Flask , render_template,request,redirect, url_for,session
import mysql.connector
import os

app=Flask(__name__,template_folder= 'templates')
app.secret_key=os.urandom(24)

try:
    conn=mysql.connector.connect(host="localhost",user="root",password="password@73",database="flaskdb")
except:
    print("Error:404.....Not Found")

cursor=conn.cursor()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    else:
        return render_template('index.html')
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/login_validation', methods=['GET','POST'])
def login_validation():
        email=request.form.get('email')
        password=request.form.get('password')

        cursor.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
        users=cursor.fetchall()

        if len(users)>0:
            session['user_id']=users[0][0]
            return redirect(url_for('home'))
        return redirect(url_for('register'))





@app.route('/new_user',methods=['POST'])
def new_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upass')
    mobile=request.form.get('umob')

    cursor.execute("""INSERT INTO `register` (`name`,`email`,`password`,`mobile no`) VALUES ('{}','{}','{}','{}') """.format(name,email,password,mobile))
    conn.commit()
    cursor.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}'""".format(email))

    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, json, request,redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session

mysql = MySQL()
app = Flask(__name__)
app.secret_key = '1111'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'employee'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')
	
@app.route('/login')
def login():
    return render_template('login.html')
	
@app.route('/signup')
def signup():
    return render_template('signup.html')
	
if __name__ == "__main__":
    app.run(port=5002)
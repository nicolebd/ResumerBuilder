from flask import Flask, render_template, json, request,redirect
import MySQLdb
from werkzeug import generate_password_hash, check_password_hash
from flask import session

#mysql = MySQL()
app = Flask(__name__)
app.secret_key = '1111'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'employee'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')
	
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/editcreate')
def editcreate():
    return render_template('editcreate.html')

@app.route('/home')
def emphome():
	return render_template('emphome.html')
	
@app.route('/signup')
def signup():
    return render_template('signup.html')
	
@app.route('/signout')
def signout():
    session.pop('user',None)
    return redirect('/')
	
@app.route('/register', methods=['POST'])
def registerUser():
	_name = request.form['user']
	_pass = request.form['pass']
	
	conn = MySQLdb.connect(host="localhost",user="root",
                  passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Connection successful"
	try:
		cursor.execute("select max(emp_id) from emp_login_details;")
		data = cursor.fetchall()
		_id = data[0][0]+1
		_x=0;
		cursor.close()
		cursor = conn.cursor()
		cursor.execute("select * from emp_login_details where emp_username ='%s';"%(_name))
		data = cursor.fetchall()
		if len(data) == 0:
			cursor.close()
			cursor = conn.cursor()
			cursor.execute("insert into emp_login_details values (%s,'%s','%s',%s);"%(_id,_name,_pass,_x))
			data = cursor.fetchall()
			if len(data) == 0:
				conn.commit()
				cursor.close()
				return redirect('/login')
		else:
			print 'Existing User'
	except Exception as e:
		print 'Error:'+str(e)
	finally:
		conn.close()
		
@app.route('/validate', methods=['POST'])
def validUser():
	_user = request.form['user']
	_pass = request.form['pass']
	
	conn = MySQLdb.connect(host="localhost",user="root",
                  passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Connection successful"
	try:
		cursor.execute("select * from emp_login_details where emp_username='%s';"%(_user))
		data = cursor.fetchall()
		x=data[0][0]
		print str(data[0][1])
		if str(data[0][2])==_pass:
			session['user'] = data[0][0]
			return render_template('emphome.html')
		else:
			print 'Wrong Password'
	except Exception as e:
		print 'No such user exists'
	finally:
		cursor.close()
		conn.close()
	
@app.route('/enterdetails', methods=['POST'])
def enter_details():
	try:
		if session.get('user'):
			_user = session.get('user')
			_empname=request.form['emp_name']
			_email=request.form['email']
			print _email
			_phone=request.form['phone']
			print _phone
			_address=request.form['address']
			_country=request.form['country']
			_state=request.form['state']
			_pincode=request.form['pin']
			_dob=request.form['dob']
			_gender=request.form['gender']
			_linkedin=request.form['linkedin']
			_github=request.form['github']
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			cursor = conn.cursor()
			print "Connection successful"
			print _user
			cursor.execute("insert into emp_personal values (%s,'%s','%s',%s,'%s','%s','%s',%s,'%s','%s','%s','%s');"%(_user,_empname,_email,_phone,_address,_country,_state,_pincode,_dob,_gender,_linkedin,_github))
			data = cursor.fetchall() 
			if len(data) is 0:
				conn.commit()
				return redirect('/home')
			else:
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:   
		cursor.close()
		conn.close()    
	
if __name__ == "__main__":
    app.run(port=5002)

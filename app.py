from flask import Flask, render_template, json, request,redirect
import MySQLdb
import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask import session
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import webbrowser

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

@app.route('/personal')
def editcreatep():
	if session.get('user'):
		conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
		print "Personal:Connection successful"
		try:
			_user=session.get('user')
			cursor = conn.cursor()
			cursor.execute("select * from emp_personal where emp_id=%s;"%(_user))
			data = cursor.fetchall()
			print data
			return render_template('editcreatepersonal.html',data=data,len=len(data))
		except Exception as e:
			return render_template('error.html',error = str(e))
		finally:
			cursor.close()
			conn.close()
	else:
		return render_template('error.html',error = 'Unauthorised user')
	
@app.route('/educational')
def editcreatee():
	if session.get('user'):
		conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
		print "Education:Connection successful"
		try:
			_user=session.get('user')
			cursor = conn.cursor()
			cursor.execute("select * from education,institutes where education.emp_id ='%s' and education.inst_id=institutes.inst_id;"%(_user))
			data = cursor.fetchall()
			return render_template('editcreateedu.html',data=data,len=len(data))
		except Exception as e:
			return render_template('error.html',error = str(e))
		finally:   
			cursor.close()
			conn.close()
	else:
		return render_template('error.html',error = 'Unauthorised user')
	
@app.route('/experience')
def editcreateex():
	if session.get('user'):
		conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
		print "Experience:Connection successful"
		try:
			_user=session.get('user')
			cursor = conn.cursor()
			cursor.execute("select * from experience where emp_id ='%s';"%(_user))
			data = cursor.fetchall()
			cursor.close()
			return render_template('editcreateexp.html',data=data,len=len(data))
		except Exception as e:
			return render_template('error.html',error = str(e))
		finally:   
			conn.close()
	else:
		return render_template('error.html',error = 'Unauthorised user')
	
@app.route('/skill')
def editcreatesk():
	if session.get('user'):
		conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
		print "Experience:Connection successful"
		try:
			_user=session.get('user')
			cursor = conn.cursor()
			cursor.execute("select * from skill where emp_id ='%s';"%(_user))
			data = cursor.fetchall()
			cursor.close()
			return render_template('editcreateskill.html',data=data,len=len(data))
		except Exception as e:
			return render_template('error.html',error = str(e))
		finally:   
			conn.close()
	else:
		return render_template('error.html',error = 'Unauthorised user')
		
@app.route('/setAdmin')
def setAdmin():
	if session.get('user'):
		_user=session.get('user')
		conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
		print "Set Admin:Connection successful"
		try:
			cursor = conn.cursor()
			cursor.execute("select * from emp_login_details where emp_id<>%s;"%(_user))
			data = cursor.fetchall()
			cursor.close()
			return render_template('setadmin.html',data=data,len=len(data))
		except Exception as e:
			return render_template('error.html',error = str(e))
		finally:   
			conn.close()
	else:
		return render_template('error.html',error = 'Unauthorised user')
	
@app.route('/searchEmp')
def searchEmp():
	return render_template('adminsrc.html',data="",len=0,skill="")

@app.route('/home')
def emphome():
	return render_template('emphome.html')
	
@app.route('/Ahome')
def adminhome():
	return render_template('adminhome.html')
	
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
	
	conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Register:Connection successful"
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
			return render_template('error.html',error = "Existing User")
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		conn.close()
		
@app.route('/validate', methods=['POST'])
def validUser():
	_user = request.form['user']
	_pass = request.form['pass']
	
	conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Validate:Connection successful"
	try:
		cursor.execute("select * from emp_login_details where emp_username='%s';"%(_user))
		data = cursor.fetchall()
		print data
		x=data[0][0]
		print str(data[0][1])
		if str(data[0][2])==_pass:
			session['user'] = data[0][0]
			if(data[0][3]==0):
				return redirect('/home')
			else:
				return redirect('/Ahome')
		else:
			return render_template('error.html',error = "Wrong Password")
	except Exception as e:
		return render_template('error.html',error = "User does not exist")
	finally:
		cursor.close()
		conn.close()
	
@app.route('/personal_details', methods=['POST'])
def enter_details_personal():
	try:
		if session.get('user'):
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			cursor = conn.cursor()
			print "Personal Details:Connection successful"
			_user = session.get('user')
			_dob=request.form['dob']
			_empname=request.form['emp_name']			
			_gender=request.form['gender']
			_email=request.form['email']
			_phone=request.form['phone']
			_address=request.form['address']
			_country=request.form['country']
			_state=request.form['state']
			_pincode=request.form['pin']			
			_linkedin=request.form['linkedin']
			_github=request.form['github']
			
			cursor.execute("insert into emp_personal values (%s,'%s','%s',%s,'%s','%s','%s',%s,'%s','%s','%s','%s');"%(_user,_empname,_email,_phone,_address,_country,_state,_pincode,_dob,_gender,_linkedin,_github))
			data = cursor.fetchall() 
			if len(data) is 0:
				conn.commit()
				return redirect('/educational')
			else:
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:   
		cursor.close()
		conn.close()

@app.route('/updt_personal_details', methods=['POST'])
def updt_details_personal():
	try:
		if session.get('user'):
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			print "Personal Details Updt:Connection successful"
			_user = session.get('user')
			_dob=request.form['dob']
			_empname=request.form['emp_name']

			_gender=request.form['gender']
			#_gender1=request.form['gender1']
			#_gender2=request.form['gender2']
			print _gender
			#print _gender1
			#print _gender2
			_email=request.form['email']
			_phone=request.form['phone']
			_address=request.form['address']

			_country=request.form['country']
			_state=request.form['state']
			_pincode=request.form['pin']			
			_linkedin=request.form['linkedin']
			_github=request.form['github']

			cursor = conn.cursor()
			cursor.execute("update emp_personal set emp_name='%s', email='%s', phone=%s, address='%s', country='%s', state='%s', pin=%s, dob='%s', gender='%s', linkedin='%s', github='%s' where emp_id=%s;"%(_empname,_email,_phone,_address,_country,_state,_pincode,_dob,_gender,_linkedin,_github,_user))
			data = cursor.fetchall()
			cursor.close()
			if len(data) is 0:
				conn.commit()
				return redirect('/educational')
			else:
				return render_template('error.html',error = 'An error occurred!')
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:   
		conn.close()

@app.route('/edu_details', methods=['POST'])
def enter_details_edu():
	try:
		if session.get('user'):
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			cursor = conn.cursor()
			print "Edu Details:Connection successful"
			_user = session.get('user')
			i=0
			while request.form['inst'+str((i+1))]:
				i=i+1
				_inst=request.form['inst'+str(i)]
				_level=request.form['level'+str(i)]			
				_yop=request.form['yop'+str(i)]
				_marks=request.form['marks'+str(i)]
				print _user
				print _inst
				print _level
				print _yop
				print _marks
				cursor = conn.cursor()
				cursor.execute("select inst_id from institutes where inst_name ='%s';"%(_inst))
				institute = cursor.fetchall()
				cursor.close()
				if len(institute) == 0:
					cursor = conn.cursor()
					cursor.execute("insert into institutes (`inst_name`) values ('%s');"%(_inst))
					cursor.close()
					conn.commit()
					cursor = conn.cursor()
					cursor.execute("select inst_id from institutes where inst_name ='%s';"%(_inst))
					institute=	cursor.fetchall()
					cursor.close()
				_num=institute[0][0]
				cursor = conn.cursor()
				cursor.execute("insert into education values (%s,%s,'%s',%s,%s);"%(_user,_num,_level,_yop,_marks))
				institute = cursor.fetchall()
				cursor.close()
				if len(institute) is 0:
					conn.commit()
					return redirect('/educational')
				else:
					return render_template('error.html',error = 'An error occurred!')
					
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:   
		conn.close()

@app.route('/edu_details_remove', methods=['POST'])
def remove_details_edu():
	_user = session.get('user')
	_inst = request.form['inst_id']
	_lvl = request.form['level']
     
	conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Edu Details Rev:Connection successful"
	try:
			cursor.execute("delete from education where emp_id=%s and inst_id=%s and level='%s';"%(_user,_inst,_lvl))
			data = cursor.fetchall()
             
			if len(data) == 0:
				conn.commit()
				cursor.close()
				return redirect('/educational')
	except Exception as e:
		return render_template('error.html',error = e)
	finally:
		conn.close()
		
@app.route('/exp_details', methods=['POST'])
def enter_details_exp():
	try:
		if session.get('user'):
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			cursor = conn.cursor()
			print "Exp Details:Connection successful"
			_user = session.get('user')
			i=0
			while request.form['exp'+str((i+1))]:
				i=i+1
				_exp=request.form['exp'+str(i)]
				_desig=request.form['desig'+str(i)]			
				_start=request.form['start'+str(i)]
				_end=request.form['end'+str(i)]
				print _user
				print _exp
				print _desig
				print _start
				print _end
				cursor = conn.cursor()
				cursor.execute("insert into experience values (%s,'%s','%s','%s','%s');"%(_user,_desig,_exp,_start,_end))
				data = cursor.fetchall()
				cursor.close()
				if len(data) is 0:
					conn.commit()
					return redirect('/experience')
				else:
					return render_template('error.html',error = 'An error occurred!')
					
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:   
		conn.close()

@app.route('/exp_details_remove', methods=['POST'])
def remove_details_exp():
	_user = session.get('user')
	_desig = request.form['desig']
	_exp = request.form['exp']
     
	conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Exp Details Rev:Connection successful"
	try:
			cursor.execute("delete from experience where emp_id=%s and designation='%s' and organisation='%s';"%(_user,_desig,_exp))
			data = cursor.fetchall()
             
			if len(data) == 0:
				conn.commit()
				cursor.close()
				return redirect('/experience')
	except Exception as e:
		return render_template('error.html',error = e)
	finally:
		conn.close()
		
@app.route('/skill_details', methods=['POST'])
def enter_details_skill():
	try:
		if session.get('user'):
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			cursor = conn.cursor()
			print "Skill Details:Connection successful"
			_user = session.get('user')
			i=0
			while request.form['skill'+str((i+1))]:
				i=i+1
				_skill=request.form['skill'+str(i)]
				_lvl=request.form['sk_level'+str(i)]			
				print _user
				print _skill
				print _lvl
				cursor = conn.cursor()
				cursor.execute("insert into skill values (%s,'%s','%s');"%(_user,_skill,_lvl))
				data = cursor.fetchall()
				cursor.close()
				if len(data) is 0:
					conn.commit()
					return redirect('/skill')
				else:
					return render_template('error.html',error = 'An error occurred!')
					
		else:
			return render_template('error.html',error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:   
		conn.close()

@app.route('/skill_details_remove', methods=['POST'])
def remove_details_skill():
	_user = session.get('user')
	_skill = request.form['skill']
	_lvl = request.form['sk_level']
     
	conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	print "Skill Details Rev:Connection successful"
	try:
			cursor.execute("delete from skill where emp_id=%s and skills='%s' and level='%s';"%(_user,_skill,_lvl))
			data = cursor.fetchall()
             
			if len(data) == 0:
				conn.commit()
				cursor.close()
				return redirect('/skill')
	except Exception as e:
		return render_template('error.html',error = e)
	finally:
		conn.close()
		
@app.route('/updt_admin_details', methods=['post'])
def updt_admin_details():
	if session.get('user'):
		try:
			conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
			print "Update Admin:Connection successful"
			_empid=request.form['empid']
			cursor=conn.cursor()
			cursor.execute("select * from emp_login_details where emp_id=%s;"%(_empid))
			data=cursor.fetchall()
			cursor.close()
			if data[0][3]==0:
				_adm=request.form['admin']
				if _adm=="yes":
					cursor=conn.cursor()
					cursor.execute("update emp_login_details set admin_perm=1 where emp_id=%s;"%(_empid))
					data=cursor.fetchall()
					if len(data)==0:
						conn.commit()
						cursor.close()
						return redirect('/setAdmin')
			else:
				_adm=request.form['admin1']
				if _adm=="no":
					cursor=conn.cursor()
					cursor.execute("update emp_login_details set admin_perm=0 where emp_id=%s;"%(_empid))
					data=cursor.fetchall()
					if len(data)==0:
						conn.commit()
						cursor.close()
						return redirect('/setAdmin')
		except Exception as e:
			return render_template('error.html',error = e)
		finally:
			conn.close()
	else:
		return render_template('error.html',error = 'Unauthorized Access')
			
@app.route('/emp_seach', methods=['post'])
def emp_search():
	if session.get('user'):
		try:
			print "Update Admin:Connection successful"
			_i=0
			_s=""
			_st="SEARCH RESULTS FOR"
			while request.form['skill'+str(_i+1)]:
				_i=_i+1
				_skill=request.form['skill'+str(_i)]
				_lvl=request.form['sk_level'+str(_i)]
				_st=_st+(";SKILL: %s, LEVEL: %s"%(_skill,_lvl))
				_s=_s + (" INNER JOIN skill s%s ON s%s.skills='%s' AND s%s.level='%s'"%(_i,_i,_skill,_i,_lvl))
		except (LookupError):
			try:
				conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
				cursor=conn.cursor()
				cursor.execute("SELECT DISTINCT s.emp_id FROM skill s %s;"%(_s))
				_data=cursor.fetchall()
				cursor.close()
				if len(_data)==0:
					return render_template('adminsrc.html',_data="",len=0,skill=_st)
				else:
					_x=""
					for i in range(len(_data)):
						_x=_x+(",%s"%(_data[i][0]))
					cursor=conn.cursor()
					cursor.execute("SELECT * FROM emp_personal where emp_id in (%s);"%(_x[1:]))
					data=cursor.fetchall()
					cursor.close()
					return render_template('adminsrc.html',data=data,len=len(data),skill=_st)
			except Exception as e:
				return render_template('error.html',error = e)
			finally:
				conn.close()
		except Exception as e:
			return render_template('error.html',error = e)
	else:
		return render_template('error.html',error = 'Unauthorized Access')


num=0
@app.route('/view')
def pdfview():
	global num
	num=num+1
	print num
	conn = MySQLdb.connect(host="localhost",user="root",passwd="1234",db="employee",port=3306)
	cursor = conn.cursor()
	#c=canvas.Canvas("hello%s.pdf"%num)
	doc=SimpleDocTemplate("hello%s.pdf"%num, rightMargin=72, leftMargin=72,topMargin=72,bottomMargin=60)
	#c.setFont('Helvetica',28)
	#c.setLineWidth(.5)
	#c.drawString(240,750,'RESUME')
	#c.line(240,747,360,747)

	Story=[]
	styles=getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Center',alignment=TA_CENTER))
	styles.add(ParagraphStyle(name='Left',alignment=TA_LEFT))
	styles.add(ParagraphStyle(name='Right',alignment=TA_RIGHT))
	styles.add(ParagraphStyle(name='Justify',alignment=TA_JUSTIFY))

	spacerp=Spacer(0,0.5*inch)
	spacer=Spacer(0,0.1*inch)
	ptext='<font size=30>RESUME</font>'
	Story.append(Paragraph(ptext,styles["Center"]))
	Story.append(spacerp)

	_user = session.get('user')
	cursor.execute("select * from emp_personal where emp_id=%s;"%(_user))
	data=cursor.fetchall()
	print data
	ptext='<font size=24>I. Personal Details </font>'
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(Spacer(0,0.3*inch))
	ptext='<font size=18>Name: </font><font size=16>%s</font>'%(data[0][1])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Email: </font><font size=16>%s</font>'%(data[0][2])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Phone: </font><font size=16>%s</font>'%(data[0][3])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Address: </font><font size=16>%s</font>'%(data[0][4])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>State: </font><font size=16>%s</font>'%(data[0][6])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Country: </font><font size=16>%s</font>'%(data[0][5])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Pincode: </font><font size=16>%s</font>'%(data[0][7])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Date Of Birth: </font><font size=16>%s</font>'%(data[0][8])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Gender: </font><font size=16>%s</font>'%(data[0][9])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>LinkedIn: </font><font size=16>%s</font>'%(data[0][10])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacer)
	ptext='<font size=18>Github: </font><font size=16>%s</font>'%(data[0][11])
	Story.append(Paragraph(ptext,styles["Justify"]))
	Story.append(spacerp)

	cursor.execute("select * from education,institutes where education.emp_id ='%s' and education.inst_id=institutes.inst_id;"%(_user))
	data = cursor.fetchall()
	print data
	length=len(data)
	print length
	ptext='<font size=24>II.Educational Details </font>'
	Story.append(Paragraph(ptext,styles["Justify"]))
	i=0
	while(i<length):
		Story.append(Spacer(0,0.3*inch))
		ptext='<font size=18>Institution: </font><font size=16>%s</font>'%(data[i][6])
		Story.append(Paragraph(ptext,styles["Justify"]))
		Story.append(spacer)
		ptext='<font size=18>Level of Education : </font><font size=16>%s</font>'%(data[i][2])
		Story.append(Paragraph(ptext,styles["Justify"]))
		Story.append(spacer)
		ptext='<font size=18>Year of Completion : </font><font size=16>%s</font><font size=18>&nbsp;&nbsp;&nbsp;&nbsp;GPA/Percentage: </font><font size=16>%s</font>'%(data[i][3],data[i][4])
		Story.append(Paragraph(ptext,styles["Justify"]))
		i=i+1
	Story.append(spacerp)
	cursor.execute("select * from skill where emp_id ='%s';"%(_user))
	data = cursor.fetchall()
	print data
	length=len(data)
	print length
	ptext='<font size=24>III.Skill Details </font>'
	Story.append(Paragraph(ptext,styles["Justify"]))
	i=0
	while(i<length):
		Story.append(Spacer(0,0.3*inch))
		ptext='<font size=18>Skill: </font><font size=16>%s</font>'%(data[i][1])
		Story.append(Paragraph(ptext,styles["Justify"]))
		Story.append(spacer)
		ptext='<font size=18>Level of skill achieved : </font><font size=16>%s</font>'%(data[i][2])
		Story.append(Paragraph(ptext,styles["Justify"]))
		i=i+1

	Story.append(spacerp)
	cursor.execute("select * from experience where emp_id ='%s';"%(_user))
	data = cursor.fetchall()
	print data
	length=len(data)
	print length
	ptext='<font size=24>IV.Experience Details </font>'
	Story.append(Paragraph(ptext,styles["Justify"]))
	i=0
	while(i<length):
		Story.append(Spacer(0,0.3*inch))
		ptext='<font size=18>Organisation: </font><font size=16>%s</font>'%(data[i][2])
		Story.append(Paragraph(ptext,styles["Justify"]))
		Story.append(spacer)
		ptext='<font size=18>Designation : </font><font size=16>%s</font>'%(data[i][1])
		Story.append(Paragraph(ptext,styles["Justify"]))
		Story.append(spacer)
		ptext='<font size=18>Date Of Joining: </font><font size=16>%s</font>'%(data[i][3])
		Story.append(Paragraph(ptext,styles["Justify"]))
		Story.append(spacer)
		ptext='<font size=18>Date of Termination: </font><font size=16>%s</font>'%(data[i][4])
		Story.append(Paragraph(ptext,styles["Justify"]))
		i=i+1
	Story.append(Spacer(0,1.1*inch))

	now=datetime.datetime.now()
	ptext='<font size=18>Date: %s</font>'%str(now)[:10]
	cursor.execute("select emp_name from emp_personal where emp_id=%s;"%(_user))
	data=cursor.fetchall()
	print data 
	ptext1='<font size=18>Signed By: %s</font>'%data[0][0]
	tbl_data=[
				[Paragraph(ptext,styles["Left"]),Paragraph(ptext1,styles["Right"])]
			]
	tbl=Table(tbl_data)
	Story.append(tbl)

	doc.build(Story)
	conn.close()
	url="hello%s.pdf"%num
	webbrowser.open(url,new=2)
	return redirect('/home')

if __name__ == "__main__":
    app.run(port=5002)
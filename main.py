
from flask import Flask, render_template,request
from flask_mysqldb import MySQL
from datetime import datetime
import time


app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='test'

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST' and 'userid' in request.form and 'password' in request.form:
        userid = request.form['userid']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT name FROM login WHERE userid = %s AND password = %s', (userid, password))
        # Fetch one record and return result
        account = cur.fetchone()
        #print(account)
        return'done'
    if request.method == 'POST' and 'userid' in request.form and 'name' in request.form and 'password' in request.form:
        userDetails = request.form
        userid = userDetails['userid']
        name = userDetails['name']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT into login (userid,name,password) values (%s,%s,%s)", (userid, name, password))
        mysql.connection.commit()
        cur.close()
        return 'done'
    return render_template('index.html')


@app.route('/model',methods=['POST','GET'])
def home():
        if request.method == 'POST' and 'From_Date' in request.form and 'From_Time' in request.form and 'To_Date' in request.form and 'To_Time' in request.form:
            userDetails = request.form
            From_Date = str(userDetails['From_Date'])
            From_Time = str(userDetails['From_Time'])
            To_Date = str(userDetails['To_Date'])
            To_Time = str(userDetails['To_Time'])
            #a=%H
            if From_Time and To_Time:
                s1Time = datetime.strptime(From_Date, "%Y-%m-%d")
                print(s1Time.timestamp())
                s2Time = datetime.strptime(To_Time, "%H:%M")
                print(s2Time.timestamp())
                #program = datetime.timedelta(s1Time)
                #program2 = datetime.timedelta(s2Time)
                #deltaInMinutes = (program2-program)
                #print (deltaInMinutes)
           # print('To_Time',%H'')
           # FMT = "%H:%M"
            #print(userDetails['To_Time']-userDetails['From_Time'])
            #tdelta = datetime.strptime(To_Time, FMT) - datetime.strptime(From_Time, FMT)
            #print(tdelta)
            cur = mysql.connection.cursor()
            a = cur.execute(
                'SELECT * FROM car where car.id not in (SELECT car_id From book_car where To_Date >= %s and (To_Time <= %s OR From_Time >= %s) AND From_Date >= %s )',
                (To_Date, To_Time, From_Time, From_Date,))
            #print("value ofd a ",a)
            if a>0:
                account = cur.fetchall()
                #print(account)
                #print (account)
                #return account
                return render_template('model.html', data=account)

        return render_template('model.html')


@app.route('/form',methods=['GET','POST'])
def home1():
    if request.method == 'POST' and 'userid' in request.form:
        userid = request.form['userid']
        cur = mysql.connection.cursor()
        a=cur.execute('SELECT * FROM book_car WHERE userid = %s', (userid,))
        # Fetch one record and return result
        if a > 0:
            account = cur.fetchall()
            print(account)
            # print (account)
            # return account
            return render_template('form.html', data=account)
    return render_template('form.html')

@app.route('/add',methods=['GET','POST'])
def home2():
    if request.method == 'POST' :
                carLicenseNumber = request.form['carLicenseNumber']
                Manufacturer = request.form['Manufacturer']
                Model = request.form['Model']
                Base_price = request.form['Base_price']
                PPH = request.form['PPH']
                Security_deposit=request.form['Security_deposit']
                cur = mysql.connection.cursor()
                cur.execute("INSERT into car (carLicenseNumber,Manufacturer,Model,base-price,PPH,Security-deposit) values (%s,%s,%s,%s,%s,%s)",(carLicenseNumber,Manufacturer,Model,Base_price,PPH,Security_deposit))
                mysql.connection.commit()
                cur.close()
                return 'done'
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)

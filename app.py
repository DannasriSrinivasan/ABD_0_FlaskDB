from distutils.log import debug
from flask import Flask, render_template, request
import pyodbc


connecttosql = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', host='danna.database.windows.net', database='datadxs',
                      trusted_connection='no', user='dxsdb', password='Happyme@1')

cursor = connecttosql.cursor()


app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/updateComment')
def updateComment():
    return render_template('updateComment.html')

@app.route('/searchClassRange')
def searchClassRange():
    return render_template('searchClassRange.html')

@app.route('/table', methods=['POST','GET'])
def viewEntity():
    cursor.execute("Select * from data")
    result = cursor.fetchall()
    return render_template("viewEntity.html",rows = result)


@app.route('/update', methods=['POST','GET'])
def update():
    sName = request.form['searchName']
    uComment = request.form['comments']
    cursor.execute("UPDATE data set comments = '"+uComment+"' where name = '"+sName+"'")
    cursor.execute("Select * from data where name = '"+sName+"'")
    result = cursor.fetchall()
    return render_template("viewEntity.html",rows = result)

@app.route('/search', methods=['POST','GET'])
def search():
    start= request.form['start']
    end= request.form['end']
    cursor.execute("Select * from data WHERE class BETWEEN "+start+" AND "+end+" and class is not null")
    result = cursor.fetchall()
    return render_template("viewEntity.html",rows = result)

if __name__ == '__main__':
    app.run(debug = True)
    
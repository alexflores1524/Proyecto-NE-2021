from flask import Flask,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "gespres"

app.config['MYSQL_HOST']= '127.0.0.1'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'gespres_flask'
mysql = MySQL(app) 

@app.route('/')
def login():
    if 'usuarioIngresado' in session:
        return render_template('Inicio.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')

@app.route('/login_autentication', methods=['POST','GET'])
def login_autentication():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT * FROM usuarios WHERE usuario = %s", [user])
        userResult = mycursor.fetchall()
        mycursor.close()
        if userResult:
            if password == userResult[0][2]:
                session['usuarioIngresado'] = request.form['user']
                return render_template('Inicio.html', usuarioGlobal = session['usuarioIngresado'])
        else:
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('usuarioIngresado',None)
    return redirect(url_for('login'))

@app.route('/Inicio.html')
def inicio():
    if 'usuarioIngresado' in session:
        return render_template('Inicio.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')

@app.route('/clientes.html')
def clientes():
    if 'usuarioIngresado' in session:
        return render_template('clientes.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')
    
@app.route('/prestamos.html')
def prestamos():
    if 'usuarioIngresado' in session:
        return render_template('prestamos.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')    

@app.route('/cobros.html')
def cobros():
    if 'usuarioIngresado' in session:
        return render_template('cobros.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')  

@app.route('/atrasos.html')
def atrasos():
    if 'usuarioIngresado' in session:
        return render_template('atrasos.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')
    

@app.route('/usuarios.html')
def usuarios():
    if 'usuarioIngresado' in session:
        return render_template('usuarios.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')   

@app.route('/reportes.html')
def reportes():
    if 'usuarioIngresado' in session:
        return render_template('usuarios.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
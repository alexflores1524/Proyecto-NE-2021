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

#CLIENTES
@app.route('/clientes.html', methods=['POST','GET'])
def clientes():
    if 'usuarioIngresado' in session:
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT * FROM clientes WHERE is_active = 1")
        clienteResult = mycursor.fetchall()
        mycursor.close()
        return render_template('clientes.html', usuarioGlobal = session['usuarioIngresado'], clientes = clienteResult)
    else:
        return render_template('/login.html')

@app.route('/registrar_clientes', methods=['POST','GET'])
def registrar_clientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        correo = request.form['correo']
        mycursor = mysql.connection.cursor()
        mycursor.execute("INSERT INTO clientes (nombre, apellido, fecha_nacimiento, telefono, email) VALUES (%s, %s, %s, %s, %s)",(nombre, apellido, fecha, telefono, correo))
        mysql.connection.commit()
        mycursor.close()
        print(nombre + apellido + fecha + telefono + correo)
        return redirect(url_for('clientes'))
    
@app.route('/obtener_cliente/<id>', methods=['POST','GET'])
def obtener_cliente(id):
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM clientes WHERE idCliente = %s", (id))
    cliente = mycursor.fetchall()
    mycursor.close()
    return render_template('clientes_editar.html', cliente = cliente[0])

@app.route('/editar_clientes/<id>', methods=['POST'])
def editar_clientes(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        correo = request.form['correo']
        mycursor = mysql.connection.cursor()
        mycursor.execute("""UPDATE clientes
                        SET 
                        nombre = %s,
                        apellido = %s,
                        fecha_nacimiento = %s,
                        telefono = %s,
                        email = %s               
                        WHERE idCliente = %s""", (nombre, apellido, fecha, telefono, correo, id))
        mysql.connection.commit()
        mycursor.close()
        return redirect(url_for('clientes'))


@app.route('/borrar_clientes/<id>')
def borrar_clientes(id):
    mycursor = mysql.connection.cursor()
    mycursor.execute("UPDATE clientes SET is_active = 0 WHERE clientes.idCliente = %s", (id))
    mysql.connection.commit()
    mycursor.close()
    return redirect(url_for('clientes'))

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
    
#USUARIOS
@app.route('/usuarios.html')
def usuarios():
    if 'usuarioIngresado' in session:
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT * FROM usuarios WHERE is_active = 1")
        usuarioResult = mycursor.fetchall()
        print (usuarioResult)
        mycursor.close()
        return render_template('usuarios.html', usuarioGlobal = session['usuarioIngresado'], usuarios = usuarioResult)
    else:
        return render_template('/login.html') 


@app.route('/registrar_usuarios', methods=['POST','GET'])
def registrar_usuarios():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        mycursor = mysql.connection.cursor()
        mycursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",(usuario, password))
        mysql.connection.commit()
        mycursor.close()
        print(usuario + password)
        return redirect(url_for('usuarios'))
    
@app.route('/obtener_usuario/<id>', methods=['POST','GET'])
def obtener_usuario(id):
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM usuarios WHERE idUser = %s", (id))
    usuario = mycursor.fetchall()
    mycursor.close()
    return render_template('usuario_editar.html', usuario = usuario[0])
    
@app.route('/editar_usuarios/<id>', methods=['POST'])
def editar_usuarios(id):
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        mycursor = mysql.connection.cursor()
        mycursor.execute("""UPDATE usuarios
                        SET 
                        usuario = %s,
                        password = %s           
                        WHERE idUser = %s""", (usuario, password,id))
        mysql.connection.commit()
        mycursor.close()
        return redirect(url_for('usuarios'))

@app.route('/borrar_usuario/<id>')
def borrar_usuarios(id):
    mycursor = mysql.connection.cursor()
    mycursor.execute("UPDATE usuarios SET is_active = 0 WHERE usuarios.idUser = %s", (id))
    mysql.connection.commit()
    mycursor.close()
    return redirect(url_for('usuarios'))


@app.route('/reportes.html')
def reportes():
    if 'usuarioIngresado' in session:
        return render_template('usuarios.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)


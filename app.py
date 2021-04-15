from flask import Flask,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "gespres"

app.config['MYSQL_HOST']= '127.0.0.1'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'gespres_flask'
mysql = MySQL(app) 

#**************************LOGIN**************************

@app.route('/')
def login():
    if 'usuarioIngresado' in session:
        return redirect(url_for('inicio'))
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
        print(userResult)
        mycursor.close()
        if userResult:
            if password == userResult[0][2]:
                session['usuarioIngresado'] = request.form['user']
                return redirect(url_for('inicio'))
                #return render_template('Inicio.html', usuarioGlobal = session['usuarioIngresado'])
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
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT COUNT(nombre) FROM clientes WHERE is_active = 1")
        cliente = mycursor.fetchall()
        mycursor.execute("SELECT COUNT(idPrestamo) FROM prestamos WHERE is_active = 1")
        prestamo = mycursor.fetchall()
        mycursor.execute("SELECT SUM(cantidad) FROM cobros")
        cobro = mycursor.fetchall()
        mycursor.execute("SELECT SUM(restante) FROM prestamos")
        restante = mycursor.fetchall()
        mycursor.close()
        if cliente:
            return render_template('inicio.html', usuarioGlobal = session['usuarioIngresado'], cliente = cliente[0],prestamo = prestamo[0], cobro = cobro[0], restante = restante[0])
        else:
            cliente = ('','No existente','No existente')
            return render_template('inicio.html', usuarioGlobal = session['usuarioIngresado'], cliente = cliente, prestamos = prestamoResult)
    else:
        return render_template('/login.html')

#************************************************************

#**************************CLIENTES**************************
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

#*************************************************************
#**************************PRESTAMOS**************************
@app.route('/prestamos.html')
def prestamos():
    if 'usuarioIngresado' in session:
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT * FROM prestamos WHERE is_active = 1")
        prestamoResult = mycursor.fetchall()
        mycursor.close()
        cliente = ('','','','','')
        return render_template('prestamos.html', usuarioGlobal = session['usuarioIngresado'], cliente = cliente, prestamos = prestamoResult)
    else:
        return render_template('/login.html')    

@app.route('/buscar_cliente_prestamos', methods=['POST','GET'])
def buscar_cliente_prestamos():
    if request.method == 'POST':
        id = request.form['idCliente']
        mycursor = mysql.connection.cursor()
        mycursor.execute("SELECT * FROM clientes WHERE idCliente = %s AND is_active = 1", (id))
        cliente = mycursor.fetchall()
        mycursor.execute("SELECT * FROM prestamos WHERE is_active = 1")
        prestamoResult = mycursor.fetchall()
        mycursor.close()
        if cliente:
            return render_template('prestamos.html', usuarioGlobal = session['usuarioIngresado'], cliente = cliente[0], prestamos = prestamoResult)
        else:
            cliente = ('','No existente','No existente')
            return render_template('prestamos.html', usuarioGlobal = session['usuarioIngresado'], cliente = cliente, prestamos = prestamoResult)

@app.route('/registrar_prestamos', methods=['POST','GET'])
def registrar_prestamos():
    if request.method == 'POST':
        idCliente = request.form['idCliente']
        cantidadPrestamo = request.form['cantidadPrestamo']
        fechaPrestamo = request.form['fechaPrestamo']
        mycursor = mysql.connection.cursor()
        mycursor.execute("INSERT INTO prestamos (idCliente, cantidad, fecha_prestamo, abono, restante) VALUES (%s, %s, %s, 0, %s)",(idCliente, cantidadPrestamo, fechaPrestamo, cantidadPrestamo))
        mysql.connection.commit()
        mycursor.close()
        return redirect(url_for('prestamos'))

@app.route('/registrar_plazos', methods=['POST','GET'])
def registrar_plazos():
    if request.method == 'POST':
        idPrestamo = request.form['idPrestamo']
        subtotal = request.form['subtotal']
        fechaPlazo = request.form['fechaPlazo']
        mycursor = mysql.connection.cursor()
        mycursor.execute("INSERT INTO plazos (idPrestamo, subtotal, fecha_pago) VALUES (%s, %s, %s)",(idPrestamo, subtotal, fechaPlazo))
        mysql.connection.commit()
        mycursor.close()
        return redirect(url_for('prestamos'))

#**************************COBROS**************************

@app.route('/cobros.html')
def cobros():
    if 'usuarioIngresado' in session:
        prestamo = ('','','','','','','')
        plazos = ('','','','')
        return render_template('cobros.html', usuarioGlobal = session['usuarioIngresado'], prestamo = prestamo, plazos = plazos)
    else:
        return render_template('/login.html')

@app.route('/buscar_prestamo', methods=['POST','GET'])
def buscar_prestamo():
    if request.method == 'POST':
        id = request.form['idPrestamo']
        mycursor = mysql.connection.cursor()
        mycursor.execute("""SELECT
                                prestamos.idPrestamo,
                                clientes.nombre,
                                clientes.apellido,
                                prestamos.abono,
                                prestamos.restante
                            FROM prestamos
                            INNER JOIN clientes on clientes.idCliente = prestamos.idCliente
                            WHERE prestamos.idPrestamo = %s AND prestamos.is_active = 1""", (id))
        prestamo = mycursor.fetchall()       
        if prestamo:
            mycursor.execute("SELECT * FROM plazos WHERE idPrestamo = %s AND is_active = 1", (id))
            plazos = mycursor.fetchall()
            mycursor.close()
            return render_template('cobros.html', usuarioGlobal = session['usuarioIngresado'], prestamo = prestamo[0], plazos = plazos)
        else:
            mycursor.close()
            plazos = ('','','','')
            prestamo = ('','No existente','No existente','No existente','No existente')
            return render_template('cobros.html', usuarioGlobal = session['usuarioIngresado'], prestamo = prestamo, plazos = plazos)

@app.route('/registrar_cobro', methods=['POST','GET'])
def registrar_cobro():
    if request.method == 'POST':
        idPlazo = request.form['idPlazo']
        fechaPago = request.form['fechaPago']
        monto = float(request.form['monto'])
        mycursor = mysql.connection.cursor()
        
        mycursor.execute("SELECT idPrestamo FROM plazos WHERE idPlazo = %s", [idPlazo])
        plazo = mycursor.fetchall()
        idPrestamo = plazo[0][0]
        mycursor.execute("INSERT INTO cobros (idPrestamo, idPlazo, cantidad, fecha_cobro) VALUES (%s, %s, %s, %s)",(idPrestamo, idPlazo, monto, fechaPago))
        mysql.connection.commit()
        
        mycursor.execute("UPDATE plazos SET is_active = 0 WHERE idPlazo = %s", [idPlazo])
        mysql.connection.commit()
        
        mycursor.execute("SELECT abono,restante FROM prestamos WHERE idPrestamo = %s", [idPrestamo])
        prestamo = mycursor.fetchall()
        abono = prestamo[0][0]
        restante = prestamo[0][1]
        abonoFinal = abono + monto
        restanteFinal = restante - monto
        
        if restanteFinal == 0:
            mycursor.execute("UPDATE prestamos SET is_active = 0, restante = %s, abono = %s WHERE idPrestamo = %s", (restanteFinal, abonoFinal, idPrestamo))
            mysql.connection.commit()
            mycursor.close()
            return redirect(url_for('cobros'))
        else:
            mycursor.execute("UPDATE prestamos SET restante = %s, abono = %s WHERE idPrestamo = %s", (restanteFinal,   abonoFinal, idPrestamo))
            mysql.connection.commit()
            mycursor.close()
            return redirect(url_for('cobros'))

#*************************************************************

#**************************ATRASOS***************************

@app.route('/atrasos.html')
def atrasos():
    if 'usuarioIngresado' in session:
        atrasos = ('','','','','','')
        return render_template('atrasos.html', usuarioGlobal = session['usuarioIngresado'], atrasos = atrasos)
    else:
        return render_template('/login.html')

@app.route('/mostrar_atrasos', methods=['POST','GET'])
def mostrar_atrasos():
    if request.method == 'POST':
        mycursor = mysql.connection.cursor()
        mycursor.execute("""SELECT plazos.idPlazo, clientes.nombre, clientes.apellido, plazos.idPrestamo, plazos.       subtotal, plazos.fecha_pago
                            FROM plazos
                            INNER JOIN prestamos ON prestamos.idPrestamo = plazos.idPrestamo
                            INNER JOIN clientes ON clientes.idCliente = prestamos.idCliente
                            WHERE fecha_pago < CURDATE() AND plazos.is_active = 1
                         """)
        atrasos = mycursor.fetchall()
        mycursor.close()
        if atrasos:
            return render_template('atrasos.html', usuarioGlobal = session['usuarioIngresado'], atrasos = atrasos)
        else:
            return redirect(url_for('atrasos'))
    else:
        return redirect(url_for('atrasos'))

   
#*************************************************************

#**************************USUARIOS**************************
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

#**************************************************************
#****************************REPORTES************************

@app.route('/reportes.html')
def reportes():
    if 'usuarioIngresado' in session:
        return render_template('reportes.html', usuarioGlobal = session['usuarioIngresado'])
    else:
        return render_template('/login.html')

#REPORTE COBROS
@app.route('/reporte_cobros', methods=['POST','GET'])
def reporte_cobros():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            reportes = ('','','','','','','','')
            return render_template('reporte_cobros.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
        else:
            return redirect(url_for('reportes'))
    else:
        return render_template('/login.html')
    

@app.route('/reporte_cobros_imprimir', methods=['POST','GET'])
def reporte_cobros_imprimir():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            fechaInicio = request.form['fechaInicio']
            fechaFin = request.form['fechaFin']
            mycursor = mysql.connection.cursor()
            mycursor.execute("""SELECT p.idPrestamo, cl.nombre, c.cantidad, c.fecha_cobro FROM cobros AS c INNER JOIN prestamos AS p ON p.idPrestamo = c.idPrestamo INNER JOIN clientes AS cl ON cl.idCliente = p.idCliente WHERE c.fecha_cobro BETWEEN %s AND %s """,(fechaInicio, fechaFin))
            reportes = mycursor.fetchall()
            mycursor.close()
            if reportes:
                return render_template('reporte_cobros.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
            else:
                reportes = ('','','','','','','','')
                return render_template('reporte_cobros.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
        else:
            return redirect(url_for('reportes'))
    else:
        return render_template('/login.html')

#REPORTE CLIENTES
@app.route('/reporte_clientes', methods=['POST','GET'])
def reporte_clientes():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            reportes = ('','','','','','','','')
            return render_template('reporte_clientes.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
        else:
            return redirect(url_for('reportes'))
    else:
        return render_template('/login.html')

@app.route('/reporte_clientes_imprimir', methods=['POST','GET'])
def reporte_clientes_imprimir():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            mycursor = mysql.connection.cursor()
            mycursor.execute("""SELECT c.nombre,c.apellido, p.cantidad, p.fecha_prestamo, p.abono, p.restante FROM prestamos as p inner JOIN clientes AS c ON c.idCliente = p.idCliente""")
            reportes = mycursor.fetchall()
            mycursor.close()
            if reportes:
                return render_template('reporte_clientes.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
            else:
                 return redirect(url_for('reporte_clientes'))
        else:
            return redirect(url_for('reportes'))
    else:
        return render_template('/login.html')

#REPORTE PRESTAMOS
@app.route('/reporte_prestamos', methods=['POST','GET'])
def reporte_prestamos():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            return render_template('reporte_prestamos.html', usuarioGlobal = session['usuarioIngresado'])
        else:
            return redirect(url_for('reportes'))
    else:
        return render_template('/login.html')
    

@app.route('/reporte_prestamos_imprimir', methods=['POST','GET'])
def reporte_prestamos_imprimir():
    if 'usuarioIngresado' in session:
        if request.method == 'POST':
            fechaInicio = request.form['fechaInicio']
            fechaFin = request.form['fechaFin']
            mycursor = mysql.connection.cursor()
            mycursor.execute("""SELECT * FROM prestamos where is_active = 0 AND fecha_prestamo BETWEEN %s AND %s """,(fechaInicio, fechaFin))
            reportes = mycursor.fetchall()
            mycursor.close()
            if reportes:
                return render_template('reporte_cobros.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
            else:
                reportes = ('','','','','','','','')
                return render_template('reporte_cobros.html', usuarioGlobal = session['usuarioIngresado'], reportes = reportes)
        else:
            return redirect(url_for('reportes'))
    else:
        return render_template('/login.html')

#**************************************************************


if __name__ == '__main__':
    app.run(port=3000, debug=True)
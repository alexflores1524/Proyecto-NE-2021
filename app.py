from flask import Flask,render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/templates/Inicio.html')
def inicio2():
    return render_template('Inicio.html')

@app.route('/templates/clientes.html')
def clientes():
    return render_template('clientes.html')

@app.route('/templates/prestamos.html')
def prestamos():
    return render_template('prestamos.html')

@app.route('/templates/cobros.html')
def cobros():
    return render_template('cobros.html')

@app.route('/templates/atrasos.html')
def atrasos():
    return render_template('atrasos.html')

@app.route('/templates/usuarios.html')
def usuarios():
    return render_template('usuarios.html')

@app.route('/templates/reportes.html')
def reportes():
    return render_template('reportes.html')




if __name__ == '__main__':
    app.run(port=3000, debug=True)
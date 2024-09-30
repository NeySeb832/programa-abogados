# Importacion de las librerias necesarias para el desarrollo del proyecto
from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
import os
from pyexpat.errors import messages
from rich.markup import render

# Conexion con la base de datos en MySQL
app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'NeySeb832'
app.config['MYSQL_DB'] = 'progabogados'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  

mysql = MySQL(app)


#Rutas de la aplocaciom
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

# Funcion del login
@app.route('/accesp-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s', (_correo, _password))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['name'] = account['nombre']
            session['id'] = account['id']
            session['idrol'] = account['idrol']

            if session['idrol'] == "1":
                return render_template("admin.html", message = "Bienvenido Administrador")
            elif session['idrol'] == "2":
                return render_template("abogado.html", message = "Bienvenido Abogado")
            elif session['idrol'] == "3":
                return render_template("cliente.html" , message = "Bienvenido Cliente")
        else:
            return render_template('index.html', mensaje="Usuario o contraseña incorrectos")


        
    #Si el métdo no es POST o faltan campos, simplemente renderiza el formulario de login

    return render_template("index.html")

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods=['GET', 'POST'])
def crear_registro():

    id = request.form['txtId']
    nombre =request.form['txtNombre']
    correo = request.form['txtCorreo']
    contraseña = request.form['txtPassword']
    idrol = request.form['txtIdRol']
    cur = mysql.connection.cursor()
    cur.execute("insert into usuarios (id, nombre, correo, contraseña, idrol) values (%s, %s, %s, %s, %s)", (id, nombre, correo, contraseña, idrol))
    mysql.connection.commit()

    return render_template("index.html")
@app.route ('/logout')
def logout():
    session.pop('logueado', None)
    return redirect('/')



if __name__ == '__main__':
    app.secret_key = "Redyen83232"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

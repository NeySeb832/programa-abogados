from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256

# Conexión con la base de datos en MySQL
app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'NeySeb832'
app.config['MYSQL_DB'] = 'progabogados'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# Decorador para verificar si el usuario ha iniciado sesión
def login_requerido(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logueado' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))  # Redirige al login si no está logueado
    return wrap

# Rutas de la aplicación
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/sobreNosotros')
def SobreNosotros():
    return render_template("sobreNosotros.html")

# Función del login
@app.route('/accesp-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        # Consulta para obtener el usuario basado en el correo
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s', (_correo,))
        account = cur.fetchone()

        if account:
            # Verificar la contraseña ingresada con la almacenada en la base de datos
            stored_password = account['contraseña']  # La contraseña cifrada almacenada en la base de datos
            if pbkdf2_sha256.verify(_password, stored_password):
                # Si la contraseña es correcta, guardar la información en la sesión
                session['logueado'] = True
                session['name'] = account['nombre']
                session['id'] = account['id']
                session['idrol'] = account['idrol']

                # Redirigir según el rol del usuario
                if session['idrol'] == "1":
                    return render_template("admin.html", message="Bienvenido Administrador")
                elif session['idrol'] == "2":
                    return render_template("abogado.html", message="Bienvenido Abogado")
                elif session['idrol'] == "3":
                    return render_template("cliente.html", message="Bienvenido Cliente")
            else:
                # Si la contraseña es incorrecta
                return render_template('index.html', mensaje="Usuario o contraseña incorrectos")
        else:
            # Si no se encuentra el correo en la base de datos
            return render_template('index.html', mensaje="Usuario o contraseña incorrectos")

    # Si el método no es POST o faltan campos, simplemente renderiza el formulario de login
    return render_template("index.html")

# Ruta protegida: solo accesible después del login
@app.route('/admin')
@login_requerido
def admin():
    return render_template("admin.html")

# Ruta para el registro de usuarios
@app.route('/registro')
@login_requerido
def registro():
    return render_template('registro.html')

# Crear un nuevo registro
@app.route('/crear-registro', methods=['GET', 'POST'])
@login_requerido
def crear_registro():
    id = request.form['txtId']
    nombre = request.form['txtNombre']
    correo = request.form['txtCorreo']
    contraseña = pbkdf2_sha256.hash(request.form['txtPassword'])
    idrol = request.form['txtIdRol']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (id, nombre, correo, contraseña, idrol) VALUES (%s, %s, %s, %s, %s)", (id, nombre, correo, contraseña, idrol))
    mysql.connection.commit()

    return render_template("index.html")

# Eliminar un usuario
@app.route('/eliminar')
@login_requerido
def eliminar():
    return render_template('eliminar.html')

@app.route('/eliminar_registro', methods=['GET', 'POST'])
@login_requerido
def eliminar_registro():
    id = request.form['txtId']
    nombre = request.form['txtNombre']
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s AND nombre = %s", (id, nombre))
    mysql.connection.commit()

    return render_template("index.html")

# Listar todos los usuarios
@app.route('/listar', methods=['GET', 'POST'])
@login_requerido
def listar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()

    return render_template("listar.html", usuarios=usuarios)

# Cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logueado', None)
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = "Redyen83232"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

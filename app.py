# Importacion de las librerias necesarias para el desarrollo del proyecto
from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

# Conexion con la base de datos en MySQL
app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'NeySeb832'
app.config['MYSQL_DB'] = 'progabogados'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  

mysql = MySQL(app)

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
            session['id'] = account['id']
            session['idrol'] = account['idrol']

            if session['idrol'] == "1":
                return render_template("admin.html")
            elif session['idrol'] == "2":
                return render_template("abogado.html")
            elif session['idrol'] == "3":
                return render_template("cliente.html")
        else:
            return render_template('index.html', mensaje="Usuario o contraseña incorrectos")
    # Si el método no es POST o faltan campos, simplemente renderiza el formulario de login
    return render_template("index.html")

if __name__ == '__main__':
    app.secret_key = "Redyen83232"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

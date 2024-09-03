#Importacion de las librerias necesarias apra el desarrollo del proyecto
from flask import Flask
from flask import render_template, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

#Conexion con la base de datos en MySQL
app = Flask(__name__, template_folder='template')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'NeySeb832'
app.config['MYSQL_DB'] = 'abogados'
app.config['MYSQL_CURSOR CLASS'] = 'DictCursor'

MySQL=MySQL(app)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.secret_key = "Redyen83232"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

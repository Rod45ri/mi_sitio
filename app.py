from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)

# 🔧 CONFIGURA TUS DATOS DE CONEXIÓN AQUÍ


app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
mysql = MySQL(app)

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    cur = mysql.connection.cursor()
    cur.execute("SELECT contrasena FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cur.fetchone()
    cur.close()

    if resultado and check_password_hash(resultado[0], contrasena):
        return f"<h2>Bienvenido, {usuario}!</h2>"
    else:
        return "<h2>Credenciales incorrectas</h2>"

@app.route('/registro')
def registro():
    return render_template('register.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    hash_contra = generate_password_hash(contrasena)

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)", (usuario, hash_contra))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('inicio'))
    except:
        cur.close()
        return "<h2>Ese usuario ya existe</h2>"

if __name__ == '__main__':
    app.run(debug=True)
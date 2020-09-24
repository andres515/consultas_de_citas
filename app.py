from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'citas'

mysql = MySQL(app)


@app.route('/presentacion')
def presentacion():
    return render_template('presentacion.html')


@app.route('/inicio_sesion', methods=["GET", "POST"])
def inicio_sesion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("/nuevos_datos.html")
            else:
                return "Puede que la contraseña no sea valida!"
        else:
            return "Error user not found"
    else:
        return render_template("inicio_sesion.html")


@app.route('/loyout', methods=["GET", "POST"])
def loyout():
    session.clear()
    return render_template("presentacion.html")


@app.route('/registrarme', methods=["GET", "POST"])
def registrarme():
    if request.method == 'GET':
        return render_template("registrarme.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                    (name, email, hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('presentacion'))


@app.route('/nuevos_datos', methods=['GET', 'POST'])
def nuevos_datos():
    if request.method == "POST":
        details = request.form
        numerodocumento = details['numerodocumento']
        nombres = details['nombres']
        apellidos = details['apellidos']
        correo = details['email']
        ciudad = details['ciudad']
        fecha = details['fecha']
        telefono = details['telefono']
        estadocivil = details['civil']
        motivoconsulta = details['motivo']
        recomendaciones = details['recomendaciones']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO datosclientes(numerodocumento, nombres, apellidos, correo, ciudad, fecha, telefono, estadocivil, motivoconsulta, recomendaciones) VALUES(%s, %s, %s, %s,%s, %s,%s, %s,%s, %s)",
        (numerodocumento, nombres, apellidos, correo, ciudad, fecha, telefono, estadocivil, motivoconsulta, recomendaciones))
        mysql.connection.commit()
        cur.close()
    return render_template('nuevos_datos.html')


@app.route('/buscar_registro')
def buscar_registro():
    return render_template('buscar_registro.html')


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)

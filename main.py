from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import datetime
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'clave_secreta_flask'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mini_proyecto_flask'

mysql = MySQL(app)


@app.context_processor
def hora_actual():
    return {
        'ahora': datetime.utcnow()
    }


@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/informacion')
def informacion():
    return render_template('informacion.html')


@app.route('/contacto')
@app.route('/contacto/<string:nombre>/<string:apellido>')
def contacto(nombre=None, apellido=None):

    texto = ''

    if nombre != None and apellido != None:
        texto = f'Nombre completo: {nombre} {apellido}'

        return render_template('contacto.html', texto=texto)
    
    else:
        texto = 'Complete los parametros necesarios'

        return render_template('contacto.html', texto=texto)


@app.route('/lenguajes-de-programacion')
@app.route('/lenguajes-de-programacion/<redireccion>')
def lenguajes(redireccion = None):

    if redireccion != None:
        return redirect(url_for('informacion'))

    return render_template('lenguajes.html')


@app.route('/crear-coche', methods=['GET', 'POST'])
def crear_coche():

    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']


        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches VALUES(NULL, %s, %s, %s, %s)", (marca, modelo, precio, ciudad))
        cursor.connection.commit()

        flash('¡Coche creado con exito!')

        return redirect(url_for('inicio'))
    
    return render_template('crear_coche.html')


@app.route('/coches')
def coches():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM coches ORDER BY id DESC')
    coches = cursor.fetchall()
    cursor.close()

    return render_template('coches.html', coches=coches)


@app.route('/coche/<int:id>')
def coche(id):

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM coches WHERE id = %s', (id))
    coche = cursor.fetchall()
    cursor.close()

    return render_template('coche.html', coche=coche[0])


@app.route('/borrar-coche/<int:id>')
def borrar_coche(id):

    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM coches WHERE id = {id}')
    mysql.connection.commit()

    flash('¡El coche ha sido eliminado!')

    return redirect(url_for('coches'))


@app.route('/editar-coche/<int:id>', methods=['GET', 'POST'])
def editar_coche(id):

    if request.method == 'POST':
            
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        cuidad = request.form['cuidad']

        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE coches
            SET marca = %s,
                modelo = %s,
                precio = %s,
                cuidad = %s,
            WHERE id = %s
        ''', (marca, modelo, precio, cuidad, id))
        cursor.connection.commit()

        flash('¡El coche se ha editado correctamente!')

        return redirect(url_for('coches'))


    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM coches WHERE id = %s', (id))
    coche = cursor.fetchall()
    cursor.close()

    return render_template('crear_coche.html', coche=coche[0])




if __name__ == '__main__':
    app.run(debug=True)


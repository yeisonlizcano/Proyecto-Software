from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#mysql conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'productosPRYT'
mysql = MySQL(app)
#sesion
app.secret_key = 'mysecretkey'

@app.route('/indice')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()
    #print(data)
    return render_template("index.html", productos=data)

@app.route('/add_product', methods=['POST'])
def addproduct():
    if request.method == 'POST':
        nompr = request.form['nompr']
        preciopr = request.form['preciopr']
        categoriapr = request.form['categoriapr']
        fechaexppr = request.form['fechaexppr']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre,precio,categoria,fechaexp) values (%s, %s, %s, %s)',
                    (nompr, preciopr, categoriapr, fechaexppr))
        mysql.connection.commit()
        mysql.connection.close()
        flash('Producto agregado satisfactoriamente')
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def obtenerProductos(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE idproductos = %s", (id))
    data = cur.fetchone()
    cur.close()
    #print(data)
    return render_template('edit-pr.html', productos = data)

@app.route('/update/<id>', methods=['POST'])
def actualizarProd(id):
    if request.method == 'POST':
        nompr = request.form['nompr']
        preciopr = request.form['preciopr']
        categoriapr = request.form['categoriapr']
        fechaexppr = request.form['fechaexppr']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE productos SET nombre = %s,
            precio = %s,
            categoria = %s,
            fechaexp = %s
        WHERE idproductos = %s
        """, (nompr, preciopr, categoriapr, fechaexppr, id))
        mysql.connection.commit()
        flash('producto actualizado satisfactoriamente')
        mysql.connection.close()
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def borrarProductos(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE idproductos = {0}".format(id))
    mysql.connection.commit()
    flash('producto removido satisfactoriamente!')
    cur.close()
    return redirect(url_for('index'))

@app.route('/')
def aux():
    return render_template('PaginaPrincipal.html')


@app.route('/auxiliar')
def aux2():
    return render_template('login.html')

@app.route('/verificacion', methods=['POST'])
def validar():
    auxi = ''
    if request.method == 'POST':
        user = request.form['email']
        pwd = request.form['pwd']
        if pwd == 'juan' and user == 'juan@gmail':
            auxi = 'Hola de nuevo'
            return redirect(url_for('index'))
        else:
            auxi= 'usuario o contraseña incorrectos'
            #flash('')
            return redirect(url_for('aux2'))
    else:
        return "Debe ser post"

@app.route('/show_products')
def mostrar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()

    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM carrito')
    data1 = cur1.fetchall()
    cur1.close()
    #print(data)
    return render_template("paginaUsr.html", productos=data, productos1=data1)

@app.route('/carrito/<id>')
def usecarrito(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE idproductos = %s", (id))
    data = cur.fetchone()
    cur.close()
    nompr = data[1]
    preciopr = data[2]
    categoriapr = data[3]
    fechaexppr = data[4]

    cur1 = mysql.connection.cursor()
    cur1.execute('INSERT INTO carrito(nombre,precio,categoria,fechaexp) values (%s, %s, %s, %s)',
                (nompr, preciopr, categoriapr, fechaexppr))
    mysql.connection.commit()
    cur1.close()
    #print(data)
    flash('Producto agregado!')
    return redirect(url_for('mostrar'))


@app.route('/compras/<id>')
def comprar(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT FROM productos WHERE idproductos = {0}".format(id))
        data = cur.fetchone()
        cur.close()
        nompr = data[1]
        preciopr = data[2]
        categoriapr = data[3]
        fechaexppr = data[4]

        cur1 = mysql.connection.cursor()
        cur1.execute('INSERT INTO registro(nombre,precio,categoria,fechaexp) values (%s, %s, %s, %s)',
                    (nompr, preciopr, categoriapr, fechaexppr))
        mysql.connection.commit()
        flash('compra realizada satisfactoriamente')
        cur1.close()
    return redirect(url_for('mostrar'))

@app.route('/vaciar')
def truncate():
    cur = mysql.connection.cursor()
    
    cur.execute("TRUNCATE table carrito")
    mysql.connection.commit()
    cur.close()
    flash('Carrito vacio!')
    return redirect(url_for('mostrar'))

if __name__=="__main__":
    app.run(debug=True)
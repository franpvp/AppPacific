# Se importa la clase Flask
import json
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy


# Se inicializa la aplicación
app = Flask(__name__)
# Configura la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:afterlife1998@localhost/sys'
db = SQLAlchemy(app)

@app.before_request
def before_request():
    print("Antes de la petición...")

@app.after_request
def after_request(response):
    print("Después de la petición")
    return response

datos = {
        'fecha_ingreso': ''
        }

#Decorador con la ruta raiz
@app.route('/')
# La función home va a ser una vista
def index():
    data = {
        'bienvenida': 'Bienvenido a PacificApp',
        'titulo': 'Sistema de reserva de habitaciones'
    }
    return render_template('index.html', data=data)

@app.route('/home')
def home():
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }
    return render_template('home.html', usuario_test=usuario_test)

# Se pone la ruta a la vista mediante el decorador @app.route()
@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

# Funcion para una consulta o query mediante una ruta
def query_string():
    print(request) # Petición del usuario
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"

class Usuario(db.Model):
    usuario_id = db.Column(db.Integer, primary_key=True)
    rut_usuario = db.Column(db.String(12))
    dv_usuario = db.Column(db.String(1))
    nombre_usuario = db.Column(db.String(45))
    apellido_usuario = db.Column(db.String(45))
    correo_usuario = db.Column(db.String(45))
    telefono_usuario = db.Column(db.String(10))
    tipo_usuario_id = db.Column(db.Integer)

    def __init__(self, rut_usuario, dv_usuario,nombre_usuario,apellido_usuario,correo_usuario,telefono_usuario,tipo_usuario_id):
        self.rut_usuario = rut_usuario
        self.dv_usuario = dv_usuario
        self.nombre_usuario = nombre_usuario
        self.apellido_usuario = apellido_usuario
        self.correo_usuario = correo_usuario
        self.telefono_usuario = telefono_usuario
        self.tipo_usuario_id = tipo_usuario_id

# Vista Perfil de usuario (Consultando a una base de datos)
@app.route('/perfil')
def perfil():
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }
    return render_template('perfil.html', usuario_test=usuario_test)

# Vista Inicio Sesión
@app.route('/inicio-sesion', methods=['GET', 'POST'])
def login():
    error = None
    # Diccionario con usuario
    usuarios = {
        'email':'juanperez@gmail.com',
        'password':'juanperez123'
    }
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['password']

        # Validación de credenciales
        if email == usuarios['email'] and contrasena == usuarios['password']:
            # Autenticación exitosa, redirige a la página de reserva
            return redirect(url_for('reserva'))
        else:
            # Credenciales incorrectas, muestra un mensaje de error
            error = "Credenciales incorrectas. Por favor, inténtalo nuevamente."

    return render_template('inicio-sesion.html', error=error)

# Vista Registro
@app.route('/registro')
def registro():
    return render_template('/registro.html')

#Vista Habitaciones
@app.route('/habitaciones')
def habitaciones():
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }
    return render_template('habitaciones.html', usuario_test=usuario_test)

# Vista Reserva
@app.route('/reserva')
def reserva():
    data = {
        'standard_matrimonial': {
            'precio_noche': 100000,
            'max_huespedes': 2
            
        },
        'standard_twin': {
            'precio_noche': 80000,
            'max_huespedes': 2
        }
    }
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }
    return render_template('reserva.html', data=data, usuario_test=usuario_test)

@app.route('/mis-reservas')
def mis_reservas():
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }

    return render_template('mis-reservas.html', usuario_test=usuario_test)

@app.route('/pago-reserva', methods=['GET'])
def pago_reserva():
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }
    datos_str = request.args.get('datos')
    datos_dic = json.loads(datos_str)
    fecha_ingreso = datos_dic.get('fechaIngreso', '')
    fecha_salida = datos_dic.get('fechaSalida', '')
    totalPrecioInicial = datos_dic.get('totalPrecioInicial', '')
    
    return render_template('pago-reserva.html', fecha_ingreso=fecha_ingreso,fecha_salida=fecha_salida,totalPrecioInicial=totalPrecioInicial, usuario_test=usuario_test)

@app.route('/reserva-exitosa')
def reserva_exitosa():
    # Datos del usuario logeado
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }

    return render_template('reserva-exitosa.html',usuario_test=usuario_test)



# Vista error 404
def pagina_no_encontrada(error):
    return render_template('404.html'), 404


if __name__=='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000) # El puerto puede ser distinto al default
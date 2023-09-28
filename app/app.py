# Se importa la clase Flask
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

#Decorador con la ruta raiz
@app.route('/')
# La función home va a ser una vista
def home():
    data = {
        'bienvenida': 'Bienvenido a PacificApp',
        'titulo': 'Sistema de reserva de habitaciones'
    }
    return render_template('home.html', data=data)

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

# Vista Perfil de usuario
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

@app.route('/perfil')
def consultar_usuarios():
    perfil = Usuario.query.all()
    return render_template('perfil.html', perfil=perfil)

# Vista Reserva



def pagina_no_encontrada(error):
    # return render_template('404.html'), 404
    return redirect(url_for('home'))

if __name__=='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000) # El puerto puede ser distinto al default
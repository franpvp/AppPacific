# Se importa la clase Flask
import json
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Date 


# Se inicializa la aplicación
app = Flask(__name__)
# Configura la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:afterlife1998@localhost/sys'
db = SQLAlchemy(app)
#Clave secreta
app.secret_key = 'DuocUC2023'

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
    usuario_id = session.get('usuario_id')
    if usuario_id:
        # Recuperar el usuario de la base de datos utilizando el ID
        usuario = Usuario.query.get(usuario_id)

        if usuario:
            # Renderizar la plantilla HTML y pasar el objeto 'usuario' a la plantilla
            return render_template('home.html', usuario=usuario)

    return render_template('home.html')

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

# Definición de la clase para el modelo TipoUsuario
# IMPORTANTE: EN LA BASE DE DATOS DEBEN HABER DATOS EN TIPO_USUARIO
class TipoUsuario(db.Model):
    __tablename__ = 'TIPO_USUARIO'
    tipo_usuario_id = db.Column(db.Integer, primary_key=True)
    nombre_tipo_usuario = db.Column(db.String(45),nullable=False)
    usuarios = db.relationship('Usuario', backref='tipo_usuario', foreign_keys='Usuario.tipo_usuario_id')
    
# Definición de la clase para el modelo Usuario
class Usuario(db.Model):
    __tablename__ = 'USUARIO'
    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rut_usuario = db.Column(db.String(12), nullable=False)
    nombre_usuario = db.Column(db.String(45), nullable=False)
    apellido_usuario = db.Column(db.String(45), nullable=False)
    correo_usuario = db.Column(db.String(45), nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    telefono_usuario = db.Column(db.String(10), nullable=False)
    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey('TIPO_USUARIO.tipo_usuario_id'), nullable=False)
    

    def __init__(self, rut_usuario,nombre_usuario,apellido_usuario,correo_usuario,contrasena,telefono_usuario,tipo_usuario_id=2):
        self.rut_usuario = rut_usuario
        self.nombre_usuario = nombre_usuario
        self.apellido_usuario = apellido_usuario
        self.correo_usuario = correo_usuario
        self.contrasena = contrasena
        self.telefono_usuario = telefono_usuario
        self.tipo_usuario_id = tipo_usuario_id

# Definición de la clase para el modelo Hotel
class Hotel(db.Model):
    __tablename__ = 'HOTEL'
    hotel_id = db.Column(db.Integer, primary_key=True)
    nombre_hotel = db.Column(db.String(45), nullable=False)
    direccion = db.Column(db.String(45), nullable=False)
    categoria = db.Column(db.String(45), nullable=True)


# Definición de la clase para el modelo Habitacion
class Habitacion(db.Model):
    __tablename__ = 'HABITACION'
    habitacion_id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('HOTEL.hotel_id'), nullable=False)
    tipo = db.Column(db.String(45), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    precio_noche = db.Column(db.Integer, nullable=False)
    cant_disponibles = db.Column(db.Integer, nullable=False)

    def __init__(self, habitacion_id,hotel_id,tipo,capacidad,precio_noche,cant_disponibles):
        self.habitacion_id = habitacion_id
        self.hotel_id = hotel_id
        self.tipo = tipo
        self.capacidad = capacidad
        self.precio_noche = precio_noche
        self.cant_disponibles = cant_disponibles


# Definición de la clase para el modelo MetodoPago
class MetodoPago(db.Model):
    __tablename__ = 'METODO_PAGO'
    metodo_pago_id = db.Column(db.Integer, primary_key=True)
    tipo_metodo = db.Column(db.String(45), nullable=False)

# Definición de la clase para el modelo DetallePago
class DetallePago(db.Model):
    __tablename__ = 'DETALLE_PAGO'
    detalle_pago_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('METODO_PAGO.metodo_pago_id'), nullable=False)
    pago_inicial = db.Column(db.Integer, nullable=False)
    pago_pendiente = db.Column(db.Integer, nullable=False)
    fecha_pago = db.Column(Date, nullable=False)

    def __init__(self, detalle_pago_id,metodo_pago_id,pago_inicial,pago_pendiente,fecha_pago):
        self.detalle_pago_id = detalle_pago_id
        self.metodo_pago_id = metodo_pago_id
        self.pago_inicial = pago_inicial
        self.pago_pendiente = pago_pendiente
        self.fecha_pago = fecha_pago

# Definición de la clase para el modelo Reserva
class Reserva(db.Model):
    __tablename__ = 'RESERVA'
    reserva_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habitacion_id = db.Column(db.Integer, db.ForeignKey('HABITACION.habitacion_id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('USUARIO.usuario_id'), nullable=False)
    detalle_pago_id = db.Column(db.Integer, db.ForeignKey('DETALLE_PAGO.detalle_pago_id'), nullable=False)
    fecha_entrada = db.Column(Date, nullable=False)
    fecha_salida = db.Column(Date, nullable=False)
    cant_personas = db.Column(db.Integer, nullable=False)

    def __init__(self,habitacion_id,usuario_id,detalle_pago_id,fecha_entrada,fecha_salida,cant_personas):
        self.habitacion_id = habitacion_id
        self.usuario_id = usuario_id
        self.detalle_pago_id = detalle_pago_id
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cant_personas = cant_personas


# Vista Inicio Sesión
@app.route('/inicio-sesion', methods=['GET', 'POST'])
def login():
    usuario = None
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        email =  request.form['email']
        contrasena = request.form['password']
        #Buscar un usuario con el email
        usuario = Usuario.query.filter_by(correo_usuario=email).first()

        if usuario and check_password_hash(usuario.contrasena, contrasena):
            # Iniciar sesión para el usuario
            session['usuario_id'] = usuario.usuario_id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home'))
            
        print('Email o contraseña incorrectos')

    return render_template('inicio-sesion.html')

# Vista Registro
@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        # Obtener datos del formulario de registro
        rut = request.form['rut']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena = request.form['password']
        # Se genera una hash seguro de la contraseña
        contrasena_hash = generate_password_hash(contrasena)

        # Creación de un nuevo usuario
        nuevo_usuario = Usuario(
            rut_usuario = rut, 
            nombre_usuario = nombre, 
            apellido_usuario = apellido, 
            correo_usuario = email,
            contrasena = contrasena_hash,
            telefono_usuario = telefono,
            tipo_usuario_id = 2
        )
        
        # Agregar al usuario a la sesión y guardar en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('/registro.html')

#Vista Habitaciones
@app.route('/habitaciones')
def habitaciones():
    usuario_id = session.get('usuario_id')
    habitacion_twin = Habitacion.query.filter_by(habitacion_id=1).first()
    habitacion_mat = Habitacion.query.filter_by(habitacion_id=2).first()
    if usuario_id and habitacion_twin and habitacion_mat:
        # Recuperar el usuario de la base de datos utilizando el ID
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            # Renderizar la plantilla HTML y pasar el objeto 'usuario' a la plantilla
            print('Llegué hasta acá')
            return render_template('habitaciones.html', usuario=usuario,habitacion_twin=habitacion_twin, habitacion_mat=habitacion_mat)

    return render_template('habitaciones.html')

# Vista Reserva
@app.route('/reserva', methods=['GET','POST'])
def reserva():
    habitacion_twin = Habitacion.query.filter_by(habitacion_id=1).first()
    habitacion_mat = Habitacion.query.filter_by(habitacion_id=2).first()
    usuario_id = session.get('usuario_id')
    standard_twin = habitacion_twin.tipo
    standard_mat = habitacion_mat.tipo
    if usuario_id:
        # Recuperar el usuario de la base de datos utilizando el ID
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            if request.method == 'POST':
                fecha_entrada = request.form['fecha_entrada']
                print('LA FECHA DE INGRESO ES: ', fecha_entrada)
                fecha_salida = request.form['fecha_salida']
                cant_personas = request.form['cantidad_huespedes']
                return redirect(url_for('pago_reserva',fecha_entrada=fecha_entrada, fecha_salida=fecha_salida,cant_personas=cant_personas))
    
    return render_template('reserva.html',usuario=usuario)

@app.route('/mis-reservas')
def mis_reservas():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        # Recuperar el usuario de la base de datos utilizando el ID
        usuario = Usuario.query.get(usuario_id)

        if usuario:
            # Renderizar la plantilla HTML y pasar el objeto 'usuario' a la plantilla
            return render_template('mis-reservas.html', usuario=usuario)

    return render_template('mis-reservas.html', usuario=usuario)

@app.route('/pago-reserva/<fecha_entrada>/<fecha_salida>/<int:cant_personas>', methods=['GET','POST'])
def pago_reserva(fecha_entrada,fecha_salida,cant_personas):
    usuario_id = session.get('usuario_id')
    # Crear reserva tipo twin
    # reserva_twin = Reserva(
    #     habitacion_id = 1,
    #     usuario_id = usuario_id,
    #     detalle_pago_id = 1,
    # )
    # Crear reserva tipo matrimonial
    # reserva_mat = Reserva(
    #     habitacion_id = 2,
    #     usuario_id = usuario_id,
    #     detalle_pago_id = 1,
    #     fecha_entrada = fecha_entrada,
    #     fecha_salida = fecha_salida,
    #     cant_personas = cant_personas
    # )
    if usuario_id:
        # Recuperar el usuario de la base de datos utilizando el ID
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            # fecha_entrada = request.args.get('fecha_entrada')
            # print('FECHA DE ENTRADA EN PAGO-RESERVA: ', fecha_entrada)
            # fecha_salida = request.args.get('fecha_salida')
            # cant_personas = request.args.get('cant_personas')
        
            return render_template('pago-reserva.html',usuario=usuario,fecha_entrada=fecha_entrada,fecha_salida=fecha_salida,cant_personas=cant_personas)
    return render_template('pago-reserva.html')
@app.route('/reserva-exitosa')
def reserva_exitosa():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        # Recuperar el usuario de la base de datos utilizando el ID
        usuario = Usuario.query.get(usuario_id)

        if usuario:
            # Renderizar la plantilla HTML y pasar el objeto 'usuario' a la plantilla
            return render_template('reserva-exitosa.html', usuario=usuario)
        
    return render_template('reserva-exitosa.html')



# Vista error 404
def pagina_no_encontrada(error):
    usuario_test = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'email': 'juanperez@gmail.com',
        'telefono': '123456789'
    }
    return render_template('404.html',usuario_test=usuario_test), 404


if __name__=='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000) # El puerto puede ser distinto al default
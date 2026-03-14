from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Tabla Clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    # Relación 1 a Muchos con Pedidos
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

# 2. Tabla Pizzas (Catálogo de tamaños e ingredientes)
class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id_pizza = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(20), nullable=False)
    ingredientes = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Numeric(8, 2), nullable=False)

    # Relación 1 a Muchos con DetallePedido
    detalles = db.relationship('DetallePedido', backref='pizza_info', lazy=True)

# 3. Tabla Pedidos (Cabecera del ticket)
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    # Relación 1 a Muchos con DetallePedido
    detalles = db.relationship('DetallePedido', backref='pedido_info', lazy=True, cascade="all, delete-orphan")

# 4. Tabla Detalle Pedido (Las pizzas específicas dentro de un pedido)
class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_pizza = db.Column(db.Integer, db.ForeignKey('pizzas.id_pizza'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
class CarritoTemporal(db.Model):
    __tablename__ = 'carrito_temporal'
    id_temp = db.Column(db.Integer, primary_key=True)
    # Guardamos los datos del cliente para que no tenga que reescribirlos
    cliente_nombre = db.Column(db.String(100))
    cliente_direccion = db.Column(db.String(200))
    cliente_telefono = db.Column(db.String(20))
    # Guardamos el detalle de la pizza
    tamano = db.Column(db.String(20))
    ingredientes = db.Column(db.String(200))
    num_pizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Numeric(10, 2))
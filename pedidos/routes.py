from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import PedidoForm
from models import db, Cliente, Pedido, DetallePedido, CarritoTemporal, Pizza
from datetime import datetime

pedidos_bp = Blueprint('pedidos', __name__, template_folder='../templates')

PRECIOS_TAMANO = {
    'Chica': 40,
    'Mediana': 80,
    'Grande': 120
}
PRECIO_INGREDIENTE = 10

@pedidos_bp.route('/', methods=['GET', 'POST'])
def index():
    form = PedidoForm()
    
    if form.validate_on_submit():
        tamano = form.tamano.data
        num_pizzas = form.numero_pizzas.data
        
        # Calculamos ingredientes
        ingredientes_seleccionados = []
        if form.ing_jamon.data: ingredientes_seleccionados.append('Jamón')
        if form.ing_pina.data: ingredientes_seleccionados.append('Piña')
        if form.ing_champinones.data: ingredientes_seleccionados.append('Champiñones')
        
        costo_base = PRECIOS_TAMANO.get(tamano, 0)
        costo_ingredientes = len(ingredientes_seleccionados) * PRECIO_INGREDIENTE
        subtotal = (costo_base + costo_ingredientes) * num_pizzas
        
        # GUARDAMOS DIRECTO EN LA BASE DE DATOS (TABLA TEMPORAL)
        nuevo_item = CarritoTemporal(
            cliente_nombre=form.nombre.data,
            cliente_direccion=form.direccion.data,
            cliente_telefono=form.telefono.data,
            tamano=tamano,
            ingredientes=', '.join(ingredientes_seleccionados) if ingredientes_seleccionados else 'Sin ingredientes',
            num_pizzas=num_pizzas,
            subtotal=subtotal
        )
        db.session.add(nuevo_item)
        db.session.commit()
        
        flash("Pizza agregada al detalle del pedido", "success")
        return redirect(url_for('pedidos.index'))
        
    elif request.method == 'POST':
        flash("Verifica que hayas seleccionado tamaño, cantidad y llenado tus datos.", "error")

    # AL CARGAR LA PÁGINA: Leemos directo de la base de datos el carrito
    carrito = CarritoTemporal.query.all()
    total_pedido = sum(item.subtotal for item in carrito)
    
    # Si ya hay pizzas en el carrito temporal, rellenamos el nombre del cliente
    if carrito and request.method == 'GET':
        form.nombre.data = carrito[0].cliente_nombre
        form.direccion.data = carrito[0].cliente_direccion
        form.telefono.data = carrito[0].cliente_telefono

    # --- Consultar las ventas exitosas del día de hoy ---
    fecha_hoy = datetime.now().date()
    ventas_hoy = Pedido.query.filter_by(fecha=fecha_hoy).all()
    total_ventas_hoy = sum(venta.total for venta in ventas_hoy)

    # Pasamos las nuevas variables (ventas_hoy y total_ventas_hoy) a la plantilla
    return render_template('index.html', form=form, carrito=carrito, total_pedido=total_pedido, ventas_hoy=ventas_hoy, total_ventas_hoy=total_ventas_hoy)

@pedidos_bp.route('/acciones', methods=['POST'])
def acciones_pedido():
    accion = request.form.get('accion')
    
    # --- BOTÓN QUITAR ---
    if accion == 'quitar':
        id_temp = request.form.get('pizza_seleccionada')
        if not id_temp:
            flash("Selecciona una pizza para quitarla", "error")
            return redirect(url_for('pedidos.index'))
            
        # Borramos esa pizza específica de la tabla temporal
        item_a_borrar = CarritoTemporal.query.get(id_temp)
        if item_a_borrar:
            db.session.delete(item_a_borrar)
            db.session.commit()
            flash("Pizza eliminada del pedido actual", "success")
            
        return redirect(url_for('pedidos.index'))

    # --- BOTÓN TERMINAR ---
    elif accion == 'terminar':
        carrito = CarritoTemporal.query.all()
        
        if not carrito:
            flash("No hay pizzas agregadas para terminar el pedido", "error")
            return redirect(url_for('pedidos.index'))

        total_pedido = sum(item.subtotal for item in carrito)

        # 1. Guardar el Cliente
        cliente_datos = carrito[0]
        nuevo_cliente = Cliente(
            nombre=cliente_datos.cliente_nombre,
            direccion=cliente_datos.cliente_direccion,
            telefono=cliente_datos.cliente_telefono
        )
        db.session.add(nuevo_cliente)
        db.session.flush() # Obtenemos su ID

        # 2. Guardar el Pedido Cabecera
        nuevo_pedido = Pedido(
            id_cliente=nuevo_cliente.id_cliente,
            fecha=datetime.now().date(),
            total=total_pedido
        )
        db.session.add(nuevo_pedido)
        db.session.flush() # Obtenemos su ID

        # 3. Guardar las Pizzas personalizadas y su Detalle
        for item in carrito:
            # A) Primero guardamos la pizza configurada exactamente como la pidió el cliente
            precio_unitario = item.subtotal / item.num_pizzas
            
            nueva_pizza = Pizza(
                tamano=item.tamano,
                ingredientes=item.ingredientes,
                precio=precio_unitario
            )
            db.session.add(nueva_pizza)
            db.session.flush() # Obtenemos el ID de esta nueva pizza creada

            # B) Ahora sí, la ligamos al detalle del pedido usando el nuevo ID
            nuevo_detalle = DetallePedido(
                id_pedido=nuevo_pedido.id_pedido,
                id_pizza=nueva_pizza.id_pizza,
                cantidad=item.num_pizzas,
                subtotal=item.subtotal
            )
            db.session.add(nuevo_detalle)

        # 4. Vaciar la tabla temporal (carrito)
        CarritoTemporal.query.delete()
        
        # Guardar todos los cambios definitivos
        db.session.commit()
        
        flash(f"¡Pedido guardado en la base de datos! Total a cobrar: ${total_pedido:.2f}", "success")
        return redirect(url_for('pedidos.index'))

    return redirect(url_for('pedidos.index'))
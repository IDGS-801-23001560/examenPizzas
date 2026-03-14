from flask import Blueprint, render_template, request
from sqlalchemy import extract, func
from models import db, Pedido
from .forms import BusquedaDiaForm, BusquedaMesForm

ventas_bp = Blueprint('ventas', __name__, template_folder='../templates')

@ventas_bp.route('/por_dia', methods=['GET', 'POST'])
def por_dia():
    form = BusquedaDiaForm()
    ventas = []
    total_acumulado = 0
    dia_nombre = ""

    if form.validate_on_submit():
        dia_num = form.dia.data
        dia_nombre = dict(form.dia.choices).get(dia_num) # Obtenemos el texto (Ej: 'Lunes')
        
        # Filtramos usando DAYOFWEEK de MySQL
        ventas = Pedido.query.filter(func.dayofweek(Pedido.fecha) == dia_num).all()
        total_acumulado = sum(v.total for v in ventas)

    return render_template('ventas/por_dia.html', form=form, ventas=ventas, total=total_acumulado, parametro=dia_nombre)

@ventas_bp.route('/por_mes', methods=['GET', 'POST'])
def por_mes():
    form = BusquedaMesForm()
    ventas = []
    total_acumulado = 0
    mes_nombre = ""

    if form.validate_on_submit():
        mes_num = form.mes.data
        mes_nombre = dict(form.mes.choices).get(mes_num)
        
        # Filtramos extrayendo el mes de la fecha
        ventas = Pedido.query.filter(extract('month', Pedido.fecha) == mes_num).all()
        total_acumulado = sum(v.total for v in ventas)

    return render_template('ventas/por_mes.html', form=form, ventas=ventas, total=total_acumulado, parametro=mes_nombre)

@ventas_bp.route('/detalles/<int:id>')
def detalles(id):
    # Buscamos el pedido por su ID. Si no existe, lanza un error 404.
    pedido = Pedido.query.get_or_404(id)
    
    # Pasamos el pedido completo a la plantilla
    return render_template('ventas/detalles.html', pedido=pedido)
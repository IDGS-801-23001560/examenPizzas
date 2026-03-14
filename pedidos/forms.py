from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PedidoForm(FlaskForm):
    # Datos del Cliente
    nombre = StringField('Nombre', validators=[DataRequired(message="El nombre es obligatorio")])
    direccion = StringField('Dirección', validators=[DataRequired(message="La dirección es obligatoria")])
    telefono = StringField('Teléfono', validators=[DataRequired(message="El teléfono es obligatorio")])

    # Opciones de la Pizza
    tamano = RadioField('Tamaño Pizza', choices=[
        ('Chica', 'Chica $40'),
        ('Mediana', 'Mediana $80'),
        ('Grande', 'Grande $120')
    ], validators=[DataRequired(message="Selecciona un tamaño de pizza")])

    # Ingredientes (Casillas independientes para fácil manejo)
    ing_jamon = BooleanField('Jamón $10')
    ing_pina = BooleanField('Piña $10')
    ing_champinones = BooleanField('Champiñones $10')

    # Cantidad
    numero_pizzas = IntegerField('Num. de Pizzas', validators=[
        DataRequired(message="Ingresa la cantidad"),
        NumberRange(min=1, message="Debe ser al menos 1 pizza")
    ])

    # Botón para agregar a la tabla temporal
    agregar = SubmitField('Agregar')
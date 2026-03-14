from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class BusquedaDiaForm(FlaskForm):
    # En MySQL, el día de la semana (DAYOFWEEK) se numera del 1 (Domingo) al 7 (Sábado)
    dia = SelectField('Día de la semana', choices=[
        ('2', 'Lunes'), 
        ('3', 'Martes'), 
        ('4', 'Miércoles'),
        ('5', 'Jueves'), 
        ('6', 'Viernes'), 
        ('7', 'Sábado'), 
        ('1', 'Domingo')
    ])
    buscar = SubmitField('Buscar Ventas por Día')

class BusquedaMesForm(FlaskForm):
    mes = SelectField('Mes del año', choices=[
        ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
        ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
        ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
        ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
    ])
    buscar = SubmitField('Buscar Ventas por Mes')

from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Email


class formCliente(FlaskForm):
    Empresa = StringField("Empresa: ", validators=[DataRequired(), Length(min=5, max=50, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    CifNif = StringField(label="Cif: ", validators=[DataRequired(), Length(min=5, max=10, 
    message='Campo obligatorio.  Minimo 5 caracteres.')])
    Direccion = StringField("Direccion: ")
    CP = IntegerField("CP: ")
    Ciudad = StringField("Ciudad: ")
    Provincia = StringField("Provincia: ")
    Telefono = IntegerField("Telefono: ", validators=[DataRequired()])
    Email = StringField("Email: ", validators=[Email(), Length(min=5, max=50,
     message='Escribe un email valido.')])
    Contacto = StringField("Contacto: ")
    
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})


class formSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')

from email import message
from email.policy import default
from logging import RootLogger
from mailbox import NoSuchMailboxError
from re import A
from threading import activeCount
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectField, PasswordField
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
    Baja = BooleanField('Baja')
   
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formProveedor(FlaskForm):
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
    Baja = BooleanField('Baja')
    
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formTrabajador(FlaskForm):
    Nombre = StringField("Nombre: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    Apellidos= StringField("Apellidos: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    Telefono = IntegerField("Telefono: ", validators=[DataRequired()])
    Baja = BooleanField('Baja', default=0)
    Rol = SelectField('Rol: ', choices=[('All'),('Admin'), ('Trabajador')])
    Usuario = StringField("Usuario: ")
    Contrasena = PasswordField('Contraseña: ')
 
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formUnidad(FlaskForm):
    Unidad= StringField("Unidad: ", validators=[DataRequired(), Length(min=1, max=10, 
    message='Campo obligatorio. Minimo 1 caracteres.')])
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')
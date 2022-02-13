
from distutils import errors
from email import message
from msilib.schema import Error
from typing_extensions import Required
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, FileField, TextAreaField
from wtforms import SelectField, PasswordField, FloatField, DateField, TimeField, validators
from wtforms.validators import ValidationError, DataRequired 
from wtforms.validators import Length, Email, NumberRange, InputRequired	
from flask_wtf.file import FileField, FileRequired



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

class formEstado(FlaskForm):
    Estado= StringField("Estado: ", validators=[DataRequired(), Length(min=1, max=45, 
    message='Campo obligatorio. Minimo 1 caracteres.')])
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formProducto(FlaskForm):
    # Nombre, Precio (float), idUnidad (que es un fk de unidad)

    Nombre = StringField("Nombre: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    Precio = FloatField("Precio: ", validators=[DataRequired(),NumberRange(0, 1E+20) ], default=1.0)
    idUnidad = SelectField('Unidad Medida: ',  coerce=int)

    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formAlbaran(FlaskForm):
  
    Numero = StringField("Numero: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    idProveedor = SelectField('Proveedor: ',  coerce=int)

    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formObra(FlaskForm):
  
    Nombre = StringField("Nombre: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    
    idEstado = SelectField('Estado: ',  coerce=int)
    idCliente = SelectField('Cliente: ',  coerce=int)
    NumeroPedido = StringField("Numero de pedido: ")

    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formObraProducto(FlaskForm):    
    Cantidad = IntegerField('Cantidad: ', default=0, validators=[InputRequired()])
    idProducto = SelectField('Producto: ',  coerce=int)
    idObra = SelectField('Obra: ',  coerce=int)
   
 #   def validate_Cantidad(form, field):
 #       if field == None or field.data < 1:          
 #           raise ValidationError("Cantidad minima 1.") 

    submit = SubmitField('Añadir')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})
    
class formObraAlbaran(FlaskForm):    
    idObra = SelectField('Obra: ',  coerce=int)
    idAlbaran = SelectField('Albaran: ',  coerce=int)
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formOperarioTrabajoRealizado(FlaskForm):    
    idTrabajador = SelectField('Trabajador: ',  coerce=int)
    idTrabajorealizado = SelectField('Trabajo realizado: ',  coerce=int)
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formProductoAlbaran(FlaskForm):    
    idProducto = SelectField('Producto: ',  coerce=int)
    idAlbaran = SelectField('Albarán: ',  coerce=int)
    Cantidad = IntegerField("Cantidad: ", validators=[DataRequired()])
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formTarea(FlaskForm):
    Descripcion = TextAreaField("Descripcion: ", validators=[DataRequired(), Length(min=5, max=500, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    EstadoTarea = SelectField('Estado: ', choices=['--','Asignada', 'En progreso', 'En Pausa', 'En espera de material', 'Finalizada'])
    Notas = TextAreaField("Notas: ")
    idObra = SelectField('Obra: ',  coerce=int)
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})
    
class formTrabajoRealizado(FlaskForm):
    Fecha = DateField('Fecha: ', format='%d-%m-%Y')
    HoraInicio = TimeField('Hora de Inicio',format='%H:%M')
    HoraFin = TimeField('Hora de Fin',format='%H:%M')
    Descripcion = TextAreaField("Descripcion: ", validators=[DataRequired(), Length(min=5, max=500, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    idObra = SelectField('Obra: ',  coerce=int)
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})
    
class formImagenAlb(FlaskForm):
    fotoAlb = FileField('Imagen: ', validators=[FileRequired()])
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')
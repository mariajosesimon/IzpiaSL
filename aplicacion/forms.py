from decimal import Decimal
from distutils import errors
from email import message
from turtle import onclick
from werkzeug.datastructures import MultiDict
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, FileField, TextAreaField, MultipleFileField
from wtforms import SelectField, PasswordField, FloatField, DateField, TimeField, DecimalField, SelectMultipleField
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
    Rol = SelectField('Rol: ', choices=[('--'),('Admin'), ('Trabajador')])
    Usuario = StringField("Usuario: ")
    password = PasswordField('Contraseña: ', validators=[DataRequired()])
 
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
    Precio = FloatField("Precio: ", validators=[DataRequired(),NumberRange(0, 1E+20) ], default=1.00)
    idUnidad = SelectField('Unidad Medida: ',  coerce=int)

    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formAlbaran(FlaskForm):
  
    Numero = StringField("Numero: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    idProveedor = SelectField('Proveedor: ',  coerce=int)
    idObra=SelectField('Obra', coerce=int)
    imagenesAlbaran=MultipleFileField("Imagenes: ")

    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formObra(FlaskForm):
  
    Nombre = StringField("Nombre: ", validators=[DataRequired(), Length(min=3, max=45, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    
    idEstado = SelectField('Estado: ',  coerce=int)
    idCliente = SelectField('Cliente: ',  coerce=int)
    NumeroPedido = StringField("Numero de pedido: ")

    Cantidad = DecimalField('Cantidad: ', default=0.0, validators=[DataRequired(message='no admite letras')], places=2)
    idProducto = SelectField('Producto: ',  coerce=int)
    idObra = SelectField('Obra: ',  coerce=int)
    btn_add = SubmitField('Añadir producto')


    submit = SubmitField('Guardar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formObraProducto(FlaskForm):    
    Cantidad = DecimalField('Cantidad: ', default=0.0, validators=[DataRequired(message='no admite letras')], places=2)
    idProducto = SelectField('Producto: ',  coerce=int)
    idObra = SelectField('Obra: ',  coerce=int)
   
    btn_add = SubmitField('Añadir producto')
    

   # def reset(self):
    #    blankData = MultiDict([ ('csrf', self.reset_csrf()  ) ]) 
     #   self.process(blankData)
   # btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})
    
class formObraAlbaran(FlaskForm):    
    idObra = SelectField('Obra: ',  coerce=int)
    idAlbaran = SelectField('Albaran: ',  coerce=int)
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

# Este formulario se anula. He añadido el campo trabajador en el formTrabajoRealizado.
# class formOperarioTrabajoRealizado(FlaskForm):    
#    idTrabajador = SelectMultipleField('Trabajador: ')
#    idTrabajorealizado = IntegerField('Trabajo realizado: ')
#    submit = SubmitField('Enviar')
#    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

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
    Fecha = DateField('Fecha: ')
    HoraInicio = TimeField('Hora de Inicio',format='%H:%M')
    HoraFin = TimeField('Hora de Fin',format='%H:%M')
    Descripcion = TextAreaField("Descripcion: ", validators=[DataRequired(), Length(min=5, max=500, 
    message='Campo obligatorio. Minimo 5 caracteres.')])
    idObra = SelectField('Obra: ',  coerce=int)
    idTrabajador = SelectMultipleField('Trabajador: ')
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})


    
class formImagenAlb(FlaskForm):
    fotoAlb = FileField('Imagen: ', validators=[FileRequired()])
    upload = SubmitField('Upload')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})

class formSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')

class formLogin(FlaskForm):
    Usuario = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Entrar')

class formChangePassword(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    cancel =SubmitField("No cambiar la contraseña", render_kw={'formnovalidate':True})
    submit = SubmitField('Aceptar')

class formFiltroObra(FlaskForm):
    idObra=SelectField('Obra ', coerce=int)
    submit = SubmitField('Aplicar filtro')
    btn_cancel = SubmitField('Reset filtro')

class formFiltroEstadoObra(FlaskForm):
    idObra=SelectField('Obra ', coerce=int)
    EstadoTarea = SelectField('Estado: ', choices=['All','Asignada', 'En progreso', 'En Pausa', 'En espera de material', 'Finalizada'])
    submit = SubmitField('Aplicar filtro')
    resetFiltro = SubmitField('Reset filtro')
    descargar = SubmitField("Descargar selección")
    
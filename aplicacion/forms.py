
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, validators



class formCliente(FlaskForm):
    Empresa = StringField("Empresa: ")
    CifNif = StringField("Cif: ")
    Direccion = StringField("Direccion: ")
    CP = IntegerField("CP: ")
    Ciudad = StringField("Ciudad: ")
    Provincia = StringField("Provincia: ")
    Telefono = IntegerField("Telefono: ")
    Email = StringField("Email: ", validators.email_validator)
    Contacto = StringField("Contacto: ")
    submit = SubmitField('Enviar')
    btn_cancel = SubmitField('Cancelar', render_kw={'formnovalidate': True})


class formSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')
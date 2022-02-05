import os

from os import abort
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import redirect
import config
from forms import formCliente, formSINO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A0Zr98j/asdf3422a3+/*?)$/abSD3yX R~XHH!jmN]LWX/,?RT'
app.config.from_object( config )


db = SQLAlchemy( app )

# esta importación se hace despues de la conexion a la BD sino, no obtendremos nada.

from models import *

@app.route( '/', methods=['GET', 'POST'] )
def inicio():
    return render_template("inicio.html")

@app.route('/Clientes', methods=['GET', 'POST'] )
def clientes():
    clientes = cliente.query.all()
    return render_template("clientes.html", clientes=clientes)


#Creacion de nuevo cliente.
@app.route('/Clientes/New', methods=['GET', 'POST'])
def clientes_new():

    cli = cliente()
    #recopilacion de datos del cliente
    formNewCliente = formCliente()

    if formNewCliente.submit.data and formNewCliente.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators
    
      #Creacion del cliente para subirlo
        cl = cliente(Empresa=formNewCliente.Empresa.data,
                        CifNif=formNewCliente.CifNif.data,
                        Direccion=formNewCliente.Direccion.data,
                        CP=formNewCliente.CP.data,
                        Ciudad=formNewCliente.Ciudad.data,
                        Provincia=formNewCliente.Provincia.data,
                        Telefono=formNewCliente.Telefono.data,
                        Email=formNewCliente.Email.data,
                        Contacto=formNewCliente.Contacto.data)


        db.session.add(cl)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewCliente.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("clientes_new.html", form=formNewCliente)


@app.route( '/Clientes/<id>/edit', methods=["get", "post"] )
def clientes_edit(id):
    clien = cliente.query.get(id)
    if clien is None:
        abort( 404 )

    formEditCliente = formCliente(obj=clien)
   

    if formEditCliente.validate_on_submit():
        formEditCliente.populate_obj( clien )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "clientes_new.html", form=formEditCliente )

@app.route( '/clientes/<id>/delete', methods=["get", "post"] )
def clientes_delete(id):
    clienteID = clientes.query.get( id )

    # Consultamos si el origen que se quiere eliminar existe en Ranas. Si existe NO se puede eliminar.
    # Integridad referencial.
    consultaExiste = db.session.query( clientes ).filter_by( clienteID=id ).first()

    if clienteID is None:
        abort( 404 )

    form = formSINO()

    if (consultaExiste == None):
        if form.validate_on_submit():

            if form.si.data:
                db.session.delete( clienteID )
                db.session.commit()
            return redirect( url_for( "clientes" ) )

        return render_template( "clientes_delete.html", form=form, cliente=cliente )

    else:

        return redirect( url_for( "clientes" ) )






if __name__ == '__main__':
    app.run()

from asyncio.windows_events import NULL
import os

from os import abort
from pickle import NONE
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

from werkzeug.utils import redirect
import config
from forms import formCliente, formSINO, formProveedor, formTrabajador, formUnidad

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A0Zr98j/asdf3422a3+/*?)$/abSD3yX R~XHH!jmN]LWX/,?RT'
app.config.from_object( config )


db = SQLAlchemy( app )

# esta importación se hace despues de la conexion a la BD sino, no obtendremos nada.

from models import *

@app.route( '/', methods=['GET', 'POST'] )
def inicio():
    return render_template("inicio.html")


####################### CLIENTES #####################################

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
                        Contacto=formNewCliente.Contacto.data,
                        Baja=formNewCliente.Baja.data)


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









####################### PROVEEDORES #####################################
@app.route('/Proveedores', methods=['GET', 'POST'] )
def proveedores():
    proveedores = proveedor.query.all()
    return render_template("proveedores.html", proveedores=proveedores)




#Creacion de nuevo proveedor.
@app.route('/Proveedores/New', methods=['GET', 'POST'])
def proveedores_new():

    prv = proveedor()
    #recopilacion de datos del proveedor
    formNewProveedor = formProveedor()

    if formNewProveedor.submit.data and formNewProveedor.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators
    
      #Creacion del proveedor para subirlo
        pv = proveedor(Empresa=formNewProveedor.Empresa.data,
                        CifNif=formNewProveedor.CifNif.data,
                        Direccion=formNewProveedor.Direccion.data,
                        CP=formNewProveedor.CP.data,
                        Ciudad=formNewProveedor.Ciudad.data,
                        Provincia=formNewProveedor.Provincia.data,
                        Telefono=formNewProveedor.Telefono.data,
                        Email=formNewProveedor.Email.data,
                        Contacto=formNewProveedor.Contacto.data,
                        Baja=formNewProveedor.Baja.data)


        db.session.add(pv)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewProveedor.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("proveedores_new.html", form=formNewProveedor)


@app.route( '/Proveedores/<id>/edit', methods=["get", "post"] )
def proveedores_edit(id):
    prv = proveedor.query.get(id)
    if prv is None:
        abort( 404 )

    formEditProveedor = formProveedor(obj=prv)
   

    if formEditProveedor.validate_on_submit():
        formEditProveedor.populate_obj( prv )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "proveedores_new.html", form=formEditProveedor )


####################### TRABAJADORES #####################################

@app.route('/Trabajadores', methods=['GET', 'POST'] )
def trabajadores():
    trabajadores = trabajador.query.all()
    return render_template("trabajadores.html", trabajadores=trabajadores)

#Creacion de nuevo trabajador.
@app.route('/Trabajadores/New', methods=['GET', 'POST'])
def trabajadores_new():

    trb = trabajador()
    #recopilacion de datos del trabajador
    formNewTrabajador = formTrabajador()

    if formNewTrabajador.submit.data and formNewTrabajador.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators

      #Creacion del trabajador para subirlo
        trb = trabajador(Nombre=formNewTrabajador.Nombre.data,
                        Apellidos=formNewTrabajador.Apellidos.data,
                        Telefono=formNewTrabajador.Telefono.data,
						Baja = formNewTrabajador.Baja.data,
                        Rol = formNewTrabajador.Rol.data,
                        Usuario=formNewTrabajador.Usuario.data,
                        Contrasena = None
                        )

        print(trb.Baja, ' ', trb.Usuario)
        db.session.add(trb)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewTrabajador.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("trabajadores_new.html", form=formNewTrabajador)


@app.route( '/Trabajadores/<id>/edit', methods=["get", "post"] )
def trabajadores_edit(id):
    trb = trabajador.query.get(id)
    if trb is None:
        abort( 404 )

    formEditTrabajador = formTrabajador(obj=trb)
   
    if formEditTrabajador.validate_on_submit():
        formEditTrabajador.populate_obj( trb )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "trabajadores_new.html", form=formEditTrabajador )


####################### UNIDADES #####################################

@app.route('/UnidadMedida', methods=['GET', 'POST'] )
def unidades():
    unidades = unidad.query.all()
    return render_template("unidadMedida.html", unidades=unidades)


@app.route('/UnidadMedida/New', methods=['POST'])
def unidades_new():
    un = unidad()
    if request.method == 'POST':
        un.Unidad = request.form['Unidad']
        db.session.add(un)
        db.session.commit()
        return redirect(url_for("inicio"))
    else:
        return render_template("unidadMedida.html")



@app.route( '/UnidadMedida/<id>/edit', methods=["get", "post"] )
def unidades_edit(id):
    un = unidad.query.get(id)
    if un is None:
        abort( 404 )

    formEditUnidad = formUnidad(obj=un)
   
    if formEditUnidad.validate_on_submit():
        formEditUnidad.populate_obj( un )
        db.session.commit()
        return redirect( url_for( "inicio" ) )
    else:
        return render_template("unidadMedida_edit.html", form=formEditUnidad)
   














if __name__ == '__main__':
    app.run()

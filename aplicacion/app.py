""" Proyecto fin de DAM"""
import os
from csv import excel
from operator import and_
from os import abort
from flask import Flask, render_template, request, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.utils import redirect, secure_filename
import config
from forms import *
from funciones import *
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
import pandas as pd
from openpyxl.workbook import Workbook
import flask_excel as excel
from selenium import webdriver

__name__ = "Izpia S.L."
__version__="1.0.0"
__author__="Mª Jose Simón Rodriguez"

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'A0Zr98j/asdf3422a3+/*?)$/abSD3yX R~XHH!jmN]LWX/,?RT'
app.config['SECRET_KEY'] =  os.urandom(16)
app.config.from_object( config )
#Carpeta para subir imagenes de albaranes
UPLOAD_FOLDER_ALBARAN = '/static/upload/Albaranes/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_ALBARAN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="inicio"
db = SQLAlchemy( app )

# esta importación se hace despues de la conexion a la BD sino, no obtendremos nada.

from models import *

@app.route( '/', methods=['GET', 'POST'] )
def inicio():
    """Inicio del programa.
    Returns:
        html -- devuelve la web de inicio.
    """
    return render_template('inicio.html')

@app.route('/changepassword/<Usuario>', methods=['Get', 'Post'])
def changepassword(username):
    """ Esta funcion nos permite cambiar la contraseña del usuario logado. 

    Args:
        username {String} -- nombre del usuario

    Returns:
        html -- formulario para el cambio de contraseña
    """    
    user=trabajador.query.filter_by(Usuario=form.Usuario.data).first()
    if user is None:
        abort(404)

    form=formChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))

    return render_template("changepassword.html",form=form)


@login_manager.user_loader
def load_user(idTrabajador):
    """Función que se utiliza para cargar los datos del usuario que está logado

    Args:
        idTrabajador {integer} -- id del usuario 

    Returns:
        interger -- id del usuario que esta logado
    """    
    return trabajador.query.get(int(idTrabajador))

####################### CLIENTES #####################################

@app.route('/Clientes', methods=['GET', 'POST'] )
def clientes():
    """ Funcion que devuelve todos los clientes almacenados en la base de datos.

    Returns:
        html de cliente -- muestra un listado de los clientes almacenados en la base de datos.
    """

    clientes = cliente.query.all()
    return render_template("clientes.html", clientes=clientes)

#Creacion de nuevo cliente.
@app.route('/Clientes/New', methods=['GET', 'POST'])
@login_required
def clientes_new():

    """Función para crear nuevos clientes.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Arguments:
        formNewCliente: formulario para la creación de un cliente.

    Returns:
        html con formulario: formulario para crear un cliente. 
    """    
    
    if current_user.is_admin()!="Admin":
        abort(401)
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
@login_required
def clientes_edit(id):

    """Función para editar, modificar un cliente.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Args: 
        id {integer} -- id del cliente
        clien {cliente} -- cliente obtenido en la consulta - cliente.query.get(id)
    Returns:
        html con formulario -- formulario para modificar un cliente.
    """    

    if current_user.is_admin()!="Admin":
        abort(401)
    clien = cliente.query.get(id)
    if clien is None:
        abort( 404 )

    formEditCliente = formCliente(obj=clien)
   

    if formEditCliente.validate_on_submit():
        formEditCliente.populate_obj( clien )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "clientes_new.html", form=formEditCliente )

@app.route('/Clientes/<id>/view', methods=["get", "post"] )
def clientes_view(id):

    """Función para ver, ver un cliente.

    Args: 
        id {integer} -- id del cliente
        clien {cliente} -- cliente obtenido en la consulta - cliente.query.get(id)
    Returns:
        html con formulario: formulario para ver un cliente.
    """    


    clien = cliente.query.get(id)
    if clien is None:
        abort( 404 ) 

    if id=="Volver":
        return redirect( url_for( "inicio" ) )

    return render_template( "clientes_view.html", client=clien )

####################### PROVEEDORES #####################################
@app.route('/Proveedores', methods=['GET', 'POST'] )
def proveedores():
    """ Funcion que devuelve todos los proveedores almacenados en la base de datos.

    Returns:
        html de proveedor -- muestra un listado de los proveedores almacenados en la base de datos.
    """
    
    proveedores = proveedor.query.all()
    return render_template("proveedores.html", proveedores=proveedores)

#Creacion de nuevo proveedor.
@app.route('/Proveedores/New', methods=['GET', 'POST'])
@login_required
def proveedores_new():

    """Función para crear nuevos proveedores.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Arguments:
        formNewProveedor -- formulario para la creación de un proveedor.
        prv {proveedor} -- proveedor

    Returns:
        html con formulario: formulario para crear un proveedor. 
    """   
    if current_user.is_admin()!="Admin":
        abort(401)
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
@login_required
def proveedores_edit(id):

    """Función para editar, modificar un proveedor.
     Se necesita estar logado para acceder a esta función y ser administrador.

    Args: 
        id {integer} -- id del cliente
        prv {proveedor} -- proveedor obtenido en la consulta - proveedor.query.get(id)
    Returns:
        html con formulario -- formulario para modificar un proveedor.
    """    

    if current_user.is_admin()!="Admin":
        abort(401)
    prv = proveedor.query.get(id)
    if prv is None:
        abort( 404 )

    formEditProveedor = formProveedor(obj=prv)

    if formEditProveedor.validate_on_submit():
        formEditProveedor.populate_obj( prv )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "proveedores_new.html", form=formEditProveedor )


@app.route('/Proveedores/<id>/view', methods=["get", "post"] )
def proveedores_view(id):

    """Función para ver, ver un proveedor.

    Args: 
        id {integer} -- id del proveedor
        prv {proveedor} -- proveedor obtenido en la consulta - proveedor.query.get(id)
    Returns:
        html con formulario: formulario para ver un proveedor.
    """    

    prv = proveedor.query.get(id)
    if prv is None:
        abort( 404 ) 

    if id=="Volver":
        return redirect( url_for( "inicio" ) )

    return render_template( "proveedores_view.html", provee=prv )

####################### TRABAJADORES #####################################

@app.route('/Trabajadores', methods=['GET', 'POST'] )
def trabajadores():

    """ Funcion que devuelve todos los trabajadores almacenados en la base de datos.

    Returns:
        html de trabajador -- muestra un listado de los trabajadores almacenados en la base de datos.
    """
    trabajadores = trabajador.query.all()
    return render_template("trabajadores.html", trabajadores=trabajadores)

#Creacion de nuevo trabajador.
@app.route('/Trabajadores/New', methods=['GET', 'POST'])
@login_required
def trabajadores_new():

    """Función para crear nuevos trabajadores.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Arguments:
        formNewtrabajador -- formulario para la creación de un trabajador.
        trb {trabajador} -- trabajador

    Returns:
        html con formulario: formulario para crear un trabajador. 
    """   
    if current_user.is_admin()!="Admin":
        abort(401)

    trb = trabajador()
    #recopilacion de datos del trabajador
    formNewTrabajador = formTrabajador()

    if formNewTrabajador.submit.data and formNewTrabajador.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators

      #Creacion del trabajador para subirlo
        #trb=trabajador()

        trb.Nombre=formNewTrabajador.Nombre.data
        trb.Apellidos=formNewTrabajador.Apellidos.data
        trb.Telefono=formNewTrabajador.Telefono.data
        trb.Baja = formNewTrabajador.Baja.data
        trb.Rol = formNewTrabajador.Rol.data
        trb.Usuario=formNewTrabajador.Usuario.data
        trb.password = formNewTrabajador.password.data

        db.session.add(trb)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewTrabajador.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("trabajadores_new.html", form=formNewTrabajador, trabajador=trb)


@app.route( '/Trabajadores/<id>/edit', methods=["get", "post"] )
@login_required
def trabajadores_edit(id):

    """Función para editar, modificar un trabajador.
     Se necesita estar logado para acceder a esta función y ser administrador.

    Args: 
        id {integer} -- id del cliente
        trb {trabajador} -- trabajador obtenido en la consulta - trabajador.query.get(id)
    Returns:
        html con formulario -- formulario para modificar un trabajador.
    """    

    if current_user.is_admin()!="Admin":
        abort(401)
    trb = trabajador.query.get(id)
    if trb is None:
        abort( 404 )

    formEditTrabajador = formTrabajador(obj=trb)
    #No quiero que desde la modificación se pueda modificar la contraseña.
    del formEditTrabajador.password
   
    if formEditTrabajador.validate_on_submit():
     
        formEditTrabajador.populate_obj( trb )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "trabajadores_new.html", form=formEditTrabajador, trabajador=trb )


#Funcion para que un usuario "Administrador" pueda cambiar la
# contraseña de un trabajador si éste no se acuerda de su propia contraseña

@app.route('/Trabajadores/<id>/changepassword', methods=["get", "post"] )
def trabajadores_changepassword(id):
    trb = trabajador.query.get(id)
        
    formChangePass = formChangePassword()
    if formChangePass.validate_on_submit():
        formChangePass.populate_obj(trb)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formChangePass.cancel.data:
        return redirect(url_for("inicio"))
    
    return render_template( "changepassword.html", form=formChangePass, trabajador=trb )


####################### UNIDADES #####################################

@app.route('/UnidadMedida', methods=['GET', 'POST'] )
@login_required
def unidades():
    """ Funcion que devuelve todos las unidades almacenadas en la base de datos.

    Returns:
        html de unidades -- muestra un listado de las unidades almacenados en la base de datos.
    """
    if current_user.is_admin()!="Admin":
        abort(401)
    unidades = unidad.query.all()
    return render_template("unidadMedida.html", unidades=unidades)

@app.route('/UnidadMedida/New', methods=['POST'])
@login_required
def unidades_new():

    """Función para crear nuevas unidades.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Returns:
        html con formulario: formulario para crear una unidad. 
    """  
    if current_user.is_admin()!="Admin":
        abort(401)
    un = unidad()
    if request.method == 'POST':
        un.Unidad = request.form['Unidad']
        db.session.add(un)
        db.session.commit()
        return redirect(url_for("inicio"))
    else:
        return render_template("unidadMedida.html")

@app.route( '/UnidadMedida/<id>/edit', methods=["get", "post"] )
@login_required
def unidades_edit(id):

    """Función para editar, modificar una unidad.
     Se necesita estar logado para acceder a esta función y ser administrador.

    Args: 
        id {integer} -- id de la unidad
        un {unidad} -- unidad obtenido en la consulta - unidad.query.get(id)
    Returns:
        html con formulario -- formulario para modificar una unidad.
    """   
    if current_user.is_admin()!="Admin":
        abort(401)
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
   
####################### PRODUCTOS #####################################


@app.route('/Productos', methods=['GET', 'POST'] )
def productos():

    """ Funcion que devuelve todos los productos almacenados en la base de datos.

    Returns:
        html de productos -- muestra un listado de los productos almacenados en la base de datos.
    """
    productos = producto.query.all()
    um = unidad.query.all()
    return render_template("productos.html", productos=productos, unidadMedida=um)

#Creacion de nuevo producto.
@app.route('/Productos/New', methods=['GET', 'POST'])
@login_required
def productos_new():
    """Función para crear nuevos productos.
    Se necesita estar logado para acceder a esta función.

    Arguments:
        formNewProducto -- formulario para la creación de un producto.
        prd {producto} -- producto

    Returns:
        html con formulario: formulario para crear un producto. 
    """   

    prd = producto()
    #recopilacion de datos del producto
    formNewProducto = formProducto()

    # Añado mi listado de medidas al select / choices definidos en el form de Producto 
    formNewProducto.idUnidad.choices = listaunidades()


    if formNewProducto.submit.data and formNewProducto.validate():
        #validacion de los campos según nuestro form, que hemos puesto Validators
    
      #Creacion del producto para subirlo
        prd = producto(Nombre=formNewProducto.Nombre.data,
                        Precio=formNewProducto.Precio.data,
                        idUnidad=formNewProducto.idUnidad.data)

      
        db.session.add(prd)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewProducto.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("productos_new.html", form=formNewProducto )

@app.route( '/Productos/<id>/edit', methods=["get", "post"] )
@login_required
def productos_edit(id):

    """Función para editar, modificar un producto.
     Se necesita estar logado para acceder a esta función.

    Args: 
        id {integer} -- id del producto
        prd {producto} -- producto obtenido en la consulta - producto.query.get(id)
    Returns:
        html con formulario -- formulario para modificar un producto.
    """  

    prd = producto.query.get(id)
    if prd is None:
        abort( 404 )

    formEditProducto = formProducto(obj=prd)
    
    # Añado mi listado de medidas al select / choices definidos en el form de Producto 
    # ver funciones.listaunidades. 
    formEditProducto.idUnidad.choices= listaunidades()
   

    if formEditProducto.validate_on_submit():
        formEditProducto.populate_obj( prd )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "productos_new.html", form=formEditProducto )

####################### ESTADOS #####################################

@app.route('/Estado', methods=['GET', 'POST'] )
@login_required
def estados():
    """ Funcion que devuelve todos los estados almacenadas en la base de datos.

    Returns:
        html de estados -- muestra un listado de los estados almacenados en la base de datos.
    """
    if current_user.is_admin()!="Admin":
        abort(401)
    estados = estado.query.all()
    return render_template("estados.html", estados=estados)

@app.route('/Estado/New', methods=['POST'])
@login_required
def estados_new():
    """Función para crear nuevos estados.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Returns:
        html con formulario: formulario para crear un estado. 
    """  
    if current_user.is_admin()!="Admin":
        abort(401)
    es = estado()
    if request.method == 'POST':
        es.Estado = request.form['Estado']
        db.session.add(es)
        db.session.commit()
        return redirect(url_for("inicio"))
    else:
        return render_template("estados.html")

@app.route( '/Estado/<id>/edit', methods=["get", "post"] )
@login_required
def estados_edit(id):
    """Función para modificar nuevos estados.
    Se necesita estar logado para acceder a esta función y ser administrador.

    Returns:
        html con formulario: formulario para modificar un estado. 
    """  
    if current_user.is_admin()!="Admin":
        abort(401)
    es = estado.query.get(id)
    if es is None:
        abort( 404 )

    formEditEstado = formEstado(obj=es)
    
    if formEditEstado.validate_on_submit():
      
        formEditEstado.populate_obj( es )
        db.session.commit()
        return redirect( url_for( "inicio" ) )
    else:
        return render_template("estados_edit.html", form=formEditEstado)


####################### ALBARANES #####################################

@app.route('/Albaranes', methods=['GET', 'POST'] )
@app.route('/Albaranes/filter', methods=['POST'] )
def albaranes():

    """Funcion para listar todos los albaranes almacenados y posibilidad de filtrarlos. 

    Args:
        albaranes {albaran} -- consulta para mostrar albaranes
        proveedores {proveedor} -- consulta para mostrar proveedores
        obras {obra} -- consulta para mostrar obras
        filtroAlb {albaran} -- muestra lo albaranes filtrados por obras.


    Returns:
        html: muestra los albaranes filtrados. 
    """


    albaranes = albaran.query.all()
    proveedores = proveedor.query.all()
    obras=obra.query.all()
    filtroAlbaranXObra=formFiltroObra()
    filtroAlbaranXObra.idObra.choices=listaobras()
    if filtroAlbaranXObra.submit.data:
        idOb=filtroAlbaranXObra.idObra.data
        albaranes= db.session.query(albaran).filter(albaran.idObra==idOb).all()
    elif filtroAlbaranXObra.btn_cancel.data:
        filtroAlbaranXObra.idObra.data=0
        filtroAlb=filtroAlbaranXObra
        albaranes=db.session.query(albaran)
       
    
    return render_template("albaranes.html", albaranes=albaranes, proveedores=proveedores, obras=obras, filtroAlb=filtroAlbaranXObra)

#Creacion de nuevo albaran.
@app.route('/Albaranes/New', methods=['GET', 'POST'])
@login_required
def albaranes_new():

    """
    Función para crear un albarán. Se requiere estar logado

    Arg:
        alb {albaran} -- albaran creado
        listaproveedores {proveedor} -- llama a la funcion listaproveedores() para mostrar todos los proveedores
        listaobras {obra} -- llama a la funcion listaobras() para mostrar todos las obras

    Returns:
        html -- formulario para crear un albarán.

    """    

    alb = albaran()
    #recopilacion de datos del albaran
    formNewAlbaran = formAlbaran()  

	# Añado el listado de los proveedores al formulario.
    # He creado un archivo donde recojo las funciones que utilizo. 
    formNewAlbaran.idProveedor.choices = listaproveedores()
    formNewAlbaran.idObra.choices = listaobras()

    if formNewAlbaran.submit.data and formNewAlbaran.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators

      #Creacion del albaran para subirlo
        alb = albaran(Numero=formNewAlbaran.Numero.data,
                       idProveedor=formNewAlbaran.idProveedor.data,
                       idObra=formNewAlbaran.idObra.data)             

        db.session.add(alb)
        db.session.commit()
        db.session.flush()
        db.session.refresh(alb)

        return redirect(url_for("inicio"))
    elif formNewAlbaran.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("albaranes_new.html", form=formNewAlbaran, alb = alb)


@app.route( '/Albaranes/<id>/edit', methods=["get", "post"] )
@login_required
def albaranes_edit(id):

    """
    Función para modificar un albarán. Se requiere estar logado

    Arg:
        alb {albaran} -- albaran a modificar
        listaproveedores {proveedor} -- llama a la funcion listaproveedores() para mostrar todos los proveedores
        listaobras {obra} -- llama a la funcion listaobras() para mostrar todos las obras
        imagenes {blob} -- necesito mostrar las imagenes del albarán.

    Returns:
        html -- formulario para editar un albarán.

    """    
    alb = albaran.query.get(id)
    if alb is None:
        abort( 404 )

    formEditAlbaran = formAlbaran(obj=alb)	
    # Añado el listado de los proveedores al formulario
    formEditAlbaran.idProveedor.choices = listaproveedores()

    #Añadir el listado de obras al formulario
    formEditAlbaran.idObra.choices=listaobras()
    #form para añadir la imagen. 
    #formImagenAlbaran = formImagenAlb()

   
    #Añadir 1 imagen 
   # if formImagenAlbaran.upload:
   #    print("estoy en el form")
   #    try:
   #           print("en el try")
   #          f = formImagenAlbaran.fotoAlb.data
   #         nombre_fichero=secure_filename(f.filename)
   #         f.save(app.root_path+app.config['UPLOAD_FOLDER']+nombre_fichero)
   #     except:
   #         print("en exept")
   #         nombre_fichero=""
   #
   #       imagenDeAlbaran=imagenalbaran()
   #       #https://stackoverflow.com/questions/39112238/sqlalchemy-insert-string-argument-without-an-encoding
   #        #para codificar el nombre del archivo hay que añadir str.enconde(nombrearchivo)
   #       imagenDeAlbaran.fotoAlb=str.encode(nombre_fichero)
   #       imagenDeAlbaran.idAlbaran=alb.idAlbaran
   #       db.session.add(imagenDeAlbaran)
   #      db.session.commit()
            

    # tutorial para subir varias imagenes:
    # https://tutorial101.blogspot.com/2021/01/python-flask-upload-multiple-images-and.html

    #Tengo que mostrar las imagenes guardadas del albaran. El nombre. 
    # llamo a la funcion imagenes_albaran()

    imagenes=imagenes_albaran(id)
    
    
    if formEditAlbaran.submit.data:
        #files = request.files.getlist('files[]')
        #print(files)
        pics = request.files.getlist(formEditAlbaran.imagenesAlbaran.name)
        files = formEditAlbaran.imagenesAlbaran.data
               
        for file in files:
            if file and allowed_file(file.filename):
                #Guardamos la imagen del albaran.
                filename = secure_filename(file.filename)
                file.save(app.root_path+app.config['UPLOAD_FOLDER']+filename)

                imagenDeAlbaran=imagenalbaran()
        #https://stackoverflow.com/questions/39112238/sqlalchemy-insert-string-argument-without-an-encoding
        #para codificar el nombre del archivo hay que añadir str.enconde(nombrearchivo)
                #imagenDeAlbaran.fotoAlb=str.encode(filename)
                imagenDeAlbaran.nombreImagen=filename
                imagenDeAlbaran.fotoAlb=str.encode(filename) 
                imagenDeAlbaran.idAlbaran=alb.idAlbaran
                db.session.add(imagenDeAlbaran)
                db.session.commit()
                formEditAlbaran.populate_obj( alb )
                db.session.commit()

                      
        return redirect( url_for( "inicio" ) )
    elif formEditAlbaran.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template( "albaranes_new.html", form=formEditAlbaran,  alb=alb, imagenes=imagenes )
   
@app.route('/deleteImagenAlbaran/<idImagenAlbaran>/<idAlbaran>', methods=["get", "post"] )
@login_required
def deleteImagenAlbaran(idImagenAlbaran, idAlbaran):

    """Funcion para eliminar una imagen de albarán que se ha subido por error.

    Returns:
        html: regresa a la edición del albarán. 
    """

    alb = albaran.query.get(idAlbaran)
    if alb is None:
        abort( 404 )

    imagen = imagenalbaran.query.get(idImagenAlbaran)
    if idImagenAlbaran!="":
        os.remove(app.root_path+"/static/upload/Albaranes/"+imagen.nombreImagen)
    db.session.delete(imagen)
    db.session.commit()
  

    return redirect( url_for("albaranes_edit", id=idAlbaran ))



####################### TAREAS #####################################

@app.route('/Tareas', methods=['GET', 'POST'] )
def tareas():

    """Función para listar todas las tareas almacenadas en la base de datos. 
    Revisar si se desea descargar un excel. Y como hacerlo. 
    Args:
        tareas {tarea} -- muestra todas las tareas
        obras {obra} -- muestra todas las obras.
        filtroTareaXObrayEstado {tarea} -- filtro en tareas por obras y/o estados.

    Returns:
        html: muestra las tareas creadas con su estado, para la obra que son
    """

    tareas = tarea.query.all()
    obras = obra.query.all()
    filtroTareaXObrayEstado=formFiltroEstadoObra()
    filtroTareaXObrayEstado.idObra.choices=listaobras()

    column_names = ['idTarea1','Descripcion1', 'EstadoTarea1', 'Notas1', 'idObra1']

    if filtroTareaXObrayEstado.submit.data:
        idOb=filtroTareaXObrayEstado.idObra.data
        estado = filtroTareaXObrayEstado.EstadoTarea.data
        
        if filtroTareaXObrayEstado.idObra.data==0 and filtroTareaXObrayEstado.EstadoTarea.data == 'All':
            tareas=db.session.query(tarea)
        elif filtroTareaXObrayEstado.idObra.data!=0 and filtroTareaXObrayEstado.EstadoTarea.data == 'All':
            tareas=db.session.query(tarea).filter(tarea.idObra==idOb)
        elif filtroTareaXObrayEstado.idObra.data ==0 and filtroTareaXObrayEstado.EstadoTarea.data != 'All':
            tareas=db.session.query(tarea).filter(tarea.EstadoTarea==estado) 
        elif filtroTareaXObrayEstado.idObra.data !=0 and filtroTareaXObrayEstado.EstadoTarea.data != 'All':
            tareas= db.session.query(tarea).filter(and_(tarea.idObra==idOb, tarea.EstadoTarea==estado) ).all()
    
    elif filtroTareaXObrayEstado.resetFiltro.data:
        idOb=0
        estado='All'
        filtroTareaXObrayEstado.idObra.data=idOb
        filtroTareaXObrayEstado.EstadoTarea.data = 'All'
        filtroTaskXObrayEstado=filtroTareaXObrayEstado
        tareas=db.session.query(tarea)

    elif filtroTareaXObrayEstado.descargar.data:

        idOb=filtroTareaXObrayEstado.idObra.data
        estado = filtroTareaXObrayEstado.EstadoTarea.data
        consulta=''

        print("Filtros: ")
        print(filtroTareaXObrayEstado.idObra.data)
        print(filtroTareaXObrayEstado.EstadoTarea.data)
        
        
        if filtroTareaXObrayEstado.idObra.data==0 and filtroTareaXObrayEstado.EstadoTarea.data == 'All':
            print("en filtro")
            consulta=db.session.query(tarea)
            print(consulta)
            resultadoidTarea=[]
            resultadoDescripcion=[]
            resultadoEstadoTarea=[]
            resultadoNotas=[]
            resultadoidObra=[]
            
            resultadoDicc={}
            for a in consulta:
                #print(a.Descripcion)
                resultadoidTarea.append(a.idTarea)
                resultadoDescripcion.append(a.Descripcion)
                resultadoEstadoTarea.append(a.EstadoTarea)
                resultadoNotas.append(a.Notas)
                resultadoidObra.append(a.idObra)

            resultadoDicc['idTarea']=resultadoidTarea
            resultadoDicc['Descripcion']=resultadoDescripcion
            resultadoDicc['EstadoTarea']=resultadoEstadoTarea
            resultadoDicc['Notas']=resultadoNotas
            resultadoDicc['idObra']=resultadoidObra
                
            df = pd.DataFrame(resultadoDicc)
            op = webdriver.ChromeOptions() 
            prefs = {'download.default_directory' : 'd:\\user\\Dercargas\\'}
            op.add_experimental_option('prefs', prefs)
           
            #driver = webdriver.Chrome(executable_path=driver_path, options=op)
            

            df.to_excel('d:/prueba2.xlsx')

           
           
            
            
        elif filtroTareaXObrayEstado.idObra.data!=0 and filtroTareaXObrayEstado.EstadoTarea.data == 'All':
            return excel.make_response_from_query_sets(db.session.query(tarea).filter(tarea.idObra==idOb), column_names, "xlsx")
        elif filtroTareaXObrayEstado.idObra.data ==0 and filtroTareaXObrayEstado.EstadoTarea.data != 'All':
            return excel.make_response_from_query_sets(db.session.query(tarea).filter(tarea.EstadoTarea==estado) , column_names, "xlsx")
        elif filtroTareaXObrayEstado.idObra.data !=0 and filtroTareaXObrayEstado.EstadoTarea.data != 'All':
            return excel.make_response_from_query_sets(db.session.query(tarea).filter(and_(tarea.idObra==idOb, tarea.EstadoTarea==estado) ).all(), column_names, "xlsx")

              
    return render_template("tareas.html", tareas=tareas, obras=obras, filtroTaskXObrayEstado= filtroTareaXObrayEstado)

#Creacion de nuevo tarea.
@app.route('/Tareas/New', methods=['GET', 'POST'])
@login_required
def tareas_new():
  
    """
    Función para crear una tarea. Se requiere estar logado

    Arg:
        tar {tarea} -- tarea a crear
        listaobras {obra} -- llama a la funcion listaobras() para mostrar todos las obras

    Returns:
        html -- formulario para crear una tarea.

    """    
    tar = tarea()
    #recopilacion de datos del tarea
    formNewTarea = formTarea()

	# Añado el listado de los obras al formulario.
    # He creado un archivo donde recojo las funciones que utilizo. 
   
    formNewTarea.idObra.choices = listaobras()



    if formNewTarea.submit.data and formNewTarea.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators


      #Creacion del tarea para subirlo
        tar = tarea(Descripcion=formNewTarea.Descripcion.data,
					EstadoTarea = formNewTarea.EstadoTarea.data,
					Notas = formNewTarea.Notas.data,
                    idObra=formNewTarea.idObra.data)             

        db.session.add(tar)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewTarea.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("tareas_new.html", form=formNewTarea)


@app.route( '/Tareas/<id>/edit', methods=["get", "post"] )
@login_required
def tareas_edit(id):
    """
    Función para modificar un albarán. Se requiere estar logado

    Arg:
        tar {tarea} -- tarea a modificar
        listaobras {obra} -- llama a la funcion listaobras() para mostrar todos las obras

    Returns:
        html -- formulario para modificar una tarea.

    """  

    tar = tarea.query.get(id)
    if tar is None:
        abort( 404 )

    formEditTarea = formTarea(obj=tar)	
	
	# Añado el listado de los obras al formulario
    formEditTarea.idObra.choices = listaobras()
   
    if formEditTarea.validate_on_submit():
        formEditTarea.populate_obj( tar )
        db.session.commit()
        return redirect( url_for( "inicio" ) )

    return render_template( "tareas_new.html", form=formEditTarea )

####################### OBRAS #####################################

@app.route('/Obras', methods=['GET', 'POST'] )
def obras():

    """Función para listar todas las obras  almacenadas en la base de datos. 
  
    Args:
        clientes {cliente} -- muestra todos los clientes 
        obras {obra} -- muestra todas las obras.
        estados {estado} -- muestra todos los estados.

    Returns:
        html: muestra las obras creadas con su estado y para el cliente.
    """

    obras = obra.query.all()
    clientes = cliente.query.all()
    estados = estado.query.all()
    return render_template("obras.html", obras=obras, clientes=clientes, estados=estados)


#Creacion de nuevo obra.
@app.route('/Obras/New', methods=['GET', 'POST'])
@login_required
def obras_new():

    """
    Función para crear una obra. Se requiere estar logado

    Arg:
        ob {obra} -- obra a crear
        listaclientes {cliente} -- llama a la funcion listaclientes() para mostrar todos los clientes
        listaestados {estado} -- llama a la funcion listaestados() para mostrar todos los estados
        formAddProducto {formObraProducto} -- requerimos añadir los productos necesarios para la obra. 
        Utilizo un formulario para añadir los productos.

    Returns:
        html -- formulario para crear una obra.

    """

    if current_user.is_admin()!="Admin":
        abort(401)
    ob = obra()
    #recopilacion de datos del obra
    formNewObra = formObra()
	
	# Añado el listado de los obras al formulario.
    # He creado un archivo donde recojo las funciones que utilizo. 
   
    formNewObra.idCliente.choices = listaclientes()
    formNewObra.idEstado.choices = listaestados()
    formAddProducto = formObraProducto()
    

    if formNewObra.submit.data and formNewObra.validate():
            #validacion de los campos según nuestro form, que hemos puesto Validators


      #Creacion del obra para subirlo
        ob = obra(Nombre=formNewObra.Nombre.data,
					idEstado = formNewObra.idEstado.data,
					idCliente = formNewObra.idCliente.data,
                    NumeroPedido=formNewObra.NumeroPedido.data)             

        db.session.add(ob)
        db.session.commit()
        return redirect(url_for("inicio"))
    elif formNewObra.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("obras_new.html", form=formNewObra, obr=ob, formularioProductos = formAddProducto)


@app.route( '/Obras/<id>/edit', methods=["get", "post"] )
@login_required
def obras_edit(id):

    """
    Función para crear una obra. Se requiere estar logado

    Arg:
        ob {obra} -- obra a modificar
        listaclientes {cliente} -- llama a la funcion listaclientes() para mostrar todos los clientes.
        listaestados {estado} -- llama a la funcion listaestados() para mostrar todos los estados.
        listaproductos {producto} -- llama a la funcion listaproductos() para mostrar todos los productos.
        formAddProducto {formObraProducto} -- requerimos añadir los productos necesarios para la obra. 
            Utilizo un formulario para añadir los productos.
        productosSeleccionados {sumaProductos} -- llama a la funcion sumaProductos enviando la obra en la que se encuentra.
            Suma la cantidad de los productos utilizados por producto. 
        albaranes {albarán} -- muestra en una segunda pestaña los albaranes asociados a la obra con su imagen. 
        resultadoTareasObra {resultadoTarObr} --  Necesito mostrar las tareas realizadas en la obra y su estado. 
    Returns:
        html -- formulario para crear una obra.

    """

    #Obra seleccionada.
    ob = obra.query.get(id)
    #Necesito saber el cliente para mostrarlo. 
    client = cliente.query.get(ob.idCliente)
    if ob is None:
        abort( 404 )

    #asigno todos los campos con los que he recuperado de la query. 
    formEditObra = formObra(obj=ob)	
	
	# Añado los listados de clientes, estado y productos al formulario
    formEditObra.idCliente.choices = listaclientes()
    formEditObra.idEstado.choices = listaestados()
    formEditObra.idProducto.choices=listaproductos()
    
    #Necesito mostrar las tareas realizadas en la obra y su estado. 
    resultadoTareasObra = resultadoTarObr(id)

    #Sumo cantidades por producto que se han comprado para la obra escogida. 
    productosSeleccionados = sumaProductos(id)

    #Necesito mostrar los productos.
    products = producto.query.all()
    albaranes = albs(id)   
   #for a in albaranes:
    #    print(a[0], " - ", a[1], " - ", a[2])

    if formEditObra.btn_add.data:
        # Añadimos un producto a la obra. 
       

        if formEditObra.idObra.data!=None:
        
            #Guaro en la base de datos el producto, la cantidad y la obra - tabla: obraproducto
            obrPrd = obraproducto(Cantidad=formEditObra.Cantidad.data,
                    idProducto = formEditObra.idProducto.data,
                    idObra = formEditObra.idObra.data)
      
            db.session.add(obrPrd)
            db.session.commit()
        

            return render_template("obras_new.html",
        form=formEditObra,
        obr = ob,
        productosSeleccionados=sumaProductos(id), 
        products= products, client=client, 
        resultadoTareasObra = resultadoTareasObra, albaranes=albaranes )

    elif formEditObra.submit.data:
       
        formEditObra.populate_obj( ob )
        db.session.commit()
        return redirect( url_for( "inicio" ) )
    elif formEditObra.btn_cancel.data:
       
        
        return redirect( url_for( "inicio" ) )
    else:
      
            
        return render_template("obras_new.html",
        form=formEditObra,
        obr = ob,
        productosSeleccionados=sumaProductos(id), 
        products= products, client=client, 
        resultadoTareasObra = resultadoTareasObra, albaranes=albaranes )


####################### TRABAJOS REALIZADOS #####################################

@app.route('/TrabajosRealizados', methods=['GET', 'POST'] )
def trabajosrealizados():

    """Función para listar todas los trabajos realizados por los operarios almacenadas en la base de datos. 
    Args:
        trabajosrealizados {trabajorealizado} -- muestro todos los trabajs realizados.
        obras {obra} -- muestra todas las obras.

    Returns:
        html: muestra los trabajos realizados creadas con su estado, para la obra que son
    """


    trabajosrealizados = trabajorealizado.query.all()
    obras = obra.query.all()
   
    return render_template("trabajosrealizados.html", trabajosrealizados=trabajosrealizados, obras = obras)


#Creacion de nuevo trabajorealizado.
@app.route('/TrabajosRealizados/New', methods=['GET', 'POST'])
@login_required
def trabajosrealizados_new():

    """
    Función para crear un trabajo realizado. Se requiere estar logado

    Arg:
        tr {trabajorealizado} -- creación del trabajo a realizar 
        listaobras {obra} -- llama a la funcion listaobras() para mostrar todos las obras
        listatrabajadores {trabajador} -- llama a la funcion listatrabajadores() para mostrar todos los trabajadores
        
    Returns:
        html -- formulario para crear un trabajo realizado.

    """

    tr = trabajorealizado()
    #recopilacion de datos del trabajorealizado
    formNewTrabajosRealizados = formTrabajoRealizado()
    formNewTrabajosRealizados.idObra.choices = listaobras()
    formNewTrabajosRealizados.idTrabajador.choices=listatrabajadores()
   

    if formNewTrabajosRealizados.submit.data:
            #validacion de los campos según nuestro form, que hemos puesto Validators

      #Creacion del trabajorealizado para subirlo
        tr = trabajorealizado(Fecha=formNewTrabajosRealizados.Fecha.data,
					HoraInicio=formNewTrabajosRealizados.HoraInicio.data,		
					HoraFin=formNewTrabajosRealizados.HoraFin.data,
					Descripcion=formNewTrabajosRealizados.Descripcion.data,
                    idObra=formNewTrabajosRealizados.idObra.data)             

        db.session.add(tr)
        db.session.commit()
        
        ## UTILIZACION DEL ID NECESARIO, EL CORRELATIVO.
        # https://www.iteramos.com/pregunta/63587/sqlalchemy-flush-y-obtener-id-insertado
        db.session.flush()
        db.session.refresh(tr)

        for a in formNewTrabajosRealizados.idTrabajador.data:
            to = operariotrabajorealizado(idTrabajador=a, 
                idTrabajoRealizado=tr.idTrabajoRealizado)
            db.session.add(to)
            db.session.commit()

        return redirect(url_for("inicio"))
    elif formNewTrabajosRealizados.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template("trabajosrealizados_new.html", form=formNewTrabajosRealizados, 
        trabajorealizado = tr)

@app.route( '/TrabajosRealizados/<id>/edit', methods=["get", "post"] )
@login_required
def trabajosrealizados_edit(id):

    """
    Función para modificar un trabajo realizado. Se requiere estar logado

    Arg:
        tr {trabajorealizado} -- modificación del trabajo a realizar 
        ob {obra} -- selecciono la obra a la que pertenece el trabajo realizado
        operarios {trabajador} -- selección de los trabajadores que están realizando el trabajo.         
    Returns:
        html -- formulario para modificar un trabajo realizado.

    """

    tr = trabajorealizado.query.get(id)
    if tr is None:
        abort( 404 )

    formEditTrabajosRealizados = formTrabajoRealizado(obj=tr)	

    #Necesito saber la obra para mostrarla. 
    ob = obra.query.get(tr.idObra)
    
	
	# Añado el listado de los obras al formulario
    formEditTrabajosRealizados.idObra.choices = listaobras()
    
    #Necesito saber los operarios que han realizado la tarea.
    
    operarios = db.session.query(trabajador.Nombre).join(operariotrabajorealizado, operariotrabajorealizado.idTrabajador==trabajador.idTrabajador).filter(operariotrabajorealizado.idTrabajoRealizado==id)   

    formEditTrabajosRealizados.idTrabajador.choices=operarios
   
    if formEditTrabajosRealizados.submit.data:
        formEditTrabajosRealizados.populate_obj( tr )
        db.session.commit()
        return redirect( url_for( "inicio" ) )
    
    elif formEditTrabajosRealizados.btn_cancel.data:
        return redirect(url_for("inicio"))
    else:
        return render_template( "trabajosrealizados_new.html",
     form=formEditTrabajosRealizados, 
     operarios=operarios,
    trabajorealizado = tr, ob=ob)


################################ LOGIN #######################################

@app.route('/login', methods=['get', 'post'])
def login():

    """Funcion para logarse.

    Returns:
        html: formulario para logarse
    """

    formularioLogarse = formLogin()
    if formularioLogarse.validate_on_submit():
        user=trabajador.query.filter_by(Usuario=formularioLogarse.Usuario.data).first()
        if user!=None and user.verify_password(formularioLogarse.password.data):
            login_user(user)
            return redirect(url_for('inicio'))
    	
        formularioLogarse.Usuario.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', formularioLogarse=formularioLogarse)
@app.route("/logout")
def logout():
    """Funcion para deslogarse.

        Returns:
            html: formulario para deslogarse
    """
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(idTrabajador):

    """ Funcion necesaria para saber qué usuario trabajador está logueado en cada momento.
    Returns:
        integer -- id del trabajador logado
    """    
    return trabajador.query.get(int(idTrabajador))

@app.errorhandler(404)
def page_not_found(error):
	return render_template("error.html",error="Página no encontrada..."), 404

@app.errorhandler(401)
def page_not_found(error):
	return render_template("error.html",error="No tienes permiso"), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0")

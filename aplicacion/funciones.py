from forms import *
from models import *
#from app import auto

#@auto.doc()
def listaproveedores():
    # Tengo que crear un select que será un list para que muestre todos los proveedores
    return [(p.idProveedor, p.Empresa) for p in proveedor.query.all()]
#@auto.doc()
def listaunidades():
 # Tengo que crear un select que será un list para las unidades de medida.
    return [(u.idUnidad, u.Unidad) for u in unidad.query.all()]
#@auto.doc()
def listaestados():
    return [(e.idEstado, e.Estado) for e in estado.query.all()]
#@auto.doc()
def listaclientes():
    return [(c.idCliente, c.Empresa) for c in cliente.query.all()]
#@auto.doc()
def listaproductos():
    return [(pd.idProducto, pd.Nombre) for pd in producto.query.order_by(producto.Nombre.asc()).all()]
#@auto.doc()
def listatrabajadores():
    return [(t.idTrabajador, t.Nombre) for t in trabajador.query.all()]
#@auto.doc()		
def listaalbaranes():
    return [(alb.idAlbaran, alb.Numero) for alb in albaran.query.all()]
#@auto.doc()	
def listaobras():
    listadoObras=[(0, 'All')]
    for o in obra.query.all():
        listadoObras.append([o.idObra, o.Nombre])
    return listadoObras
#@auto.doc()
def listatrabajosrealizados():
    return [(tr.idTrabajorealizado, tr.Descripcion, tr.Fecha) for tr in trabajorealizado.query.all()]		


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf', 'docx'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
#@auto.doc()	
def imagenes_albaran(id):
    """ Funcion que recibe el id del albaran y devuelve las imagenes asociadas a ese id de albaran.

    Arguments:
        id {integer} -- id del albarán.
    Return:
        imagenes {[blob]} -- devuelve las imagenes asociadas al id del albaran.
    """
    imagenes=db.session.query(imagenalbaran.idImagenAlbaran, imagenalbaran.nombreImagen).filter(imagenalbaran.idAlbaran==id)
    return imagenes
#@auto.doc()
def resultadoTarObr(id):
    """Función que devuelve las tareas asociadas a la obra.

    Arguments:
        id {integer} -- id de la obra.
    Returns:
        resultadoTareasObra {[TareasObras]} -- devulve las tareas que tiene asociada la obra.
    """
    resultadoTareasObra = db.session.query(tarea.Descripcion, tarea.Notas, tarea.EstadoTarea).filter(tarea.idObra==id)
    return resultadoTareasObra
#@auto.doc()
def sumaProductos(id):

    """Funcion que suma los productos de una obra por producto.
     Ej: en una obra un día se han utilizado 3 tornillos,
     un segundo dia se han utilizado 5 tornillos + 1m de cable. El resultado es: 
     8 tornillos, 1m cable.

    Arguments:
        id {integer} -- id de la obra.
    Returns:
        productosSeleccionados {[id del producto, cantidad]} -- producto y cantidades utlizadas.
    """
    productosSeleccionados = db.session.query(obraproducto.idProducto, db.func.sum(obraproducto.Cantidad)).group_by(obraproducto.idProducto, obraproducto.idObra).filter(obraproducto.idObra==id).all()
    return productosSeleccionados
	
#@auto.doc()
def albs(id): 
    #alba = db.session.query(albaran.idAlbaran, albaran.Numero, proveedor.Empresa, imagenalbaran.nombreImagen).select_from(albaran).join(proveedor).join(imagenalbaran).filter(albaran.idObra==id)
    
    """Funcion que devuelve los albanes que se han comprado/utilizado por obra.

    Arguments:
        id {integer} -- id de la obra
    Returns:
        alba {[albaran]}: devuelve los albaranes: el id de albarán, nº de albaran, proveedor (Empresa), imagen si tiene.
    """
    alba=[]
    nombreAlbaranes = db.session.query(albaran.idAlbaran, imagenalbaran.nombreImagen).select_from(imagenalbaran).join(albaran).filter(albaran.idObra==id)
    if nombreAlbaranes.count() > 0:
        alba = db.session.query(albaran.idAlbaran, albaran.Numero, proveedor.Empresa, imagenalbaran.nombreImagen).select_from(albaran).join(proveedor).join(imagenalbaran).filter(albaran.idObra==id)
    else:
        alba = db.session.query(albaran.idAlbaran, albaran.Numero, proveedor.Empresa).select_from(albaran).join(proveedor).filter(albaran.idObra==id)
    return alba


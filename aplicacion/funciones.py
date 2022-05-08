from forms import *
from models import *

def listaproveedores():
    # Tengo que crear un select que será un list para que muestre todos los proveedores
    return [(p.idProveedor, p.Empresa) for p in proveedor.query.all()]

def listaunidades():
 # Tengo que crear un select que será un list para las unidades de medida.
    return [(u.idUnidad, u.Unidad) for u in unidad.query.all()]

def listaestados():
    return [(e.idEstado, e.Estado) for e in estado.query.all()]

def listaclientes():
    return [(c.idCliente, c.Empresa) for c in cliente.query.all()]

def listaproductos():
    return [(pd.idProducto, pd.Nombre) for pd in producto.query.order_by(producto.Nombre.asc()).all()]

def listatrabajadores():
    return [(t.idTrabajador, t.Nombre) for t in trabajador.query.all()]
		
def listaalbaranes():
    return [(alb.idAlbaran, alb.Numero) for alb in albaran.query.all()]
	
def listaobras():
    listadoObras=[(0, 'All')]
    for o in obra.query.all():
        listadoObras.append([o.idObra, o.Nombre])
    return listadoObras

def listatrabajosrealizados():
    return [(tr.idTrabajorealizado, tr.Descripcion, tr.Fecha) for tr in trabajorealizado.query.all()]		


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf', 'docx'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
	
def imagenes_albaran(id):
    imagenes=db.session.query(imagenalbaran.idImagenAlbaran, imagenalbaran.nombreImagen).filter(imagenalbaran.idAlbaran==id)
    return imagenes

def resultadoTarObr(id):
    resultadoTareasObra = db.session.query(tarea.Descripcion, tarea.Notas, tarea.EstadoTarea).filter(tarea.idObra==id)
    return resultadoTareasObra

def sumaProductos(id):
    productosSeleccionados = db.session.query(obraproducto.idProducto, db.func.sum(obraproducto.Cantidad)).group_by(obraproducto.idProducto, obraproducto.idObra).filter(obraproducto.idObra==id).all()
    return productosSeleccionados
	

def albs(id): 
    #alba = db.session.query(albaran.idAlbaran, albaran.Numero, proveedor.Empresa, imagenalbaran.nombreImagen).select_from(albaran).join(proveedor).join(imagenalbaran).filter(albaran.idObra==id)
    alba=[]
    nombreAlbaranes = db.session.query(albaran.idAlbaran, imagenalbaran.nombreImagen).select_from(imagenalbaran).join(albaran).filter(albaran.idObra==id)
    if nombreAlbaranes.count() > 0:
        alba = db.session.query(albaran.idAlbaran, albaran.Numero, proveedor.Empresa, imagenalbaran.nombreImagen).select_from(albaran).join(proveedor).join(imagenalbaran).filter(albaran.idObra==id)
    else:
        alba = db.session.query(albaran.idAlbaran, albaran.Numero, proveedor.Empresa).select_from(albaran).join(proveedor).filter(albaran.idObra==id)
    return alba


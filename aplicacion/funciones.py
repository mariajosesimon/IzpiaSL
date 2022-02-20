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
    return [(pd.idProducto, pd.Nombre) for pd in producto.query.all()]

def listatrabajadores():
    return [(t.idTrabajador, t.Nombre) for t in trabajador.query.all()]
		
def listaalbaranes():
    return [(alb.idAlbaran, alb.Numero) for alb in albaran.query.all()]
	
def listaobras():
    return [(o.idObra, o.Nombre) for o in obra.query.all()]

def listatrabajosrealizados():
    return [(tr.idTrabajorealizado, tr.Descripcion, tr.Fecha) for tr in trabajorealizado.query.all()]		

	
	
	
	
	
	
	

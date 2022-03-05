from ssl import DefaultVerifyPaths
from sqlalchemy import Column, ForeignKey, BLOB, Boolean, Float, Text, Time
from sqlalchemy import Integer, String, Date
from app import db


class cliente(db.Model):
    __tablename__ = 'cliente'
    idCliente = Column(Integer, primary_key=True)
    Empresa = Column(String(100), nullable=False)
    CifNif = Column(String(45), nullable=False)
    Direccion = Column(String(45), nullable=False)
    CP = Column(Integer)
    Ciudad = Column(String(45))
    Provincia = Column(String(45))
    Telefono = Column(Integer)
    Email  = Column(String(100))
    Contacto = Column(String(45))
    Baja = Column(Boolean)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class proveedor(db.Model):
    __tablename__ = 'proveedor'
    idProveedor = Column(Integer, primary_key=True)
    Empresa = Column(String(100), nullable=False)
    CifNif = Column(String(45), nullable=False)
    Direccion = Column(String(45), nullable=False)
    CP = Column(Integer)
    Ciudad = Column(String(45))
    Provincia = Column(String(45))
    Telefono = Column(Integer)
    Email  = Column(String(100))
    Contacto = Column(String(45))
    Baja = Column(Boolean)


    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class estado(db.Model):
    __tablename__ = 'estado'
    idEstado = Column(Integer, primary_key=True)
    Estado = Column(String(45), nullable=False)

class unidad(db.Model):
    __tablename__ = 'unidad'
    idUnidad = Column(Integer, primary_key=True)
    Unidad = Column(String(45), nullable=False)

class trabajador(db.Model):
    __tablename__ = 'trabajador'
    idTrabajador = Column(Integer, primary_key=True)
    Nombre = Column(String(45), nullable=False)
    Apellidos = Column(String(45), nullable=False)
    Telefono = Column(Integer, nullable=False)
    Baja = Column(Boolean)
    Rol = Column(String(45), default='Trabajador', nullable=False)
    Usuario = Column(String(45))
    Contrasena  = Column(String(100))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class producto(db.Model):
    __tablename__= 'producto'
    idProducto = Column(Integer, primary_key=True)
    Nombre = Column(String(45), nullable=False)
    Precio = Column(Float, nullable=False)

    # idUnidad -> toma el id de unidad de medida.
    idUnidad = Column(Integer, ForeignKey('unidad.idUnidad'), nullable=False)


    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class obra(db.Model):
    __tablename__= 'obra'
    idObra = Column(Integer, primary_key=True)
    Nombre = Column(String(100), nullable=False)
    NumeroPedido = Column(String(10), nullable=False)

    # EstadoID -> toma el Estado que va a estar la obra (Parada, finalizada, en proceso...).
    idEstado = Column(Integer, ForeignKey('estado.idEstado'), nullable=False)

    # ClienteID -> toma el cliente de la obra.
    idCliente = Column(Integer, ForeignKey('cliente.idCliente'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class albaran(db.Model):
    __tablename__= 'albaran'
    idAlbaran = Column(Integer, primary_key=True)
    Numero = Column(String(45), nullable=False)

    # ProveedorID -> toma el proveedor del albarán.
    idProveedor = Column(Integer, ForeignKey('proveedor.idProveedor'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class tarea(db.Model):
    __tablename__= 'tarea'
    idTarea = Column(Integer, primary_key=True)
    Descripcion = Column(Text(), nullable=False)
    EstadoTarea = Column(String(45), nullable=False, default='Pendiente')
    Notas = Column(Text())

    # ObraID -> se asigna a una obra.
    idObra = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class trabajorealizado(db.Model):
    __tablename__= 'trabajorealizado'
    idTrabajoRealizado = Column(Integer, primary_key=True)
    Fecha = Column(Date, nullable=False)
    HoraInicio = Column(Time())
    HoraFin = Column(Time())
    Descripcion = Column(Text(), nullable=False)

    # ObraIDTR -> se asigna a una obra.
    #En la clase tarea ya aparece ObraID no puedo tener repedidas las variables, añado TR de trabajo realizado
    idObra = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class productoalbaran(db.Model):
    __tablename__= 'productoalbaran'
    idProductoAlbaran = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)

    # ProductoID -> se asigna a un producto.
    idProducto = Column(Integer, ForeignKey('producto.idProducto'), nullable=False)
    # AlbaranID -> se asigna a un albaran.
    idAlbaran = Column(Integer, ForeignKey('albaran.idAlbaran'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class obraproducto(db.Model):
    __tablename__ = 'obraproducto'
    idObraProducto = Column(Integer, primary_key=True, default=0)
    Cantidad = Column(Integer, nullable=False)

    # ProductoIDOP -> se asigna a un producto.
    idProducto = Column(Integer, ForeignKey('producto.idProducto'), nullable=False)
    # ObraID -> se asigna a una obra.
    idObra = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class obraalbaran(db.Model):
    __tablename__ = 'obraalbaran'
    idObraAlbaran = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)

    # ProveedorIDOPv -> se asigna a un producto.
    idAlbaran = Column(Integer, ForeignKey('albaran.idAlbaran'), nullable=False)
    # ObraID -> se asigna a una obra.
    idObra = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class operariotrabajorealizado(db.Model):
    __tablename__ = 'operariotrabajorealizado'
    idOperariotrabajorealizado = Column(Integer, primary_key=True)

    # TrabajadorID -> se asigna a un trabajador.
    idTrabajador = Column(Integer, ForeignKey('trabajador.idTrabajador'), nullable=False)
    # TrabajoRealizadoID -> se asigna a un trabajo realizado
    idTrabajoRealizado = Column(Integer, ForeignKey('trabajorealizado.idTrabajoRealizado'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class imagenobra(db.Model):
    __tablename__='imagenobra'
    idImagenObra = Column(Integer, primary_key=True)
    fotoObra = Column(BLOB, nullable=False )

    #necesito el id de la obra para asignarlo a la imagen
    idObra=Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class imagenalbaran(db.Model):
    __tablename__='imagenalbaran'
    idImagenAlbaran = Column(Integer, primary_key=True)
    nombreImagen = Column(String, nullable=False )
    fotoAlb = Column(BLOB, nullable=False )

    #necesito el id de la obra para asignarlo a la imagen
    idAlbaran=Column(Integer, ForeignKey('albaran.idAlbaran'), nullable=False)
    
    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
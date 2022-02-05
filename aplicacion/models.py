from sqlalchemy import Column, ForeignKey, BLOB, Boolean, Float, Text, Time
from sqlalchemy import Integer, String, Date
from app import db


class cliente(db.Model):
    __tablename__ = 'Cliente'
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
    Activo = Column(Boolean)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class proveedor(db.Model):
    __tablename__ = 'Proveedor'
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
    Activo = Column(Boolean)


    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class estado(db.Model):
    __tablename__ = 'Estado'
    idEstado = Column(Integer, primary_key=True)
    Estado = Column(String(45), nullable=False)

class unidad(db.Model):
    __tablename__ = 'Unidad'
    idUnidad = Column(Integer, primary_key=True)
    Unidad = Column(String(45), nullable=False)

class trabajador(db.Model):
    __tablename__ = 'Trabajador'
    idTrabajador = Column(Integer, primary_key=True)
    Nombre = Column(String(45), nullable=False)
    Apellidos = Column(String(45), nullable=False)
    Telefono = Column(Integer, nullable=False)
    Activo = Column(Boolean)
    Rol = Column(String(45), default='Trabajador', nullable=False)
    Usuario = Column(String(45))
    Contrasena  = Column(String(100))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class producto(db.Model):
    __tablename__= 'Producto'
    idProducto = Column(Integer, primary_key=True)
    Nombre = Column(String(45), nullable=False)
    Precio = Column(Float, nullable=False)

    # UnidadID -> toma el id de unidad de medida.
    UnidadID = Column(Integer, ForeignKey('unidad.idUnidad'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class obra(db.Model):
    __tablename__= 'Obra'
    idObra = Column(Integer, primary_key=True)
    Nombre = Column(String(100), nullable=False)
    Foto = Column(BLOB)
    PDF = Column(BLOB)

    # EstadoID -> toma el Estado que va a estar la obra (Parada, finalizada, en proceso...).
    EstadoID = Column(Integer, ForeignKey('estado.idEstado'), nullable=False)

    # ClienteID -> toma el cliente de la obra.
    ClienteID = Column(Integer, ForeignKey('cliente.idCliente'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class albaran(db.Model):
    __tablename__= 'Albaran'
    idAlbaran = Column(Integer, primary_key=True)
    Numero = Column(String(45), nullable=False)

    # ProveedorID -> toma el proveedor del albarán.
    ProveedorID = Column(Integer, ForeignKey('proveedor.idProveedor'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class tarea(db.Model):
    __tablename__= 'Tarea'
    idTarea = Column(Integer, primary_key=True)
    Descripcion = Column(Text(), nullable=False)
    EstadoAlbaran = Column(String(45), nullable=False, default='Pendiente')
    Notas = Column(Text())

    # ObraID -> se asigna a una obra.
    ObraID = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class trabajorealizado(db.Model):
    __tablename__= 'Trabajorealizado'
    idTrabajoRealizado = Column(Integer, primary_key=True)
    Fecha = Column(Date, nullable=False)
    HoraInicio = Column(Time())
    HoraFin = Column(Time())
    Descripcion = Column(Text(), nullable=False)

    # ObraIDTR -> se asigna a una obra.
    #En la clase tarea ya aparece ObraID no puedo tener repedidas las variables, añado TR de trabajo realizado
    ObraIDTR = Column(Integer, ForeignKey('obra.idObraTR'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class productoalbaran(db.Model):
    __tablename__= 'Productoalbaran'
    idProductoAlbaran = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)

    # ProductoID -> se asigna a un producto.
    ProductoID = Column(Integer, ForeignKey('producto.idProducto'), nullable=False)
    # AlbaranID -> se asigna a un albaran.
    AlbaranID = Column(Integer, ForeignKey('albaran.idAlbaran'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class obraproducto(db.Model):
    __tablename__ = 'Obraproducto'
    idObraProducto = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)

    # ProductoIDOP -> se asigna a un producto.
    ProductoIDOP = Column(Integer, ForeignKey('producto.idProducto'), nullable=False)
    # ObraID -> se asigna a una obra.
    ObraIDOP = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class obraproveedor(db.Model):
    __tablename__ = 'Obraproveedor'
    idObraProveedor = Column(Integer, primary_key=True)
    Cantidad = Column(Integer, nullable=False)

    # ProveedorIDOPv -> se asigna a un producto.
    ProveedorIDOPv = Column(Integer, ForeignKey('proveedor.idProveedor'), nullable=False)
    # ObraID -> se asigna a una obra.
    ObraIDOPv = Column(Integer, ForeignKey('obra.idObra'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

class operariotrabajorealizado(db.Model):
    __tablename__ = 'Pperariotrabajorealizado'
    idOperariotrabajorealizado = Column(Integer, primary_key=True)

    # TrabajadorID -> se asigna a un trabajador.
    TrabajadorID = Column(Integer, ForeignKey('trabajador.idTrabajador'), nullable=False)
    # TrabajoRealizadoID -> se asigna a un trabajo realizado
    TrabajoRealizadoID = Column(Integer, ForeignKey('trabajotealizado.idTrabajoRealizado'), nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
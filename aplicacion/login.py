from flask import session,redirect

def login_user(trabajador):
	session["idTrabajador"]=trabajador.idTrabajador
	session["Usuario"]=trabajador.Usuario
	session["Rol"]=trabajador.Rol

def logout_user():
	session.pop("idTrabajador",None)
	session.pop("Usuario",None)
	session.pop("Rol",None)


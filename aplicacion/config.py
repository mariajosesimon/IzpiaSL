import os

#secret_key = 'A0Zr98j/asdf3422a3+/*?)$/abSD3yX R~XHH!jmN]LWX/,?RT'
secret_key = os.urandom(16)
PWD = os.path.abspath(os.curdir)

DEBUG = True
USERNAME = 'root'  # nombre de usuario
password = 'root'  # Contraseña de la base de datos
HOST = 'localhost'  # dirección local
PORT = '3307'  # Número de puerto
DATABASE = 'izpiasl'  # Nombre de la base de datos

# Conectar a la base de datos

#con = sqlite3.connect('mydatabase.db')
#SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(USERNAME, password, HOST, DATABASE)
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/izpiasl"
SQLALCHEMY_TRACK_MODIFICATIONS = False

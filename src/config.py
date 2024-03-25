#Configuraciones del proyecto

class DevelopmentConfig():
    DEBUG           = True
    MYSQL_HOST      = 'localhost'
    MYSQL_USER      = 'developer'
    MYSQL_PASSWORD  = ''
    MYSQL_DB        = 'almacen_db'

config = {
    'development': DevelopmentConfig
}
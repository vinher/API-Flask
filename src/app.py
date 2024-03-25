from flask import Flask,jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)

conection = MySQL(app)

@app.route('/clients',methods=['GET'])
def listClients():
    try:
        cursor = conection.connection.cursor()
        sql = "SELECT * FROM cliente"
        cursor.execute(sql)
        datos = cursor.fetchall()
        datos_client = []
        for fila in datos:
            dato_client = {
                'id'        :fila[0],
                'cliente'   :fila[1],
                'telefono'  :fila[2],
            }
            datos_client.append(dato_client)

        print(datos)
        return jsonify({'data':datos_client,'message':'success'})
    except Exception as ex:
        return jsonify({'message':'false'})


#Decorador que sirve para:
#Declara la ruta
#Asignar el verbo por el que va a recibir la solictud
#Pasar parametros <parametro> indica que vamosa  pasar un parametro 
# Funcion para consultar un solo cliente
@app.route('/get/<client>',methods=['GET'])
def selectClient(client):
    try:
        cursor  = conection.connection.cursor()
        sql     = "SELECT * FROM cliente WHERE id ='{0}'".format(client)
        cursor.execute(sql)
        datos   = cursor.fetchone()
        if datos != None:
            dato_client = {
                'id'        :datos[0],
                'cliente'   :datos[1],
                'telefono'  :datos[2],
            }
            return jsonify({'data':dato_client,'message':'success'})
        else:
            return jsonify({'message':'false'})
    except Exception as ex:
        return "Error"


@app.route('/add/<client>',methods=['POST'])
def addClient(client):
    try:
        cursor  = conection.connection.cursor()
        sql     = "SELECT * FROM cliente WHERE id ='{0}'".format(client)
        cursor.execute(sql)
        datos   = cursor.fetchone()
        if datos != None:
            dato_client = {
                'id'        :datos[0],
                'cliente'   :datos[1],
                'telefono'  :datos[2],
            }
            return jsonify({'data':dato_client,'message':'success'})
        else:
            return jsonify({'message':'false'})
    except Exception as ex:
        return "Error"


@app.route('/insertclient', methods=['POST'])
def registerClient():
    try:
        print(request.json['cliente'])
        print(request.json['direccion'])
        print(request.json['telefono'])
        cursor  = conection.connection.cursor()
        sql     = """INSERT INTO cliente (nombre, direccion, telefono) 
        VALUES ('{0}','{1}','{2}')""".format(request.json['cliente'],
                                             request.json['direccion'],
                                             request.json['telefono'])
        print(sql)
        cursor.execute(sql)
        conection.connection.commit()#confirma la accion de insersion
        
        return jsonify({'message':'Success'})
    except Exception as ex:
        return ex

#Crear funcion para eliminar y actualizar
@app.route('/delete/<id>',methods=['DELETE'])
def deleteCliente(id):
    try:
        #PRIMERO VERIFICAMOS SI EXISTE EN REGISTRO
        cursor  = conection.connection.cursor()
        sql     = "SELECT * FROM cliente WHERE id ='{0}'".format(id)
        cursor.execute(sql)
        datos   = cursor.fetchone()
        # Si existe lo borramos
        if datos != None:
            cursor  = conection.connection.cursor()
            sql     = "DELETE FROM cliente WHERE id ='{0}'".format(id)
            cursor.execute(sql)
            conection.connection.commit()
            return jsonify({'data':'Registro {0} Eliminado'.format(id),'message':'success'})
        else:
            return jsonify({'message':'Registro Inexistente'})
    except Exception as ex:
        return "Error"


@app.route('/upateclient/<id>', methods=['PUT'])
def updateCliente(id):
    try:
        print(request.json)
        #PRIMERO VERIFICAMOS SI EXISTE EN REGISTRO
        cursor  = conection.connection.cursor()
        sql     = "SELECT * FROM cliente WHERE id ='{0}'".format(id)
        cursor.execute(sql)
        datos   = cursor.fetchone()
        # Si existe lo actualizamos
        if datos != None:
            cursor  = conection.connection.cursor()
            sql     = """UPDATE cliente SET nombre = '{0}', direccion = '{1}', telefono = '{2}' 
            WHERE id = '{3}'""".format(request.json['nombre'],
                                             request.json['direccion'],
                                             request.json['telefono'],
                                             id)
            cursor.execute(sql)
            conection.connection.commit()
            return jsonify({'data':'Registro {0} Actualizado'.format(id),'message':'success'})
        else:
            return jsonify({'message':'Registro Inexistente'})
    except Exception as ex:
            return ex





def pageNotFound(error):
    return "<h3>Pagina No Disponible</h3>",404





if __name__ == '__main__':
    #Llamamos a nuestra clase con la configuración
    app.config.from_object(config['development'])
    #Manejo de errores: En el primer parametro pasamos el error 
    #En el segundo la funcionq ue se va a llamar si este error sucede
    app.register_error_handler(404,pageNotFound)
    app.run()
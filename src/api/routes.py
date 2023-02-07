"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
import json
from api.models import db, Usuario, Mascotas
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

api = Blueprint('api', __name__)


# Registro Usuario
@api.route('/signup', methods=['POST'])
def signup():

    body = json.loads(request.data)
    
    # Verifico username que no exista
    user = Usuario.query.filter_by(username=body["username"]).first() 
    
    if user is None:
        # Verifico email que no exista
        userEmail = Usuario.query.filter_by(email=body["email"]).first() 
        if userEmail is None:
            agregar_new_user = Usuario(username=body["username"], email=body["email"], password=body["password"], nombre=body["nombre"],apellido=body["apellido"],contacto=body["contacto"], admin=body["admin"])
            # Add
            db.session.add(agregar_new_user)
            db.session.commit()
            response_body = {
                "msg": "El usuario fue creado exitosamente"
            }
            return jsonify(response_body), 200

    response_body = {
            "msg": "El usuario ya existe en el sistema"
        }
    return jsonify(response_body), 400



# Login Usuario
@api.route("/login", methods=["POST"])
def login():
    # Obtengo credenciales del usuario desde el cuerpo de la solicitud
    username = request.json.get("username")
    password = request.json.get("password")

    usuario_login = Usuario.query.filter_by(username=username).first()

    if usuario_login  is None:
        return jsonify({"msg": "Usuario no existe"}), 404

    if username != usuario_login.username or password != usuario_login.password:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

    #Token de acceso
    access_token = create_access_token(identity=usuario_login.id)

    response_body = {
        "access_token": access_token,
        "user": usuario_login.serialize()
    }

    return jsonify(response_body), 200

# -----------------------Usuarios----------------------

# Get - All Users
@api.route('/users', methods=['GET'])
def getUsers():

    users = Usuario.query.all() 
    all_users = list(map(lambda item: item.serialize(), users))

    return jsonify(all_users), 200

# Get - One User for ID
@api.route('/users/<int:id>', methods=['GET'])
def getUser(id):

    user = Usuario.query.filter_by(id=id).first()

    if user is not None:
        return jsonify(user.serialize()), 200
    
    # Afuera del if
    response_body = {
            "msg": "Usuario no existe"
        }
    return jsonify(response_body), 400

# Delete - User
@api.route('/users', methods=['DELETE'])
def deleteUser():
    body = json.loads(request.data)

    user = Usuario.query.filter_by(id=body["usuario_id"]).first()
    
    if user is not None:
        db.session.delete(user)
        db.session.commit()

        response_body = {
            "msg": "Eliminación correcta de Usuario"
        }
        return jsonify(response_body), 200

    # Afuera del if
    response_body = {
            "msg": "Usuario no existe"
        }
    return jsonify(response_body), 400

# Put - User
@api.route('/users', methods=['PUT'])
def putUser():
    body = json.loads(request.data)
    
    user = Usuario.query.filter_by(id=body["usuario_id"]).first()
    
    if user is not None:
        user.username = body["username"]
        user.contraseña = body["contraseña"]
        user.email = body["email"]
        user.nombre = body["nombre"]
        user.apellido = body["apellido"]
        user.contacto = body["contacto"]

        db.session.add(user)
        db.session.commit()

        response_body = {
            "msg": "El usuario fue modificado con exito"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "El usuario no existe en el sistema"
        }
    return jsonify(response_body), 400



# ----------------------- Mascotas ----------------------

# Get - All Mascotas
@api.route('/pets', methods=['GET'])
def getPets():

    pets = Mascotas.query.all() 
    all_pets = list(map(lambda item: item.serialize(), pets))

    return jsonify(all_pets), 200

# Get - One Pets for ID
@api.route('/pets/<int:id>', methods=['GET'])
def getPet(id):

    pet = Mascotas.query.filter_by(id=id).first()

    if pet is not None:
        return jsonify(pet.serialize()), 200
    
    # Afuera del if
    response_body = {
            "msg": "Mascota no existe"
        }
    return jsonify(response_body), 400

# Post - Pets
@api.route('/pets', methods=['POST'])
def postPets():
    body = json.loads(request.data)

    newPets = Mascotas(genero=body["genero"], tamaño=body["tamaño"], color=body["color"], nombre=body["nombre"], edad=body["edad"], raza=body["raza"], estado=body["estado"], especie=body["especie"],latitud=body["latitud"],url=body["url"] ,usuario_id=body["usuario_id"])
    db.session.add(newPets)
    db.session.commit()

    response_body = {
            "msg": "La mascota fue añadida con exito"
    }
    return jsonify(response_body), 200

# Put - Pets
@api.route('/pets', methods=['PUT'])
def putPets():
    body = json.loads(request.data)

    pet = Mascotas.query.filter_by(id=body["mascota_id"]).first()
    
    if pet is not None:
        pet.genero = body["genero"]
        pet.tamaño = body["tamaño"]
        pet.color = body["color"]
        pet.nombre = body["nombre"]
        pet.edad = body["edad"]
        pet.raza = body["raza"]
        pet.estado = body["estado"]
        pet.especie = body["especie"]
        pet.latitud = body["latitud"]
        pet.longitud = body["longitud"]
        pet.url = ["url"]
        pet.usuario_id = body["usuario_id"]

        db.session.add(pet)
        db.session.commit()

        response_body = {
            "msg": "La mascota fue modificada con exito"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "La mascota no existe en el sistema"
        }
    return jsonify(response_body), 400

# Get - All Mascotas Perdidas
@api.route('/pets/lost', methods=['GET'])
def getPetsLost():

    pets = Mascotas.query.filter_by(estado="lost").all()
    all_pets = list(map(lambda item: item.serialize(), pets))

    return jsonify(all_pets), 200

# Get - All Mascotas Huerfanas
@api.route('/pets/orphan', methods=['GET'])
def getPetsOrphan():

    pets = Mascotas.query.filter_by(estado="orphan").all()
    all_pets = list(map(lambda item: item.serialize(), pets))

    return jsonify(all_pets), 200

# Mascotas - Usuarios
@api.route('/users/<int:id>/pets', methods=['GET'])
def getUserPets(id):

    pets = Mascotas.query.filter_by(usuario_id=id).all()
    all_pets = list(map(lambda item: item.serialize(), pets))

    if (all_pets == []):
      return  jsonify({"msg": "Usuario no tiene mascotas"}), 404

    return jsonify({"usuario_id": pets[0].usuario_id, "results":  all_pets}), 200

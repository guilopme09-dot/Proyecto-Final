from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os

chivistas=Flask("Finanzas App")
CORS(chivistas)

cliente=MongoClient(
    os.getenv(
        "MONGODB_URI",
        "mongodb+srv://IvanMontes:010309@cluster0.kltb6j0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
)

db=cliente["finanzas"]

usuarios=db["usuarios"]
categorias=db["categorias"]
gastos=db["gastos"]

@chivistas.route("/")
def inicio():
    return "Servidor funcionando"

@chivistas.route("/usuarios",methods=["GET"])
def obtener_usuarios():

    lista=[]

    for usuario in usuarios.find():

        lista.append({
            "nombre":usuario["nombre"],
            "correo":usuario["correo"],
            "password":usuario["password"],
            "saldo":usuario["saldo"],
            "ahorro":usuario["ahorro"],
            "limite":usuario["limite"]
        })

    return jsonify(lista)

@chivistas.route("/usuarios",methods=["POST"])
def agregar_usuario():

    datos=request.json

    nuevo_usuario={
        "nombre":datos["nombre"],
        "correo":datos["correo"],
        "password":datos["password"],
        "saldo":datos["saldo"],
        "ahorro":datos["ahorro"],
        "limite":datos["limite"]
    }

    usuarios.insert_one(nuevo_usuario)

    return jsonify({
        "mensaje":"Usuario agregado"
    })

@chivistas.route("/usuarios/<nombre>",methods=["PUT"])
def actualizar_usuario(nombre):

    datos=request.json

    usuarios.update_one(
        {"nombre":nombre},
        {"$set":{
            "correo":datos["correo"],
            "password":datos["password"],
            "saldo":datos["saldo"],
            "ahorro":datos["ahorro"],
            "limite":datos["limite"]
        }}
    )

    return jsonify({
        "mensaje":"Usuario actualizado"
    })

@chivistas.route("/categorias",methods=["GET"])
def obtener_categorias():

    lista=[]

    for categoria in categorias.find():

        lista.append({
            "nombre":categoria["nombre"],
            "descripcion":categoria["descripcion"]
        })

    return jsonify(lista)

@chivistas.route("/categorias",methods=["POST"])
def agregar_categoria():

    datos=request.json

    nueva_categoria={
        "nombre":datos["nombre"],
        "descripcion":datos["descripcion"]
    }

    categorias.insert_one(nueva_categoria)

    return jsonify({
        "mensaje":"Categoria agregada"
    })

@chivistas.route("/categorias/<nombre>",methods=["PUT"])
def actualizar_categoria(nombre):

    datos=request.json

    categorias.update_one(
        {"nombre":nombre},
        {"$set":{
            "descripcion":datos["descripcion"]
        }}
    )

    return jsonify({
        "mensaje":"Categoria actualizada"
    })

@chivistas.route("/categorias/<nombre>",methods=["DELETE"])
def eliminar_categoria(nombre):

    categorias.delete_one({
        "nombre":nombre
    })

    return jsonify({
        "mensaje":"Categoria eliminada"
    })

@chivistas.route("/gastos",methods=["GET"])
def obtener_gastos():

    lista=[]

    for gasto in gastos.find():

        lista.append({
            "titulo":gasto["titulo"],
            "cantidad":gasto["cantidad"],
            "categoria":gasto["categoria"],
            "fecha":gasto["fecha"]
        })

    return jsonify(lista)

@chivistas.route("/gastos",methods=["POST"])
def agregar_gasto():

    datos=request.json

    nuevo_gasto={
        "titulo":datos["titulo"],
        "cantidad":datos["cantidad"],
        "categoria":datos["categoria"],
        "fecha":datos["fecha"]
    }

    gastos.insert_one(nuevo_gasto)

    return jsonify({
        "mensaje":"Gasto agregado"
    })

@chivistas.route("/gastos/<titulo>",methods=["PUT"])
def actualizar_gasto(titulo):

    datos=request.json

    gastos.update_one(
        {"titulo":titulo},
        {"$set":{
            "cantidad":datos["cantidad"],
            "categoria":datos["categoria"],
            "fecha":datos["fecha"]
        }}
    )

    return jsonify({
        "mensaje":"Gasto actualizado"
    })

@chivistas.route("/gastos/<titulo>",methods=["DELETE"])
def eliminar_gasto(titulo):

    gastos.delete_one({
        "titulo":titulo
    })

    return jsonify({
        "mensaje":"Gasto eliminado"
    })

if __name__=="__main__":
    chivistas.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
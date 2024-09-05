from flask import Flask
from flask_cors import CORS
import mysql.connector

cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='cinestar')
cursor = cnx.cursor(dictionary=True)

app = Flask(__name__)
CORS(app)

@app.route("/cines")
def cines():
    cursor.callproc("sp_getCines")
    for row in cursor.stored_results() :
        cines = row.fetchall()
        
    cines={'success':True, 'data':cines, 'message':'lista de cines'}

    return cines

@app.route("/cines/<int:id>")
def cine(id):
    cursor.callproc("sp_getCine", [id])
    for row in cursor.stored_results() :
        cine = row.fetchone()

    if cine is None : return dict([])

    cursor.callproc("sp_getCinePeliculas", [id])
    for row in cursor.stored_results() :
        peliculas = row.fetchall()

    cursor.callproc("sp_getCineTarifas", [id])
    for row in cursor.stored_results() :
        tarifas = row.fetchall()
    
    cine['peliculas'] = peliculas
    cine['tarifas'] = tarifas
    
    #cine={'success':True, 'data':cine, 'message':'informacion de cine'}
    return cine

@app.route("/peliculas/<string:id>")
def peliculas(id):
    id = 1 if id ==  'cartelera' else 2 if id == 'estrenos' else 0
    cursor.callproc("sp_getPeliculas", [id])
    for row in cursor.stored_results() :
        peliculas = row.fetchall()

    if peliculas is None : return dict([])

    return peliculas

@app.route("/peliculas/<int:id>")
def pelicula(id):
    cursor.callproc("sp_getPelicula", [id])
    for row in cursor.stored_results() :
        pelicula = row.fetchone()

    if pelicula is None : return dict([])

    return pelicula


if __name__== "__main__":
    app.run(debug=False,port=5000, host="0.0.0.0")
    
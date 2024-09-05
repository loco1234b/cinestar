from fastapi import FastAPI
import mysql.connector

cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='cinestar')
cursor = cnx.cursor(dictionary=True)

app = FastAPI()

@app.get("/cines")
def cines():
    cursor.callproc("sp_getCines")
    for row in cursor.stored_results() :
        cines = row.fetchall()

    #cines = {'success':True, 'data': cines, 'message': 'Lista de cines' }
    return cines

@app.get("/cines/{id}")
def cine(id: int):
    cursor.callproc("sp_getCine", [id])
    for row in cursor.stored_results() :
        cine = row.fetchone()

    if cine is None : 
        #return {'success':False, 'data': None, 'message': 'Cine no existe' }
        return dict([])

    cursor.callproc("sp_getCinePeliculas", [id])
    for row in cursor.stored_results() :
        peliculas = row.fetchall()

    cursor.callproc("sp_getCineTarifas", [id])
    for row in cursor.stored_results() :
        tarifas = row.fetchall()
    
    cine['peliculas'] = peliculas
    cine['tarifas'] = tarifas

    #cine = {'success':True, 'data': cine, 'message': 'Informacón del cine' }
    return cine

@app.get("/peliculas/{id}")
def peliculas(id: str):
    id = 1 if id ==  'cartelera' else 2 if id == 'estrenos' else 0
    cursor.callproc("sp_getPeliculas", [id])
    for row in cursor.stored_results() :
        peliculas = row.fetchall()

    if peliculas is None : return dict([])

    return peliculas

@app.get("/pelicula/{id}")
def pelicula(id: int):
    cursor.callproc("sp_getPelicula", [id])
    for row in cursor.stored_results() :
        pelicula = row.fetchone()

    if pelicula is None : return dict([])

    return pelicula

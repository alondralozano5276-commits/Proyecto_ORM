from flask import Flask, render_template, request, redirect, url_for
from models import db
import controllers

app = Flask(__name__)

# Configuración de la conexión a MySQL con la contraseña 'hola1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola1234@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación de Flask
db.init_app(app)

@app.route("/")
@app.route("/juegos")
def juegos():
    lista_juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=lista_juegos)

@app.route("/agregar_juego")
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for("juegos"))

@app.route("/eliminar_juego", methods=["POST"])
def eliminar_juego():
    id = request.form["id"]
    controllers.eliminar_juego(id)
    return redirect(url_for("juegos"))

@app.route("/formulario_editar_juego/<int:id>")
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(id, nombre, descripcion, precio)
    return redirect(url_for("juegos"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(port=8000, debug=True)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos_personales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    ciudad = db.Column(db.String(80), nullable=False)
    cedula = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    personas = Persona.query.all()
    return render_template('index.html', personas=personas)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nuevo_persona = Persona(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            edad=request.form['edad'],
            ciudad=request.form['ciudad'],
            cedula=request.form['cedula']
        )
        db.session.add(nuevo_persona)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona = Persona.query.get_or_404(id)
    if request.method == 'POST':
        persona.nombre = request.form['nombre']
        persona.apellido = request.form['apellido']
        persona.edad = request.form['edad']
        persona.ciudad = request.form['ciudad']
        persona.cedula = request.form['cedula']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', persona=persona)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        cedula_busqueda = request.form['cedula']
        personas_encontradas = Persona.query.filter_by(cedula=cedula_busqueda).all()
        return render_template('resultados.html', personas=personas_encontradas)
    
    return render_template('buscar.html')

if __name__ == '__main__':
    app.run(debug=True)
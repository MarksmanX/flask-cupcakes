"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, flash, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'GOOGLYBOOGLYWOOGLY'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

with app.app_context():
    db.create_all()


@app.route('/')
def root():
    """Render homepage."""

    return render_template('index.html')


@app.route('/api/cupcakes')
def list_cupcakes():
    """Shows list of cupcakes."""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def show_one_cupcake(cupcake_id):
    """Shows one cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Updates a cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def remove_cupcake(cupcake_id):
    """Delete a cupcake and return confirmation message."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")


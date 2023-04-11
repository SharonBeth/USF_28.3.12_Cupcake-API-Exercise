"""Flask app for Cupcakes"""

from flask import Flask, render_template, jsonify, request
from models import connect_db, Cupcake, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)

def serialize_cupcake(cupcake):
    """serialize a cupcake SQLAlchemy obj to dicationary."""

    return {
        "id"    : cupcake.id,
        "flavor": cupcake.flavor,
        "size"  : cupcake.size,
        "rating": cupcake.rating,
        "image" : cupcake.image,
    }

@app.route("/api")
def homepage():
    """Homepage for cupcake DB. """
    return render_template("main_page.html")

@app.route("/api/cupcakes")
def get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(d) for d in cupcakes]
    
    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<cupcake_id>")
def get_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """"create cupcake from form data & return it as JSON
        {'cupcake': {id, flavor, size, rating, image}}"""
    
    flavor  = request.json["flavor"]
    size    = request.json["size"]
    rating  = request.json["rating"]
    image   = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    return (jsonify(cupcake=serialized), 201)

    # new_cupcake = Cupcake(flavor=request.json["flavor"])
    # db.session.add(new_cupcake)
    # db.session.commit()
    # response_json = jsonify(cupcake=new_cupcake.serialize())
    # return (response_json, 201)

@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """update a specific ID'ed cupcake entry"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor  = request.json.get('flavor', cupcake.flavor)
    cupcake.size    = request.json.get('size', cupcake.size)
    cupcake.rating  = request.json.get('rating', cupcake.rating)
    cupcake.image   = request.json.get('image', cupcake.image)

    db.session.commit()
    serialized = serialize_cupcake(cupcake)
    return (jsonify(cupcake=serialized), 200)


@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake entry"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")

 

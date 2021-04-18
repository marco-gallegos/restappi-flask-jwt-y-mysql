from flask import Flask, jsonify, request, redirect, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

# Uso de cors para publicarla
CORS(app=app)

# configuracion mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sexp2p@192.168.0.111/apirest_python_jwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Configuracion JWT
app.config["JWT_SECRET_KEY"] = "nekdress-secret"
jwt = JWTManager(app)

# Modelo tabla Task base de datos


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

        # Modelo tabla Task base de datos


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    lastName = db.Column(db.String(70))
    nickName = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(40))

    def __init__(self, name, lastName, nickName, email, password):
        self.name = name
        self.lastName = lastName
        self.nickName = nickName
        self.email = email
        self.password = password


# Crear el modelo de la tabla
# db.create_all()

# Esquema para ingresar los datos a la base de datos tabla Task


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')


# Para guardar solo un dato a la base de datos
task_schema = TaskSchema()

# Para guardar multiple datos
tasks_schema = TaskSchema(many=True)

# Esquema para ingresar los datos a la base de datos tabla Task


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'lastName', 'nickName', 'email', 'password')


# Para guardar solo un dato a la base de datos
user_schema = UserSchema()

# Para guardar multiple datos
users_schema = UserSchema(many=True)

# ~~~~~~~~ RUTAS ~~~~~~~~
# Ruta raiz que redirije a la ruta http://url/api/


@app.route('/')
def home():
    return redirect(url_for('api'), 302)


@app.route('/api/')
def api():
    mensaje = {
        "mensaje": "Bienvenido a la ApiNek",
        "login": "http://127.0.0.1:5000/api/login",
        "apis": [
            {"task": "http://127.0.0.1:5000/api/task"},
            {"user": "http://127.0.0.1:5000/api/user"}
        ],
        "estado": 200
    }
    return jsonify(mensaje), 200

# login


@app.route('/api/login', methods=['POST'])
def login():
    nickName = request.json.get('nickName').strip()
    password = request.json.get('password').strip()

    userFind = User.query.filter_by(nickName=nickName).first()

    if userFind is None:
        return jsonify({"Respuesta":"Usuario no existe o datos invalidos."}),409

    if userFind.password != password:
        return jsonify({"Respuesta":"Error en las credenciales."}),999

    access_token = create_access_token(identity=nickName)
    return jsonify(access_token=access_token)

# api/task


@app.route('/api/task', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)


@app.route('/api/task', methods=['GET'])
@jwt_required()
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)


@app.route('/api/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    result = task_schema.dump(task)
    return jsonify(result)


@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)


@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)


# api/user

@app.route('/api/protected', methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/api/user/', methods=['POST'])
@app.route('/api/user', methods=['POST'])
def create_user():
    name = request.json['name']
    lastName = request.json['lastName']
    nickName = request.json['nickName']
    email = request.json['email']
    password = request.json['password']

    new_user = User(name, lastName, nickName, email, password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/api/user/')
@app.route('/api/user')
#@jwt_required()
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/api/user/<id>/', methods=['GET'])
@app.route('/api/user/<id>', methods=['GET'])
#@jwt_required()
def get_user(id):
    user = User.query.get(id)
    result = user_schema.dump(user)
    return jsonify(result)

@app.route('/api/user/<id>/', methods=['PUT'])
@app.route('/api/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    name = request.json['name']
    lastName = request.json['lastName']
    nickName = request.json['nickName']
    email = request.json['email']
    password = request.json['password']

    user.name = name
    user.lastName = lastName
    user.nickName = nickName
    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/api/user/<id>/', methods=['DELETE'])
@app.route('/api/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

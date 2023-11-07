
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "super-secret"  
jwt = JWTManager(app)


api = Api(app)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)



@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

students = []
class StudentNames(Resource):
    def get(self, name):
        print(students)
        for stud in students:
            if stud['name'] == name:
                return stud
        return {'name': None}, 404

    def post(self,name):
        stud = {'name': name}
        students.append(stud)
        print(students)
        return stud


    def delete(self,name):
        for ind, stud in enumerate(students):
            if stud['name'] == name:
                delted_stud = students.pop(ind)
                return {'note': 'delete successful'}



class AllNames(Resource):
    
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'students': students}

api.add_resource(StudentNames, '/student/<string:name>')
api.add_resource(AllNames, '/students')



if __name__ == "__main__":
    app.run(debug=True)
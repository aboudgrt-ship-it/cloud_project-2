from flask import flask , request , jsonify
from flask_jwt_extended import JWTManager ,create_access_token , jwt_required , get_jwt_identity


app = flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)
@app.route("/login", methods=["POST"])
def login(): 
    username = request.json.get("username" , None )
    password = request.json.get("password" , None)
    if username != "admin":
        return jsonify({"msg":" password is wrong " }) , 401 
    access_token = create_access_token(identity = username)
    return jsonify(access_token = access_token)

@app.route("protected" , methods =["GET"])
@jwt_required() 
def protecred():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as = current_user , message = "current path is protected")

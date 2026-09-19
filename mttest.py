from datetime import datetime, timedelta, timezone
import hmac 
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///: memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_TOKEN_EXPIRES # Set the access token expiration time to 1 hour  
db = SQLAlchemy(app)
jwt = JWTManager(app)


app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    username = db.Column(db.String(80), unique = True , nullable = False ) 
    password = db.Column(db.String(120), nullable = False )
    role = db.Column(db.String(80), nullable = False , default='user')

    def compare_password(self, password):
        return hmac.compare_digest(self.password, password)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id  

@jwt.user_lookup_loader
def user_lookup_loader(jwt_data):
    user_id = jwt_data['sub']
    return User.query.get(user_id)

@app.route('/who_am_i' , methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    return jsonify(username=user.username), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.compare_password(password):
        set_access_cookies(jsonify(), create_access_token(identity=user,
                                                           expires_delta=ACCESS_TOKEN_EXPIRES))
        access_token = create_access_token(identity=user, 
                                           expires_delta=ACCESS_TOKEN_EXPIRES)      
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = TokenBlockList.query.filter_by(jti=jti).first()
    return token is not None

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    set_access_cookies(jsonify(), create_access_token(identity=user, expires_delta=ACCESS_TOKEN_EXPIRES))
    return user


def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    return {"role": user.role}

@app.route('/protected', methods=['POST'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    return jsonify(logged_in_as=user.username), 200


@app.route('/optionally_protected', methods=['GET'])
@jwt_required(optional=True)
def optionally_protected_route():
    current_user = get_jwt_identity()
    if current_user:
        user = User.query.get(current_user)
        return jsonify(logged_in_as=user.username), 200
    else:
        return jsonify(message="No JWT provided"), 200

@app.route('/login_with_cookies', methods=['POST'])
def login_with_cookies():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.compare_password(password):
        access_token = create_access_token(identity=user,
                                            additional_claims={"role": user.role}
                                            , expires_delta=ACCESS_TOKEN_EXPIRES
        )
        response = jsonify(access_token=access_token)
        response.set_cookie('access_token', access_token, httponly=True)
        set_access_cookies(response, access_token)
        return response, 200
    
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/protected_with_cookies', methods=['GET'])
@jwt_required()
def protected_with_cookies():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    return jsonify(logged_in_as=user.username), 200

@app.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    db.session.add(TokenBlockList(jti=jti))
    db.session.commit()
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@app.after_request
def refresh_cookies(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=5))
        if target_timestamp > exp_timestamp:
            current_user = get_jwt_identity()
            user = User.query.get(current_user)
            access_token = create_access_token(identity=user,
                                                additional_claims={"role": user.role}
                                                , expires_delta=ACCESS_TOKEN_EXPIRES
            )
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


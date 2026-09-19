import os
import boto3
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from botocore.exceptions import NoCredentialsError, ClientError

app = Flask(__name__)

# --- الإعدادات (Configurations) ---
# في الإنتاج، نستخدم متغيرات البيئة للحفاظ على سرية المفاتيح
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "fallback-secret-for-dev")
jwt = JWTManager(app)

# إعداد اتصال AWS (يفضل استخدام IAM Roles في AWS لضمان الأمان)
s3_client = boto3.client('s3')

# --- المسارات (Routes) ---

@app.route("/login", methods=["POST"])
def login():
    """
    مسار تسجيل الدخول: يتحقق من الهوية ويعطي الرمز.
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # في الواقع، نتحقق من قاعدة البيانات هنا
    if username == "aws_user" and password == "secure_password":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "بيانات الدخول غير صحيحة"}), 401


@app.route("/list-my-buckets", methods=["GET"])
@jwt_required()
def list_buckets():
    """
    مسار محمي: لا يمكن الوصول إليه إلا بـ JWT، ويقوم بعمل حقيقي في AWS.
    """
    current_user = get_jwt_identity()
    
    try:
        # محاولة جلب قائمة الـ Buckets من حساب AWS الخاص بك
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        return jsonify({
            "user": current_user,
            "buckets": buckets,
            "message": "تم جلب البيانات بنجاح من AWS"
        }), 200

    except NoCredentialsError:
        return jsonify({"error": "فشل التحقق من صلاحيات AWS"}), 500
    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "حدث خطأ غير متوقع"}), 500


if __name__ == "__main__":
    # تشغيل التطبيق في وضع التطوير
    app.run(debug=True, port=5000)

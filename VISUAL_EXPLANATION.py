"""
═══════════════════════════════════════════════════════════════════════════════
                    شرح مرئي - Visual Code Explanation
                          S3Manager Architecture
═══════════════════════════════════════════════════════════════════════════════
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                   1. تسلسل العمل - How It Works
╚════════════════════════════════════════════════════════════════════════════╝

المستخدم (User)
    ↓
    ↓ (استدعاء)
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ S3Manager Class                                                 │
│                                                                 │
│  __init__()  ← يُستدعى عند الإنشاء                            │
│    ├─ self.s3 = boto3.client('s3', region_name=region)        │
│    └─ self.region = region                                     │
│                                                                 │
│  create_bucket(bucket_name)                                     │
│  upload_file(bucket_name, file_path)                           │
│  list_objects(bucket_name)                                      │
│  delete_object(bucket_name, key)                               │
│  ... (دوال أخرى)                                               │
└─────────────────────────────────────────────────────────────────┘
    ↓ (استدعاء)
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ boto3.client('s3')                                              │
│ (الاتصال الفعلي بـ AWS)                                         │
└─────────────────────────────────────────────────────────────────┘
    ↓ (HTTP requests)
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ AWS S3 Service                                                  │
│ (الخدمة الفعلية على أجهزة Amazon)                               │
└─────────────────────────────────────────────────────────────────┘


════════════════════════════════════════════════════════════════════════════════
مثال عملي خطوة بخطوة:
════════════════════════════════════════════════════════════════════════════════

1. الخطوة الأولى: الاستيراد والإنشاء
   ─────────────────────────────────
   from s3_guide_v2 import S3Manager
   s3 = S3Manager(region='us-east-1')
   
   ↓ ماذا يحدث؟
   
   • __init__() يُستدعى تلقائيًا
   • يُنشئ اتصال boto3
   • يحفظ المنطقة الجغرافية


2. الخطوة الثانية: إنشاء bucket
   ────────────────────────────
   s3.create_bucket('my-bucket')
   
   ↓ ماذا يحدث؟
   
   • البحث عن الـ method: create_bucket
   • استدعاء self.s3.create_bucket(Bucket='my-bucket')
   • boto3 يرسل request إلى AWS
   • AWS ينشئ الـ bucket
   • النتيجة تُطبع: ✓ تم إنشاء الـ bucket


3. الخطوة الثالثة: رفع ملف
   ───────────────────────
   s3.upload_file('my-bucket', 'test.txt')
   
   ↓ ماذا يحدث؟
   
   • البحث عن الـ method: upload_file
   • التحقق من أن الملف موجود: os.path.exists()
   • استدعاء self.s3.upload_file(...)
   • boto3 يرسل الملف إلى AWS
   • AWS يحفظ الملف
   • النتيجة تُطبع: ✓ تم رفع


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   2. شرح self - What is self?
╚════════════════════════════════════════════════════════════════════════════╝

self = الكائن نفسه (الـ object itself)

تشبيه:
───────
تخيل أنك تكتب تعليمات لروبوت.

class Robot:
    def __init__(self, color):
        self.color = color           # self = الروبوت
                                     # color = لون الروبوت
    
    def print_info(self):
        print(f"لوني: {self.color}")  # اطبع لون الروبوت


robot1 = Robot('أحمر')
robot2 = Robot('أزرق')

robot1.print_info()  → لوني: أحمر
robot2.print_info()  → لوني: أزرق


# في S3Manager:

class S3Manager:
    def __init__(self, region='us-east-1'):
        self.s3 = boto3.client(...)     # self = الـ manager object
        self.region = region             # احفظ الخصائص
    
    def create_bucket(self, bucket_name):
        self.s3.create_bucket(...)      # استخدم الاتصال المحفوظ


s3_manager1 = S3Manager(region='us-east-1')
s3_manager2 = S3Manager(region='eu-west-1')

# كل manager لديه اتصاله الخاص والمنطقته الخاصة


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   3. شرح boto3.client - The Connection
╚════════════════════════════════════════════════════════════════════════════╝

boto3.client('s3', region_name='us-east-1')
│      │        │                    │
│      │        │                    └─ المنطقة الجغرافية
│      │        └─────────────────── الخدمة (S3)
│      └────────────────────────── مكتبة AWS
└───────────────────────────────── إنشاء اتصال

النتيجة: كائن يمكنه:
────────────────

s3.create_bucket()     ← إنشاء bucket
s3.upload_file()       ← رفع ملف
s3.list_buckets()      ← عرض الـ buckets
s3.delete_object()     ← حذف ملف
... (وهكذا)


المناطق الجغرافية (Regions):
─────────────────────────────

us-east-1       ← أمريكا (فرجينيا)
eu-west-1       ← أوروبا (أيرلندا)
ap-southeast-1  ← آسيا (سنغافورة)
... (وغيرها)

# اختيار منطقة مختلفة:

s3_eu = S3Manager(region='eu-west-1')
# الآن جميع العمليات ستكون في أوروبا


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   4. شرح try/except - Error Handling
╚════════════════════════════════════════════════════════════════════════════╝

try/except = جرب الكود، وإذا حدث خطأ افعل كذا

try:
    ┌──────────────────────────────────────────┐
    │ الكود الذي قد يسبب خطأ                  │
    │                                          │
    │ s3.create_bucket(Bucket=bucket_name)    │
    │                                          │
    │ إذا نجح: ← يطبع ✓ وينتهي                │
    │ إذا فشل: ← ينتقل إلى except              │
    └──────────────────────────────────────────┘

except ClientError as e:
    ┌──────────────────────────────────────────┐
    │ الكود الذي يُستدعى إذا حدث خطأ           │
    │                                          │
    │ print(f"✗ خطأ: {e}")                   │
    │                                          │
    │ e = معلومات الخطأ                       │
    └──────────────────────────────────────────┘


أمثلة الأخطاء:
──────────────

# خطأ 1: Bucket مستخدم بالفعل
try:
    s3.create_bucket(Bucket='my-bucket')
except ClientError as e:
    if 'BucketAlreadyExists' in str(e):
        print("هذا الـ bucket موجود بالفعل")


# خطأ 2: لا توجد credentials
try:
    s3 = S3Manager()
except NoCredentialsError:
    print("لم يتم العثور على AWS credentials")
    print("قم بـ: aws configure")


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   5. شرح response - Getting Results Back
╚════════════════════════════════════════════════════════════════════════════╝

response = s3.list_buckets()

response = dictionary يحتوي على النتيجة
│
├─ 'Buckets' ← قائمة الـ buckets
│   ├─ {'Name': 'bucket1', 'CreationDate': ...}
│   └─ {'Name': 'bucket2', 'CreationDate': ...}
│
└─ 'ResponseMetadata' ← معلومات إضافية عن الـ request


تصور بصري:
──────────

response = {
    'Buckets': [
        {
            'Name': 'test-bucket-1',
            'CreationDate': datetime(2026, 8, 15, 1, 23, 45)
        },
        {
            'Name': 'test-bucket-2',
            'CreationDate': datetime(2026, 8, 15, 1, 24, 30)
        }
    ],
    'ResponseMetadata': {
        'HTTPStatusCode': 200,
        'RequestId': '...'
    }
}

# للوصول إلى الـ buckets:
buckets = response['Buckets']

# للمرور على كل bucket:
for bucket in buckets:
    name = bucket['Name']
    date = bucket['CreationDate']
    print(f"{name}: {date}")


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   6. شرح Methods vs Functions
╚════════════════════════════════════════════════════════════════════════════╝

الفرق بين Method و Function:
─────────────────────────────

Function (دالة):
────────────────
def greet(name):
    print(f"السلام عليكم {name}")

greet("أحمد")  ← استدعاء مباشر


Method (دالة داخل class):
─────────────────────────
class Person:
    def greet(self, name):
        print(f"السلام عليكم {name}")

person = Person()
person.greet("أحمد")  ← استدعاء من object

# في S3Manager:

class S3Manager:
    def create_bucket(self, bucket_name):  ← method
        self.s3.create_bucket(Bucket=bucket_name)

# الاستدعاء:
s3 = S3Manager()           ← إنشاء object
s3.create_bucket('my-b')   ← استدعاء method من الـ object


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   7. شرح Dictionary و Keys
╚════════════════════════════════════════════════════════════════════════════╝

Dictionary = مثل قاموس (مفتاح - قيمة)

person = {
    'name': 'أحمد',
    'age': 25,
    'city': 'القاهرة'
}
  │      │
  └──────┴─ (key, value) أزواج

للوصول إلى القيمة:
─────────────────

person['name']   → 'أحمد'
person['age']    → 25
person['city']   → 'القاهرة'

# في S3:

obj = {
    'Key': 'test.txt',
    'Size': 1024,
    'LastModified': datetime(...),
    'ETag': '...'
}

obj['Key']           → 'test.txt'
obj['Size']          → 1024
obj['LastModified']  → datetime(...)


مثال في S3Manager:
──────────────────

response = s3.list_objects_v2(Bucket='my-bucket')

# النتيجة:
{
    'Contents': [
        {'Key': 'file1.txt', 'Size': 100},
        {'Key': 'file2.txt', 'Size': 200}
    ]
}

# للوصول:
for obj in response['Contents']:
    print(obj['Key'])    → file1.txt, file2.txt


════════════════════════════════════════════════════════════════════════════════


╔════════════════════════════════════════════════════════════════════════════╗
║                   8. ملخص الخطوات - Step by Step
╚════════════════════════════════════════════════════════════════════════════╝

1️⃣  استيراد وإنشاء:
   from s3_guide_v2 import S3Manager
   s3 = S3Manager()
   
   ↓ يحدث:
   - Python يفتح الملف s3_guide_v2.py
   - يجد class S3Manager
   - ينشئ object جديد
   - يستدعي __init__()
   - يتصل بـ AWS


2️⃣  استدعاء method:
   s3.create_bucket('my-bucket')
   
   ↓ يحدث:
   - Python يبحث عن method create_bucket
   - يستدعيه مع self و bucket_name
   - البحث عن condition (if/else)
   - استدعاء self.s3.create_bucket()
   - معالجة النتيجة أو الخطأ
   - طبع الرسالة


3️⃣  معالجة النتيجة:
   response = s3.list_objects(bucket)
   
   ↓ يحدث:
   - method يرجع response
   - response = dictionary
   - يمكن الوصول إلى 'Contents'
   - المرور على الملفات


════════════════════════════════════════════════════════════════════════════════

✅ الآن تفهم البنية الكاملة!

الخطوة التالية:
1. اقرأ التعليقات في s3_guide_v2.py
2. جرب تعديل الأكواد
3. اقرأ AWS Boto3 Official Documentation
""")

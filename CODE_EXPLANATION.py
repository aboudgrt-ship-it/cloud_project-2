"""
═══════════════════════════════════════════════════════════════════════════════
                    شرح تفصيلي لـ S3Manager Code
                   Detailed Code Explanation - S3Manager
═══════════════════════════════════════════════════════════════════════════════

هذا الملف يشرح كل سطر كود في S3Manager
This file explains every line of code in S3Manager

"""

# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 1: الاستيراد (Imports)
# ═══════════════════════════════════════════════════════════════════════════════

"""
import boto3
════════════════════
ماذا يفعل:
- استيراد مكتبة boto3 (AWS SDK للـ Python)
- boto3 = مكتبة تسمح لك بالتحدث مع خدمات AWS من Python

مثال تشبيهي:
- boto3 = remote control لـ TV (AWS)
- بدون boto3، لا يمكنك التحكم في AWS من Python
"""

import boto3

"""
import os
════════════════════
ماذا يفعل:
- استيراد مكتبة os للتعامل مع نظام التشغيل
- استخدام: التحقق من وجود ملفات، الحصول على أسماء الملفات، إلخ

مثال:
os.path.exists('file.txt')  → هل الملف موجود؟
os.listdir('./folder')       → قائمة الملفات في المجلد
"""

import os

"""
from datetime import datetime
════════════════════════════════
ماذا يفعل:
- استيراد فئة datetime للتعامل مع التاريخ والوقت
- استخدام: الحصول على التاريخ الحالي، تنسيق الوقت، إلخ

مثال:
datetime.now()               → الوقت الحالي
datetime.now().strftime('%Y-%m-%d')  → تاريخ بصيغة YYYY-MM-DD
"""

from datetime import datetime

"""
from botocore.exceptions import ClientError, NoCredentialsError
════════════════════════════════════════════════════════════════
ماذا يفعل:
- استيراد فئات الأخطاء من botocore (جزء داخلي من boto3)
- ClientError = خطأ عند التواصل مع AWS
- NoCredentialsError = خطأ عندما لا يوجد AWS credentials

مثال للأخطاء:
try:
    s3.create_bucket(Bucket='bucket')
except ClientError as e:
    print(f"خطأ: {e}")  → يطبع رسالة الخطأ
"""

from botocore.exceptions import ClientError, NoCredentialsError


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 2: تعريف الـ Class
# ═══════════════════════════════════════════════════════════════════════════════

"""
class S3Manager:
    '''مدير S3 - S3 Manager Class'''
═════════════════════════════════════════════════
ماذا يفعل:
- class = قالب (template) لإنشاء كائنات
- S3Manager = اسم الـ class
- كل object من S3Manager سيحتوي على نفس الدوال والخصائص

تشبيه:
- class = مثل وصفة الطبخ
- object = الطبخة الفعلية (لكل طبخة نفس المكونات والطريقة)

مثال الاستخدام:
s3 = S3Manager()                    # إنشاء object
s3.create_bucket('my-bucket')       # استخدام الدالة من الـ class
"""


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 3: دالة __init__ (البناء - Constructor)
# ═══════════════════════════════════════════════════════════════════════════════

"""
def __init__(self, region='us-east-1'):
════════════════════════════════════════════
ماذا يفعل:
- __init__ = دالة تُستدعى تلقائيًا عند إنشاء object جديد
- self = إشارة إلى الـ object نفسه (نقول له: هذا الـ object)
- region = معامل (parameter) مع قيمة افتراضية 'us-east-1'

متى تُستدعى:
s3 = S3Manager()                    # هنا __init__ يُستدعى تلقائيًا
s3 = S3Manager(region='eu-west-1') # هنا أيضًا مع region مختلفة

الـ self:
- مثل "I" في الإنجليزية
- self.s3 = "معلومات الـ object نفسه"
- self.region = "إحفظ المنطقة في الـ object"
"""

"""
try:
    self.s3 = boto3.client('s3', region_name=region)
═════════════════════════════════════════════════════════════
شرح مفصل لهذا السطر:

1. boto3.client('s3', ...)
   ━━━━━━━━━━━━━━━━━━━━━━━
   - client() = دالة في boto3 لإنشاء اتصال مع خدمة AWS
   - 's3' = اسم الخدمة (في هذه الحالة S3)
   - region_name=region = تحديد المنطقة الجغرافية
   
   مثال:
   s3_client = boto3.client('s3', region_name='us-east-1')
   ↓ هذا يُنشئ متغير يسمى s3_client يتحكم في S3 في منطقة us-east-1

2. self.s3 = ...
   ━━━━━━━━━━━━━━━
   - حفظ الاتصال في الـ object
   - self.s3 يمكن استخدامه في أي دالة أخرى في الـ class
   
   مثال:
   def upload_file(self):
       self.s3.upload_file(...)  ← يستخدم الاتصال المحفوظ

3. try/except
   ━━━━━━━━━━━
   - try = جرب هذا الكود
   - except = إذا حدث خطأ، افعل كذا
   
   مثال:
   try:
       x = 10 / 2      # سينجح
   except:
       print("خطأ")    # لن يُطبع
   
   try:
       x = 10 / 0      # خطأ!
   except:
       print("خطأ")    # سيُطبع
"""

# مثال عملي شامل:
print("""
مثال عملي:

import boto3

# الطريقة القديمة (بدون class):
s3 = boto3.client('s3', region_name='us-east-1')
response = s3.list_buckets()
print(response)

# الطريقة الحديثة (مع S3Manager):
from s3_guide_v2 import S3Manager

s3 = S3Manager(region='us-east-1')
s3.list_buckets()  ← أسهل وأكثر وضوحًا!
""")


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 4: شرح الدوال الرئيسية
# ═══════════════════════════════════════════════════════════════════════════════

"""
════════════════════════════════════════════════════════════════════════════════
دالة: create_bucket
════════════════════════════════════════════════════════════════════════════════

def create_bucket(self, bucket_name):
    '''إنشاء bucket جديد'''
    
شرح المعاملات:
- self = الـ object نفسه
- bucket_name = اسم الـ bucket المراد إنشاؤه (مثل 'my-bucket')

الكود:
    if self.region == 'us-east-1':
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - تحقق: هل المنطقة us-east-1؟
    - لأن us-east-1 لا تحتاج CreateBucketConfiguration
    - باقي المناطق تحتاج كود إضافي
    
    مثال:
    if True:
        print("نعم")  ← يُطبع
    
    if False:
        print("نعم")  ← لا يُطبع


        self.s3.create_bucket(Bucket=bucket_name)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - استخدم الاتصال المحفوظ في self.s3
        - استدعِ دالة create_bucket من boto3
        - مرر اسم الـ bucket
        
        مثال:
        self.s3.create_bucket(Bucket='my-awesome-bucket')
        ↓
        AWS سينشئ bucket بهذا الاسم


    else:
        ━━━━━━
        - إذا لم تكن us-east-1، فافعل كذا...
        
        self.s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': self.region}
        )
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - Bucket=bucket_name = اسم الـ bucket
        - CreateBucketConfiguration = إعدادات الإنشاء
        - LocationConstraint = تحديد المنطقة
        
        مثال:
        إذا كنت في eu-west-1 (أيرلندا):
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
        ↓
        AWS سينشئ الـ bucket في أيرلندا وليس أمريكا


    print(f"✓ تم إنشاء الـ bucket: {bucket_name}")
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - print = طبع رسالة على الشاشة
    - f"..." = f-string (طريقة حديثة لدمج المتغيرات في النصوص)
    - {bucket_name} = ضع قيمة المتغير هنا
    
    مثال:
    bucket_name = 'my-bucket'
    print(f"✓ تم إنشاء الـ bucket: {bucket_name}")
    ↓
    ✓ تم إنشاء الـ bucket: my-bucket


    return True
    ━━━━━━━━━━━
    - return = ارجع إلى الكود الذي استدعى هذه الدالة
    - True = قيمة المرجع (صح/نعم)
    
    مثال:
    success = s3.create_bucket('my-bucket')
    if success:
        print("نجح!")  ← يُطبع


except ClientError as e:
━━━━━━━━━━━━━━━━━━━━━
- إذا حدث خطأ (ClientError)
- احفظ تفاصيل الخطأ في متغير يسمى 'e'

مثال:
try:
    x = 10 / 0      # خطأ!
except ZeroDivisionError as e:
    print(e)        # يطبع: division by zero
"""


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 5: شرح دوال Upload
# ═══════════════════════════════════════════════════════════════════════════════

"""
════════════════════════════════════════════════════════════════════════════════
دالة: upload_file (رفع ملف من جهازك)
════════════════════════════════════════════════════════════════════════════════

def upload_file(self, bucket_name, file_path, s3_key=None):
    '''رفع ملف من جهازك إلى S3'''

المعاملات:
- bucket_name = اسم الـ bucket (مثل 'my-bucket')
- file_path = مسار الملف على جهازك (مثل '/home/user/test.txt')
- s3_key = اسم الملف في S3 (اختياري، default = نفس اسم الملف)


    if not os.path.exists(file_path):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - تحقق: هل الملف موجود على جهازك؟
    - os.path.exists() = دالة تُرجع True/False
    - not = نفي (معاكس)
    
    مثال:
    os.path.exists('/home/user/test.txt')  → True (موجود)
    os.path.exists('/home/user/xyz.txt')   → False (غير موجود)
    not False  → True


    if s3_key is None:
    ━━━━━━━━━━━━━━━━━━
    - تحقق: هل المستخدم لم يحدد اسم الملف في S3؟
    - is None = يساوي None (لا يوجد قيمة)
    
    مثال:
    s3_key = None
    if s3_key is None:
        print("لا يوجد قيمة")  ← يُطبع


        s3_key = os.path.basename(file_path)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - os.path.basename() = احصل على اسم الملف فقط
        
        مثال:
        file_path = '/home/user/folder/test.txt'
        os.path.basename(file_path)  → 'test.txt'
        ↓
        s3_key = 'test.txt'


    self.s3.upload_file(file_path, bucket_name, s3_key)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - استخدم الاتصال المحفوظ
    - استدعِ دالة upload_file من boto3
    - file_path = من أين (ملفك المحلي)
    - bucket_name = إلى أين (الـ bucket)
    - s3_key = باسم كذا (في S3)
    
    مثال:
    self.s3.upload_file(
        '/home/user/test.txt',    # الملف المحلي
        'my-bucket',              # الـ bucket
        'test.txt'                # الاسم في S3
    )
    ↓
    رفع /home/user/test.txt إلى s3://my-bucket/test.txt


════════════════════════════════════════════════════════════════════════════════
دالة: upload_text (رفع نص مباشرة)
════════════════════════════════════════════════════════════════════════════════

def upload_text(self, bucket_name, s3_key, text):
    '''رفع نص مباشرة بدون ملف'''

المعاملات:
- bucket_name = اسم الـ bucket
- s3_key = اسم الملف في S3
- text = محتوى النص

    if isinstance(text, str):
    ━━━━━━━━━━━━━━━━━━━━━━━━━
    - isinstance() = دالة تتحقق من نوع المتغير
    - str = نوع النص (string)
    
    مثال:
    isinstance("hello", str)      → True (نص)
    isinstance(123, str)          → False (رقم)


        text = text.encode('utf-8')
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        - .encode() = حول النص إلى bytes
        - 'utf-8' = تشفير معياري يدعم اللغات جميع
        
        مثال:
        "مرحبا" (نص عادي)
        ↓
        .encode('utf-8')
        ↓
        b'\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7' (bytes)


    self.s3.put_object(Bucket=bucket_name, Key=s3_key, Body=text)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - put_object() = ضع ملف في S3
    - Bucket = الـ bucket
    - Key = اسم الملف
    - Body = محتوى الملف
    
    مثال:
    self.s3.put_object(
        Bucket='my-bucket',
        Key='hello.txt',
        Body=b'Hello World'  ← bytes
    )
"""


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 6: شرح دوال List/Search
# ═══════════════════════════════════════════════════════════════════════════════

"""
════════════════════════════════════════════════════════════════════════════════
دالة: list_objects (عرض الملفات)
════════════════════════════════════════════════════════════════════════════════

def list_objects(self, bucket_name, prefix='', limit=None):
    '''عرض الملفات في الـ bucket'''

المعاملات:
- bucket_name = الـ bucket
- prefix = مجلد معين (مثل 'documents/')
- limit = عدد الملفات المراد عرضها


    response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - استدعِ دالة list_objects_v2 من boto3
    - Bucket = الـ bucket
    - Prefix = (اختياري) تصفية حسب البادئة
    - response = احفظ النتيجة
    
    مثال:
    response = self.s3.list_objects_v2(Bucket='my-bucket', Prefix='documents/')
    ↓
    response سيحتوي على جميع الملفات التي تبدأ بـ 'documents/'


    if 'Contents' not in response:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - تحقق: هل توجد ملفات في النتيجة؟
    - 'Contents' = مفتاح يحتوي على الملفات
    - not in = هل المفتاح غير موجود؟
    
    مثال:
    my_dict = {'name': 'Ahmed', 'age': 25}
    'email' in my_dict       → False (غير موجود)
    'email' not in my_dict   → True


    for obj in response.get('Contents', []):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - for = حلقة (استدعِ لكل عنصر)
    - response.get('Contents', []) = احصل على الملفات أو قائمة فارغة
    - obj = متغير يمثل كل ملف
    
    مثال:
    my_list = [1, 2, 3, 4]
    for num in my_list:
        print(num)  ← يطبع 1، ثم 2، ثم 3، ثم 4


        if limit and i >= limit:
        ━━━━━━━━━━━━━━━━━━━━━━━━━
        - تحقق: هل وصلنا إلى الحد الأقصى؟
        - and = و (يجب أن تكون الشرطتان صحيحتان)
        
        مثال:
        limit = 10
        i = 15
        if limit and i >= limit:  → True (10 موجود و 15 >= 10)


        key = obj['Key']
        size = obj['Size']
        ━━━━━━━━━━━━━━━━━━━━━━━
        - احصل على خصائص الملف من obj
        - obj['Key'] = اسم الملف
        - obj['Size'] = حجم الملف
        
        مثال:
        obj = {'Key': 'test.txt', 'Size': 1024}
        key = obj['Key']   → 'test.txt'
        size = obj['Size'] → 1024
"""


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 7: شرح دوال Download
# ═══════════════════════════════════════════════════════════════════════════════

"""
════════════════════════════════════════════════════════════════════════════════
دالة: download_text (تحميل نص)
════════════════════════════════════════════════════════════════════════════════

def download_text(self, bucket_name, s3_key):
    '''تحميل نص من S3'''

    response = self.s3.get_object(Bucket=bucket_name, Key=s3_key)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - get_object() = احصل على ملف من S3
    - Bucket = الـ bucket
    - Key = اسم الملف
    - response = احفظ النتيجة


    data = response['Body'].read()
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - response['Body'] = جسم الملف (محتواه)
    - .read() = اقرأ المحتوى كاملاً
    - data = احفظه في متغير
    
    مثال:
    response['Body'] = <object يحتوي على البيانات>
    response['Body'].read() = اقرأ كل البيانات
    ↓
    data = b'Hello World'  ← bytes


    text = data.decode('utf-8')
    ━━━━━━━━━━━━━━━━━━━━━━━━━━
    - .decode() = حول bytes إلى نص
    - 'utf-8' = استخدم نفس التشفير
    
    مثال:
    b'\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7'  (bytes)
    ↓
    .decode('utf-8')
    ↓
    "مرحبا"  (نص)
"""


# ═══════════════════════════════════════════════════════════════════════════════
# الجزء 8: شرح دوال Delete
# ═══════════════════════════════════════════════════════════════════════════════

"""
════════════════════════════════════════════════════════════════════════════════
دالة: delete_object (حذف ملف)
════════════════════════════════════════════════════════════════════════════════

def delete_object(self, bucket_name, s3_key):
    '''حذف ملف واحد'''

    self.s3.delete_object(Bucket=bucket_name, Key=s3_key)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - delete_object() = احذف ملف من S3
    - Bucket = الـ bucket
    - Key = اسم الملف
    
    مثال:
    self.s3.delete_object(Bucket='my-bucket', Key='test.txt')
    ↓
    حذف s3://my-bucket/test.txt


════════════════════════════════════════════════════════════════════════════════
دالة: delete_multiple (حذف عدة ملفات)
════════════════════════════════════════════════════════════════════════════════

def delete_multiple(self, bucket_name, keys_list):
    '''حذف عدة ملفات'''

    objects_to_delete = [{'Key': key} for key in keys_list]
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - list comprehension = طريقة سريعة لإنشاء قائمة
    - for key in keys_list = لكل مفتاح في القائمة
    - {'Key': key} = أنشئ dictionary بهذا الشكل
    
    مثال:
    keys_list = ['file1.txt', 'file2.txt', 'file3.txt']
    
    objects_to_delete = [{'Key': key} for key in keys_list]
    ↓
    [
        {'Key': 'file1.txt'},
        {'Key': 'file2.txt'},
        {'Key': 'file3.txt'}
    ]
    
    # بدون list comprehension:
    objects_to_delete = []
    for key in keys_list:
        objects_to_delete.append({'Key': key})


    self.s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - delete_objects() = احذف عدة ملفات دفعة واحدة
    - Bucket = الـ bucket
    - Delete = معامل يحتوي على الملفات المراد حذفها
    - Objects = قائمة الملفات
"""


# ═══════════════════════════════════════════════════════════════════════════════
# ملخص شامل: مقارنة بين الطرق المختلفة
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                        ملخص شامل - المقارنة
╚════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. استخدام boto3 مباشرة (بدون S3Manager)
│ ─────────────────────────────────────────
│
│ import boto3
│ 
│ s3 = boto3.client('s3', region_name='us-east-1')
│ s3.create_bucket(Bucket='my-bucket')
│ s3.upload_file('local.txt', 'my-bucket', 'local.txt')
│ response = s3.list_objects_v2(Bucket='my-bucket')
│ s3.delete_object(Bucket='my-bucket', Key='file.txt')
│
│ الفوائد:
│ ✓ بسيط ومباشر
│ ✗ نفس الأكواد متكررة
│ ✗ معالجة الأخطاء تحتاج تكرار
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. استخدام S3Manager (مع Class)
│ ───────────────────────────────────
│
│ from s3_guide_v2 import S3Manager
│ 
│ s3 = S3Manager(region='us-east-1')
│ s3.create_bucket('my-bucket')
│ s3.upload_file('my-bucket', 'local.txt')
│ s3.list_objects('my-bucket')
│ s3.delete_object('my-bucket', 'file.txt')
│
│ الفوائد:
│ ✓ أكثر وضوحًا وسهولة
│ ✓ معالجة الأخطاء مدمجة
│ ✓ رسائل خطأ واضحة بالعربية
│ ✓ إعادة استخدام الكود أسهل
│ ✓ دوال helper (مثل upload_folder)
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. تفكك الأجزاء الرئيسية
│ ──────────────────────────
│
│ boto3.client('s3', region_name=region)
│  ↓
│ إنشاء اتصال مع خدمة S3 في منطقة معينة
│
│ self.s3 = ...
│  ↓
│ حفظ الاتصال لاستخدامه لاحقًا
│
│ try/except
│  ↓
│ التعامل مع الأخطاء بشكل آمن
│
│ response = self.s3.method(...)
│  ↓
│ استدعاء دالة من boto3 والحصول على النتيجة
│
│ for obj in response.get('Contents', []):
│  ↓
│ المرور على قائمة الملفات واحدًا تلو الآخر
└─────────────────────────────────────────────────────────────────────────────┘
""")


# ═══════════════════════════════════════════════════════════════════════════════
# أمثلة إضافية للتوضيح
# ═══════════════════════════════════════════════════════════════════════════════

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                       أمثلة إضافية للتوضيح
╚════════════════════════════════════════════════════════════════════════════╝

مثال 1: فهم self
════════════════

class Car:
    def __init__(self, color):
        self.color = color      # self = هذه السيارة
    
    def print_color(self):
        print(self.color)       # اطبع لون هذه السيارة

car1 = Car('red')
car2 = Car('blue')

car1.print_color()  → red
car2.print_color()  → blue

# كل سيارة لديها لونها الخاص (self)


مثال 2: فهم boto3.client
═══════════════════════════

s3 = boto3.client('s3')
# مثل: فتح برنامج للتحكم في S3

s3.create_bucket(Bucket='test')
# مثل: اضغط على زر "Create Bucket"

response = s3.list_buckets()
# مثل: اضغط على زر "List Buckets" وحفظ النتيجة


مثال 3: فهم response (النتيجة)
═══════════════════════════════

response = s3.list_buckets()
print(response)

# النتيجة (dictionary كبير):
{
    'Buckets': [
        {'Name': 'bucket1', 'CreationDate': ...},
        {'Name': 'bucket2', 'CreationDate': ...}
    ]
}

# للوصول إلى الملفات:
for bucket in response['Buckets']:
    print(bucket['Name'])
# يطبع: bucket1, bucket2


مثال 4: فهم معالجة الأخطاء
════════════════════════════

try:
    s3.create_bucket(Bucket='bucket')
except ClientError as e:
    print(e)

# إذا حدث خطأ (مثلاً: الـ bucket موجود بالفعل):
# يطبع رسالة الخطأ بدل إيقاف البرنامج كليًا
""")

print("""
✅ الآن تفهم كل سطر في الكود!

للمزيد من الفهم:
1. اقرأ التعليقات في s3_guide_v2.py
2. جرب تعديل الأكواد بنفسك
3. اقرأ AWS Boto3 Documentation
""")

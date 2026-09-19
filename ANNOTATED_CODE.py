"""
═══════════════════════════════════════════════════════════════════════════════
              S3Manager Code - Fully Annotated Version
                      مع شرح كل سطر بالتفصيل
═══════════════════════════════════════════════════════════════════════════════
"""

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ الجزء 1: الاستيراد (Imports)                                                 │
# └─────────────────────────────────────────────────────────────────────────────┘

# استيراد boto3 - مكتبة AWS الرسمية للـ Python
# boto3 = أداة للتحكم في خدمات AWS من داخل Python
import boto3

# استيراد os - للتعامل مع نظام التشغيل والملفات
# os.path.exists() = التحقق من وجود ملف
# os.listdir() = قائمة الملفات في مجلد
import os

# استيراد datetime - للتعامل مع التاريخ والوقت
# datetime.now() = الوقت الحالي
from datetime import datetime

# استيراد فئات الأخطاء من botocore (جزء داخلي من boto3)
# ClientError = خطأ عند التواصل مع AWS
# NoCredentialsError = خطأ عندما لا يوجد AWS credentials
from botocore.exceptions import ClientError, NoCredentialsError


# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ الجزء 2: تعريف الـ Class                                                      │
# └─────────────────────────────────────────────────────────────────────────────┘

class S3Manager:
    """
    مدير S3 - S3 Manager Class
    
    هذا الـ class يجمع كل عمليات S3 في مكان واحد
    بدل استخدام boto3 مباشرة
    """
    
    # ═════════════════════════════════════════════════════════════════════════
    # الدالة: __init__ (البناء - Constructor)
    # ═════════════════════════════════════════════════════════════════════════
    
    def __init__(self, region='us-east-1'):
        """
        دالة البناء - تُستدعى تلقائيًا عند إنشاء object جديد
        
        المعاملات:
        - self = إشارة إلى الـ object نفسه (ضروري في كل method)
        - region = المنطقة الجغرافية (افتراضي: us-east-1)
        
        المثال:
        s3 = S3Manager()                    # تُستدعى __init__ هنا
        s3 = S3Manager(region='eu-west-1') # تُستدعى مع region مختلفة
        """
        try:
            # إنشاء اتصال مع خدمة S3 في المنطقة المحددة
            # boto3.client() = دالة في boto3 لإنشاء اتصال
            # 's3' = اسم الخدمة (في هذه الحالة S3)
            # region_name = تحديد المنطقة (us-east-1, eu-west-1, إلخ)
            self.s3 = boto3.client('s3', region_name=region)
            
            # حفظ المنطقة في الـ object لاستخدامها لاحقًا
            # self.region = معنى "خاصيتي" (خاصية الـ object)
            self.region = region
            
            # اطبع رسالة نجاح
            print(f"✓ متصل بـ S3 في المنطقة: {region}")
            
        # إذا حدث خطأ (مثل: لا توجد AWS credentials)
        except NoCredentialsError:
            # اطبع رسالة خطأ واضحة
            print("✗ خطأ: لم يتم العثور على AWS credentials")
            print("  تأكد من تشغيل: aws configure")
            # أعد رفع الخطأ ليتوقف البرنامج هنا
            raise


    # ═════════════════════════════════════════════════════════════════════════
    # الدالة: create_bucket
    # ═════════════════════════════════════════════════════════════════════════
    
    def create_bucket(self, bucket_name):
        """
        إنشاء bucket جديد
        
        المعاملات:
        - bucket_name = اسم الـ bucket (مثل 'my-bucket')
        
        الملاحظات المهمة:
        - اسم الـ bucket يجب أن يكون فريدًا عالميًا
        - lowercase فقط
        - بدون spaces أو underscores
        """
        try:
            # تحقق: هل المنطقة us-east-1؟
            # لأن us-east-1 لا تحتاج CreateBucketConfiguration
            if self.region == 'us-east-1':
                # مناطق us-east-1 تستخدم هذا الشكل الأبسط
                # Bucket = اسم الـ bucket المراد إنشاؤه
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                # مناطق أخرى غير us-east-1 تحتاج معاملات إضافية
                try:
                    # استدعِ create_bucket مع إعدادات المنطقة
                    # CreateBucketConfiguration = إعدادات الإنشاء
                    # LocationConstraint = تحديد المنطقة الجغرافية
                    self.s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                except ClientError as e:
                    # إذا فشل بسبب مشكلة في المنطقة
                    # حاول بدون CreateBucketConfiguration
                    if 'IllegalLocationConstraintException' in str(e):
                        # اطبع رسالة تحذيرية
                        print(f"⚠️  تحويل إلى us-east-1 بسبب مشكلة في المنطقة")
                        # أعد إنشاء الاتصال بـ us-east-1
                        self.s3 = boto3.client('s3', region_name='us-east-1')
                        # جرب الإنشاء مرة أخرى
                        self.s3.create_bucket(Bucket=bucket_name)
                    else:
                        # إذا كان الخطأ مختلف، رفعه للأعلى
                        raise
            
            # اطبع رسالة النجاح
            # f"..." = f-string (طريقة حديثة لدمج المتغيرات في النصوص)
            # {bucket_name} = ضع قيمة المتغير هنا
            print(f"✓ تم إنشاء الـ bucket: {bucket_name}")
            
            # ارجع True (صح/نعم)
            return True
        
        # إذا حدث خطأ من نوع ClientError
        # ClientError = خطأ من AWS
        except ClientError as e:
            # e = معلومات الخطأ (بها الـ error code والرسالة)
            # e.response['Error']['Code'] = رمز الخطأ
            # e.response['Error']['Message'] = رسالة الخطأ
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            
            # اطبع رسالة الخطأ بشكل منسق
            print(f"✗ خطأ [{error_code}]: {error_msg}")
            
            # ارجع False (خطأ)
            return False


    # ═════════════════════════════════════════════════════════════════════════
    # الدالة: list_objects
    # ═════════════════════════════════════════════════════════════════════════
    
    def list_objects(self, bucket_name, prefix='', limit=None):
        """
        عرض جميع الملفات في الـ bucket
        
        المعاملات:
        - bucket_name = الـ bucket (مثل 'my-bucket')
        - prefix = مجلد معين (مثل 'documents/')
        - limit = عدد الملفات المراد عرضها
        
        المثال:
        s3.list_objects('my-bucket')                    # جميع الملفات
        s3.list_objects('my-bucket', prefix='docs/')    # ملفات في مجلد
        s3.list_objects('my-bucket', limit=10)          # أول 10 ملفات
        """
        try:
            # استدعِ list_objects_v2 من boto3
            # list_objects_v2 = الإصدار الأحدث من list_objects
            # Bucket = الـ bucket
            # Prefix = (اختياري) البادئة (مثل مجلد)
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            
            # تحقق: هل توجد ملفات في النتيجة؟
            # 'Contents' = مفتاح يحتوي على الملفات
            # not in = هل المفتاح غير موجود؟
            if 'Contents' not in response:
                print("⚠️  المجلد فارغ")
                return []
            
            # اطبع رأس الجدول
            print(f"\n📁 الملفات في: s3://{bucket_name}/{prefix}")
            print("=" * 70)
            
            # قائمة لحفظ أسماء الملفات
            objects = []
            
            # حلقة: لكل ملف في النتيجة
            # response.get('Contents', []) = احصل على الملفات أو قائمة فارغة
            # .get() = آمن (لا يسبب خطأ إذا لم يكن المفتاح موجود)
            for i, obj in enumerate(response.get('Contents', [])):
                # تحقق: هل وصلنا إلى الحد الأقصى؟
                # limit = الحد الأقصى
                # i = المؤشر الحالي (0, 1, 2, ...)
                # enumerate() = تُعطيك الفهرس والعنصر
                if limit and i >= limit:
                    # توقف عن الحلقة
                    break
                
                # احصل على خصائص الملف
                # obj['Key'] = اسم الملف
                key = obj['Key']
                # obj['Size'] = حجم الملف بـ bytes
                size = obj['Size']
                # obj['LastModified'] = آخر تعديل
                modified = obj['LastModified']
                
                # تنسيق الحجم إلى صيغة مقروءة
                # بدل 1024 bytes، قل 1KB
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024**2:  # 1024 * 1024
                    size_str = f"{size/1024:.2f}KB"
                else:
                    size_str = f"{size/(1024**2):.2f}MB"
                
                # اطبع معلومات الملف
                print(f"  • {key}")
                print(f"    الحجم: {size_str} | التاريخ: {modified}\n")
                
                # أضف إلى القائمة
                objects.append(key)
            
            # ارجع قائمة الملفات
            return objects
        
        # إذا حدث خطأ
        except ClientError as e:
            # اطبع الخطأ
            print(f"✗ خطأ: {e}")
            # ارجع قائمة فارغة
            return []


    # ═════════════════════════════════════════════════════════════════════════
    # الدالة: upload_text
    # ═════════════════════════════════════════════════════════════════════════
    
    def upload_text(self, bucket_name, s3_key, text):
        """
        رفع نص مباشرة بدون ملف محلي
        
        المعاملات:
        - bucket_name = الـ bucket
        - s3_key = اسم الملف في S3 (مثل 'hello.txt')
        - text = محتوى النص (نص عادي)
        
        المثال:
        s3.upload_text('my-bucket', 'hello.txt', 'مرحبا بالعالم')
        """
        try:
            # تحقق: هل text من نوع string؟
            # isinstance() = دالة تتحقق من نوع المتغير
            # str = نوع النص
            if isinstance(text, str):
                # حول النص إلى bytes (ضروري لـ S3)
                # .encode() = حول النص إلى bytes
                # 'utf-8' = تشفير معياري يدعم كل اللغات
                text = text.encode('utf-8')
            
            # استدعِ put_object من boto3
            # put_object() = ضع (أنشئ) ملف في S3
            # Bucket = الـ bucket
            # Key = اسم الملف
            # Body = محتوى الملف (bytes)
            self.s3.put_object(Bucket=bucket_name, Key=s3_key, Body=text)
            
            # اطبع رسالة النجاح
            print(f"✓ تم رفع النص: {s3_key}")
            return True
        
        # إذا حدث خطأ
        except ClientError as e:
            # اطبع الخطأ
            print(f"✗ خطأ: {e}")
            return False


    # ═════════════════════════════════════════════════════════════════════════
    # الدالة: download_text
    # ═════════════════════════════════════════════════════════════════════════
    
    def download_text(self, bucket_name, s3_key):
        """
        تحميل نص من S3
        
        المعاملات:
        - bucket_name = الـ bucket
        - s3_key = اسم الملف في S3
        
        الإرجاع:
        النص المحمّل (string)
        
        المثال:
        content = s3.download_text('my-bucket', 'hello.txt')
        print(content)
        """
        try:
            # استدعِ get_object من boto3
            # get_object() = احصل على ملف من S3
            # Bucket = الـ bucket
            # Key = اسم الملف
            response = self.s3.get_object(Bucket=bucket_name, Key=s3_key)
            
            # احصل على محتوى الملف
            # response['Body'] = جسم الملف (محتواه)
            # .read() = اقرأ كل المحتوى
            data = response['Body'].read()
            
            # حول من bytes إلى string
            # .decode() = فك التشفير
            # 'utf-8' = استخدم نفس التشفير
            text = data.decode('utf-8')
            
            # اطبع رسالة النجاح
            print(f"✓ تم تحميل: {s3_key}")
            
            # ارجع النص
            return text
        
        # إذا حدث خطأ
        except ClientError as e:
            # اطبع الخطأ
            print(f"✗ خطأ: {e}")
            # ارجع None (لا شيء)
            return None


    # ═════════════════════════════════════════════════════════════════════════
    # الدالة: delete_object
    # ═════════════════════════════════════════════════════════════════════════
    
    def delete_object(self, bucket_name, s3_key):
        """
        حذف ملف واحد
        
        المعاملات:
        - bucket_name = الـ bucket
        - s3_key = اسم الملف المراد حذفه
        
        المثال:
        s3.delete_object('my-bucket', 'test.txt')
        """
        try:
            # استدعِ delete_object من boto3
            # Bucket = الـ bucket
            # Key = اسم الملف
            self.s3.delete_object(Bucket=bucket_name, Key=s3_key)
            
            # اطبع رسالة النجاح
            print(f"✓ تم حذف: {s3_key}")
            return True
        
        # إذا حدث خطأ
        except ClientError as e:
            # اطبع الخطأ
            print(f"✗ خطأ: {e}")
            return False


# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ الجزء 3: مثال على الاستخدام                                                  │
# └─────────────────────────────────────────────────────────────────────────────┘

if __name__ == '__main__':
    """
    if __name__ == '__main__':
    معناها: اشتغل هذا الكود فقط إذا كنت تشغل هذا الملف مباشرة
    وليس إذا تم استيراده كـ module في ملف آخر
    """
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║           مثال على استخدام S3Manager                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # إنشاء اتصال مع S3
    # هنا __init__() يُستدعى تلقائيًا
    s3 = S3Manager(region='us-east-1')
    
    # اسم bucket فريد (لأن bucket names يجب أن تكون فريدة عالميًا)
    import time
    bucket_name = f'test-{int(time.time())}'
    
    # إنشاء bucket جديد
    s3.create_bucket(bucket_name)
    
    # رفع نص
    s3.upload_text(bucket_name, 'test.txt', 'Hello World!')
    
    # عرض الملفات
    s3.list_objects(bucket_name)
    
    # تحميل النص
    content = s3.download_text(bucket_name, 'test.txt')
    print(f"محتوى الملف: {content}")
    
    # حذف الملف
    s3.delete_object(bucket_name, 'test.txt')
    
    print("\n✅ انتهى المثال!")


"""
════════════════════════════════════════════════════════════════════════════════
                            ملخص شامل
════════════════════════════════════════════════════════════════════════════════

الـ Class Structure:
───────────────────
class S3Manager:
    ├─ __init__()              ← البناء (يُستدعى عند الإنشاء)
    ├─ create_bucket()         ← إنشاء bucket
    ├─ list_objects()          ← عرض الملفات
    ├─ upload_text()           ← رفع نص
    ├─ download_text()         ← تحميل نص
    └─ delete_object()         ← حذف ملف


مفاهيم أساسية:
──────────────
1. self = الكائن نفسه
2. __init__() = دالة البناء (تُستدعى عند الإنشاء)
3. boto3.client() = إنشاء اتصال مع AWS
4. try/except = معالجة الأخطاء
5. response = النتيجة من AWS (dictionary)
6. Bucket = صندوق التخزين
7. Key = اسم الملف


التدفق العام:
─────────────
User
  ↓
s3 = S3Manager()  ← __init__() يُستدعى
  ↓
s3.create_bucket('my-b')  ← استدعاء method
  ↓
self.s3.create_bucket(...)  ← استدعاء boto3
  ↓
boto3 يرسل request إلى AWS
  ↓
AWS ينشئ الـ bucket
  ↓
النتيجة تُطبع


════════════════════════════════════════════════════════════════════════════════
"""

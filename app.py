from s3_guide_v2 import S3Manager
import time

print("🚀 مثال عملي شامل - S3 with Boto3")
print("=" * 70)

# إنشاء اتصال S3 مع region us-east-1
s3 = S3Manager(region='us-east-1')

# إنشاء bucket بـ timestamp فريد (لأن أسماء الـ buckets يجب أن تكون فريدة عالميًا)
bucket_name = f'my-bucket-{int(time.time())}'
print(f"\n1️⃣  إنشاء bucket: {bucket_name}...")
s3.create_bucket(bucket_name)

# رفع ملفات
print(f"\n2️⃣  رفع ملفات...")
s3.upload_text(bucket_name, 'hello.txt', 'Hello World - مرحبا بالعالم')
s3.upload_text(bucket_name, 'config.json', '{"app": "myapp", "version": "1.0"}')

# عرض الملفات
print(f"\n3️⃣  عرض الملفات:")
s3.list_objects(bucket_name)

# تحميل الملف
print(f"\n4️⃣  تحميل الملف...")
content = s3.download_text(bucket_name, 'hello.txt')
print(f"   المحتوى: {content}")

# الحصول على معلومات الملف
print(f"\n5️⃣  معلومات الملف...")
s3.get_object_info(bucket_name, 'hello.txt')

# نسخ الملف
print(f"\n6️⃣  نسخ الملف...")
s3.copy_object(bucket_name, 'hello.txt', bucket_name, 'hello_backup.txt')

# البحث عن ملفات
print(f"\n7️⃣  البحث عن ملفات .txt...")
txt_files = s3.search_by_extension(bucket_name, 'txt')

# حذف ملف واحد
print(f"\n8️⃣  حذف ملف واحد...")
s3.delete_object(bucket_name, 'config.json')

# عرض الملفات المتبقية
print(f"\n9️⃣  الملفات المتبقية...")
s3.list_objects(bucket_name)

# تنظيف - حذف جميع الملفات والـ bucket
print(f"\n🔟 تنظيف...")
s3.delete_all_objects(bucket_name)
s3.delete_bucket(bucket_name)

print(f"\n✅ انتهى المثال بنجاح!")
print("=" * 70)

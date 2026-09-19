"""
═══════════════════════════════════════════════════════════════════════════════
               دليل السريع - Boto3 S3 Quick Reference
═══════════════════════════════════════════════════════════════════════════════

هذا ملف يحتوي على أمثلة عملية سهلة للاستخدام المباشر
This file contains practical examples ready to use
"""

from s3_guide_v2 import S3Manager


# ═══════════════════════════════════════════════════════════════════════════════
# الإعداد الأساسي / Basic Setup
# ═══════════════════════════════════════════════════════════════════════════════

print("🚀 إنشاء مدير S3...")
s3 = S3Manager(region='us-east-1')


# ═══════════════════════════════════════════════════════════════════════════════
# 1. عمليات الـ Bucket / Bucket Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("1. عمليات الـ Bucket")
print("=" * 70)

# إنشاء bucket
# my_bucket = 'my-awesome-bucket-12345'  # اجعله فريد
# s3.create_bucket(my_bucket)

# عرض جميع الـ buckets
print("\n🔍 عرض الـ buckets:")
buckets = s3.list_buckets()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. رفع الملفات / Upload Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("2. رفع الملفات")
print("=" * 70)

# مثال: إذا كان لديك bucket موجود، استخدم:
# bucket = 'your-bucket-name'

# أ) رفع ملف محلي
# s3.upload_file(bucket, 'path/to/local/file.txt')

# ب) رفع نص مباشرة
# s3.upload_text(bucket, 'hello.txt', 'مرحبا بالعالم')

# ج) رفع مجلد كامل
# s3.upload_folder(bucket, './my-folder', prefix='archive/')


# ═══════════════════════════════════════════════════════════════════════════════
# 3. عرض الملفات / List Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("3. عرض الملفات")
print("=" * 70)

# مثال:
# bucket = 'your-bucket-name'

# أ) عرض جميع الملفات
# files = s3.list_objects(bucket)

# ب) عرض ملفات في مجلد معين
# files = s3.list_objects(bucket, prefix='documents/')

# ج) عرض أول 10 ملفات فقط
# files = s3.list_objects(bucket, limit=10)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. البحث / Search Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("4. البحث عن ملفات")
print("=" * 70)

# البحث عن ملفات بامتداد معين
# pdf_files = s3.search_by_extension(bucket, 'pdf')
# txt_files = s3.search_by_extension(bucket, '.txt')


# ═══════════════════════════════════════════════════════════════════════════════
# 5. تحميل الملفات / Download Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("5. تحميل الملفات")
print("=" * 70)

# أ) تحميل ملف
# s3.download_file(bucket, 'hello.txt', './hello_local.txt')

# ب) تحميل نص
# content = s3.download_text(bucket, 'hello.txt')
# print(content)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. معلومات الملف / File Info
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("6. معلومات الملف")
print("=" * 70)

# الحصول على معلومات الملف (الحجم، التاريخ، إلخ)
# s3.get_object_info(bucket, 'hello.txt')


# ═══════════════════════════════════════════════════════════════════════════════
# 7. نسخ الملفات / Copy Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("7. نسخ الملفات")
print("=" * 70)

# نسخ ملف داخل نفس الـ bucket
# s3.copy_object(bucket, 'original.txt', bucket, 'backup.txt')

# نسخ ملف إلى bucket آخر
# s3.copy_object(bucket1, 'file.txt', bucket2, 'file.txt')


# ═══════════════════════════════════════════════════════════════════════════════
# 8. حذف الملفات / Delete Operations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("8. حذف الملفات")
print("=" * 70)

# أ) حذف ملف واحد
# s3.delete_object(bucket, 'file.txt')

# ب) حذف عدة ملفات
# s3.delete_multiple(bucket, ['file1.txt', 'file2.txt', 'file3.txt'])

# ج) حذف جميع الملفات (احذر!)
# s3.delete_all_objects(bucket)


# ═══════════════════════════════════════════════════════════════════════════════
# ملخص الأوامر الأساسية / Quick Command Reference
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📋 ملخص الأوامر")
print("=" * 70)

print("""
# الإعداد
s3 = S3Manager()
s3 = S3Manager(region='eu-west-1')  # منطقة مختلفة

# Bucket
s3.create_bucket('my-bucket')
s3.list_buckets()
s3.delete_bucket('my-bucket')

# Upload
s3.upload_file(bucket, 'local-file.txt')
s3.upload_text(bucket, 'file.txt', 'محتوى النص')
s3.upload_folder(bucket, './folder', prefix='archive/')

# List
s3.list_objects(bucket)
s3.list_objects(bucket, prefix='documents/')
s3.search_by_extension(bucket, 'pdf')

# Download
s3.download_file(bucket, 'file.txt', './local.txt')
s3.download_text(bucket, 'file.txt')

# Info
s3.get_object_info(bucket, 'file.txt')

# Copy
s3.copy_object(bucket1, 'file.txt', bucket2, 'file.txt')

# Delete
s3.delete_object(bucket, 'file.txt')
s3.delete_multiple(bucket, ['f1.txt', 'f2.txt'])
s3.delete_all_objects(bucket)
""")

print("\n✅ جاهز للاستخدام!")
print("📚 للمزيد من المعلومات، اقرأ التعليقات في s3_guide_v2.py")

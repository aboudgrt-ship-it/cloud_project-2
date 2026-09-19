#!/usr/bin/env python3
"""
سكريبت اختبار بسيط لـ S3
Simple S3 test script
"""

import boto3
import sys
from datetime import datetime

print("=" * 60)
print("🔍 اختبار اتصال S3 - S3 Connection Test")
print("=" * 60)

try:
    # 1. محاولة الاتصال
    print("\n1️⃣  محاولة الاتصال بـ AWS...")
    s3 = boto3.client('s3', region_name='us-east-1')
    print("   ✓ تم الاتصال بـ boto3")
    
    # 2. اختبار الصلاحيات
    print("\n2️⃣  اختبار الصلاحيات...")
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    
    print(f"   ✓ Account ID: {identity['Account']}")
    print(f"   ✓ ARN: {identity['Arn']}")
    print(f"   ✓ User ID: {identity['UserId']}")
    
    # 3. عرض الـ buckets الموجودة
    print("\n3️⃣  عرض الـ buckets الموجودة...")
    response = s3.list_buckets()
    
    if response['Buckets']:
        print(f"   عدد الـ buckets: {len(response['Buckets'])}")
        for bucket in response['Buckets']:
            print(f"      • {bucket['Name']} (تاريخ: {bucket['CreationDate']})")
    else:
        print("   ⚠️  لا توجد buckets حاليًا")
    
    # 4. محاولة إنشاء bucket
    print("\n4️⃣  محاولة إنشاء bucket جديد...")
    bucket_name = f"test-bucket-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    s3.create_bucket(Bucket=bucket_name)
    print(f"   ✓ تم إنشاء الـ bucket: {bucket_name}")
    
    # 5. التحقق من إنشاء الـ bucket
    print("\n5️⃣  التحقق من الـ bucket الجديد...")
    response = s3.list_buckets()
    bucket_found = any(b['Name'] == bucket_name for b in response['Buckets'])
    
    if bucket_found:
        print(f"   ✓ تم العثور على الـ bucket: {bucket_name}")
    else:
        print(f"   ✗ لم يتم العثور على الـ bucket")
    
    # 6. رفع ملف اختبار
    print("\n6️⃣  رفع ملف اختبار...")
    s3.put_object(Bucket=bucket_name, Key='test.txt', Body=b'Hello from S3!')
    print(f"   ✓ تم رفع الملف: test.txt")
    
    # 7. عرض الملفات
    print("\n7️⃣  عرض الملفات في الـ bucket...")
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"      • {obj['Key']} ({obj['Size']} bytes)")
    
    print("\n" + "=" * 60)
    print("✅ كل شيء يعمل بشكل صحيح!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ حدث خطأ: {type(e).__name__}")
    print(f"   الرسالة: {e}")
    print("\n" + "=" * 60)
    print("💡 الحل:")
    print("=" * 60)
    print("""
1. تأكد من أن boto3 مثبت:
   pip install boto3

2. تأكد من AWS credentials:
   aws configure
   
   أو أضفها يدويًا في:
   ~/.aws/credentials (Linux/Mac)
   C:\\Users\\YourName\\.aws\\credentials (Windows)
   
   الصيغة:
   [default]
   aws_access_key_id = YOUR_KEY
   aws_secret_access_key = YOUR_SECRET
   region = us-east-1

3. تأكد من أن المستخدم لديه صلاحيات S3:
   - s3:ListAllMyBuckets
   - s3:CreateBucket
   - s3:PutObject
   
4. للمزيد من المعلومات:
   https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
    """)
    sys.exit(1)

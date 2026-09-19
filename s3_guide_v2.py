#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                    دليل Boto3 S3 - نسخة محسّنة
                     Boto3 S3 Guide - Enhanced Version
═══════════════════════════════════════════════════════════════════════════════

هذا الملف يحتوي على جميع عمليات S3 - نسخة محسّنة وأسهل في الاستخدام
This file contains all S3 operations - improved and easier to use

المتطلبات / Requirements:
1. pip install boto3
2. aws configure (أو AWS credentials)
3. S3 permissions in IAM
"""

import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


class S3Manager:
    """مدير S3 - S3 Manager Class"""
    
    def __init__(self, region='us-east-1'):
        """
        إنشاء اتصال S3
        Create S3 connection
        """
        try:
            self.s3 = boto3.client('s3', region_name=region)
            self.region = region
            print(f"✓ متصل بـ S3 في المنطقة: {region}")
        except NoCredentialsError:
            print("✗ خطأ: لم يتم العثور على AWS credentials")
            print("  تأكد من تشغيل: aws configure")
            raise
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Bucket Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def create_bucket(self, bucket_name):
        """
        إنشاء bucket جديد
        Create a new S3 bucket
        
        ملاحظات / Notes:
        - اسم الـ bucket يجب أن يكون فريدًا عالميًا (globally unique)
        - lowercase فقط
        - بدون spaces أو underscores
        """
        try:
            # استخدم us-east-1 افتراضيًا لتجنب مشاكل التوافقية
            # Use us-east-1 by default to avoid compatibility issues
            if self.region == 'us-east-1':
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                try:
                    self.s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                except ClientError as e:
                    # إذا فشل مع LocationConstraint، حاول بدونه
                    if 'IllegalLocationConstraintException' in str(e):
                        print(f"⚠️  تحويل إلى us-east-1 بسبب مشكلة في المنطقة")
                        self.s3 = boto3.client('s3', region_name='us-east-1')
                        self.s3.create_bucket(Bucket=bucket_name)
                    else:
                        raise
            
            print(f"✓ تم إنشاء الـ bucket: {bucket_name}")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            print(f"✗ خطأ [{error_code}]: {error_msg}")
            return False
    
    def list_buckets(self):
        """
        عرض جميع الـ buckets
        List all buckets
        """
        try:
            response = self.s3.list_buckets()
            buckets = response['Buckets']
            
            if not buckets:
                print("⚠️  لا توجد buckets حاليًا")
                return []
            
            print(f"\n📦 عدد الـ Buckets: {len(buckets)}")
            print("=" * 60)
            for bucket in buckets:
                print(f"  • {bucket['Name']}")
                print(f"    تاريخ: {bucket['CreationDate']}\n")
            
            return [b['Name'] for b in buckets]
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def delete_bucket(self, bucket_name):
        """
        حذف bucket (يجب أن يكون فارغًا)
        Delete a bucket (must be empty)
        """
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"✓ تم حذف الـ bucket: {bucket_name}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Upload Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def upload_file(self, bucket_name, file_path, s3_key=None):
        """
        رفع ملف
        Upload a file
        """
        if not os.path.exists(file_path):
            print(f"✗ الملف غير موجود: {file_path}")
            return False
        
        if s3_key is None:
            s3_key = os.path.basename(file_path)
        
        try:
            self.s3.upload_file(file_path, bucket_name, s3_key)
            print(f"✓ تم رفع: {file_path} → s3://{bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def upload_text(self, bucket_name, s3_key, text):
        """
        رفع نص مباشرة
        Upload text directly
        """
        try:
            if isinstance(text, str):
                text = text.encode('utf-8')
            
            self.s3.put_object(Bucket=bucket_name, Key=s3_key, Body=text)
            print(f"✓ تم رفع النص: {s3_key}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def upload_folder(self, bucket_name, folder_path, prefix=''):
        """
        رفع جميع ملفات مجلد
        Upload all files from a folder
        """
        if not os.path.isdir(folder_path):
            print(f"✗ المجلد غير موجود: {folder_path}")
            return False
        
        try:
            count = 0
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    s3_key = f"{prefix}{filename}" if prefix else filename
                    self.s3.upload_file(file_path, bucket_name, s3_key)
                    print(f"  ✓ {filename}")
                    count += 1
            
            print(f"\n✓ تم رفع {count} ملف")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Download Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def download_file(self, bucket_name, s3_key, local_path):
        """
        تحميل ملف
        Download a file
        """
        try:
            self.s3.download_file(bucket_name, s3_key, local_path)
            print(f"✓ تم تحميل: s3://{bucket_name}/{s3_key} → {local_path}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def download_text(self, bucket_name, s3_key):
        """
        تحميل نص
        Download text
        """
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=s3_key)
            text = response['Body'].read().decode('utf-8')
            print(f"✓ تم تحميل: {s3_key}")
            return text
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # List/Search Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def list_objects(self, bucket_name, prefix='', limit=None):
        """
        عرض الملفات في الـ bucket
        List objects in bucket
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            
            if 'Contents' not in response:
                print("⚠️  المجلد فارغ")
                return []
            
            print(f"\n📁 الملفات في: s3://{bucket_name}/{prefix}")
            print("=" * 70)
            
            objects = []
            for i, obj in enumerate(response.get('Contents', [])):
                if limit and i >= limit:
                    break
                
                key = obj['Key']
                size = obj['Size']
                modified = obj['LastModified']
                
                # تنسيق الحجم
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024**2:
                    size_str = f"{size/1024:.2f}KB"
                else:
                    size_str = f"{size/(1024**2):.2f}MB"
                
                print(f"  • {key}")
                print(f"    الحجم: {size_str} | التاريخ: {modified}\n")
                objects.append(key)
            
            return objects
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def search_by_extension(self, bucket_name, extension):
        """
        البحث عن ملفات بامتداد معين
        Search files by extension
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            
            matching = []
            for obj in response.get('Contents', []):
                if obj['Key'].endswith(extension):
                    matching.append(obj['Key'])
            
            print(f"\n🔍 ملفات {extension}:")
            for file in matching:
                print(f"  • {file}")
            
            print(f"\nالعدد: {len(matching)}")
            return matching
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Delete Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def delete_object(self, bucket_name, s3_key):
        """
        حذف ملف واحد
        Delete a single file
        """
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=s3_key)
            print(f"✓ تم حذف: {s3_key}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def delete_multiple(self, bucket_name, keys_list):
        """
        حذف عدة ملفات
        Delete multiple files
        """
        try:
            objects = [{'Key': key} for key in keys_list]
            self.s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects})
            print(f"✓ تم حذف {len(keys_list)} ملف")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def delete_all_objects(self, bucket_name, prefix=''):
        """
        حذف جميع الملفات في الـ bucket
        Delete all files in bucket
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            
            if 'Contents' not in response:
                print("الـ bucket فارغ بالفعل")
                return True
            
            keys = [obj['Key'] for obj in response['Contents']]
            return self.delete_multiple(bucket_name, keys)
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # Copy/Info Operations
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def copy_object(self, src_bucket, src_key, dest_bucket, dest_key):
        """
        نسخ ملف
        Copy a file
        """
        try:
            copy_source = {'Bucket': src_bucket, 'Key': src_key}
            self.s3.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key
            )
            print(f"✓ تم نسخ: s3://{src_bucket}/{src_key} → s3://{dest_bucket}/{dest_key}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def get_object_info(self, bucket_name, s3_key):
        """
        الحصول على معلومات الملف
        Get file metadata
        """
        try:
            response = self.s3.head_object(Bucket=bucket_name, Key=s3_key)
            
            print(f"\n📋 معلومات: {s3_key}")
            print("=" * 50)
            print(f"  الحجم: {response['ContentLength']} bytes")
            print(f"  النوع: {response.get('ContentType', 'unknown')}")
            print(f"  التعديل: {response['LastModified']}")
            print(f"  ETag: {response['ETag']}")
            
            if response.get('Metadata'):
                print(f"  Metadata:")
                for k, v in response['Metadata'].items():
                    print(f"    - {k}: {v}")
            
            return response
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return None

    def get_s3_identity(self):
        try:
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"✓ Account ID: {identity['Account']}")
            print(f"✓ ARN: {identity['Arn']}")
            print(f"✓ User ID: {identity['UserId']}")
            return identity
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return None

    def delete_bucket_force(self, bucket_name):
        try:
            self.delete_all_objects(bucket_name)
            self.delete_bucket(bucket_name)
            print(f"✓ تم حذف الـ bucket وجميع الملفات: {bucket_name}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
        
# ═══════════════════════════════════════════════════════════════════════════════
# Examples / أمثلة
# ═══════════════════════════════════════════════════════════════════════════════

def example_complete_workflow():
    """
    مثال كامل على عملية S3
    Complete workflow example
    """
    print("\n" + "=" * 70)
    print("                    مثال عملي شامل")
    print("=" * 70)
    
    # إنشاء مدير S3
    s3 = S3Manager(region='us-east-1')
    
    # إنشاء bucket
    bucket_name = f"demo-bucket-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print("\n1️⃣  إنشاء bucket...")
    s3.create_bucket(bucket_name)
    
    # رفع ملفات
    print("\n2️⃣  رفع ملفات...")
    s3.upload_text(bucket_name, 'hello.txt', 'مرحبا بالعالم')
    s3.upload_text(bucket_name, 'test.txt', 'ملف اختبار')
    s3.upload_text(bucket_name, 'folder/document.txt', 'وثيقة')
    
    # عرض الملفات
    print("\n3️⃣  عرض الملفات...")
    s3.list_objects(bucket_name)
    
    # معلومات الملف
    print("\n4️⃣  معلومات الملف...")
    s3.get_object_info(bucket_name, 'hello.txt')
    
    # تحميل الملف
    print("\n5️⃣  تحميل الملف...")
    text = s3.download_text(bucket_name, 'hello.txt')
    print(f"   المحتوى: {text}")
    
    # البحث
    print("\n6️⃣  البحث عن ملفات .txt...")
    s3.search_by_extension(bucket_name, 'txt')
    
    # نسخ الملف
    print("\n7️⃣  نسخ الملف...")
    s3.copy_object(bucket_name, 'hello.txt', bucket_name, 'hello_backup.txt')
    
    # عرض النهائي
    print("\n8️⃣  الملفات النهائية...")
    s3.list_objects(bucket_name)
    
    # تنظيف
    print("\n9️⃣  تنظيف...")
    s3.delete_all_objects(bucket_name)
    s3.delete_bucket(bucket_name)
    
    print("\n✅ انتهى المثال")


if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════╗
║               دليل Boto3 S3 - نسخة محسّنة                  ║
║                                                                ║
║  الاستخدام:                                                   ║
║  1. from s3_guide_v2 import S3Manager                          ║
║  2. s3 = S3Manager()                                           ║
║  3. s3.create_bucket('my-bucket')                              ║
║  4. s3.upload_file('my-bucket', 'file.txt')                    ║
║                                                                ║
║  أو للعرض التوضيحي:                                            ║
║  python3 s3_guide_v2.py                                        ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    example_complete_workflow()

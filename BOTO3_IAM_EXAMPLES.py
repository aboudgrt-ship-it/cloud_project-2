"""
═══════════════════════════════════════════════════════════════════════════════
                  Boto3 IAM - أمثلة عملية شاملة
                     Practical IAM Examples with Boto3
═══════════════════════════════════════════════════════════════════════════════
"""

import boto3
import json
from botocore.exceptions import ClientError


class IAMManager:
    """
    مدير IAM - دالة شاملة لإدارة IAM
    Complete IAM Management Class
    """
    
    def __init__(self):
        """إنشاء اتصال مع خدمة IAM"""
        try:
            self.iam = boto3.client('iam')
            print("✓ متصل بـ IAM")
        except Exception as e:
            print(f"✗ خطأ: {e}")
    
    # ═════════════════════════════════════════════════════════════════════════
    # عمليات المستخدمين (Users)
    # ═════════════════════════════════════════════════════════════════════════
    
    def create_user(self, username, tags=None):
        """
        إنشاء مستخدم جديد
        Create a new IAM user
        
        Args:
            username: اسم المستخدم
            tags: وسوم إضافية (اختياري)
        """
        try:
            response = self.iam.create_user(UserName=username)
            print(f"✓ تم إنشاء المستخدم: {username}")
            return response['User']
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  المستخدم {username} موجود بالفعل")
            else:
                print(f"✗ خطأ: {e}")
            return None
    
    def list_users(self):
        """
        عرض جميع المستخدمين
        List all IAM users
        """
        try:
            response = self.iam.list_users()
            users = response['Users']
            
            print(f"\n📋 عدد المستخدمين: {len(users)}")
            print("=" * 60)
            
            for user in users:
                print(f"  اسم المستخدم: {user['UserName']}")
                print(f"  تاريخ الإنشاء: {user['CreateDate']}")
                print(f"  ARN: {user['Arn']}\n")
            
            return users
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def delete_user(self, username):
        """
        حذف مستخدم
        Delete an IAM user
        
        ملاحظة: يجب حذف جميع الأذونات والمفاتيح أولاً
        """
        try:
            self.iam.delete_user(UserName=username)
            print(f"✓ تم حذف المستخدم: {username}")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'DeleteConflict':
                print(f"⚠️  لا يمكن حذف {username} - يجب حذف الأذونات أولاً")
            else:
                print(f"✗ خطأ: {e}")
            return False
    
    def get_user_info(self, username):
        """
        الحصول على معلومات المستخدم
        Get information about a user
        """
        try:
            response = self.iam.get_user(UserName=username)
            user = response['User']
            
            print(f"\n📋 معلومات المستخدم: {username}")
            print("=" * 60)
            print(f"  الاسم: {user['UserName']}")
            print(f"  ARN: {user['Arn']}")
            print(f"  User ID: {user['UserId']}")
            print(f"  تاريخ الإنشاء: {user['CreateDate']}")
            
            return user
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return None
    
    # ═════════════════════════════════════════════════════════════════════════
    # عمليات المفاتيح (Access Keys)
    # ═════════════════════════════════════════════════════════════════════════
    
    def create_access_key(self, username):
        """
        إنشاء مفتاح وصول للمستخدم
        Create access keys for a user
        
        الإرجاع:
        - AccessKeyId
        - SecretAccessKey
        
        ⚠️  احفظ SecretAccessKey في مكان آمن!
        """
        try:
            response = self.iam.create_access_key(UserName=username)
            key = response['AccessKey']
            
            print(f"\n🔑 مفتاح وصول جديد للمستخدم: {username}")
            print("=" * 60)
            print(f"  Access Key ID: {key['AccessKeyId']}")
            print(f"  Secret Access Key: {key['SecretAccessKey']}")
            print(f"  الحالة: {key['Status']}")
            print("\n⚠️  احفظ Secret Access Key - لن تراه مرة أخرى!")
            
            return key
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return None
    
    def list_access_keys(self, username):
        """
        عرض جميع مفاتيح الوصول للمستخدم
        List access keys for a user
        """
        try:
            response = self.iam.list_access_keys(UserName=username)
            keys = response['AccessKeyMetadata']
            
            print(f"\n🔑 مفاتيح الوصول للمستخدم: {username}")
            print("=" * 60)
            
            for key in keys:
                print(f"  Access Key ID: {key['AccessKeyId']}")
                print(f"  الحالة: {key['Status']}")
                print(f"  تاريخ الإنشاء: {key['CreateDate']}\n")
            
            return keys
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def delete_access_key(self, username, access_key_id):
        """
        حذف مفتاح وصول
        Delete an access key
        """
        try:
            self.iam.delete_access_key(
                UserName=username,
                AccessKeyId=access_key_id
            )
            print(f"✓ تم حذف المفتاح: {access_key_id}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    # ═════════════════════════════════════════════════════════════════════════
    # عمليات المجموعات (Groups)
    # ═════════════════════════════════════════════════════════════════════════
    
    def create_group(self, group_name):
        """
        إنشاء مجموعة جديدة
        Create a new group
        """
        try:
            response = self.iam.create_group(GroupName=group_name)
            print(f"✓ تم إنشاء المجموعة: {group_name}")
            return response['Group']
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  المجموعة {group_name} موجودة بالفعل")
            else:
                print(f"✗ خطأ: {e}")
            return None
    
    def add_user_to_group(self, group_name, username):
        """
        إضافة مستخدم إلى مجموعة
        Add user to a group
        """
        try:
            self.iam.add_user_to_group(
                GroupName=group_name,
                UserName=username
            )
            print(f"✓ تم إضافة {username} إلى المجموعة {group_name}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def list_group_members(self, group_name):
        """
        عرض أعضاء المجموعة
        List members of a group
        """
        try:
            response = self.iam.get_group(GroupName=group_name)
            users = response['Users']
            
            print(f"\n👥 أعضاء المجموعة: {group_name}")
            print("=" * 60)
            
            for user in users:
                print(f"  {user['UserName']}")
            
            return users
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def list_groups(self):
        """
        عرض جميع المجموعات
        List all groups
        """
        try:
            response = self.iam.list_groups()
            groups = response['Groups']
            
            print(f"\n👥 عدد المجموعات: {len(groups)}")
            print("=" * 60)
            
            for group in groups:
                print(f"  اسم المجموعة: {group['GroupName']}")
                print(f"  ARN: {group['Arn']}\n")
            
            return groups
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    # ═════════════════════════════════════════════════════════════════════════
    # عمليات الأذونات (Policies)
    # ═════════════════════════════════════════════════════════════════════════
    
    def attach_policy_to_user(self, username, policy_arn):
        """
        ربط سياسة مع مستخدم
        Attach a policy to a user
        
        Args:
            username: اسم المستخدم
            policy_arn: ARN السياسة
        
        مثال:
        arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
        """
        try:
            self.iam.attach_user_policy(
                UserName=username,
                PolicyArn=policy_arn
            )
            print(f"✓ تم ربط السياسة مع المستخدم {username}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def attach_policy_to_group(self, group_name, policy_arn):
        """
        ربط سياسة مع مجموعة
        Attach a policy to a group
        """
        try:
            self.iam.attach_group_policy(
                GroupName=group_name,
                PolicyArn=policy_arn
            )
            print(f"✓ تم ربط السياسة مع المجموعة {group_name}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False
    
    def list_user_policies(self, username):
        """
        عرض السياسات المرتبطة مع المستخدم
        List policies for a user
        """
        try:
            response = self.iam.list_attached_user_policies(UserName=username)
            policies = response['AttachedPolicies']
            
            print(f"\n📋 سياسات المستخدم: {username}")
            print("=" * 60)
            
            for policy in policies:
                print(f"  اسم السياسة: {policy['PolicyName']}")
                print(f"  ARN: {policy['PolicyArn']}\n")
            
            return policies
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def create_custom_policy(self, policy_name, policy_document):
        """
        إنشاء سياسة مخصصة
        Create a custom policy
        
        Args:
            policy_name: اسم السياسة
            policy_document: مستند JSON للسياسة
        """
        try:
            response = self.iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document)
            )
            print(f"✓ تم إنشاء السياسة: {policy_name}")
            print(f"  ARN: {response['Policy']['Arn']}")
            return response['Policy']
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return None
    
    # ═════════════════════════════════════════════════════════════════════════
    # عمليات الأدوار (Roles)
    # ═════════════════════════════════════════════════════════════════════════
    
    def create_role(self, role_name, trust_policy):
        """
        إنشاء دور جديد
        Create a new role
        
        Args:
            role_name: اسم الدور
            trust_policy: من يمكنه افتراض هذا الدور؟
        """
        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy)
            )
            print(f"✓ تم إنشاء الدور: {role_name}")
            return response['Role']
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                print(f"⚠️  الدور {role_name} موجود بالفعل")
            else:
                print(f"✗ خطأ: {e}")
            return None
    
    def list_roles(self):
        """
        عرض جميع الأدوار
        List all roles
        """
        try:
            response = self.iam.list_roles()
            roles = response['Roles']
            
            print(f"\n🎭 عدد الأدوار: {len(roles)}")
            print("=" * 60)
            
            for role in roles:
                print(f"  اسم الدور: {role['RoleName']}")
                print(f"  ARN: {role['Arn']}\n")
            
            return roles
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return []
    
    def attach_policy_to_role(self, role_name, policy_arn):
        """
        ربط سياسة مع دور
        Attach a policy to a role
        """
        try:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"✓ تم ربط السياسة مع الدور {role_name}")
            return True
        except ClientError as e:
            print(f"✗ خطأ: {e}")
            return False


# ═════════════════════════════════════════════════════════════════════════════
# أمثلة عملية
# ═════════════════════════════════════════════════════════════════════════════

def example_1_create_user_with_s3_access():
    """
    مثال 1: إنشاء مستخدم مع الوصول إلى S3
    Example 1: Create user with S3 access
    """
    print("\n" + "=" * 70)
    print("مثال 1: إنشاء مستخدم مع الوصول إلى S3")
    print("=" * 70)
    
    iam = IAMManager()
    
    # إنشاء مستخدم
    username = "s3-user"
    iam.create_user(username)
    
    # ربط سياسة قراءة S3 (AWS Managed Policy)
    s3_readonly_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
    iam.attach_policy_to_user(username, s3_readonly_arn)
    
    # إنشاء مفتاح وصول
    key = iam.create_access_key(username)
    
    # عرض السياسات
    iam.list_user_policies(username)
    
    return key


def example_2_create_group_with_users():
    """
    مثال 2: إنشاء مجموعة وإضافة مستخدمين
    Example 2: Create a group and add users
    """
    print("\n" + "=" * 70)
    print("مثال 2: إنشاء مجموعة وإضافة مستخدمين")
    print("=" * 70)
    
    iam = IAMManager()
    
    # إنشاء مجموعة
    group_name = "developers"
    iam.create_group(group_name)
    
    # إنشاء مستخدمين
    users = ["developer1", "developer2", "developer3"]
    for user in users:
        iam.create_user(user)
        iam.add_user_to_group(group_name, user)
    
    # ربط سياسة مع المجموعة
    ec2_full_access = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
    iam.attach_policy_to_group(group_name, ec2_full_access)
    
    # عرض أعضاء المجموعة
    iam.list_group_members(group_name)


def example_3_create_custom_policy():
    """
    مثال 3: إنشاء سياسة مخصصة
    Example 3: Create a custom policy
    """
    print("\n" + "=" * 70)
    print("مثال 3: إنشاء سياسة مخصصة")
    print("=" * 70)
    
    iam = IAMManager()
    
    # تعريف السياسة (قراءة S3 فقط لـ bucket محدد)
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::my-app-bucket",
                    "arn:aws:s3:::my-app-bucket/*"
                ]
            }
        ]
    }
    
    # إنشاء السياسة
    policy_name = "S3-MyBucket-ReadOnly"
    iam.create_custom_policy(policy_name, policy_document)
    
    # ربط السياسة مع مستخدم
    iam.create_user("app-user")
    iam.attach_policy_to_user(
        "app-user",
        f"arn:aws:iam::YOUR_ACCOUNT_ID:policy/{policy_name}"
    )


def example_4_create_role_for_ec2():
    """
    مثال 4: إنشاء دور للـ EC2
    Example 4: Create a role for EC2
    """
    print("\n" + "=" * 70)
    print("مثال 4: إنشاء دور للـ EC2")
    print("=" * 70)
    
    iam = IAMManager()
    
    # تعريف سياسة الثقة (من يمكنه افتراض هذا الدور؟)
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # إنشاء الدور
    role_name = "EC2-S3-Access"
    iam.create_role(role_name, trust_policy)
    
    # ربط سياسة مع الدور
    s3_full_access = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
    iam.attach_policy_to_role(role_name, s3_full_access)
    
    # الآن يمكن ربط هذا الدور مع EC2 instance
    print("\n💡 الآن يمكنك ربط هذا الدور مع EC2 instance في AWS Console")


if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    أمثلة Boto3 IAM العملية                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # اختر الأمثلة التي تريد تشغيلها
    print("""
اختر مثال:
1. إنشاء مستخدم مع الوصول إلى S3
2. إنشاء مجموعة وإضافة مستخدمين
3. إنشاء سياسة مخصصة
4. إنشاء دور للـ EC2

أو جرّب الدالات الفردية من IAMManager class
    """)
    
    # مثال على استخدام الـ class
    iam = IAMManager()
    iam.list_users()
    iam.list_groups()
    iam.list_roles()

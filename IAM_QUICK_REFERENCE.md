# IAM سريعة - مرجع IAM
## Quick Reference - IAM

---

## 1️⃣ المصطلحات الأساسية (Basic Terminology)

| المصطلح | الشرح | الاستخدام | الأذونات |
|--------|-------|-----------|---------|
| **User** | مستخدم - شخص أو تطبيق | مباشر - له Access Keys | تُعطى للـ User |
| **Group** | مجموعة مستخدمين | تنظيمية | تُعطى للـ Group |
| **Role** | دور يمكن افتراضه | للخدمات AWS | تُعطى للـ Role |
| **Policy** | مستند JSON بالأذونات | تعريف الأذونات | تُربط مع User/Group/Role |
| **ARN** | معرف فريد للموارد | تحديد الموارد في السياسات | - |
| **Access Key** | مفتاح للوصول البرمجي | للـ API و CLI | - |

---

## 2️⃣ عمليات الـ User (User Operations)

### إنشاء مستخدم
```python
iam.create_user(UserName='ahmed')
```

### عرض المستخدمين
```python
iam.list_users()
```

### الحصول على معلومات مستخدم
```python
iam.get_user(UserName='ahmed')
```

### حذف مستخدم
```python
iam.delete_user(UserName='ahmed')
```

### إنشاء Access Key
```python
iam.create_access_key(UserName='ahmed')
# النتيجة:
# AccessKeyId: AKIA2XKLP4NNPD8UZYQJ
# SecretAccessKey: wJalrXUtnFEMI/K7MDENG/...
```

### عرض Access Keys
```python
iam.list_access_keys(UserName='ahmed')
```

### حذف Access Key
```python
iam.delete_access_key(
    UserName='ahmed',
    AccessKeyId='AKIA2XKLP4NNPD8UZYQJ'
)
```

---

## 3️⃣ عمليات المجموعة (Group Operations)

### إنشاء مجموعة
```python
iam.create_group(GroupName='developers')
```

### عرض المجموعات
```python
iam.list_groups()
```

### إضافة مستخدم للمجموعة
```python
iam.add_user_to_group(
    GroupName='developers',
    UserName='ahmed'
)
```

### عرض أعضاء المجموعة
```python
iam.get_group(GroupName='developers')
```

### إزالة مستخدم من المجموعة
```python
iam.remove_user_from_group(
    GroupName='developers',
    UserName='ahmed'
)
```

### حذف مجموعة
```python
iam.delete_group(GroupName='developers')
```

---

## 4️⃣ عمليات الـ Role (Role Operations)

### إنشاء دور
```python
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

iam.create_role(
    RoleName='EC2-S3-Access',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)
```

### عرض الأدوار
```python
iam.list_roles()
```

### حذف دور
```python
iam.delete_role(RoleName='EC2-S3-Access')
```

---

## 5️⃣ عمليات السياسات (Policy Operations)

### ربط سياسة مع مستخدم
```python
iam.attach_user_policy(
    UserName='ahmed',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
```

### ربط سياسة مع مجموعة
```python
iam.attach_group_policy(
    GroupName='developers',
    PolicyArn='arn:aws:iam::aws:policy/AmazonEC2FullAccess'
)
```

### ربط سياسة مع دور
```python
iam.attach_role_policy(
    RoleName='EC2-S3-Access',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
)
```

### عرض سياسات المستخدم
```python
iam.list_attached_user_policies(UserName='ahmed')
```

### إنشاء سياسة مخصصة
```python
policy_doc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}

iam.create_policy(
    PolicyName='S3-MyBucket-ReadOnly',
    PolicyDocument=json.dumps(policy_doc)
)
```

### فصل سياسة عن مستخدم
```python
iam.detach_user_policy(
    UserName='ahmed',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
)
```

---

## 6️⃣ السياسات المدارة من AWS (AWS Managed Policies)

| الاسم | الوصف | ARN |
|-------|-------|-----|
| **AdministratorAccess** | وصول كامل | `arn:aws:iam::aws:policy/AdministratorAccess` |
| **ReadOnlyAccess** | قراءة فقط | `arn:aws:iam::aws:policy/ReadOnlyAccess` |
| **AmazonS3FullAccess** | S3 - كل شيء | `arn:aws:iam::aws:policy/AmazonS3FullAccess` |
| **AmazonS3ReadOnlyAccess** | S3 - قراءة فقط | `arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess` |
| **AmazonEC2FullAccess** | EC2 - كل شيء | `arn:aws:iam::aws:policy/AmazonEC2FullAccess` |
| **AWSLambdaFullAccess** | Lambda - كل شيء | `arn:aws:iam::aws:policy/AWSLambdaFullAccess` |
| **AmazonDynamoDBFullAccess** | DynamoDB - كل شيء | `arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess` |

---

## 7️⃣ أمثلة سياسات شائعة (Common Policy Examples)

### 1. قراءة S3 فقط
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

### 2. رفع وقراءة S3
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

### 3. إنشاء مستخدمين IAM فقط
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:CreateUser",
        "iam:AddUserToGroup"
      ],
      "Resource": "*"
    }
  ]
}
```

### 4. DynamoDB - قراءة وكتابة جدول محدد
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:228107397172:table/Users"
    }
  ]
}
```

### 5. رفع ملفات لمجلد محدد في S3
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/uploads/*"
    }
  ]
}
```

---

## 8️⃣ أمثلة ARN (ARN Examples)

| الموارد | ARN | الوصف |
|--------|-----|-------|
| مستخدم | `arn:aws:iam::228107397172:user/ahmed` | مستخدم محدد |
| مجموعة | `arn:aws:iam::228107397172:group/developers` | مجموعة محددة |
| دور | `arn:aws:iam::228107397172:role/EC2-S3` | دور محدد |
| سياسة مخصصة | `arn:aws:iam::228107397172:policy/MyPolicy` | سياسة مخصصة |
| جميع المستخدمين | `arn:aws:iam::228107397172:user/*` | جميع المستخدمين |
| S3 Bucket | `arn:aws:s3:::my-bucket` | bucket محدد |
| S3 أشياء | `arn:aws:s3:::my-bucket/*` | جميع الأشياء في bucket |
| EC2 instance | `arn:aws:ec2:us-east-1:228107397172:instance/*` | جميع instances |

---

## 9️⃣ نصائح الأمان (Security Tips)

✅ **افعل هذا:**
- استخدم Least Privilege (أقل أذونات ممكنة)
- استخدم Groups بدلاً من أذونات فردية
- احفظ Access Keys في ~/.aws/credentials
- استخدم Environment Variables للـ Secret Keys
- فعّل MFA للحسابات المهمة
- راجع الأذونات بشهر

❌ **لا تفعل هذا:**
- لا تستخدم Root Account مباشرة
- لا تضع Access Keys في الكود
- لا تشارك Secret Access Key
- لا تستخدم AdministratorAccess للجميع
- لا تحفظ Keys في GitHub
- لا تستخدم نفس User لتطبيقات مختلفة

---

## 🔟 الاختلافات بين User و Role

| الميزة | User | Role |
|--------|------|------|
| المستخدم | شخص أو تطبيق | خدمة AWS أو Cross-Account |
| Access Keys | ✅ نعم | ❌ لا |
| Console Password | ✅ نعم | ❌ لا |
| الاستخدام | مباشر | يجب الافتراض (Assume) |
| Trust Policy | ❌ لا | ✅ نعم |
| مثال | مهندس AWS | EC2 instance أو Lambda |

---

## 1️⃣1️⃣ أكثر الأخطاء شيوعاً (Common Mistakes)

| الخطأ | المشكلة | الحل |
|------|--------|------|
| نسيان Attach Policy | المستخدم بدون أذونات | attach policy قبل الاستخدام |
| Root Account مباشر | خطر أمني | أنشئ IAM users عاديين |
| Secret Key في GitHub | أي شخص يدخل | استخدم .gitignore |
| نفس User لتطبيقات | صعوبة في التتبع | استخدم Users منفصلة |
| AdministratorAccess | خطر كبير | استخدم أذونات محدودة |
| نسيان حفظ Secret Key | لا يمكن الاسترجاع | احذف وأنشئ واحد جديد |

---

## 1️⃣2️⃣ أوامر Boto3 السريعة (Quick Boto3 Commands)

```python
import boto3
import json

# الاتصال
iam = boto3.client('iam')

# Users
iam.create_user(UserName='test')
iam.list_users()
iam.delete_user(UserName='test')

# Groups
iam.create_group(GroupName='test')
iam.add_user_to_group(GroupName='test', UserName='ahmed')
iam.get_group(GroupName='test')

# Roles
iam.create_role(RoleName='test', AssumeRolePolicyDocument=json.dumps({...}))
iam.list_roles()

# Policies
iam.attach_user_policy(UserName='ahmed', PolicyArn='...')
iam.list_attached_user_policies(UserName='ahmed')

# Access Keys
iam.create_access_key(UserName='ahmed')
iam.list_access_keys(UserName='ahmed')
iam.delete_access_key(UserName='ahmed', AccessKeyId='...')
```

---

## 1️⃣3️⃣ متى تستخدم ماذا (When to Use What)

| الحالة | استخدم |
|------|--------|
| مهندس يحتاج AWS Console | **User** + Console Password |
| تطبيق يحتاج AWS API | **User** + Access Keys |
| EC2 يحتاج S3 | **Role** مرتبط مع EC2 |
| Lambda يحتاج DynamoDB | **Role** مرتبط مع Lambda |
| فريق متشابه | **Group** + Shared Policy |
| تطبيقات مختلفة | **Different Users** |
| خدمات خارجية | **Cross-Account Role** |

---

## 1️⃣4️⃣ مثال كامل (Complete Example)

```python
import boto3
import json

iam = boto3.client('iam')

# 1. إنشاء مستخدم
iam.create_user(UserName='app-user')

# 2. إنشاء مفاتيح وصول
keys = iam.create_access_key(UserName='app-user')
print(f"Key ID: {keys['AccessKey']['AccessKeyId']}")
print(f"Secret: {keys['AccessKey']['SecretAccessKey']}")

# 3. إنشاء سياسة مخصصة
policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::data-bucket/*"
    }]
}

iam.create_policy(
    PolicyName='S3-Read-Only',
    PolicyDocument=json.dumps(policy)
)

# 4. ربط السياسة مع المستخدم
iam.attach_user_policy(
    UserName='app-user',
    PolicyArn='arn:aws:iam::228107397172:policy/S3-Read-Only'
)

print("✅ تم إنشاء المستخدم مع الأذونات!")
```

---

## 📚 المزيد من الموارد

- 📖 اقرأ: `IAM_DETAILED_GUIDE.py`
- 💻 مثال: `BOTO3_IAM_EXAMPLES.py`
- 🔑 S3: `s3_guide_v2.py`

---

**آخر تحديث**: IAM Guide v1.0
**اللغة**: العربية + English
**الحالة**: جاهز للاستخدام ✅

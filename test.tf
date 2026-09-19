use "aws_vpc" 
resource "aws_vpc" "test" {
  cidr_block = "10.0.0.0/16" , target = local.cidr_block
  nat_gateway_id = "nat-0a0b0c0d0e0f0g" , target = local.nat_gateway_id
  route_table_id = "rtb-0a0b0c0d0e0f0g" , target = local.route_table_id
  instance_tenancy = "default"
  enable_dns_support = true
  enable_dns_hostnames = true
  nat_instance_enabled = true

  instance_state {
    name = "running"
    id = "i-0a0b0c0d0e0f0g"
  }

  tags = {
    Name = "test"
    Environment = "test"
    Owner = "test"
  }
  resource "aws_vpc" "vpc1" {
  ipv4_ipam_pool_id   = data.aws_ssm_parameter.vpc_ipam_id.value
  ipv4_netmask_length = data.aws_ssm_parameter.vpc_netmask.value

  enable_dns_hostnames                 = var.enable_dns_hostnames
  enable_dns_support                   = var.enable_dns_support
  enable_network_address_usage_metrics = var.enable_network_address_usage_metrics

  tags = var.tags
  }
  terraform_init {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 3.0"
      }
    }
    terraform_version = "~> 1.0"
  }
  availability_zones = ["us-east-1a"]

  
}
user "aws_s3_bucket" 
resource "aws_s3_bucket" "test" {
    bucket = "test"
    acl = "private"

    tags = {
        Name = "test"
        Environment = "test"
        Owner = "test"
    }
    
    versioning {
        enabled = true
    }

    lifecycle_rule {
        id = "test"
        enabled = true
        prefix = "test"
        tags = {
            Name = "test"
            Environment = "test"
            Owner = "test"
        }
        abort_incomplete_multipart_upload_days = 7
        expiration {
            days = 30
        }
        noncurrent_version_expiration {
            days = 30
        }
        transition {
            days = 30
            storage_class = "STANDARD_IA"
        }
        noncurrent_version_transition {
            days = 30
            storage_class = "STANDARD_IA"
        }
      }
}
provider "aws" {
region = "us-east-1"
}
resource "RDS" "test" { 
   allocated_storage = 10
   storage_type = "gp2"
   engine = "mysql"
   engine_version = "5.7"
   instance_class = "db.t2.micro"
   name = "test"
   username = "test"
   password = "test"
   skip_final_snapshot = true
   vpc_security_group_ids = ["sg-0a0b0c0d0e0f0g"]
   db_subnet_group_name = "test"
   parameter_group_name = "default.mysql5.7"
   publicly_accessible = false
   apply_immediately = true
}
provider "aws" {
region = "us-east-1"
}
resource "aws_s3_bucket" "test" {
  bucket = "test"
  acl = "private"

  tags = {
    Name = "test"
    Environment = "test"
    Owner = "test"
  }

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id = "test"
    enabled = true
    prefix = "test"
    tags = {
      Name = "test"
      Environment = "test"
      Owner = "test"
    }
    abort_incomplete_multipart_upload_days = 7
    expiration {
      days = 30
    }
    noncurrent_version_expiration {
      days = 30
    }
    transition {
      days = 30
      storage_class = "STANDARD_IA"
    }
    noncurrent_version_transition {
      days = 30
      storage_class = "STANDARD_IA"
    }
  }
} 



resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-validate-jwt"
  force_destroy = true

  tags = {
    Name = "Terraform State Bucket"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "Terraform Lock Table"
  }
}

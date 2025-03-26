terraform {
  backend "s3" {
    bucket         = "terraform-state-validate-jwt"
    key            = "envs/prod/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = "us-west-2"
}

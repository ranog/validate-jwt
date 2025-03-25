variable "app_name" {
  type        = string
  description = "Nome da aplicação"
}

variable "container_port" {
  type        = number
  default     = 8080
}

variable "vpc_cidr_block" {
  type        = string
  default     = "10.0.0.0/16"
}

variable "image_tag" {
  type        = string
  description = "Tag da imagem Docker a ser usada no ECS (ex: GITHUB_SHA)"
}

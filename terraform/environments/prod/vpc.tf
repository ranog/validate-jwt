# resource "aws_vpc" "main" {
#   cidr_block = var.vpc_cidr_block
#   enable_dns_support = true
#   enable_dns_hostnames = true
# }
#
# resource "aws_subnet" "public" {
#   count                   = 2
#   vpc_id                  = aws_vpc.main.id
#   cidr_block              = cidrsubnet(var.vpc_cidr_block, 8, count.index)
#   availability_zone       = data.aws_availability_zones.available.names[count.index]
#   map_public_ip_on_launch = true
# }
#
# resource "aws_internet_gateway" "gw" {
#   vpc_id = aws_vpc.main.id
# }
#
# resource "aws_route_table" "public" {
#   vpc_id = aws_vpc.main.id
#
#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = aws_internet_gateway.gw.id
#   }
# }
#
# resource "aws_route_table_association" "public" {
#   count          = 2
#   subnet_id      = aws_subnet.public[count.index].id
#   route_table_id = aws_route_table.public.id
# }
#
# data "aws_availability_zones" "available" {}

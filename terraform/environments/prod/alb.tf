# resource "aws_security_group" "alb" {
#   name        = "${var.app_name}-alb-sg"
#   description = "ALB Security Group"
#   vpc_id      = aws_vpc.main.id
#
#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }
#
# resource "aws_lb" "app" {
#   name               = "${var.app_name}-alb"
#   internal           = false
#   load_balancer_type = "application"
#   security_groups    = [aws_security_group.alb.id]
#   subnets            = aws_subnet.public[*].id
# }
#
# resource "aws_lb_target_group" "app" {
#   name     = "${var.app_name}-tg"
#   port     = var.container_port
#   protocol = "HTTP"
#   vpc_id   = aws_vpc.main.id
#   target_type = "ip"
#
#    lifecycle {
#     create_before_destroy = true
#   }
#
#   health_check {
#     path = "/health"
#     port = "traffic-port"
#   }
# }
#
# resource "aws_lb_listener" "http" {
#   load_balancer_arn = aws_lb.app.arn
#   port              = 80
#   protocol          = "HTTP"
#
#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.app.arn
#   }
# }

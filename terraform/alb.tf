resource "aws_lb" "alb" {
    name = "${var.project_name}-alb"
    load_balancer_type = "application"
    subnets = aws_subnet.public[*].id
    security_groups = [aws_security_group.alb_sg.id]
}


resource "aws_lb_target_group" "tg" {
    port = var.container_port
    protocol = "HTTP"
    target_type = "ip"
    vpc_id = aws_vpc.main.id


    health_check {
        path = "/"
    }
}


resource "aws_lb_listener" "listener" {
    load_balancer_arn = aws_lb.alb.arn
    port = 80
    protocol = "HTTP"


    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.tg.arn
    }
}
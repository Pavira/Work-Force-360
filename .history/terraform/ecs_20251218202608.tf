resource "aws_ecs_cluster" "cluster" {
name = "${var.project_name}-cluster"
}


resource "aws_ecs_task_definition" "task" {
    family = "${var.project_name}-task"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = "256"
    memory = "512"
    execution_role_arn = aws_iam_role.ecs_execution_role.arn


    container_definitions = jsonencode([
        {
            name = "app"
            image = aws_ecr_repository.repo.repository_url
            essential = true
            portMappings = [{
                containerPort = var.container_port
            }]
        }
    ])
}


resource "aws_ecs_service" "service" {
    name = "${var.project_name}-service"
    cluster = aws_ecs_cluster.cluster.id
    task_definition = aws_ecs_task_definition.task.arn
    desired_count = 1
    launch_type = "FARGATE"


    network_configuration {
        subnets = aws_subnet.private[*].id
        security_groups = [aws_security_group.ecs_sg.id]
    }


    load_balancer {
        target_group_arn = aws_lb_target_group.tg.arn
        container_name = "app"
        container_port = var.container_port
    }
}
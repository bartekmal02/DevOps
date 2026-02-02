# Definicja uprawnień dla grup (Zasada Least Privilege)
GROUP_CONFIG = {
    "Development": ["s3:ListBucket", "s3:GetObject", "ec2:DescribeInstances"],
    "QA": ["ecs:ListServices", "cloudwatch:GetMetricData"],
    "Admins": ["*"]
}

# Mapowanie użytkowników do grup
USER_ASSIGNMENTS = {
    "dev_user_1": "Development",
    "qa_tester_1": "QA",
    "admin_chief": "Admins"
}